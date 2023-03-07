import arcade

ESCAPE_THRESHOLD = 10
MAX_ITERATIONS = 50
X_DIMENSION, Y_DIMENSION = 1000, 600
DRAW_STEP = 2
# the position in the Argand plane (complex number plane) that is drawn at the bottom-left of the window
X_POS, Y_POS = -2.25, -0.9
PIXEL_SIZE = 0.003  # the dimensions of each screen pixel in the Argand plane


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


def make_point_list():
    point_list = []
    for x_pixel in range(0, X_DIMENSION, DRAW_STEP):
        if x_pixel % 50 == 0:
            print(x_pixel)
        for y_pixel in range(0, Y_DIMENSION, DRAW_STEP):
            real = X_POS + (x_pixel * PIXEL_SIZE)
            img = Y_POS + (y_pixel * PIXEL_SIZE)
            c = complex(real, img)
            s = iterate(c, MAX_ITERATIONS)
            if is_bound(s):
                point_list.append((x_pixel, y_pixel))
    return point_list


if __name__ == '__main__':
    points = make_point_list()
    print('point list done')

    arcade.open_window(X_DIMENSION, Y_DIMENSION, "Fractal Experiments")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.start_render()
    arcade.draw_points(points, arcade.color.WHITE, 1)
    arcade.finish_render()
    arcade.run()
