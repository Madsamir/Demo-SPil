import arcade
import subprocess

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

class MainScreen(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.RED_DEVIL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Screen", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.BLACK, 20, anchor_x="center")

        # Knap til at køre Hellgame.py
        arcade.draw_rectangle_filled(500, 307, 200, 50, arcade.color.LIGHT_GRAY)
        arcade.draw_text("Run Hellgame", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25, arcade.color.BLACK, 14, anchor_x="center")


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