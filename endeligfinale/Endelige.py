import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Hell Game"

CHARACTER_SCALING = 0.3
ENEMY_SCALING = 0.4
SPRITE_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 4
GRAVITY = 0.8
PLAYER_JUMP_SPEED = 22

# Enemy class
class Enemy(arcade.Sprite):
    def __init__(self, image_source, scaling=1):
        super().__init__(image_source, scaling)
        self.change_x = 0
        self.change_y = 0

        # Forward walking frames
        self.walk_frames_reverse = [
            arcade.load_texture("Demon 1.png"),
            arcade.load_texture("Demon 2.png"),
            arcade.load_texture("Demon 3.png")
        ]

        # Reverse walking frames
        self.walk_frames_forward = [
            arcade.load_texture("Devil v1.png"),
            arcade.load_texture("Devil v2.png"),
            arcade.load_texture("Devil v3.png"),
            arcade.load_texture("Devil v4.png")
        ]

        self.current_frame = 0
        self.frame_timer = 0.0
        self.animation_interval = 0.1

    def animate(self, delta_time, moving_forward=True):
        # Update frame timer
        self.frame_timer += delta_time

        # If it's time to change frame, change it
        if self.frame_timer >= self.animation_interval:
            self.frame_timer = 0.0
            if moving_forward:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_forward)
                self.texture = self.walk_frames_forward[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_reverse)
                self.texture = self.walk_frames_reverse[self.current_frame]

# Game class
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.tile_map = None
        self.scene = None
        self.key_sprite = None
        self.player_sprite = None
        self.enemy_sprite = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.background = None
        self.door_layer = None
        self.game_over = False

        self.walk_frames_forward = [
            arcade.load_texture("Player1.png"),
            arcade.load_texture("Player2.png"),
            arcade.load_texture("Player3.png")
        ]

        self.walk_frames_reverse = [
            arcade.load_texture("Spiller 1.png"),
            arcade.load_texture("Spiller 2.png"),
            arcade.load_texture("Spiller 3.png")
        ]

        self.current_frame = 0
        self.frame_timer = 0.0
        self.animation_interval = 0.1
        self.is_walking = False
        self.enemy_direction = 1  # 1 for moving forward, -1 for moving backward
        self.player_direction = 1  # 1 for moving forward, -1 for moving backward

    def setup(self):
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.background = arcade.load_texture("image.png")
        map_name = "Platforms.tmx"
        layer_options = {
            "Platforms": {"use_spatial_hash": True},
            "Lava": {"use_spatial_hash": True},
            "Key": {"use_spatial_hash": True},
            "Door": {"use_spatial_hash": True}
        }
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        player_image_source = "Player1.png"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 500
        self.scene.add_sprite("Player", self.player_sprite)

        enemy_image_source = "Demon 1.png"
        self.enemy_sprite = Enemy(enemy_image_source, ENEMY_SCALING)
        self.enemy_sprite.center_x = 580
        self.enemy_sprite.center_y = 177
        self.scene.add_sprite("Enemy", self.enemy_sprite)

        key_image_source = "key.png"
        self.key_sprite = arcade.Sprite(key_image_source, SPRITE_SCALING)
        self.key_sprite.center_x = 2950
        self.key_sprite.center_y = 100
        self.scene.add_sprite("Key", self.key_sprite)

        self.key_sprite = self.scene["Key"]
        self.door_layer = self.scene["Door"]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
        )

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        if self.game_over:
            arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, arcade.color.BLACK)
            arcade.draw_text(
                "Game is done, congratz",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                font_size=50,
                anchor_x="center",
                anchor_y="center"
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            self.player_direction = -1  # Moving backward
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.player_direction = 1  # Moving forward

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        screen_center_x = max(screen_center_x, 0)
        screen_center_y = max(screen_center_y, 0)
        self.camera.move_to((screen_center_x, screen_center_y))

    def on_update(self, delta_time):
        self.physics_engine.update()

        enemy_movement_speed = 2
        moving_forward = True

        if self.enemy_sprite.center_x <= 580:  # Leftmost position
            self.enemy_sprite.change_x = enemy_movement_speed
            self.enemy_direction = 1  # Moving forward
        elif self.enemy_sprite.center_x >= 780:  # Rightmost position
            self.enemy_sprite.change_x = -enemy_movement_speed
            self.enemy_direction = -1  # Moving backward
        self.enemy_sprite.center_x += self.enemy_sprite.change_x

        if arcade.check_for_collision(self.player_sprite, self.enemy_sprite):
            self.setup()  # Restart game

        lava_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Lava"])
        if lava_hit:
            self.setup()  # Restart game

        key_hit = arcade.check_for_collision_with_list(self.player_sprite, self.key_sprite)
        if key_hit:
            for key in key_hit:
                key.remove_from_sprite_lists()

        door_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.door_layer)
        if door_hit_list and not self.key_sprite:
            self.game_over = True

        if self.player_sprite.change_x != 0:
            self.is_walking = True
        else:
            self.is_walking = False

        if self.is_walking:
            self.animate_player(delta_time)
        else:
            self.player_sprite.texture = arcade.load_texture("Player1.png")

        self.center_camera_to_player()
        self.enemy_sprite.animate(delta_time, moving_forward=self.enemy_direction == 1)

    def animate_player(self, delta_time):
        self.frame_timer += delta_time

        if self.frame_timer >= self.animation_interval:
            self.frame_timer = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames_forward)

        if self.player_direction == 1:
            self.player_sprite.texture = self.walk_frames_forward[self.current_frame]
        else:
            self.player_sprite.texture = self.walk_frames_reverse[self.current_frame]

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
