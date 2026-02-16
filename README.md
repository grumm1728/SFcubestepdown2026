# Integer Prism Surface-Minimizing Sequence Visualizer

This small browser app computes, for each `n`, an integer-sided rectangular prism `(a,b,c)` with:

- `a*b*c = n`
- minimal surface area `2(ab + ac + bc)` among all integer triples with that volume.

It then places each prism in a shared 3D scene centered at `(a,b,c)` and lets you scrub through the sequence with a slider so prisms appear over time.

## Run locally

```bash
python -m http.server 8000
```

Open <http://localhost:8000>.

## Controls

- **Max n in sequence**: upper bound for sequence generation.
- **Build sequence**: recompute all prisms from `1..n`.
- **Show first k prisms** (slider): reveal the first `k` sequence entries.

## Notes

- The app enforces sorted dimensions (`a <= b <= c`) so each prism shape is unique.
- If multiple triples tie for minimal area (rare), it chooses the lexicographically smallest triple.
