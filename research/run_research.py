"""Run reproducible baseline validation and a bounded targeted tie search."""
import argparse
import csv
from dataclasses import asdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
from time import perf_counter

from a075777 import (
    certify_box, greedy, pair_rebalance_witness, prime_transfer_witness,
    solve, solve_reference, surface, tied_pairs,
)

HERE = Path(__file__).resolve().parent


def load_oeis(path):
    entries = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            n, area = map(int, line.split())
            entries[n] = area
    return entries


def baseline(path):
    entries = load_oeis(path)
    if any(n not in entries for n in range(1, 10001)):
        raise AssertionError("OEIS fixture must contain every index 1..10000")
    failures, nonunique = [], []
    worst = (0, 1, 1)
    for n in range(1, 10001):
        optimized, reference = solve(n), solve_reference(n)
        if optimized != reference or optimized.surface_area != entries[n]:
            raise AssertionError((n, optimized, reference, entries[n]))
        for dims in optimized.minimizers:
            certify_box(n, dims, optimized.surface_area)
        if len(optimized.minimizers) > 1:
            nonunique.append(n)
        heuristic_area = surface(greedy(n))
        if heuristic_area != optimized.surface_area:
            failures.append(n)
        if heuristic_area * worst[2] > worst[1] * optimized.surface_area:
            worst = (n, heuristic_area, optimized.surface_area)
    return {
        "validated_through": 10000,
        "oeis_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "reference_and_optimized_agree": True,
        "nonunique_volumes": nonunique,
        "greedy_failure_count": len(failures),
        "first_greedy_failures": failures[:20],
        "worst_greedy_ratio": {"n": worst[0], "numerator": worst[1],
                               "denominator": worst[2]},
    }


def search(bound, max_volume, output):
    cached_solve = lru_cache(maxsize=None)(solve)
    stats = {
        "smaller_side_bound": bound, "max_volume": max_volume,
        "base_pairs": bound * (bound + 1) // 2,
        "tied_pairs": 0, "distinct_volumes": 0, "largest_volume_found": 0,
        "pairs_above_100_million": 0,
        "both_prime_transfer_stable": 0,
        "both_pairwise_stable": 0,
        "optimal_ties": [], "pairwise_stable_examples": [],
    }
    volumes = set()
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["n", "a", "b", "c", "d", "e", "f", "tied_area",
                         "minimum_area", "witness_a", "witness_b", "witness_c",
                         "both_prime_transfer_stable", "both_pairwise_stable"])
        for n, x, y in tied_pairs(bound, max_volume):
            area = surface(x)
            certify_box(n, x, area)
            certify_box(n, y, area)
            if set(x) & set(y):
                raise AssertionError("no-shared-side lemma violated")
            result = cached_solve(n)
            witness = result.minimizers[0]
            certify_box(n, witness, result.surface_area)
            if result.surface_area > area:
                raise AssertionError("solver missed a feasible tied box")
            prime_stable = all(prime_transfer_witness(d) is None for d in (x, y))
            pair_stable = all(pair_rebalance_witness(d) is None for d in (x, y))
            stats["tied_pairs"] += 1
            stats["largest_volume_found"] = max(stats["largest_volume_found"], n)
            stats["pairs_above_100_million"] += n > 10 ** 8
            stats["both_prime_transfer_stable"] += prime_stable
            stats["both_pairwise_stable"] += pair_stable
            volumes.add(n)
            if pair_stable and len(stats["pairwise_stable_examples"]) < 10:
                stats["pairwise_stable_examples"].append(
                    {"n": n, "boxes": [x, y], "area": area,
                     "optimum": asdict(result)})
            if result.surface_area == area:
                # Crucial finding: independently enumerate every sorted triple.
                if solve_reference(n) != result:
                    raise AssertionError("counterexample failed independent verification")
                stats["optimal_ties"].append(
                    {"n": n, "boxes": [x, y], "result": asdict(result)})
            writer.writerow([n, *x, *y, area, result.surface_area, *witness,
                             int(prime_stable), int(pair_stable)])
    stats["distinct_volumes"] = len(volumes)
    stats["certificates_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
    return stats


def verify_certificates(path):
    count = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            n, area, minimum = (int(row[k]) for k in ("n", "tied_area", "minimum_area"))
            x = tuple(int(row[k]) for k in ("a", "b", "c"))
            y = tuple(int(row[k]) for k in ("d", "e", "f"))
            w = tuple(int(row[k]) for k in ("witness_a", "witness_b", "witness_c"))
            certify_box(n, x, area)
            certify_box(n, y, area)
            certify_box(n, w, minimum)
            # No trust in the solver needed to reject this pair as optimal.
            if minimum >= area:
                raise AssertionError("row has no strictly better witness")
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound", type=int, default=100)
    parser.add_argument("--max-volume", type=int, default=10 ** 12)
    parser.add_argument("--skip-baseline", action="store_true")
    parser.add_argument("--verify-certificates", type=Path)
    parser.add_argument("--output-dir", type=Path, default=HERE / "results")
    args = parser.parse_args()
    if args.verify_certificates:
        print(json.dumps({"verified_rejections": verify_certificates(args.verify_certificates)}))
        return
    if args.bound < 1 or args.max_volume < 1:
        parser.error("bounds must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = perf_counter()
    report = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "source_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (HERE / "a075777.py", HERE / "run_research.py")
        },
        "coverage": "All tied pairs with both second-smallest sides <= bound and n <= max_volume; not all n up to max_volume.",
    }
    if not args.skip_baseline:
        print("Validating 1..10000 against OEIS and independent enumeration...", flush=True)
        report["baseline"] = baseline(HERE / "data" / "b075777.txt")
        print(json.dumps(report["baseline"]), flush=True)
    print(f"Searching tied pairs with smaller sides <= {args.bound}...", flush=True)
    report["search"] = search(args.bound, args.max_volume, args.output_dir / "tie_certificates.csv")
    if not report["search"]["optimal_ties"]:
        report["independent_certificate_rejections"] = verify_certificates(
            args.output_dir / "tie_certificates.csv")
    report["elapsed_seconds"] = round(perf_counter() - started, 3)
    (args.output_dir / "summary.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["search"], indent=2), flush=True)
    print(f"Finished in {report['elapsed_seconds']} seconds.", flush=True)


if __name__ == "__main__":
    main()
