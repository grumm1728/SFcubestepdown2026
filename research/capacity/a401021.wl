(* OEIS A401021: minimum area of an integer-sided box holding at least n cubes. *)
Clear[a401021];
a401021[n_Integer] /; n >= 1 := Module[{k, best, x, y, z},
  k = Ceiling[n^(1/3)];
  best = 3 k^2;
  Do[
    Do[
      z = Max[y, Ceiling[n/(x y)]];
      best = Min[best, x y + x z + y z],
      {y, x, Floor[Sqrt[best + x^2]] - x}
    ],
    {x, 1, k}
  ];
  2 best
];
(* Example: Table[a401021[n], {n, 1, 64}] *)
