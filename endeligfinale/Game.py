import arcade
import subprocess

# Fra Arcade
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Hell Game"

# "Sprite Scaling" som enten gror eller formindsker vores sprite, men holder højde og bredde forskellen det samme
CHARACTER_SCALING = 0.3
# Samme fra arcade, men er her til vores enemy sprites
ENEMY_SCALING = 0.7
SPRITE_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Fra arcade
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class MainScreen(arcade.View):
    def setup(self):
        self.background = None

    def on_show(self):
        self.background = arcade.load_texture("image.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("WELCOME TO HELL GAME!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.GOLD, 20, anchor_x="center")

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # Knap til at køre Hellgame.py
        arcade.draw_rectangle_filled(500, 307, 200, 50, arcade.color.LIGHT_GRAY)
        arcade.draw_text("Run Hellgame", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25, arcade.color.BLACK, 14, anchor_x="center")
        arcade.draw_text("Made by Isse!", 400, 600, arcade.color.GOLD, 20 )
        arcade.draw_text("Press the Button to run Hellgame", 250, 350,arcade.color.BLACK_OLIVE, 25)



    def on_mouse_press(self, x, y, button, modifiers):
        if 300 <= x <= 500 and 200 <= y <= 340:
            # Run Endelige.py
            subprocess.run(["python", "Endelige.py"])
            arcade.close_window()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Main Screen")
    window.show_view(MainScreen())
    arcade.run()







if __name__ == "__main__":
    main()