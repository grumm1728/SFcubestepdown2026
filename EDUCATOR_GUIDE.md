# Dandy Candies: choosing the rule

Start with seven unit-cube candies and ask students to build the rectangular box that uses the least packaging. After they propose a box, ask whether the box must be completely full. The choice changes the problem: an exact-fit box is 1 by 1 by 7 with area 30, while a 2 by 2 by 2 box has area 24 and one empty cell.

Use the [interactive comparison](index.html) to test ideas after students have made predictions. It displays optimal integer-sided boxes under both rules for 1 to 150 candies. The drawings are scaled independently; dimensions and surface areas carry the comparison.

## Questions to try

- What happens at 5, 6, 7, 8, and 9 candies? Why is 7 a turning point?
- At which values does allowing space help? Can students predict the next value before checking?
- If a box may hold more candies than we have, why does a larger capacity sometimes use *less* surface area?
- Can two different shapes have the same minimum area? What would count as a proof that no better shape exists?
- How does the problem change if you may join unit cubes into a shape that is not rectangular?

## Three distinct models

1. **Exact-fit rectangular box:** positive integer sides and volume exactly n. This gives [OEIS A075777](https://oeis.org/A075777).
2. **Rectangular box with empty cells:** positive integer sides and volume at least n. This gives [OEIS A401021](https://oeis.org/A401021), currently a submitted draft.
3. **Any polycube of exactly n cells:** the outside exposed faces are minimized. This gives [OEIS A193416](https://oeis.org/A193416).

The answer under model 2 never exceeds that of model 1, since every exact-fit box is allowed in model 2. At n=7 the two values are 24 and 30. Model 3 is a different comparison: at n=5 it gives 20, while model 2 gives 22.

## From play to justification

Students can list small integer boxes and compare their volumes and areas. A box with sides a,b,c has volume abc and surface area 2(ab+ac+bc). For a proposed minimum A, a proof must account for every box that could have area below A. The [research note](research/capacity/OEIS_SUBMISSION.md) gives finite bounds for an exact algorithm; the [generator](research/capacity_sequence.py) and its independently checked [table](research/capacity/b401021.txt) make larger examples inspectable.

The question of allowing gaps was raised publicly by Kevin Karplus in [Dan Meyer's 2014 Dandy Candies comments](https://blog.mrmeyer.com/2014/purposeful-practice-dandy-candies/) (comment 12), including this seven-candies example. Addison Stumpf and Jonah discussed the variant in [Meyer's 2015 comments](https://blog.mrmeyer.com/2015/the-math-problem-that-1000-math-teachers-couldnt-solve/) (comments 135–136). Meyer excluded gaps from the original version posed there.
