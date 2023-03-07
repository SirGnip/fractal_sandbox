import arcade

ESCAPE_THRESHOLD = 10
MAX_ITERATIONS = 50
X_DIMENSION, Y_DIMENSION = 500, 500


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


if __name__ == '__main__':
    arcade.open_window(X_DIMENSION, Y_DIMENSION, "Fractal Experiments")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.start_render()

    STRIDE = 3
    DIVISOR = 200

    for x_pixel in range(0, X_DIMENSION, STRIDE):
        if x_pixel % 50 == 0:
            print(x_pixel)
        for y_pixel in range(0 ,Y_DIMENSION, STRIDE):
            real = (x_pixel / DIVISOR) - 1.75
            img = (y_pixel / DIVISOR) - 1.25
            c = complex(real, img)
            s = iterate(c, MAX_ITERATIONS)
            if is_bound(s):
                arcade.draw_point(x_pixel, y_pixel, arcade.color.WHITE, 1)

    arcade.finish_render()
    print('done')
    arcade.run()
