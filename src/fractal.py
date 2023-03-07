ESC = 10


def funct(z, c):
    return z*z+c


def iterate(c, ct):
    z = 0
    items = [z]
    for i in range(ct):
        z = funct(z, c)
        items.append(z)
    return items


def is_bound(items):
    return max([abs(i) for i in items]) < ESC


t = []
for img in range(-15, 15):
    row = '' 
    for r in range(-15, 15):
        c = complex(r, img)
        s = iterate(c, 10)
        b = is_bound(s)
        row += 'X' if b else ' '
    t.append(row)
for row in t:
    print(row)
