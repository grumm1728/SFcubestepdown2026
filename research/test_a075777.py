import unittest
from collections import defaultdict
from itertools import combinations
from math import prod

from a075777 import (
    all_dimensions_reference, certify_box, dominant_prime_formula, greedy, icbrt,
    pair_rebalance_witness, prime_power_formula, prime_transfer_witness,
    solve, solve_reference, surface, tied_pairs,
)


class ExactArithmeticTests(unittest.TestCase):
    def test_integer_cube_root_boundaries(self):
        for k in (1, 2, 3, 10, 100, 2 ** 54 + 3):
            self.assertEqual(icbrt(k ** 3), k)
            self.assertEqual(icbrt(k ** 3 - 1), k - 1)
            self.assertEqual(icbrt(k ** 3 + 1), k)
        self.assertEqual(icbrt(0), 0)

    def test_invalid_input(self):
        for value in (0, -1, 1.5, True, "12"):
            with self.assertRaises(ValueError):
                solve(value)

    def test_reference_agreement(self):
        for n in range(1, 2001):
            self.assertEqual(solve(n), solve_reference(n), n)

    def test_known_examples_and_greedy_failures(self):
        for n, area, dims in (
            (1, 6, (1, 1, 1)), (12, 32, (2, 2, 3)),
            (68, 144, (2, 2, 17)), (246, 422, (2, 3, 41)),
        ):
            self.assertEqual(solve(n).surface_area, area)
            self.assertEqual(solve(n).minimizers, (dims,))
        self.assertEqual(next(n for n in range(1, 100)
                              if surface(greedy(n)) > solve(n).surface_area), 68)

    def test_prime_powers_and_bounds(self):
        for p in (2, 3, 5, 7, 11):
            for exponent in range(13):
                result = solve(p ** exponent)
                self.assertEqual(result.surface_area, prime_power_formula(p, exponent))
                self.assertEqual(len(result.minimizers), 1)
        for n in range(1, 1001):
            area = solve(n).surface_area
            self.assertGreaterEqual(area ** 3, 216 * n ** 2)
            self.assertLessEqual(area, 4 * n + 2)

    def test_tie_generator_completeness_against_brute_force(self):
        bound, limit = 12, 1000
        expected = set()
        for n in range(1, limit + 1):
            groups = defaultdict(list)
            for dims in all_dimensions_reference(n):
                if dims[1] <= bound:
                    groups[surface(dims)].append(dims)
            for boxes in groups.values():
                for x, y in combinations(boxes, 2):
                    expected.add((n, tuple(sorted((x, y)))))
        rows = list(tied_pairs(bound, limit))
        actual = {(n, tuple(sorted((x, y)))) for n, x, y in rows}
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), len(rows))
        self.assertIn((162, ((2, 9, 9), (3, 3, 18))), actual)

    def test_tie_and_improvement_certificates(self):
        count = 0
        for n, x, y in tied_pairs(20, 10 ** 6):
            count += 1
            certify_box(n, x)
            certify_box(n, y, surface(x))
            self.assertFalse(set(x) & set(y))
            for dims in (x, y):
                for method in (prime_transfer_witness, pair_rebalance_witness):
                    witness = method(dims)
                    if witness:
                        certify_box(n, witness)
                        self.assertLess(surface(witness), surface(dims))
        self.assertGreater(count, 0)

    def test_nonoptimal_tie(self):
        self.assertEqual(surface((2, 9, 9)), surface((3, 3, 18)))
        self.assertEqual(solve(162).minimizers, ((3, 6, 9),))

    def test_dominant_prime_family(self):
        for p in (2, 3, 5, 7, 11, 17, 31, 101):
            for m in range(1, p):
                self.assertEqual(solve(m * p), dominant_prime_formula(m, p))

    def test_pairwise_stability_is_not_sufficient(self):
        self.assertIsNone(pair_rebalance_witness((5, 8, 9)))
        self.assertEqual(surface((5, 8, 9)), 314)
        self.assertEqual(solve(360).surface_area, 312)

    def test_scaling_does_not_preserve_optimality(self):
        original = solve(3).minimizers[0]
        scaled = tuple(2 * d for d in original)
        self.assertGreater(surface(scaled), solve(24).surface_area)

    def test_greedy_bad_family(self):
        for t, p in ((2, 17), (3, 83), (4, 257), (10, 10007)):
            self.assertGreater(p, t ** 4)
            n = t * t * p
            self.assertEqual(greedy(n), (1, t * t, p))
            self.assertLess(surface((t, t, p)), surface(greedy(n)))


if __name__ == "__main__":
    unittest.main()
