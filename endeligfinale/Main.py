import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# "Sprite Scaling" som enten gror eller formindsker vores sprite, men holder højde og bredde forskellen det samme
CHARACTER_SCALING = 0.7
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Spiller bevægelse
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1.7
PLAYER_JUMP_SPEED = 20

# Enemy class, "image_source" er længere nede, og scaling er bare det samme som står ovenpå

class Enemy(arcade.Sprite):
    def __init__(self, image_source, scaling=1):
        super().__init__(image_source, scaling)
        self.change_x = 0
        self.change_y = 0

# Den her del er fra arcade
class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Separate variable that holds the enemy sprite
        self.enemy_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0
        self.background = None

# Også fra arcade
    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        # Her har vi sat vores billede som baggrund
        self.background = arcade.load_texture("image.png")

        # Name of map file to load
        map_name = "Platforms.tmx"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            "Lava": {  # Adding lava layer options
                "use_spatial_hash": True,
            }
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Set up the player, specifically placing it at these coordinates.
        player_image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(player_image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 500
        self.scene.add_sprite("Player", self.player_sprite)

        # Set up the enemy, place it at appropriate coordinates
        enemy_image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.enemy_sprite = Enemy(enemy_image_source, CHARACTER_SCALING)
        self.enemy_sprite.center_x = 80  # Adjust these coordinates according to your map
        self.enemy_sprite.center_y = 195  # Adjust these coordinates according to your map
        self.scene.add_sprite("Enemy", self.enemy_sprite)

        # --- Other stuff

        # Set the background color

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
        )

    def on_draw(self):
        """Render the screen."""
        # Activate the game camera
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""
        # Move the player with the physics engine
        self.physics_engine.update()

        # Så fjenden bevæger sig
        self.enemy_sprite.center_x += self.enemy_sprite.change_x
        self.enemy_sprite.center_y += self.enemy_sprite.change_y

        # Collision detection with player
        if arcade.check_for_collision(self.player_sprite, self.enemy_sprite):
            self.setup()  # Reset the game if player collides with enemy

        # Check for collision with lava
        lava_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Lava"]
        )
        if lava_hit_list:
            self.setup()  # Reset the game if player collides with lava

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Add one to the score
            self.score += 1

        # Position the camera
        self.center_camera_to_player()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
