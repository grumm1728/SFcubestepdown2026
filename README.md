# Dandy Candies: integer boxes and surface area

[Explore the interactive comparison](index.html) or [open the original 3D sequence view](sequence.html).

Seven unit-cube candies show why the rules matter. An exact-fit rectangular box has dimensions 1 × 1 × 7 and surface area 30. If one empty cell is allowed, a 2 × 2 × 2 box holds all seven with surface area 24. The comparison lets you try 1 to 150 candies and see each box's dimensions, surface area, capacity, and unused cells. Its diagrams scale each box to fit, so use the numbers when comparing their size.

| Model | Box rule | Sequence | At n=7 |
| --- | --- | --- | ---: |
| Exact fit | Rectangular, integer sides, volume exactly n | [A075777](https://oeis.org/A075777) | 30 |
| Empty space allowed | Rectangular, integer sides, volume at least n | [A401021](https://oeis.org/A401021) (submitted draft) | 24 |
| Polycube | Any joined shape of exactly n cubes | [A193416](https://oeis.org/A193416) | 24 |

The third model is a different shape family; at n=5 its value is 20, versus 22 for the rectangular box that may contain empty cells. See the [educator guide](EDUCATOR_GUIDE.md) for classroom prompts and the story behind the variant.

## Run locally

Open [index.html](index.html) directly, or serve the repository with Python:

```powershell
python -m http.server 8000
```

Then open <http://localhost:8000>. The comparison needs no external libraries. The original 3D view uses Three.js from a CDN, so it needs an internet connection.

## Reproduce the sequence

Python 3.10 or later, standard library only:

```powershell
python research/capacity_sequence.py --terms 64
python research/capacity_sequence.py --terms 10000 --verify --b-file research/capacity/b401021.txt
python -m unittest discover -s research -v
```

The [generator](research/capacity_sequence.py) uses exact integer arithmetic and verifies its results against a second enumeration method. The [10,000-term b-file](research/capacity/b401021.txt) has offset 1 and the required OEIS filename. The [Mathematica program](research/capacity/a401021.wl), [submission draft](research/capacity/OEIS_SUBMISSION.md), [verification record](research/capacity/verification.json), and [prior-work review](research/capacity/PRIOR_WORK.md) are also here.

A closed form is not claimed. The [exact-volume research](research/README.md) includes proofs, computational experiments, and limitations for A075777.

## Credit

Kevin Karplus described the empty-space variant, including the seven-candies example and a capacity-record search, in comment 12 of [Dan Meyer's 2014 Dandy Candies post](https://blog.mrmeyer.com/2014/purposeful-practice-dandy-candies/). Addison Stumpf and Jonah discussed the variant further in comments 135–136 of [Meyer's 2015 post](https://blog.mrmeyer.com/2015/the-math-problem-that-1000-math-teachers-couldnt-solve/). The sequence table, generators, and verification in this repository document the formulation for OEIS.
