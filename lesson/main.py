# :'######::'##:::'##:'##:::'##:
# '##... ##: ##::'##::. ##:'##::
#  ##:::..:: ##:'##::::. ####:::
# . ######:: #####::::::. ##::::
# :..... ##: ##. ##:::::: ##::::
# '##::: ##: ##:. ##::::: ##::::
# . ######:: ##::. ##:::: ##::::
# :......:::..::::..:::::..:::::
# '########::'#######::'########:::'######::'########:
#  ##.....::'##.... ##: ##.... ##:'##... ##: ##.....::
#  ##::::::: ##:::: ##: ##:::: ##: ##:::..:: ##:::::::
#  ######::: ##:::: ##: ########::. ######:: ######:::
#  ##...:::: ##:::: ##: ##.. ##::::..... ##: ##...::::
#  ##::::::: ##:::: ##: ##::. ##::'##::: ##: ##:::::::
#  ##:::::::. #######:: ##:::. ##:. ######:: ########:
# ..:::::::::.......:::..:::::..:::......:::........::
"""
sky forse Game
"""

import arcade
import arcade.key

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN_TITLE = "sky forse Game"
CHARACTER_SCALING = 0.7
PLAYER_MOVEMENT_SPEED = 8

BULLET_SCALE = 0.7
BULLET_SPEED = 5
BULLET_WEIGHT = 50

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("lesson/img/startscreen.png")
        self.button_texture = arcade.load_texture("lesson/img/start_button.png")
        self.button_pressed_texture = arcade.load_texture("lesson/img/start_button_pressed.png")
        self.button_center_x = SCREEN_WIDTH // 2
        self.button_center_y = SCREEN_HEIGHT // 5
        self.button_width = 159.75
        self.button_height = 159.75
        self.button_pressed = False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        button_texture = self.button_pressed_texture if self.button_pressed else self.button_texture
        arcade.draw_texture_rectangle(self.button_center_x, self.button_center_y, self.button_width, self.button_height, button_texture)

    def on_mouse_press(self, x, y, button, modifiers):
        if (self.button_center_x - self.button_width / 2 < x < self.button_center_x + self.button_width / 2 and
            self.button_center_y - self.button_height / 2 < y < self.button_center_y + self.button_height / 2):
            self.button_pressed = True

    def on_mouse_release(self, x, y, button, modifiers):
        if self.button_pressed:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)
        self.button_pressed = False

class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("lesson/img/game_background.png")
        self.player_sprite = None
        self.left_pressed = False
        self.right_pressed = False
        self.bullets_list = arcade.SpriteList()

    def setup(self):
        self.player_sprite = arcade.Sprite("lesson/img/spaceship.png", CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 50

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player_sprite.draw()
        self.bullets_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.fire_bullet()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def update(self, delta_time):
        if self.left_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0
        
        self.player_sprite.update()
        self.player_sprite.center_x = max(0, min(SCREEN_WIDTH, self.player_sprite.center_x))
        self.player_sprite.center_y = max(0, min(SCREEN_HEIGHT, self.player_sprite.center_y))

        self.bullets_list.update()

    def fire_bullet(self):
        bullet = arcade.Sprite("lesson/img/bullet.png", BULLET_SCALE)
        bullet.center_x = self.player_sprite.center_x
        bullet.center_y = self.player_sprite.center_y + self.player_sprite.height // 2
        bullet.change_y = BULLET_SPEED
        self.bullets_list.append(bullet)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartScreen()  # Создание экземпляра StartScreen
    window.show_view(start_view)  # Переключение на стартовый экран
    arcade.run()

if __name__ == "__main__":
    main()
