import tempfile
from pathlib import Path
import unittest

from capacity_sequence import a, ceil_cuberoot, reference_terms, terms, verify, write_b_file


class CapacitySequenceTests(unittest.TestCase):
    def test_known_prefix(self):
        self.assertEqual(terms(32), [
            6, 10, 14, 16, 22, 22, 24, 24,
            30, 32, 32, 32, 40, 40, 40, 40,
            42, 42, 48, 48, 52, 52, 52, 52,
            54, 54, 54, 62, 62, 62, 64, 64])

    def test_independent_enumeration(self):
        self.assertEqual(terms(1000), reference_terms(1000))

    def test_root_boundaries_and_large_integers(self):
        self.assertEqual(ceil_cuberoot(1), 1)
        for k in (2, 3, 10, 100, 2 ** 54 + 3):
            self.assertEqual(ceil_cuberoot(k ** 3 - 1), k)
            self.assertEqual(ceil_cuberoot(k ** 3), k)
            self.assertEqual(ceil_cuberoot(k ** 3 + 1), k + 1)

    def test_bounds_monotonicity_and_cubes(self):
        values = terms(1000)
        self.assertEqual(values, sorted(values))
        for n, area in enumerate(values, 1):
            self.assertEqual(area % 2, 0)
            self.assertGreaterEqual(area ** 3, 216 * n*n)
            self.assertLessEqual(area, 6 * ceil_cuberoot(n) ** 2)
        for k in range(1, 31):
            self.assertEqual(a(k ** 3), 6 * k*k)

    def test_invalid_inputs(self):
        for value in (0, -1, True, 1.5, "7"):
            for method in (a, terms, reference_terms):
                with self.assertRaises(ValueError):
                    method(value)

    def test_b_file_format(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "terms.txt"
            write_b_file(path, terms(8))
            self.assertEqual(path.read_bytes(),
                             b"1 6\n2 10\n3 14\n4 16\n5 22\n6 22\n7 24\n8 24\n")

    def test_verifier_rejects_bad_term(self):
        values = terms(8)
        values[6] = 30
        with self.assertRaisesRegex(AssertionError, "n=7"):
            verify(values)


if __name__ == "__main__":
    unittest.main()
