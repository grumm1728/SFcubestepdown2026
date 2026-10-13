// Small-number solvers for the interactive classroom view (n <= 150).
// The Python generator in research/ is the source for the full OEIS table.
function validate(n) {
  if (!Number.isSafeInteger(n) || n < 1) throw new RangeError("n must be a positive safe integer");
}
function chosen(next, current) {
  if (!current || next.surfaceArea < current.surfaceArea) return true;
  if (next.surfaceArea > current.surfaceArea) return false;
  if (next.capacity !== current.capacity) return next.capacity < current.capacity;
  for (let i = 0; i < 3; i++) {
    if (next.dims[i] !== current.dims[i]) return next.dims[i] < current.dims[i];
  }
  return false;
}
function result(a, b, c, n) {
  return { dims: [a, b, c], surfaceArea: 2 * (a*b + a*c + b*c),
    capacity: a*b*c, unused: a*b*c - n };
}
export function exactBox(n) {
  validate(n);
  let best;
  for (let a = 1; a*a*a <= n; a++) {
    if (n % a !== 0) continue;
    const rem = n/a;
    for (let b = a; b*b <= rem; b++) {
      if (rem % b !== 0) continue;
      const candidate = result(a, b, rem/b, n);
      if (chosen(candidate, best)) best = candidate;
    }
  }
  return best;
}
export function capacityBox(n) {
  validate(n);
  const k = Math.ceil(Math.cbrt(n));
  let best = result(k, k, k, n);
  for (let a = 1; a <= k; a++) {
    // If b <= c, half-area is at least b² + 2ab.
    const maxB = Math.floor(Math.sqrt(best.surfaceArea/2 + a*a)) - a;
    for (let b = a; b <= maxB; b++) {
      const c = Math.max(b, Math.ceil(n/(a*b)));
      const candidate = result(a, b, c, n);
      if (chosen(candidate, best)) best = candidate;
    }
  }
  return best;
}
