import time
import arcade
import utils
import concurrent.futures

ESCAPE_THRESHOLD = 10
MAX_ITERATIONS = 200
X_DIMENSION, Y_DIMENSION = 1000, 600
DRAW_STEP_START = 10
# the position in the Argand plane (complex number plane) that is drawn at the bottom-left of the window
X_START, Y_START = -2.25, -0.9
PIXEL_SIZE_START = 0.003  # the dimensions of each screen pixel in the Argand plane
NUM_PIXELS_TO_MOVE = 20
ZOOM_PERCENT = .1
MAX_PROC_WORKERS = 8


def iterate(c, count) -> bool:
    """Returns true if bound, false if unbound"""
    z = 0
    items = [z]
    for i in range(count):
        z = z * z + c
        items.append(z)
        if abs(z) > ESCAPE_THRESHOLD:
            return False
    return True


def do_work(x_pix_start, x_pix_end, x_off, y_off, pix_size, draw_step):
    # print('do_work', x_pix)
    with utils.SimpleTimer() as timer:
        point_list = []
        for x_pix in range(x_pix_start, x_pix_end, draw_step):
            for y_pixel in range(0, Y_DIMENSION, draw_step):
                real = x_off + (x_pix * pix_size)
                img = y_off + (y_pixel * pix_size)
                c = complex(real, img)
                is_bound = iterate(c, MAX_ITERATIONS)
                if is_bound:
                    point_list.append((x_pix, y_pixel))
    # print("worker", x_pix_start, timer.elapsed)
    return point_list


def make_point_list(executor, x_pos, y_pos, pixel_size, draw_step):
    chunk_size = 20
    chunks = 0
    futures = []
    for x_pixel in range(0, X_DIMENSION, chunk_size):
        futures.append(executor.submit(do_work, x_pixel, x_pixel + chunk_size, x_pos, y_pos, pixel_size, draw_step))  # non blocking
        chunks += 1
    print('waiting for results after scheduling chunks:', chunks)
    results = [fut.result() for fut in futures]  # blocking

    points = []
    for r in results:
        points.extend(r)
    return points


class MyFractal(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.x_pos, self.y_pos = X_START, Y_START
        self.pixel_size = PIXEL_SIZE_START
        self.draw_step = DRAW_STEP_START

        self.exe = concurrent.futures.ProcessPoolExecutor(max_workers=MAX_PROC_WORKERS)
        arcade.set_background_color(arcade.color.BLACK)
        self.point_list = []
        self.recalc()

    def recalc(self):
        with utils.SimpleTimer() as timer:
            self.point_list = make_point_list(self.exe, self.x_pos, self.y_pos, self.pixel_size, self.draw_step)
        print(f"{self.x_pos:.6f},{self.y_pos:.6f} pixel_size={self.pixel_size:.6f} elapsed={timer.elapsed:.2f}")

    def on_draw(self):
        self.clear()
        arcade.draw_points(self.point_list, arcade.color.WHITE, 1)

    def on_update(self, delta_time):
        time.sleep(0.001)

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
            self.exe.shutdown()
            self.close()

    def on_mouse_press(self, x, y, button, key_modifiers):
        print('mouse', x, y, button)


def main():
    app = MyFractal(X_DIMENSION, Y_DIMENSION, "Mandelbrot Set experimentation")
    app.set_location(250, 20)
    arcade.run()


if __name__ == "__main__":
    main()
