# Prior work on integer box capacity and surface area

Research date: October 13, 2026.

## Question and conclusion

We study B(n) = min 2(xy+xz+yz) over positive integers x,y,z with xyz >= n. Unused capacity is allowed. This exact variant has public antecedents in math-education discussions from 2014 and 2015. We should credit those discussions and avoid claiming that the problem or its basic enumeration approach is new.

No scholarly source located in this search establishes a closed form for this capacity sequence. That is a search outcome, not proof that one is unknown. The previous OEIS prefix searches found no match; equivalent or transformed entries remain possible.

## Direct references

1. **gasstationwithoutpumps (Kevin Karplus), August 10, 2014, 11:46 am**, comment 12 on Dan Meyer's [Purposeful Practice & Dandy Candies](https://blog.mrmeyer.com/2014/purposeful-practice-dandy-candies/), posted August 5, 2014. Explicitly permits empty space, gives seven candies in a 2-by-2-by-2 box with area 24, and describes enumerating boxes and retaining capacity records as area increases. This is a direct computational precursor. His [About page](https://gasstationwithoutpumps.wordpress.com/about/) identifies the commenter as Kevin Karplus.

2. **Addison Stumpf and Jonah, September 26, 2015**, comments 135 (12:30 pm) and 136 (12:54 pm) on [The Math Problem That 1,000 Math Teachers Couldn't Solve](https://blog.mrmeyer.com/2015/the-math-problem-that-1000-math-teachers-couldnt-solve/). Stumpf asks about unused capacity and searching through the next cube; Jonah gives a list of volumes for which gaps do not improve area. Elsewhere in that thread, Meyer excludes empty spaces from his original question. Thus our sequence describes a discussed extension, rather than his original constraint.

These are primary records of public discussion, not peer-reviewed proofs. Use author, date, time, and comment number to locate passages; the web reader strips comment anchors.

## Related work, with different constraints

- **Jonathan Rotge and Gerald Tenenbaum**, [On integral boxes of minimal surface](https://tenenb.perso.math.cnrs.fr/PPP/on_integral_boxes.pdf), *Journal of Number Theory* 289 (2026), 85-95. The author-hosted paper explicitly imposes product of sides equal to n. It studies average optimal edge lengths in general fixed dimension. Relevant to A075777 and the wider number theory, but not a solution of B(n).

- **Shawn Alspaugh**, [Farmer Ted Goes 3D](https://www.jstor.org/stable/30044156), *Mathematics Magazine* 78(3) (2005), 192-204, DOI 10.2307/30044156. Bibliographic information and its almost-cube sequence are recorded in [A048874](https://oeis.org/A048874). Almost-cubes are records of n/A075777(n), a different optimization criterion. The [2000 conference abstract](https://www.rose-hulman.edu/class/ma/web/mathconf/2000/abstracts.htm) independently states the exact-volume and ratio setting (with a spelling discrepancy in the presenter's name). Full journal text was not accessible in this search; do not attribute more specific theorems to it without reading it.

- **Benjamin Dickman et al.**, [What arrangement of unit cubes minimizes surface area?](https://mathoverflow.net/questions/179371/what-arrangement-of-unit-cubes-minimizes-surface-area), MathOverflow, 2014. Separates arbitrary polycubes from rectangular prisms made of exactly n cubes and supplies references. A useful bibliography trail, not a direct treatment of our capacity sequence.

- [A075777](https://oeis.org/A075777) requires xyz=n. [A193416](https://oeis.org/A193416) minimizes exposed surface over polycubes of n cells, allowing nonrectangular shapes. Neither equals B(n). In particular, B(7)=24 whereas A075777(7)=30, and B(5)=22 whereas A193416(5)=20.

Further scholarly search details are in [SCHOLARLY_SEARCH.md](SCHOLARLY_SEARCH.md).

## Mathematical interpretation of the prior algorithm

Our notation for the inverse optimization is

M(s) = max{xyz : x,y,z positive integers, 2(xy+xz+yz) <= s},

with M(s)=0 if no box is feasible. Then B(n)=min{s : M(s)>=n}. This is our formal expression of the capacity-record approach, not a quotation or an asserted theorem from a paper.

For a finite list through n=N, enumeration can be bounded rigorously: put k=ceil(N^(1/3)). A k-cube holds every requested n, and AM-GM excludes any box of volume greater than k^3 from improving its area. Our independently checked finite enumeration implements this principle. The existing generator and 10,000-term table remain applicable.

## OEIS and educator implications

The submission can say that the empty-space variant was discussed in comments on Meyer's 2014 and 2015 posts. Link both and identify the commenters. Credit the sequence's definition and computational antecedents separately from preparation of the current program and table. An existing question can still warrant an OEIS entry.

For teaching, changing the permission to leave gaps gives an explicit modeling decision. Students can compare three rules: completely fill a rectangular box; fit the candies in a rectangular box with gaps permitted; or minimize exposed faces of any polycube. They can then test conjectures under one clearly stated rule.

## Search scope and limitations

Searches covered exact prefixes and half-area prefixes, integer boxes with volume at least n, empty-space packaging, maximum volume under a surface-area bound, the two Meyer comment threads, MathOverflow and CS Stack Exchange reference trails, OEIS cross-references, and accessible mathematical papers. Search engines often return continuous boxes, exact-volume factorization, arbitrary polycubes, or open boxes cut from a sheet. Those should not be silently treated as our problem.

This is a targeted review, not an exhaustive literature survey or a proof of novelty. No claim that the capacity problem is NP-hard, unsolved, or lacks a closed form follows from these sources.
