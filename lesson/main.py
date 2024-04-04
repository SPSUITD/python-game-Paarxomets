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

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN_TITLE = "My Arcade Game"
CHARACTER_SCALING = 0.7
PLAYER_MOVEMENT_SPEED = 8

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.background = arcade.load_texture("lesson/img/game_background.png")
        self.player_list = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        image_source = "lesson/img/player_sprite.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 330
        self.player_sprite.center_y = 60
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT and self.player_sprite.change_x < 0:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT and self.player_sprite.change_x > 0:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.player_sprite.update()
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y

        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
