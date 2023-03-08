import arcade
import utils

ESCAPE_THRESHOLD = 10
MAX_ITERATIONS = 50
X_DIMENSION, Y_DIMENSION = 1000, 600
DRAW_STEP_START = 2
# the position in the Argand plane (complex number plane) that is drawn at the bottom-left of the window
X_START, Y_START = -2.25, -0.9
PIXEL_SIZE_START = 0.003  # the dimensions of each screen pixel in the Argand plane
NUM_PIXELS_TO_MOVE = 20
ZOOM_PERCENT = .1


def funct(z, c):
    return z * z + c


def iterate(c, count):
    z = 0
    items = [z]
    for i in range(count):
        z = funct(z, c)
        items.append(z)
    return items


def is_bound(items):
    try:
        return max([abs(i) for i in items]) < ESCAPE_THRESHOLD
    except OverflowError:
        return False


def make_point_list(x_pos, y_pos, pixel_size, draw_step):
    point_list = []
    for x_pixel in range(0, X_DIMENSION, draw_step):
        if x_pixel % 50 == 0:
            print(x_pixel)
        for y_pixel in range(0, Y_DIMENSION, draw_step):
            real = x_pos + (x_pixel * pixel_size)
            img = y_pos + (y_pixel * pixel_size)
            c = complex(real, img)
            s = iterate(c, MAX_ITERATIONS)
            if is_bound(s):
                point_list.append((x_pixel, y_pixel))
    return point_list


class MyFractal(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.x_pos, self.y_pos = X_START, Y_START
        self.pixel_size = PIXEL_SIZE_START
        self.draw_step = DRAW_STEP_START

        arcade.set_background_color(arcade.color.BLACK)
        self.point_list = []
        self.recalc()

    def recalc(self):
        with utils.SimpleTimer() as timer:
            self.point_list = make_point_list(self.x_pos, self.y_pos, self.pixel_size, self.draw_step)
        print(f"{self.x_pos:.6f},{self.y_pos:.6f} pixel_size={self.pixel_size:.6f} elapsed={timer.elapsed:.1f}")

    def on_draw(self):
        self.clear()
        arcade.draw_points(self.point_list, arcade.color.WHITE, 1)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.H:
            self.x_pos -= self.pixel_size * NUM_PIXELS_TO_MOVE
            self.recalc()
        elif key == arcade.key.L:
            self.x_pos += self.pixel_size * NUM_PIXELS_TO_MOVE
            self.recalc()
        elif key == arcade.key.J:
            self.y_pos -= self.pixel_size * NUM_PIXELS_TO_MOVE
            self.recalc()
        elif key == arcade.key.K:
            self.y_pos += self.pixel_size * NUM_PIXELS_TO_MOVE
            self.recalc()
        elif key == arcade.key.D:
            self.pixel_size *= 1.0 - ZOOM_PERCENT
            self.recalc()
        elif key == arcade.key.F:
            self.pixel_size *= 1.0 + ZOOM_PERCENT
            self.recalc()
        elif arcade.key.KEY_0 <= key <= arcade.key.KEY_9:
            if key == arcade.key.KEY_0:
                self.draw_step = 10
            else:
                self.draw_step = key - arcade.key.KEY_0
            print("Changing draw step:", self.draw_step)
            self.recalc()
        elif key in (arcade.key.Q, arcade.key.ESCAPE):
            print("Quitting")
            self.close()

    def on_mouse_press(self, x, y, button, key_modifiers):
        print('mouse', x, y, button)


def main():
    app = MyFractal(X_DIMENSION, Y_DIMENSION, "Mandelbrot Set experimentation")
    arcade.run()


if __name__ == "__main__":
    main()
