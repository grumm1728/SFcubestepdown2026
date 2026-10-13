# A075777 research notebook

Research date: October 8, 2026 (America/Los_Angeles).

## Status and question

For positive integer n, let
\[
A(n)=\min_{\substack{a,b,c\in\mathbb Z_{>0}\\abc=n}}2(ab+ac+bc).
\]
Dimensions are sorted when identifying boxes; permutations are the same box.

The sequence definition, Scott Farrar's 2015 correction, and the reference values come from [OEIS A075777](https://oeis.org/A075777). This notebook investigates a universal search-free formula and uniqueness of the minimizing sorted triple.

Jonathan Rotgé and Gérald Tenenbaum's [On integral boxes of minimal surface](https://tenenb.perso.math.cnrs.fr/PPP/on_integral_boxes.pdf), Journal of Number Theory 289 (2026), 85–95, studies the same optimization in arbitrary fixed dimension. Its introduction leaves uniqueness open and reports tests through volume \(10^8\) in dimensions 3–5. It proves estimates for average optimal edge lengths. The author-hosted PDF includes corrections; [arXiv:2602.02349](https://arxiv.org/abs/2602.02349) lists a February 2, 2026 submission.

A targeted literature search found no subsequent resolution. That is not an exhaustive claim about all literature.

**Status labels:** The elementary results below are proved in this notebook and independently reviewed by a separate research agent. Their historical novelty is unverified. Numerical observations appear in [FINDINGS.md](FINDINGS.md) and are not proofs of universal uniqueness.

## 1. Bounds and elementary exact cases

**Proposition.**
\[
6n^{2/3}\le A(n)\le4n+2.
\]

AM–GM applied to \(ab,ac,bc\) gives the lower bound because their product is \(n^2\). Equality requires \(a=b=c\), so it occurs exactly when n is a perfect cube.

The feasible box \((1,1,n)\) gives the upper bound. For a composite n, choose \(n=uv\) with \(u,v>1\). The box \((1,u,v)\) improves its half-area by
\[
(2n+1)-(n+u+v)=(u-1)(v-1)>0.
\]
Thus upper equality occurs exactly for primes and n=1.

In particular,
\[
A(k^3)=6k^2,\qquad A(p)=4p+2\quad(p\text{ prime}).
\]
The ratio \(A(n)/(6n^{2/3})\) is one on cubes and unbounded along primes. There is no uniform constant-factor comparison to \(n^{2/3}\) over all inputs.

**Prime-power formula and uniqueness.** For prime p and \(n=p^{3q+r}\), \(0\le r<3\),
\[
A(n)=2p^{2q}
\begin{cases}
3,&r=0,\\
1+2p,&r=1,\\
p^2+2p,&r=2.
\end{cases}
\]
The unique sorted dimensions have exponents differing by at most one.

To prove this, suppose two sides are x and y with prime-power exponents differing by at least two, so \(y\ge p^2x\). Moving one factor p gives \((px,y/p)\). Their product stays fixed and their sum changes by
\[
(px+y/p)-(x+y)=(p-1)(x-y/p)<0.
\]
With the third side fixed, the surface strictly decreases. Repeated improvement leaves precisely the balanced exponent multiset.

## 2. Exact divisor formula and solver

Define
\[
D(m)=\max\{d\in\mathbb Z_{>0}:d\mid m,\ d^2\le m\}.
\]
Then
\[
A(n)=2\min_{\substack{x\mid n\\x^3\le n}}
\left[\frac nx+x\left(D(n/x)+\frac{n/x}{D(n/x)}\right)\right].
\]

**Proof.** Fix a side x and write \(yz=m=n/x\). Half-area becomes \(m+x(y+z)\). Among factor pairs \(y\le z\), \(y+m/y\) decreases strictly as y approaches \(\sqrt m\). Thus the unique best remaining pair is \((D(m),m/D(m))\). Every sorted optimum has a smallest side satisfying \(x^3\le n\), so the displayed search includes it.

The formula may include a candidate whose x is not actually its smallest side; it is still a feasible box and cannot make the minimum too small. The implementation discards candidates with \(D(n/x)<x\): in that case there is no sorted factor triple with x as smallest side. Every minimizer is still retained.

This eliminates enumeration of all second sides for each first side. It does not remove factorization or the outer search and is not the desired search-free formula.

The public research function solve(n) returns a Result with integer surface_area and a tuple of **all** sorted minimizers. The reference solver independently enumerates integer side lengths without factoring. Python integers, integer square roots, and an exact binary cube-root routine avoid floating-point decisions.

Trial division is adequate for the recorded bounded experiments. This is not a claim of efficient computation for arbitrary huge input.

## 3. A dominant prime forces a unique optimum

**Proposition.** If \(n=mp\), p is prime, and \(p>m\), then
\[
(a,b,c)=\left(D(m),\frac m{D(m)},p\right)
\]
is the unique minimizing sorted triple, and
\[
A(mp)=2\left[m+p\left(D(m)+\frac m{D(m)}\right)\right].
\]

**Proof.** Since \(p>m\), p divides exactly one side. Write that side as pr and the other two as a,b, with \(abr=m\). If \(r>1\), choose a prime divisor q of r. We have
\[
a\le m<p\le pr/q.
\]
Replace \((a,pr)\) by \((qa,pr/q)\), preserving their product. Their sum decreases by the strictly negative quantity
\[
(q-1)(a-pr/q).
\]
With b fixed this strictly lowers surface area. Therefore r=1 at an optimum, so p stands alone. The remaining pair with product m has a unique closest factor pair, as in Section 2.

For example, if \(m=t^2\) and \(p>t^2\),
\[
A(t^2p)=2t^2+4tp,\qquad (a,b,c)=(t,t,p).
\]

## 4. No universal algebraic formula

**Theorem.** There is no nonzero polynomial \(F\in\mathbb R[X,Y]\) such that
\[
F(n,A(n))=0
\]
for every sufficiently large positive integer n.

**Proof.** Fix any positive integer t. Infinitely many primes satisfy \(p>t^2\), and Section 3 shows that the sequence points with \(n=t^2p\) lie on the line
\[
L_t:\quad Y=\frac4tX+2t^2.
\]
If F existed, the polynomial
\[
Q_t(X)=F\left(X,\frac4tX+2t^2\right)
\]
would have infinitely many roots \(X=t^2p\), hence would be identically zero. Dividing F as a polynomial in Y shows that
\[
Y-\frac4tX-2t^2
\]
divides F. Distinct positive integers t give infinitely many distinct linear factors. A nonzero polynomial of finite degree cannot have all these factors. Contradiction.

**Consequence for closed forms.** No fixed finite expression formed from n, fixed real constants, arithmetic operations, and roots of fixed integer degrees can give all A(n). Such expressions are algebraic over \(\mathbb R(n)\); clearing denominators would yield the forbidden polynomial relation. The underlying closure and tower properties are standard; see [Stacks Project, Lemmas 9.8.7–9.8.8](https://stacks.math.columbia.edu/tag/09GB).

Even a finite menu of algebraic formulas cannot suffice, regardless of the rule selecting between them: multiply the finitely many polynomial relations to obtain another forbidden relation.

**Limits.** This does not rule out formulas involving floor, ceiling, logarithms, exponentials, trigonometric functions, variable-degree roots, or variable-length operations. It does not prove computational hardness or a reduction to factorization. It says nothing by itself about algebraic generating functions or recurrences among different terms.

Our working search-free target permits fixed-length expressions using floor, logarithms and exponentials, so the complete target remains unresolved. The theorem rules out a substantial subclass. Novelty is unverified; no claim of a new published discovery is made.

## 5. How badly can the original heuristic fail?

Take an integer \(t\ge2\) and a prime \(p>t^4\), and put \(n=t^2p\).

Every divisor of n not containing p is at most \(t^2\). Every divisor containing p is larger than \(\sqrt[3]n\), whereas \(t^2<\sqrt[3]n\). Hence the historical heuristic selects \(t^2\) first and then the factor pair \((1,p)\). Its box is \((1,t^2,p)\).

Section 3 gives the unique true optimum \((t,t,p)\). The exact ratio is
\[
\frac{\text{heuristic area}}{A(n)}
=\frac{t^2+p+t^2p}{t^2+2tp}>\frac t2.
\]
Indeed, subtracting t/2 times the denominator from the numerator leaves \(p+t^2-t^3>0\). Letting t increase proves unbounded approximation error.

This is stronger than exhibiting isolated failures such as n=68 and n=246. It remains an elementary derivation with unverified novelty.

## 6. Constraints on hypothetical optimal ties

**No shared side.** Two distinct equal-volume, equal-area boxes cannot share any side length. If h is shared, the remaining pairs have the same product \(n/h\), and area equality forces the same sum. They are therefore roots of the same quadratic and are the same unordered pair.

**Prime transfer.** If a smaller edge x and larger edge y satisfy \(xq<y\), where q is the smallest prime factor of y, transferring q from y to x decreases their sum and hence the area with the third edge fixed. This is the three-dimensional instance of Lemma 2.1 in the [Rotgé–Tenenbaum paper](https://tenenb.perso.math.cnrs.fr/PPP/on_integral_boxes.pdf).

**Every pair must be balanced.** An optimal sorted triple satisfies
\[
D(ab)=a,\qquad D(ac)=a,\qquad D(bc)=b.
\]
Otherwise balance that pair while holding the third side fixed.

This condition is not sufficient: at n=360, \((5,8,9)\) is pairwise balanced but has area 314; \((6,6,10)\) has area 312. Thus a proof based solely on being a local optimum under two-edge changes fails.

**Composite largest side.** If the largest side c of an optimal sorted box is composite, then \(c\le a^2\). If instead \(c>a^2\), its smallest prime factor satisfies \(q\le\sqrt c\), so \(aq<c\), contradicting the prime-transfer condition.

**A useful bound for uniqueness searches.** If \(c>ab\), then \(c>a^2\), so c must be prime. Section 3 then proves uniqueness because \(c>ab\). Thus every hypothetical nonunique optimum has \(c\le ab\). If both smaller sides are at most B,
\[
n=abc\le(ab)^2\le B^4.
\]
This is an upper bound on the volumes of these bounded-side candidates, not exhaustive coverage of all volumes through \(B^4\).

In particular, the B=100 search cannot improve on the paper's reported \(10^8\) range for optimal uniqueness. Larger-volume ties in that search are necessarily nonoptimal. B=200 allows potential tied optima up to \(1.6\times10^9\), while still restricting both boxes' middle sides.

## 7. Algebraic generation of tied boxes

Write two sorted boxes as \((a,b,c)\), \((d,e,f)\). Let
\[
u=ab,\quad v=de,\quad s=a+b,\quad t=d+e.
\]
Equal volume and equal half-area give
\[
uc=vf,\qquad u+cs=v+ft.
\]
If u=v, these equations force identical boxes. Orient distinct boxes so u<v. Solving gives
\[
c=\frac{(v-u)v}{sv-tu},\qquad
f=\frac{(v-u)u}{sv-tu},\qquad
n=\frac{(v-u)uv}{sv-tu}.
\]

The generator enumerates \(1\le a\le b\le B\), \(1\le d\le e\le B\), then requires a positive denominator, integral c and f, sorted dimensions, and the chosen volume cap. It therefore finds every distinct tied pair within that exact region, once each.

An equivalent divisibility form is useful for future implementations: with \(g=\gcd(u,v)\), \(U=u/g\), \(V=v/g\), \(H=sV-tU\), require \(H>0\) and \(H\mid g(V-U)\); then \(k=g(V-U)/H\), \(c=kV\), \(f=kU\).

No arbitrary largest-side cutoff is used. The formula implies \(n<B^6\). At B=100 the configured volume cap \(10^{12}\) therefore excludes nothing; at B=200 it can exclude nonoptimal ties, but every possible optimal tie in the side region has volume at most \(B^4=1.6\times10^9\), well below the cap.

Do not divide out common scaling and assume optimality survives. For n=3 the optimum is \((1,1,3)\), but scaling it by 2 produces \((2,2,6)\) at volume 24, which loses to \((2,3,4)\).

## 8. Reproducibility and next questions

The [runner instructions](README.md), [findings](FINDINGS.md), JSON summaries, and CSV certificates record exact parameters, source hashes, and results. Each rejected pair has a valid box with strictly smaller area. Checking that witness needs only integer multiplication and addition; it does not require trusting the optimized solver or uniqueness.

The strongest next mathematical lead is the question: must every pair of distinct tied boxes contain a box improvable by balancing just two of its sides? A proof would imply uniqueness, but local balance alone does not imply global optimality, as n=360 demonstrates. The recorded finite searches only provide evidence for this stronger statement.

For the original closed-form target, any further effort must address operations beyond algebraic functions. The remaining question should not be treated as settled by the polynomial obstruction.
