"""Exact, dependency-free tools for OEIS A075777.

All decisions use integer arithmetic. No uniqueness assumption is made.
"""
import argparse
from dataclasses import asdict, dataclass
import json
from functools import lru_cache
from itertools import combinations
from math import isqrt, prod


def positive_integer(n):
    if type(n) is not int or n < 1:
        raise ValueError("expected a positive integer")
    return n


def icbrt(n):
    """Floor cube root, including values beyond float precision."""
    if type(n) is not int or n < 0:
        raise ValueError("expected a nonnegative integer")
    lo, hi = 0, 1 << ((n.bit_length() + 2) // 3)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


@lru_cache(maxsize=16384)
def factorization(n):
    """Trial division; exact, intended for the bounded experiments here."""
    positive_integer(n)
    factors = []
    p = 2
    while p * p <= n:
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if exponent:
            factors.append((p, exponent))
        p = 3 if p == 2 else p + 2
    if n > 1:
        factors.append((n, 1))
    return tuple(factors)


def divisors(n):
    values = [1]
    for p, exponent in factorization(n):
        old = values[:]
        power = 1
        for _ in range(exponent):
            power *= p
            values.extend(d * power for d in old)
    return sorted(values)


def closest_divisor(n):
    return next(d for d in reversed(divisors(n)) if d * d <= n)


def surface(dims):
    a, b, c = dims
    return 2 * (a * b + a * c + b * c)


@dataclass(frozen=True)
class Result:
    surface_area: int
    minimizers: tuple[tuple[int, int, int], ...]


def solve(n):
    """One closest factor pair per possible smallest side; retain all ties."""
    positive_integer(n)
    best, winners = None, set()
    for a in divisors(n):
        if a ** 3 > n:
            break
        remaining = n // a
        b = closest_divisor(remaining)
        c = remaining // b
        # No sorted triple with smallest side a exists if b < a.
        if b < a:
            continue
        dims = (a, b, c)
        area = surface(dims)
        if best is None or area < best:
            best, winners = area, {dims}
        elif area == best:
            winners.add(dims)
    return Result(best, tuple(sorted(winners)))


def all_dimensions_reference(n):
    """Independent exhaustive integer-loop enumeration, with no factoring."""
    positive_integer(n)
    a = 1
    while a ** 3 <= n:
        if n % a == 0:
            remaining = n // a
            for b in range(a, isqrt(remaining) + 1):
                if remaining % b == 0:
                    yield (a, b, remaining // b)
        a += 1


def solve_reference(n):
    best, winners = None, []
    for dims in all_dimensions_reference(n):
        area = surface(dims)
        if best is None or area < best:
            best, winners = area, [dims]
        elif area == best:
            winners.append(dims)
    return Result(best, tuple(winners))


def greedy(n):
    """Historical cube-step-down heuristic, with exact roots."""
    positive_integer(n)
    a = icbrt(n)
    while n % a:
        a -= 1
    b = isqrt(n // a)
    while (n // a) % b:
        b -= 1
    return tuple(sorted((a, b, n // (a * b))))


def prime_power_formula(p, exponent):
    positive_integer(p)
    if factorization(p) != ((p, 1),):
        raise ValueError("p must be prime")
    if type(exponent) is not int or exponent < 0:
        raise ValueError("exponent must be a nonnegative integer")
    q, r = divmod(exponent, 3)
    return 2 * p ** (2 * q) * (3, 1 + 2 * p, p * p + 2 * p)[r]


def prime_transfer_witness(dims):
    """Lemma 2.1 of Rotge--Tenenbaum: return a strictly better box if found."""
    for i, j in combinations(range(3), 2):
        small, large = dims[i], dims[j]
        if large > 1:
            p = factorization(large)[0][0]
            if small * p < large:
                other = list(dims)
                other[i], other[j] = small * p, large // p
                return tuple(sorted(other))
    return None


def pair_rebalance_witness(dims):
    """A stronger necessary test: every pair must be its closest factor pair."""
    for i, j in combinations(range(3), 2):
        product = dims[i] * dims[j]
        small = closest_divisor(product)
        large = product // small
        if small + large < dims[i] + dims[j]:
            other = list(dims)
            other[i], other[j] = small, large
            return tuple(sorted(other))
    return None


def tied_pairs(bound=100, max_volume=10 ** 12):
    """Every distinct tied pair with both second-smallest sides <= bound.

    Orient ab < de; equal products force identical boxes. No scaling quotient
    is applied: scaling preserves a tie but need not preserve global optimality.
    """
    positive_integer(bound)
    positive_integer(max_volume)
    pairs = sorted((a * b, a + b, a, b)
                   for a in range(1, bound + 1)
                   for b in range(a, bound + 1))
    for i, (u, s, a, b) in enumerate(pairs):
        for j in range(i + 1, len(pairs)):
            v, t, d, e = pairs[j]
            if u == v:
                continue
            denominator = s * v - t * u
            if denominator <= 0:
                continue
            numerator = (v - u) * v
            c, remainder = divmod(numerator, denominator)
            if remainder or c < b:
                continue
            n = u * c
            if n > max_volume or n % v:
                continue
            f = n // v
            if f < e:
                continue
            yield n, (a, b, c), (d, e, f)


def certify_box(n, dims, expected_area=None):
    if len(dims) != 3 or any(type(d) is not int or d < 1 for d in dims):
        raise AssertionError("invalid integer dimensions")
    if tuple(sorted(dims)) != tuple(dims) or prod(dims) != n:
        raise AssertionError("dimensions are unsorted or have wrong volume")
    if expected_area is not None and surface(dims) != expected_area:
        raise AssertionError("surface area mismatch")


def dominant_prime_formula(m, p):
    """Unique optimum for n=m*p, prime p>m."""
    positive_integer(m)
    positive_integer(p)
    if p <= m or factorization(p) != ((p, 1),):
        raise ValueError("require a prime p > m")
    a = closest_divisor(m)
    dims = (a, m // a, p)
    return Result(surface(dims), (dims,))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("--reference", action="store_true")
    args = parser.parse_args()
    if args.n < 1:
        parser.error("n must be positive")
    result = solve_reference(args.n) if args.reference else solve(args.n)
    print(json.dumps({"n": args.n, **asdict(result)}, indent=2))
