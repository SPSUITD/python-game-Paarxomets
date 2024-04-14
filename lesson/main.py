import pyfiglet
bunner = pyfiglet.figlet_format("sky forse", font="banner3-d")
print(bunner)

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Sky Forse"

CHARACTER_SCALING = 0.8
TILE_SCALING = 0.6
# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

BULLET_SCALE = 1
BULLET_SPEED = 10

CLOUD_SPAWN_INTERVAL = 60

BACKGROUND_SCROLL_SPEED = 50




class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background = arcade.load_texture('img_second/background.png')
        self.background_y1 = 0  # начальное положение первой копии фона по оси Y
        self.background_y2 = SCREEN_HEIGHT  # начальное положение второй копии фона по оси Y
        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a lists
        self.player_list = None
        self.player_sprite = None


        self.moving_left = False
        self.moving_right = False

        self.player_sprite_left = arcade.load_texture("img_second/player_left.png")
        self.player_sprite_right = arcade.load_texture("img_second/player_right.png")

        self.bullets_list = arcade.SpriteList()


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "img_second/sprite_img.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)


    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.background_y1,
                                        SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.background_y2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        # Draw our sprites
        self.player_list.draw()

        self.bullets_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.moving_left = True
            self.player_sprite.texture = self.player_sprite_left 
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.moving_right = True
            self.player_sprite.texture = self.player_sprite_right
        elif key == arcade.key.SPACE:
            self.fire_bullet()

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.moving_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.moving_right = False

    
    def on_update(self, delta_time):
        """Movement and game logic"""
        if self.moving_left:
            self.player_sprite.center_x -= 8
        elif self.moving_right:
            self.player_sprite.center_x += 8

        self.bullets_list.update()

        self.background_y1 -= BACKGROUND_SCROLL_SPEED * delta_time
        self.background_y2 -= BACKGROUND_SCROLL_SPEED * delta_time

        # Если первая копия фона уходит за верхний край экрана,
        # перемещаем ее вниз на высоту экрана
        if self.background_y1 < -SCREEN_HEIGHT:
            self.background_y1 = SCREEN_HEIGHT

        # Если вторая копия фона уходит за верхний край экрана,
        # перемещаем ее вниз на высоту экрана
        if self.background_y2 < -SCREEN_HEIGHT:
            self.background_y2 = SCREEN_HEIGHT


    def fire_bullet(self):
        bullet = arcade.Sprite("img_second/bullet.png", BULLET_SCALE)
        bullet.center_x = self.player_sprite.center_x
        bullet.center_y = self.player_sprite.center_y + self.player_sprite.height // 2
        bullet.change_y = BULLET_SPEED
        self.bullets_list.append(bullet)

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()