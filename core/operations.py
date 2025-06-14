def add(c0_left, c1_left, c0_right, c1_right):
    return c0_left + c0_right, c1_left + c1_right

def mul(c0_left, c1_left, c0_right, c1_right):
    return c0_left * c0_right, c0_left * c1_right + c1_left * c0_right, c1_left * c1_right