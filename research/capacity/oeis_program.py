from math import isqrt


def ceil_cuberoot(n):
    """Exact ceil(cube_root(n)) for a positive integer."""
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 < n:
            lo = mid
        else:
            hi = mid
    return hi


def a(n):
    """Minimum of 2*(x*y+x*z+y*z) over positive integers x*y*z >= n."""
    k = ceil_cuberoot(n)
    best = 3 * k * k  # Half-area of a feasible k by k by k cube.
    for x in range(1, k + 1):
        # For x <= y <= z, half-area >= y*y + 2*x*y.
        for y in range(x, isqrt(best + x*x) - x + 1):
            z = max(y, (n + x*y - 1) // (x*y))
            best = min(best, x*y + x*z + y*z)
    return 2 * best


if __name__ == "__main__":
    print([a(n) for n in range(1, 65)])
