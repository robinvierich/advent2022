
def vector_add(v1, v2):
    return tuple((v1i + v2i) for v1i, v2i in zip(v1, v2))

def vector_sub(v1, v2):
    return tuple((v1i - v2i) for v1i, v2i in zip(v1, v2))

def vector_mult(v1, v2):
    return tuple((v1i * v2i) for v1i, v2i in zip(v1, v2))

def vector_scale(v1, scalar):
    return tuple((v1i * scalar) for v1i in v1)
