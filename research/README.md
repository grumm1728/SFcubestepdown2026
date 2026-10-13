# A075777 research harness

Start with [FINDINGS.md](FINDINGS.md) for outcomes and [NOTEBOOK.md](NOTEBOOK.md) for proofs, source citations, and research limitations.

The original browser visualization is [sequence.html](../sequence.html); [index.html](../index.html) compares exact fit with boxes allowing unused capacity. The research code has no third-party dependencies. Use Python 3.10 or later; the recorded runs used Python 3.13.7.

## Run on Windows

In PowerShell:

~~~powershell
Set-Location -LiteralPath 'C:\Users\scott\Cloned from GitHub\SFcubestepdown2026'
python -m unittest discover -s research -v
python research/a075777.py 68
python research/a075777.py 246 --reference
python research/run_research.py
python research/run_research.py --bound 200 --skip-baseline --output-dir research/results/bound200
~~~

The default experiment validates every index 1..10000 against both the OEIS fixture and independent exhaustive enumeration, then searches tied pairs with both middle sides at most 100 and volume at most one trillion. The second command extends the side bound to 200. Output directories are created if needed; rerunning replaces their summary and certificate files.

Recorded runtimes on this machine were about 4 seconds for the baseline/default experiment and 48 seconds for the B=200 search. These are observations, not performance guarantees. Pair enumeration grows approximately as the fourth power of the side bound; factorization can also dominate at larger sizes.

To verify the saved rejection witnesses without rerunning factorization or the search:

~~~powershell
python research/run_research.py --verify-certificates research/results/tie_certificates.csv
python research/run_research.py --verify-certificates research/results/bound200/tie_certificates.csv
~~~

This verifier checks positive sorted integer dimensions, equal volume, equal tied area, and a strictly smaller witness area. It proves each listed pair is nonoptimal. It does not prove that the witness itself is a global minimum, nor that the candidate list is complete; the solver and generator proofs establish those separate claims. If a later search finds an optimal tie, the rejection-only verifier intentionally fails on that row.

## Research interfaces

- solve(n): optimized exact Result(surface_area, minimizers); retains all sorted optimal triples.
- solve_reference(n): independent exhaustive integer-loop version with the same result.
- dominant_prime_formula(m, p): exact unique result for prime p > m.
- prime_power_formula(p, exponent): exact area for prime-power volume.
- tied_pairs(bound, max_volume): yields (n, first_box, second_box).
- prime_transfer_witness(dims) and pair_rebalance_witness(dims): return a strictly better sorted box when the respective necessary optimality test fails, otherwise None. Pass positive sorted triples.

Positive-integer inputs exclude bool values. All mathematical decisions use exact integer arithmetic. Floating-point values are used only for elapsed-time reporting.

## Data and output provenance

[data/b075777.txt](data/b075777.txt) is Robert Israel's [OEIS reference table](https://oeis.org/A075777/b075777.txt), downloaded October 8, 2026, unchanged. Its SHA-256 and the two computation source hashes appear in each applicable summary.

[results/summary.json](results/summary.json) records baseline checks and B=100 results. [results/bound200/summary.json](results/bound200/summary.json) records B=200. Their CSV files contain all generated ties under the declared limits and explicit better-box witnesses. The B=100 data are contained within the B=200 search region; do not add their counts as independent cases.

Timestamps in JSON use UTC; the notebook uses the user's local research date. No package installation, external service, or network connection is needed to reproduce the saved experiments.

## Verification coverage

The 12 A075777 unit tests cover exact roots beyond floating-point precision, invalid inputs, independent solver agreement, historical examples, prime powers, dominant-prime families, tie-generator completeness against brute force in a small region, valid improvement witnesses, nonoptimal ties, local-versus-global optimality, scaling, and the arbitrarily bad greedy family.

The main experiment separately compares all 10,000 reference terms. A candidate optimal tie triggers independent exhaustive verification before it is recorded. The scripts do not assume uniqueness.

The checkout began at commit 49381476e62ca43293934605c6eb3263405d5a9a. These research files are included as a reproducible companion to the submission.

## Empty-space-allowed capacity sequence

[Submission draft](capacity/OEIS_SUBMISSION.md), [10,000-term table](capacity/b401021.txt), and [verification record](capacity/verification.json).

The standalone [capacity generator](capacity_sequence.py) computes minimum surface area for volume **at least** n. It needs no OEIS table, factorization library, or network access. The shorter [OEIS program](capacity/oeis_program.py) is self-contained and copy-pastable.

~~~powershell
python research/capacity_sequence.py --terms 64
python research/capacity_sequence.py --terms 10000 --verify --b-file research/capacity/b401021.txt
python -m unittest discover -s research -v
~~~

The first command prints terms. The second verifies them by independent exact-volume enumeration before writing the b-file. Seven capacity tests bring the total to nineteen. The sequence is submitted as draft [A401021](https://oeis.org/A401021). Its b-file now has the assigned filename. See the [educator guide](../EDUCATOR_GUIDE.md) and [Mathematica program](capacity/a401021.wl).
