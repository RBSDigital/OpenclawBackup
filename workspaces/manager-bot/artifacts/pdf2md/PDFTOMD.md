# How To Read and Do Mathematical Proofs

Source: *How To Read and Do Mathematical Proofs* by James A. Foster, Laboratory for Uphill Computing, University of Idaho, September 26, 1996.

## Slide 1
How To Read and Do Mathematical Proofs

James A. Foster  
Laboratory for Uphill Computing  
Dept. of Computer Science  
University of Idaho  
September 26, 1996

Overview:
- High level strategy
- Indicators for specific strategies
- Specific strategies
- Some good books

## Slide 2
Notation

- `^` means and
- `_` means or
- `:` means not
- `8` means for all, or "every"
- `9` means there exists, or "some"
- `!` means if...then, or implies
- `$` means if and only if

## Slide 3
Your Task (High Level)

Show that conclusion `C` is a necessary consequence of premises `P` and what you know `K`.

1. Review definitions (Study)
2. How would you know `C` was true? (Ponder)
3. Is the theorem true? (Play)
4. Analyze `P` and `C` (Work)
5. Apply proof techniques (Work hard)
6. Re-write for legibility and clarity (Communicate)

## Slide 4
Specific Strategies

| Technique | Indicator |
|---|---|
| Forward-Backward | Any time |
| Construction | There is |
| Choose | For all, each, any |
| Induction | For all, each, any |
| Contrapositive | Not, no in `C` |
| Contradiction | Not, no, any time |
| Cases | Or |
| Compound | And, both |
| Inspiration | Anytime |

## Slide 5
Forward-Backward

Indicator: Any time

Strategy: Work simultaneously from premise and conclusion.

Theorem: `\binom{n}{r} = \binom{n}{n-r}`

## Slide 6
Forward-Backward Example

Theorem: `\binom{n}{r} = \binom{n}{n-r}`

Proof: By definition,

`(n r) = n! / (r!(n-r)!)`

But `r = n - (n-r)`. So

`n! / (r!(n-r)!) = n! / ((n-(n-r))!(n-r)!) = (n n-r)`

where the last step is by definition. So, `\binom{n}{r} = \binom{n}{n-r}`.

## Slide 7
Construction

Indicator: "There is"

Strategy: Build a witness and use it.

Theorem: The integers are denumerable.

## Slide 8
Construction Example

Theorem: The integers are denumerable.

Proof: We will produce an enumeration of the integers. Let

```text
E(x) = 2x - 1        if x > 0
E(x) = 2|x| + 2      otherwise
```

`E` clearly maps the integers to the natural numbers, since every integer is either greater than 0 or is not. `E` is 1:1, since `x != y` implies `E(x) != E(y)`. Finally, `E` is onto, since every natural number is either even or odd. Therefore, `E` is the desired enumeration of the integers, showing that the integers are denumerable.

## Slide 9
Choose

Indicator: "For all, each, any"

Strategy: Choose and use an arbitrary witness.

Theorem: The sum of any two odd integers is even.

## Slide 10
Choose Example

Theorem: The sum of any two odd integers is even.

Proof: Let `x` and `y` be two arbitrary odd integers. Then, by definition, `x = 2a + 1` and `y = 2b + 1` for two integers `a` and `b`. Now, let `c = a + b + 1`. Then

`x + y = 2a + 2b + 2 = 2c`

So, by definition, `x + y` is even.

## Slide 11
Induction

Indicator: "For all, each, any" in a countable domain

Strategy: Find a base case, show how to express a large instance in terms of smaller instance(s), and show that if it holds for the small instance then it holds for the next larger one.

Theorem: Prove that `sum(i=1 to n) i = n(n+1)/2`

## Slide 12
Induction Example

Theorem: Prove that `sum(i=1 to n) i = n(n+1)/2`

Proof:

For the base case, assume `n = 1`. Then

`sum(i=1 to 1) i = 1 = 1(1 + 1)/2`

So the base case holds.

Now, show that if the theorem holds for `n = k` then it holds for `n = k + 1`.

`sum(i=1 to k+1) i = sum(i=1 to k) i + (k + 1) = k(k + 1)/2 + (k + 1) = (k + 1)(k + 2)/2`

The first step is by definition of summation, the second by inductive assumption, and the third by algebraic manipulation. This completes the induction.

## Slide 13
Contrapositive

Indicator: "Not, no in C"

Strategy: Assume `not C`, prove `not P`.

Theorem: For real number `p, q`, if `pq != (p + q)/2` then `p != q`

## Slide 14
Contrapositive Example

Theorem: For real number `p, q`, if `pq != (p + q)/2` then `p != q`

Proof: Assume `p = q`. Then

`pq = pp = p = 2p/2 = (p + p)/2 = (p + q)/2`

So `pq = (p + q)/2`. Therefore, the theorem must hold by contrapositive.

## Slide 15
Contradiction

Indicator: "Not, no, any time" or desperation

Strategy: Assume `not C`, derive a contradiction using `P` and `K`.

Theorem: `sqrt(2)` is irrational.

## Slide 16
Contradiction Example

Theorem: `sqrt(2)` is irrational.

We will need the following lemma:

Lemma: If `x^2` is even, then so is `x`.

Proof: Let `x^2 = 2a`. Then `x^2 = x * x = 2a`. So 2 must divide one of the multiplicands in `x^2`. So `x` must be even.

## Slide 17
Contradiction Example (cont'd)

Proof of theorem: Suppose `sqrt(2)` is rational.

Then `sqrt(2) = p/q` for some integers `p` and `q` which have no common factors. Then `2 = p^2/q^2`, so `2q^2 = p^2`.

So, `p^2` is even, which by the lemma implies that `p` is even. In other words, `p = 2a` for some integer `a`. This implies that `2 = (2a)^2/q^2 = 4a^2/q^2`, which implies that `2q^2 = 4a^2` and that `q^2 = 2a^2`.

So, `q^2` is even, which by the lemma implies that `q` is even.

This means that both `q` and `p` are even, and so they have the common factor 2. This contradicts our assumption and proves the theorem.

## Slide 18
Cases

Indicator: "Or" or any time

Strategy: Divide and conquer.

Theorem: There are irrational `b` and `c` such that `b^c` is rational.

## Slide 19
Cases Example

Theorem: There are irrational `b` and `c` such that `b^c` is rational.

Proof: Consider the number `sqrt(2)^(sqrt(2))`.

Case 1: if `sqrt(2)^(sqrt(2))` is rational, then let `b = c = sqrt(2)`.

Case 2: Suppose `sqrt(2)^(sqrt(2))` is irrational. Then let `b = sqrt(2)^(sqrt(2))` and `c = sqrt(2)`. Now

`b^c = (sqrt(2)^(sqrt(2)))^(sqrt(2)) = sqrt(2)^(sqrt(2)*sqrt(2)) = sqrt(2)^2 = 2`

So that `b^c` is rational.

These are the only two cases, so the theorem is true.

## Slide 20
Compound proofs

Indicator: "And, both"

Strategy: Prove each part separately.

Theorem: There is exactly one even prime.

## Slide 21
Compound Example

Theorem: There is exactly one even prime.

Proof: 2 is an even prime, so there is at least one.

If `p` and `q` were both even primes, then both would have 2 as a divisor. But the only divisors of a prime are 1 and itself. So, both `p` and `q` must equal 2. So there are no other even primes than 2.

## Slide 22
Inspiration

Indicator: Any time

Strategy: Change the problem.

## Slide 23
Good Books

Some excellent books on doing proofs:

- Polya, G. *How to Solve It*, 2nd ed., Princeton, 1957.
- Solow, D. *How to Read and Do Proofs*, Wiley, 1990.
- Wickelgren, W. *How to Solve Problems*, Freeman, 1974.
- Polya, G. *Patterns of Plausible Inference*, 2nd ed., Princeton, 1968.
- Polya, G. *Induction and Analogy in Mathematics*, Princeton, 1973.
- Lakatos, I. *Proofs and Refutations*, Cambridge, 1976.

