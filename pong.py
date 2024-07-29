from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

# Creamos una clase para las palas de cada jugador
class PongPaddle(Widget):
    score = NumericProperty(0)  # propiedad para contar los puntos
    
    # Método para que la bola rebote cuando toca una de las palas
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

# Clase para la pelota 
class PongBall(Widget):
    # Velocidad de la pelota en los ejes x, y
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # Propiedad de lista de referencia para usar ball.velocity como un atajo
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    # Función para mover la pelota un paso. Se llamará a intervalos iguales para animar la pelota
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

# Clase para el juego de Pong
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    #Método para usar las teclas del ordenador para manejar las palas
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.keys_pressed = set()
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self.keyboard = None
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keys_pressed.add(keycode[1])
        return True
    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self.keys_pressed:
            self.keys_pressed.remove(keycode[1])
        return True
    
    # Método para servir la pelota con una velocidad inicial
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    
    # Método de actualización que se llama en cada frame    
    def update(self, dt):
        self.ball.move()
        
        # Hacer rebotar la pelota en las paletas
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        # Hacer rebotar la pelota en la parte superior e inferior
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        # Verificar si la pelota salió por un lado para anotar un punto
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            
        # Mover las palas según las teclas presionadas
        if 'w' in self.keys_pressed:
            self.player1.center_y += 10
        if 's' in self.keys_pressed:
            self.player1.center_y -= 10
        if 'up' in self.keys_pressed:
            self.player2.center_y += 10
        if 'down' in self.keys_pressed:
            self.player2.center_y -= 10
    
    # Método para mover las paletas cuando se detecta un toque en la pantalla        
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
        
# Clase principal de la aplicación
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        # Programar la actualización del juego a 60 FPS
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
# Ejecutar la aplicación    
if __name__ == '__main__':
    PongApp().run()