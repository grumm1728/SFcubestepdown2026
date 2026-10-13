"""Minimum surface area of an integer-sided box with volume at least n.

This is the empty-space-allowed sequence, not OEIS A075777 or A193416.
Python 3.10+, standard library only. All mathematical decisions are exact.
"""
import argparse
from math import isqrt
from pathlib import Path
import sys


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


def terms(count):
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")
    return [a(n) for n in range(1, count + 1)]


def reference_terms(count):
    """Independent method: enumerate exact-volume boxes, then suffix minima.

    Every relevant volume is <= ceil(cube_root(count))**3 by AM-GM.
    This deliberately does not use the direct solver's side-area bounds.
    """
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")
    side = 1
    while side ** 3 < count:
        side += 1
    limit = side ** 3
    exact = [4 * m + 2 for m in range(limit + 1)]
    x = 1
    while x ** 3 <= limit:
        y = x
        while x * y * y <= limit:
            for z in range(y, limit // (x*y) + 1):
                m = x*y*z
                exact[m] = min(exact[m], 2 * (x*y + x*z + y*z))
            y += 1
        x += 1
    best = exact[limit]
    for m in range(limit, 0, -1):
        best = min(best, exact[m])
        exact[m] = best
    return exact[1:count + 1]


def verify(values):
    reference = reference_terms(len(values))
    for n, (actual, expected) in enumerate(zip(values, reference), 1):
        if actual != expected:
            raise AssertionError(f"n={n}: direct={actual}, reference={expected}")
    return len(values)


def write_b_file(path, values):
    """Consecutive indices, one ASCII space, LF endings, no BOM."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for n, value in enumerate(values, 1):
            handle.write(f"{n} {value}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", type=int, default=64, metavar="N")
    parser.add_argument("--verify", action="store_true",
                        help="compare every term with independent enumeration")
    parser.add_argument("--b-file", type=Path,
                        help="write a table instead of printing comma-separated terms")
    args = parser.parse_args()
    if args.terms < 1:
        parser.error("--terms must be positive")
    values = terms(args.terms)
    if args.verify:
        verify(values)
        print(f"Verified {len(values)} terms by two independent methods.", file=sys.stderr)
    if args.b_file:
        write_b_file(args.b_file, values)
        print(f"Wrote {len(values)} terms to {args.b_file}", file=sys.stderr)
    else:
        print(", ".join(map(str, values)))


if __name__ == "__main__":
    main()
