# Findings: A075777

October 8, 2026 (America/Los_Angeles).

## Main mathematical outcome

**No universal algebraic formula exists.** The [notebook, Section 4](NOTEBOOK.md#4-no-universal-algebraic-formula) proves that no nonzero polynomial F(X,Y) can satisfy F(n,A(n))=0 for all sufficiently large positive integers n.

The key family is
\[
A(t^2p)=2t^2+4tp,\qquad p>t^2\text{ prime}.
\]
For each fixed t, infinitely many sequence points lie on a different line. A polynomial vanishing on the entire sequence would need infinitely many distinct linear factors.

This excludes fixed finite formulas using arithmetic and fixed-degree radicals, including a finite selection among such formulas. It does **not** exclude formulas using floor, log, exp, or other operations outside algebraic functions. The broader search-free question remains unresolved.

This is an independently reviewed elementary proof, with historical novelty unverified.

## Exact cases and algorithmic results

The notebook proves uniqueness and formulas for prime powers and for n=mp with p prime and p>m. It also proves that the original greedy heuristic has unbounded approximation ratio: at n=t²p with p>t⁴, the ratio exceeds t/2.

The optimized exact solver retains one closest factor pair for each candidate smallest side and returns every minimizing sorted triple. This is a genuine reduction of the original inner search, but still uses divisors.

The two independent solvers agree with all 10,000 OEIS reference values. The historical heuristic fails at 2,424 of these inputs, first at n=68. Its largest ratio in that finite range is 20,998/9,022 at n=9,980. This is a finite-range statistic, not an asymptotic failure frequency.

## Uniqueness experiments

| Measure | Middle-side bound 100 | Middle-side bound 200 |
|---|---:|---:|
| Volume cap | 1,000,000,000,000 | 1,000,000,000,000 |
| Generated tied pairs | 6,056 | 32,640 |
| Distinct volumes | 4,351 | 22,039 |
| Largest generated volume | 6,007,574,720 | 562,862,113,400 |
| Pairs above volume 100,000,000 | 176 | 5,430 |
| Both boxes pass prime-transfer tests | 21 | 123 |
| Both boxes pass all pair-rebalancing tests | 0 | 0 |
| Optimal ties found | 0 | 0 |
| Independently checked rejection certificates | 6,056 | 32,640 |

Every pair has a certified box of the same volume with strictly smaller surface area. Counts refer to unordered pairs of distinct sorted boxes; one volume can contain multiple tied pairs. B=100 is nested within B=200, so the combined result is 32,640 distinct pairs, not their sum.

Coverage is **all tied pairs in which both boxes have middle side at most B, subject to the volume cap**. It is not all volumes through that cap.

A further lemma proves that every hypothetical nonunique optimum has largest side c <= ab, so a bounded-middle-side candidate has volume <= B⁴. Therefore B=100 cannot extend optimal-uniqueness evidence beyond the paper's reported 10⁸ range. The B=200 experiment reaches a potentially new region up to 1.6×10⁹, without exhaustive coverage of every volume there.

From the B=200 certificates, 17,705 pairs satisfy c <= ab and f <= de; 581 of these have volume above 10⁸. All were rejected. These extra counts can be recomputed directly from the CSV dimensions.

The largest prime-transfer-stable pair volume at B=200 was 9,828,000. Thus no pair above 10⁸ even survived that necessary condition in this experiment.

## A near miss and a failed proof strategy

The B=200 pair closest to the optimum in relative surface area was at n=5,760,000:

- (160,160,225) and (144,200,200) both have area 195,200.
- (160,180,200) has minimum area 193,600.
- Both tied boxes pass the prime-transfer tests, but a broader two-side rebalance improves them.

A tempting proof strategy is to characterize global optimality by pairwise balance. It fails: (5,8,9) is already balanced within every pair, but at volume 360 its area 314 loses to (6,6,10), with area 312.

A stronger question remains promising: does every distinct equal-volume, equal-area pair contain at least one box that is not pairwise balanced? Every recorded pair supports this statement, but no general proof is supplied. Such a proof would imply uniqueness.

## What remains unresolved

The [2026 paper](https://tenenb.perso.math.cnrs.fr/PPP/on_integral_boxes.pdf) leaves general optimal-box uniqueness open. Our search found no counterexample and does not prove uniqueness. A targeted literature check found no subsequent resolution, but that check is not exhaustive.

No universal search-free formula with floor/log/exp was found, and none was ruled out. The notebook's obstruction is specifically algebraic. None of these computations establishes computational complexity.

The next useful investigation is symbolic analysis of pairs that pass all pair-rebalancing conditions, followed by targeted searches in larger side regions. Simply scaling smaller examples is unreliable because scaling need not preserve optimality.

## Reproduce and inspect

Use [README.md](README.md) for commands and interfaces; [NOTEBOOK.md](NOTEBOOK.md) for proofs. The two JSON summaries and their CSV certificates under results/ preserve bounds, checksums, run metadata, and explicit rejection witnesses. All 12 unit tests passed.
