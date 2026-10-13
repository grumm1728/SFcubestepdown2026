# Scholarly and primary-source search for the capacity sequence

Research date: October 13, 2026. Target: B(n) = min 2(ab+ac+bc), over positive integers a,b,c with abc >= n. This note records a bounded web search, not an exhaustive literature review.

## Direct precursor: Kevin Karplus, 2014

The clearest direct predecessor found is the comment by **gasstationwithoutpumps**, August 10, 2014 at 11:46 am, comment 12 on Dan Meyer's *Purposeful Practice & Dandy Candies* (post dated August 5, 2014). It explicitly permits holes/dummy candies, observes that seven candies fit a 2 by 2 by 2 box of area 24, and proposes enumerating integer boxes, sorting by increasing area and decreasing volume, then removing boxes dominated by earlier ones. This constructs the area-capacity frontier needed for B(n). It is a public primary source for the same variant, although it does not present the sequence or a general closed formula.

- [Original post and comment](https://blog.mrmeyer.com/2014/purposeful-practice-dandy-candies/)
- [Author's own About page](https://gasstationwithoutpumps.wordpress.com/about/) identifies the blog's author as Kevin Karplus.

Citation suggestion: Kevin Karplus (gasstationwithoutpumps), comment on Dan Meyer, *Purposeful Practice & Dandy Candies*, August 10, 2014, 11:46 am. A comment-fragment permalink was not exposed by the web reader; the complete page, author, timestamp, and comment number identify the passage unambiguously. A direct HTML fetch was blocked by HTTP 403.

## Scholarly papers: relevant but different optimization problems

### Exact volume: Rotge and Tenenbaum (2026)

Jonathan Rotge and Gerald Tenenbaum, *On integral boxes of minimal surface*, arXiv:2602.02349, submitted February 2, 2026. The opening definition fixes integral-edge box volume **equal to n**, in any dimension k >= 2. Its subject is mean values of optimal edge lengths. Thus it treats the A075777 family, not the abc >= n variant. Useful as a labeled related-work reference; do not imply it solves the capacity sequence.

- [arXiv record and DOI](https://arxiv.org/abs/2602.02349)
- [Full HTML](https://arxiv.org/html/2602.02349v1)
- [Author-hosted PDF](https://tenenb.perso.math.cnrs.fr/PPP/on_integral_boxes.pdf)

### Exact-volume algorithm: Lin, Meng, and Li (2021)

Shu Lin, Na Meng, and Wenxin Li, *Generating Efficient Solvers from Constraint Models*, Proceedings of ESEC/FSE 2021, DOI 10.1145/3468264.3468566. Section 3 (PDF page 3), including Listing 3 and Algorithm 1, uses a minimum-area integer cuboid of prescribed exact volume as its running example. The displayed constraint is V = L*W*H. The paper studies automatic generation and pruning of solvers; it is not prior publication of B(n).

- [Author-hosted paper](https://people.cs.vt.edu/nm8247/publications/linshu-fse-2021-CR.pdf)
- [DOI](https://doi.org/10.1145/3468264.3468566)

### Attainable areas: Borwein and Choi (2000)

Jonathan Borwein and Kwok-Kwong Stephen Choi, *On the Representations of xy + yz + zx*, Experimental Mathematics 9(1) (2000), 153-158, DOI 10.1080/10586458.2000.10504642. This studies which positive integers occur as xy+yz+zx with positive integer variables. Theorem 1.1 bounds the nonrepresentable integers; Lemma 2.1 of the author-hosted manuscript characterizes representations via factoring N+k^2. The published year is 2000; do not substitute the publisher's 2012 online date or manuscript's regenerated date.

- [Publisher abstract and bibliographic record](https://www.tandfonline.com/doi/abs/10.1080/10586458.2000.10504642)
- [Author-hosted manuscript](https://www.sfu.ca/~schoia/paper/rep.pdf)
- [Author's publication list](https://www.sfu.ca/~schoia/paper.html)

Applicability (our interpretation): this concerns which **half-areas** an integer box can have, but does not maximize volume among boxes of a given half-area. Consequently it is mathematical background, not a formula for B(n). [OEIS A025052](https://oeis.org/A025052) lists nonrepresentable half-areas and links additional papers. Do not confuse representability with optimal capacity.

## Inverse formulation clarifies what a matching reference must solve

Define C(s) = max({0} union {abc: a,b,c positive integers, ab+ac+bc <= s}). Then B(n) = 2 min{s: C(s) >= n}. This equivalence follows directly from the two feasibility inequalities; it is our explanatory derivation, not a theorem attributed to a located paper.

A study of maximum product with **sum of sides fixed**, exact surface area only, box net cut from fixed paper, surface/volume ratio records, or arbitrary polycubes does not automatically determine C(s). Such variants need an explicit transformation before being called equivalent prior work.

[OEIS A193416](https://oeis.org/A193416) concerns arbitrary polycubes of exact volume n. It differs from B already at n=5 (20 rather than 22). [OEIS A075777](https://oeis.org/A075777) concerns exact-volume rectangular solids, and differs at n=7 (30 rather than 24).

## Search coverage and limits

Searches included the area and half-area prefixes, minimum area of integer/integral boxes and cuboids with volume at least n, integer-box isoperimetry, maximum volume under surface-area bounds, and the quadratic form ab+ac+bc. Primary paper contents were inspected where available. One page describing grid packing of spheres also uses spare grid spaces, but lacks an established date and research attribution, so it is not recommended as an OEIS reference.

No scholarly paper explicitly solving the complete capacity sequence was located in this pass. That is a search outcome, not evidence that no such paper exists. The 2014 Karplus comment is positive evidence that the problem and frontier method were discussed publicly long before this project. An OEIS submission can cite that direct precursor and distinguish its proposed sequence table from the older problem formulation.
