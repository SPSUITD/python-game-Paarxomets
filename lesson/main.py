import arcade
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Sky Force"

CHARACTER_SCALING = 0.8
PLAYER_MOVEMENT_SPEED = 5
BULLET_SCALE = 1
BULLET_SPEED = 10
BACKGROUND_SCROLL_SPEED = 50
ENEMY_SPEED = 3
ENEMY_SHOOT_FREQUENCY = 0.8  
PLAYER_INVINCIBILITY_TIME = 0.2  
EXPLOSION_DURATION = 0.05 

class Enemy(arcade.Sprite):
    def __init__(self, image, scale, game):
        super().__init__(image, scale=scale)
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = SCREEN_HEIGHT + self.height // 2
        self.game = game
        self.shoot_timer = 0
        self.health = 1  

    def update(self):
        self.center_y -= ENEMY_SPEED
        self.shoot_timer += 1 / 60  
        if self.shoot_timer >= ENEMY_SHOOT_FREQUENCY:
            self.shoot_timer = 0
            bullet = arcade.Sprite("img_second/bullet_enemy.png", BULLET_SCALE)
            bullet.center_x = self.center_x
            bullet.center_y = self.center_y - self.height // 2
            bullet.change_y = -BULLET_SPEED  
            self.game.enemy_bullets.append(bullet)  

        if self.top < 0:
            self.kill()

        for bullet in self.game.bullets:
            if arcade.check_for_collision(bullet, self):
                bullet.kill()
                self.health -= 1
                if self.health <= 0:
                    self.kill()
                    self.game.score += 10  
                    self.game.enemy_killed += 1  
                    
                    explosion = Explosion("img_second/explosion.png", scale=1)
                    explosion.center_x = self.center_x
                    explosion.center_y = self.center_y
                    self.game.explosions.append(explosion)

class Player(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale=scale)
        self.moving_left = False
        self.moving_right = False
        self.lives = 3
        self.invincible_time = 0

    def update(self):
        if self.invincible_time > 0:
            self.invincible_time -= 1
            if self.invincible_time % 10 == 0:  
                self.alpha = 0 if self.alpha == 255 else 255  
        else:
            self.alpha = 255  
            if self.moving_left:
                self.center_x -= PLAYER_MOVEMENT_SPEED
            elif self.moving_right:
                self.center_x += PLAYER_MOVEMENT_SPEED

class GameOverView(arcade.View):
    def __init__(self, game_view, distance_traveled, enemy_killed):
        super().__init__()
        self.game_view = game_view
        self.distance_traveled = distance_traveled
        self.enemy_killed = enemy_killed

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Игра завершена", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100,
                        arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text(f"Дистанция: {int(self.distance_traveled)}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                        arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text(f"Уничтожено противников: {self.enemy_killed}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20,
                        arcade.color.WHITE, font_size=15, anchor_x="center")
        arcade.draw_text("Нажмите R для новой игры", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
                        arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.game_view.reset()
            self.game_view.setup()
            self.window.show_view(self.game_view)

class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture('img_second/background.png')
        self.background_y1 = 0
        self.background_y2 = SCREEN_HEIGHT
        self.player = Player("img_second/sprite_img.png", CHARACTER_SCALING)
        self.player.center_x = 500
        self.player.center_y = 50
        self.player_start_texture = self.player.texture
        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()  
        self.explosions = arcade.SpriteList() 
        self.score = 0
        self.distance_traveled = 0
        self.lives_textures = [arcade.load_texture("img_second/heart.png") for _ in range(self.player.lives)]
        self.enemy_killed = 0 

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_show(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.background_y1,
                                    SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + self.background_y2,
                                    SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player_list.draw()
        self.bullets.draw()
        self.enemies.draw()
        self.enemy_bullets.draw() 
        arcade.draw_text(f"Distance: {int(self.distance_traveled)}", 10, SCREEN_HEIGHT - 90, (226, 177, 92), 14)
        for i, texture in enumerate(self.lives_textures):
            arcade.draw_texture_rectangle(30 + i * 40, SCREEN_HEIGHT - 40, texture.width, texture.height, texture)
        arcade.draw_text(f"Enemies Killed: {self.enemy_killed}", 10, SCREEN_HEIGHT - 70, (226, 177, 92), 14)
        self.explosions.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.moving_left = True
            self.player.texture = arcade.load_texture("img_second/player_left.png")
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.moving_right = True
            self.player.texture = arcade.load_texture("img_second/player_right.png")
        elif key == arcade.key.SPACE:
            self.fire_bullet()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.moving_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.moving_right = False
        if not self.player.moving_left and not self.player.moving_right:
            self.player.texture = self.player_start_texture

    def on_update(self, delta_time):
        self.player.update()
        self.bullets.update()
        self.enemies.update()
        self.enemy_bullets.update()  
        self.explosions.update()
        self.background_y1 -= BACKGROUND_SCROLL_SPEED * delta_time
        self.background_y2 -= BACKGROUND_SCROLL_SPEED * delta_time
        if self.background_y1 < -SCREEN_HEIGHT:
            self.background_y1 = SCREEN_HEIGHT
        if self.background_y2 < -SCREEN_HEIGHT:
            self.background_y2 = SCREEN_HEIGHT
        self.distance_traveled += BACKGROUND_SCROLL_SPEED * delta_time
        self.score += 1

        
        for bullet in self.enemy_bullets:
            if arcade.check_for_collision(bullet, self.player):
                bullet.kill()
                self.player.lives -= 1
                self.player.invincible_time = int(PLAYER_INVINCIBILITY_TIME * 60)  
                if self.player.lives == 0:
                    game_over_view = GameOverView(self, self.distance_traveled, self.enemy_killed)
                    self.window.show_view(game_over_view)
                else:
                    self.lives_textures.pop()

        for explosion in self.explosions:
            if explosion.alpha <= 0:
                explosion.kill()

    def spawn_enemy(self, dt):
        enemy = Enemy("img_second/sprite_enemy.png", CHARACTER_SCALING, self)
        self.enemies.append(enemy)

    def fire_bullet(self):
        bullet = arcade.Sprite("img_second/bullet.png", BULLET_SCALE)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y + self.player.height // 2
        bullet.change_y = BULLET_SPEED
        self.bullets.append(bullet)
        
    def reset(self):
        self.background_y1 = 0
        self.background_y2 = SCREEN_HEIGHT
        self.bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()  
        self.explosions = arcade.SpriteList()
        self.score = 0
        self.distance_traveled = 0
        self.player.lives = 3
        self.lives_textures = [arcade.load_texture("img_second/heart.png") for _ in range(self.player.lives)]
        self.enemy_killed = 0  

class Explosion(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_to_live = EXPLOSION_DURATION

    def update(self):
        super().update()
        self.time_to_live -= 1 / 60
        if self.time_to_live <= 0:
            self.kill()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = MyGame()
    game_over_view = GameOverView(game_view, 0, 0)
    game_view.setup()
    game_view.window = window
    game_over_view.window = window
    arcade.schedule(game_view.spawn_enemy, 0.4) 
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
