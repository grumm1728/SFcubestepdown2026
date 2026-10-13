# OEIS submission draft: capacity surface area

Prepared October 13, 2026. Submitted as OEIS draft A401021; acceptance is pending.

## Name

Minimum surface area of a rectangular solid with positive integer side lengths and volume at least n.

## Data

6, 10, 14, 16, 22, 22, 24, 24, 30, 32, 32, 32, 40, 40, 40, 40, 42, 42, 48, 48, 52, 52, 52, 52, 54, 54, 54, 62, 62, 62, 64, 64, 66, 66, 66, 66, 76, 76, 76, 76, 78, 78, 78, 78, 78, 80, 80, 80, 90, 90, 90, 90, 90, 90, 94, 94, 94, 94, 94, 94, 96, 96, 96, 96

## Offset

1,1

## Comments

Equivalently, the minimum surface area of an integer-sided rectangular box that can hold n unit cubes in an axis-aligned arrangement, allowing unused space.

Unlike A075777, the volume may exceed n. Unlike A193416, the enclosing shape must be a rectangular solid.

The sequence is nondecreasing and all terms are even.

The variant allowing unused space was discussed by gasstationwithoutpumps (Kevin Karplus) in comments on Dan Meyer's 2014 post and by Addison Stumpf and Jonah in comments on his 2015 post; see Links.

## Formula

a(n) = 2*min{x*y + x*z + y*z : x,y,z are positive integers and x*y*z >= n}.

a(n) = min{A075777(m) : n <= m <= ceiling(n^(1/3))^3}.

6*n^(2/3) <= a(n) <= 6*ceiling(n^(1/3))^2.

a(k^3) = 6*k^2 for k >= 1.

a(n) ~ 6*n^(2/3).

## Example

For n = 5, a box with dimensions 1,2,3 has volume 6 and surface area 22, which is minimal. One unit of capacity is unused.

For n = 7, a box with dimensions 2,2,2 has volume 8 and surface area 24, which is minimal. This differs from A075777(7) = 30, where the box must have volume exactly 7.

a(10) = a(11) = a(12) = 32, attained by the box with dimensions 2,2,3.

## Program

Paste the following into the Programs field, with the language label "(Python)" before the code. The same runnable code is saved as oeis_program.py beside this draft.

~~~python
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
~~~

## Cross-references

Cf. A075777, A193416.

## Keywords

nonn

## Author

Use your OEIS account signature and actual submission date. The proposed submitting author is Scott B. Farrar; confirm the account's preferred spelling when submitting.

## Links

- Dan Meyer, [Purposeful Practice & Dandy Candies](https://blog.mrmeyer.com/2014/purposeful-practice-dandy-candies/), August 5, 2014. See comment 12 by gasstationwithoutpumps, August 10, 2014, 11:46 am.
- Dan Meyer, [The Math Problem That 1,000 Math Teachers Couldn't Solve](https://blog.mrmeyer.com/2015/the-math-problem-that-1000-math-teachers-couldnt-solve/), September 24, 2015. See comments 135-136 by Addison Stumpf and Jonah, September 26, 2015.

## Links / attachment preparation

The accompanying b401021.txt contains the first 10,000 terms. Upload it through the A401021 edit page and add a Links entry to /A401021/b401021.txt. Add the resulting table link with your name and range 1..10000.

The A-number is allocated to the submitted draft. The source code and verification records accompany this repository.

## Proof and verification notes for the editor

Let k = ceiling(n^(1/3)). The cube with side k is feasible and has area 6*k^2. By AM-GM, every box of volume m has area at least 6*m^(2/3). If m > k^3, that area is strictly larger than 6*k^2, so such volumes cannot improve the cube. This proves the finite formula using A075777.

For the direct program, sort the sides x <= y <= z and work with half the surface area. The initial bound is H = 3*k^2. Any improving or tying box has x <= k, since its half-area is at least 3*x^2. It also satisfies y^2 + 2*x*y <= H, because z >= y. Thus y <= floor(sqrt(H+x^2))-x. For any fixed x,y, the smallest feasible z is max(y, ceiling(n/(x*y))); increasing z only increases the surface area. These observations prove that the finite integer loops return the exact minimum. Updating H to the best value already found only removes boxes that cannot improve or tie it.

Monotonicity follows because increasing the required capacity reduces the feasible set. The cube formula follows from the matching AM-GM bound. The stated asymptotic follows by squeezing between the two displayed bounds.

All first 10,000 terms were independently checked by enumerating every sorted integer box with exact volume at most 22^3 = 10,648 and then taking suffix minima. The independent method does not use the direct solver's side-area pruning. The standalone program pasted above was also checked against all 10,000 saved terms.

Seven capacity-specific unit tests cover the prefix, independent enumeration, integer cube-root boundaries beyond float precision, bounds, monotonicity, cubes, input validation, b-file encoding, and rejection of an incorrect term. The existing twelve A075777 tests also pass.

## Duplicate search record

On October 13, 2026, OEIS's direct JSON search returned HTTP 200 with null (no results) for both:

- 6,10,14,16,22,22,24,24,30,32,32,32
- 3,5,7,8,11,11,12,12,15,16,16,16

This supports proposing the entry but does not prove that no equivalent description or transformation is already listed. A193416 was checked directly and differs at n=5.

## Submission instructions consulted

- [OEIS submission page](https://oeis.org/Submit.html)
- [Style sheet](https://oeis.org/wiki/Style_Sheet)
- [B-file format](https://oeis.org/wiki/B-files)

These sections below the Author field are preparation notes, not additional OEIS fields. A closed form is not needed to define this sequence: the precise minimization, terminating exact program, proof of its finite bounds, and independently verified terms provide the mathematical content for review.
