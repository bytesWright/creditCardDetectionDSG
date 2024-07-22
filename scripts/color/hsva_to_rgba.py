# n_ = normalized to 0-1
def n_hsva_to_n_rgba(value):
    r = None
    g = None
    b = None

    h, s, v, a = value
    if s == 0.0:
        r = g = b = v
        return r, g, b

    i = int(h * 6)  # assuming h is in [0, 1]
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))

    i = i % 6

    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    elif i == 5:
        r, g, b = v, p, q

    if None in (r,g,b):
        raise Exception("could not convert from normalized hsva to normalized rgba")

    return r, g, b, a
