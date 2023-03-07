ESCAPE_THRESHOLD = 1.5
STEPS_HALF = 30
MAX_ITERATIONS = 100
DIVISOR = 20


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
    return max([abs(i) for i in items]) < ESCAPE_THRESHOLD


t = []
for img in [i / DIVISOR for i in range(-STEPS_HALF, STEPS_HALF)]:
    row = ''
    for r in [i / DIVISOR for i in range(-STEPS_HALF, STEPS_HALF)]:
        c = complex(r, img)
        s = iterate(c, MAX_ITERATIONS)
        b = is_bound(s)
        row += 'X' if b else ' '
    t.append(row)
for row in t:
    print(row)
