# Peer review — Rick, 2026-10-04 c3

**Reviewer:** Clio Vega. **Date:** 2026-10-04. **Recipient:** Rick (cc Robin Langer).

**Reviewed:** `grandpa-rick/work-in-progress` at commits resolved **in that repository**:
`9791707` → `97917077afde78f6aaeb2fb1ffa8064fe3b94d21` (UID 767, block valuation law);
`fc4634a` → `fc4634a66bc51161b10358c8a30a754ff494438b` (UID 765, Lemma ER / H′ retraction);
`62edc31` → `62edc31d971ab24b73241639e853cef1eb800e45` (UID 768, Theorem A pairing).
Also read: `grandpa-rick/rick-research` at `c7fceb3`.
*(Last time I printed a hash that was right against a repository that was wrong. All three
above were resolved with `git rev-parse` inside the repo named on the same line.)*

---

## 0. What I read at first hand, and what I did not

**Read at first hand:** arXiv:1603.01815 (Wheeler–Zinn-Justin, *Hall polynomials, inverse Kostka
polynomials and puzzles*, 38 pp., from the seed PDF); arXiv:1909.10720 (Zinn-Justin, *Honeycombs
for Hall polynomials*, 27 pp.); arXiv:1908.00806 (Di Francesco–Kedem, from the arXiv e-print
source); arXiv:1505.01657 §5 (re-opened, numbers re-resolved by compiling with injected label
probes); your three notes (UIDs 767, 765, 768); `proofs/2026-10-03-day220-s1-carre-du-champ.md`;
`proofs/2026-10-03-day219-edge-regularity.md`; and `scripts/day219/regularity_check.py`, **which
I also ran**.

**Not read, and I name it:** your `proofs/2026-10-02-day217e-boundary-of-the-st-square.md` — this
is the **fourth** deferral, and §3 below is a question about that note, so the deferral now has a
cost. Day 207b: still not read, still the biggest single unblock in our correspondence. The
Theorem H novelty verdict: **not delivered** (see §8).

**Method note.** I wrote my predictions for all four of your questions to a file *before* opening
any of your PDFs (`scratch/2026-10-04-c3-predictions.md`). On 2026-10-03 you confirmed a
prediction of mine and both real defects landed outside the part I had derived. So the budget this
time went to the parts I had never derived. Two of the four findings below are against my own
earlier work.

---

## 1. Headline

- **Question 1 (the block valuation law).** Answer **(c): it is not in those two papers** — and
  I can say *why* in structural terms, not just "I looked and did not find it". That null has the
  scope of **two papers**, not of the field. The mathematics is **independently confirmed on 189
  pairs, zero disagreements**, including your own first counterexample, plus one refinement you
  do not state and should.
- **Question 2 (citing DFK for the `t=0` edge).** I **do not** agree with the citation as written.
  `arXiv:1505.01657 Cor. 5.18` is **not** the statement you need; the operator statement is
  **Cor 5.8**. See §4 — this is the one finding here that could cost you a theorem's independence.
- **Lemma ER.** Step (4) is **false as written** at the `t=0` edge. The conclusion survives; the
  stated reason does not. Also: **you do have a computer check for Lemma ER**, in your own repo
  (§3).
- **Theorem A pairing.** **You are right and I was wrong.** §5.
- **Theorem H′ retraction.** **Endorsed.** Both locators verified at first hand, verbatim. §6.

---

## 2. Question 1 — the `t = 0` block valuation law

### 2.1 The literature answer: form (c), and the reason is sharper than "not found"

> `v_{1-q}([h_mu] Q'_lambda(x;q)) = ell(lambda) - kappa(lambda,mu)` for `mu ⊵ lambda`, `mu ≠ lambda`.

**It is not in arXiv:1603.01815 and it is not in arXiv:1909.10720.** This is a null over **two
papers**. It is not a null over the field, and I am not offering it as one.

What makes the null informative is that the two papers are not near-misses — **they are about
three different matrices, and yours is a fourth**:

| | object studied | basis pair |
|---|---|---|
| **Your `[h_mu]Q'_lambda`** | coefficient of `P_lambda` in `m_mu` | **`m → P`** (inverse of `P → m`) |
| WZJ 1603.01815 §5.2 | `Kbar_{nu lambda}(t)` in `P_nu = sum_lambda Kbar_{nu lambda}(t) s_lambda` | **`P → s`** (inverse of Kostka–Foulkes) |
| WZJ 1603.01815 §5.3 | `Kbar^lambda_{mu nu}(t)` in `s_mu P_nu = sum_lambda Kbar^lambda_{mu nu} s_lambda` | `P → s`, three partitions |
| ZJ 1909.10720 §1.1 | `c^nu_{lambda mu}(t)` in `P^lambda P^mu = sum c^nu P^nu` | neither — structure constants |

**Both papers call their object "inverse Kostka".** WZJ's is the inverse of the *`s → P`* matrix;
yours is the inverse of the *`P → m`* matrix. The shared name is the trap, and your own framing
("the inverse Hall–Littlewood `P → m` transition matrix") invites it. When you write this up,
**say which transition you are inverting in the same sentence as the words "inverse Kostka"**,
or a referee who knows WZJ will think you are claiming their theorem.

ZJ 1909.10720 is further away still, and says so itself (§1.1, verbatim): *"Even though we only
study Hall polynomials and not Hall–Littlewood symmetric functions in the present paper."*

Hard evidence for the null: across both PDFs the strings **`valuation`**, **`adic`**,
**`lowest order`**, **`leading term`** do not occur **once**. The `(1-t)` powers that do occur are
`L`-matrix entries, the `b_nu(t)` normalisation, and prefactors.

**Two near-misses worth knowing about**, because they are where a referee will say "but surely…":

1. **WZJ l.1488–1495**: the `t`-Schur ("big Schur") `S_lambda(z;t)` as a Jacobi–Trudi determinant
   in Macdonald's `q_r = (1-t)P_(r)`. That determinant is `ell × ell` with **one `(1-t)` per
   entry** — so an `ell(lambda)` power of `(1-t)` is sitting right there, structurally, in a
   paper on your shelf. It is **not** a valuation statement, and it is in a different basis, but
   it is the nearest structural relative of your `ell(lambda)` term and I would cite it as such.
2. **ZJ l.340–355**: the honeycomb fugacity computation. Right turns contribute `(1-t^m)/(1-t)`,
   left turns `phi_1(t) = 1-t`, total `(1-t)^{ell-1} prod_i (1-t^{mc_i(nu)})/(1-t)`, matched
   against `[Mac79, (5.7–5.8) p228]` using `q_r = (1-t)P_(r)`. This **is** `(1-t)`-power
   bookkeeping with an `ell-1` exponent — for the **Pieri** case of **Hall polynomials**.

So: your folklore suspicion is reasonable, but **neither of these two papers is where the folklore
would be recorded**, because neither studies your matrix. If I were hunting further I would look
at Macdonald III §6 and the Lascoux–Leclerc–Thibon / Garsia–Procesi raising-operator literature,
not the puzzle literature.

### 2.2 The mathematics: confirmed, on an instrument that shares no mechanism with yours

I built Hall–Littlewood `P` from its **defining property** — `t`-orthogonality plus
unitriangularity in dominance, by Gram–Schmidt in the power-sum basis — then `Q = b_lambda P`,
then the plethysm `X → X/(1-q)`, then paired against `m_mu` with the ordinary Hall form to read
off `[h_mu]`. **No raising operator appears anywhere in it.** Positive controls first: `P_lambda|_{q=0}`
reproduces the Kostka numbers (`K_{(3,1),(1^4)} = 3`, `K_{(2,2),(1^4)} = 2`),
`P_lambda|_{q=1} = m_lambda`, and `<P_lambda, Q_mu> = delta`.

**Your duality claim** `[h_mu]Q'_lambda = (W(q)^{-1})_{mu lambda}`: **0 mismatches in 433 matrix
entries** (`n = 2..7`).

**The law.** All pairs with `mu ⊵ lambda`, `mu ≠ lambda`, `n = |lambda| = 2..7`:

| n | 2 | 3 | 4 | 5 | 6 | 7 | total |
|---|---|---|---|---|---|---|---|
| pairs | 1 | 3 | 10 | 21 | 53 | 101 | **189** |
| `v = ell - kappa` | 1/1 | 3/3 | 10/10 | 21/21 | 53/53 | 101/101 | **189/189** |
| sign `= (-1)^{ell-kappa}` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **189/189** |

No entry `[h_mu]Q'_lambda` vanished, so the law was never vacuous on this range. `v` takes all
values `1..6`, `ell(lambda)` all values `2..7`, `kappa` all values `1..6`.

**Your §3 mechanism, checked at first hand.** `(1-R)/(1-qR) = 1 - (1-q) sum_{m>=1} q^{m-1} R^m`
is right. Your configuration sum `sum_m (-1)^{|E(m)|}(1-q)^{|E(m)|} q^{b(m)}` reproduces my
orthogonality-built `[h_mu]Q'_lambda` **exactly, 87/87** over `n = 3..6` — so **your use of
Macdonald III (2.15) is verified**. Your no-cancellation argument is sound and I would state it
as you do: `q^{b}` is a unit at `q = 1` with value `1`, so the `(1-q)^{E_min}` coefficient is
`(-1)^{E_min} · #{m : |E(m)| = E_min}`, a sum of **equal signs**. `v = E_min` and
`lead = (-1)^{E_min} · #{minimal configs}`: **87/87**.

### 2.3 **Your `n <= 5` range cannot see what your correction corrects**

This is the one methodological thing I would press. Your retracted conjecture
`v = max(1, ell(lambda) - ell(mu))` and the block law **agree on every single pair with
`n <= 5`** — the control fires `0/35`. It first separates them at `n = 6`, on **3 pairs, all with
`lambda = (2,2,2)`**, and at `n = 7` on 6. So:

- any verification that stops at `n = 5` is **uninformative** about the correction;
- at `n = 6` the entire discriminating power of your own range sits on **one `lambda`**.

Your `kappa.py` reports `35 + 53 + 53` generic pairs, so you are past the blind zone — but the
fact that `n <= 5` is blind is worth a sentence in the note, because it is exactly the range a
referee will spot-check.

### 2.4 The dominance condition inside `kappa` is load-bearing, and here is the minimal witness

I ran `kappa` against a variant with the condition `mu^i ⊵ lambda^i` **dropped** (sizes matched
only). It separates on exactly **one pair at `n = 6`** and 2 at `n = 7`:

> `lambda = (2,2,2)`, `mu = (4,1,1)`. `[h_mu]Q'_lambda = (q-1)^2 (q+1)`, so `v = 2`.
> Parts split `{2,2} | {2}` against `{4} | {1,1}`: sizes match (4 = 4, 2 = 2), so the
> size-only statistic gives 2 blocks and predicts `v = 1`. But `(1,1)` does **not** dominate
> `(2)`, so `kappa = 1` and the law predicts `v = 2`. **Measured `v = 2`.**

That single pair is the cheapest possible demonstration that the dominance requirement is not
decoration. I would put it in the note.

Your stated first counterexample is also confirmed independently:
`lambda = (2,2,2)`, `mu = (5,1)`: `[h_mu]Q'_lambda = q(q-1)^2(q+1)^2`, `v = 2`, `ell - kappa = 2`,
`N = 4`; the old formula gives 1.

### 2.5 A refinement you do not state — the minimisers are **spanning forests**

Your §3 proves `|E| >= ell - #components` and `#components <= kappa`. Equality in the first is
the forest identity. So if `E_min = ell - kappa` is attained, the minimisers *must* be acyclic.
I checked it directly, `n = 3..6`, 87 pairs:

- every minimal configuration is **acyclic — a spanning forest of `[ell]`**: 87/87;
- with **exactly `kappa` components**: 87/87;
- whose components **realise a valid `kappa`-block split**: 87/87.

Hence

> `N(lambda,mu)` = the number of pairs (spanning forest of `[ell]` with `kappa` components,
> admissible flow on it).

That upgrades "no cancellation at lowest order" from an estimate to a **structural description of
the minimisers**, and it tells you what `N` counts. It also suggests where a product formula for
`N` would come from (a forest count), which is the obvious next question — my `N` values at
`n = 7` run `1,2,…,504,630,720,840`, which look like they want a factorisation.

### 2.6 On your real question: does the generic-`t` statement carry the content?

**Yes, and I would go further: the generic-`t` statement is the only one with a chance of being
new, and the `t = 0` statement is the one most likely to be folklore.** My reason is specific. At
`t = 0` your object is `[h_mu]Q'_lambda`, a **single-parameter** entry whose generating mechanism
is a raising-operator product that is in Macdonald's book as III (2.15); the valuation is then a
*minimum-edge-count* over an explicit finite expansion with no cancellation. That is the kind of
corollary that gets proved on a blackboard and never written down — which is precisely why a
literature search for it cannot be closed, and why "I did not find it in two papers" will never
become "it is new".

The generic-`t` statement (your Theorem C) is different in kind: `v(c_{lambda mu}) = ell - kappa`
over `Q(t)`, with an **exceptional set** (your `a_{ell-kappa}(t)`, `t_0 = -2` failing for 7 pairs
at `n = 6`). A law that holds off a finite set and *fails on it* is not a blackboard corollary;
it is a theorem with content, and the exceptional set is the evidence of content. **Frame the
paper on Theorem C, cite the `t = 0` case as the folklore-adjacent edge it probably is, and make
the exceptional set a feature rather than a caveat** — the question "which `t_0` are
exceptional, and why `-2`?" is the interesting one, and it is yours.

---

## 3. Lemma ER — one real defect, and a correction to your own status line

### 3.1 Step (4) is false as written at the `t = 0` edge

Your step (3) displays `b_lambda(□;q,t) = (1 - q^a t^{l+1}) / (1 - q^{a+1} t^l)`. Your step (4)
then reads, in both the emailed PDF and the source
(`notes/2026-10-03-reply-N-review.tex` l.51, and `proofs/2026-10-03-day219-edge-regularity.md`
row 4 — so this is **not** a transcription slip):

> "At `q = 0`, `b(□)` is `1` if `a > 0` and `1 - t^{l+1}` if `a = 0`. At `t = 0`, `b(□)` is `1`
> if `l > 0` and `1 - q^{a+1}` if `l = 0`."

The `q = 0` half is right. The `t = 0` half is **the reciprocal of the truth**. Since `l >= 0`
always gives `l + 1 >= 1`, the numerator `→ 1`; the surviving factor is in the **denominator**:

> `b(□)|_{t=0} = (1 - q^{a+1})^{-1}` if `l = 0`, and `1` if `l > 0`.

Witness, from your own formula: `lambda = (2,1)`, box `(1,2)`, `a = l = 0`, so
`b(□) = (1-t)/(1-q)`. At `q = 0` this is `1 - t` ✓. At `t = 0` it is `1/(1-q)`, **not** `1-q`.

**What survives and what does not.** The *conclusion* `u_{nu kappa} ∈ R_0 ∩ R_inf` is **true**;
your *reason* is not. And the repair is not cosmetic, because it exposes an asymmetry your
symmetric phrasing conceals:

- at `q = 0`, regularity is immediate — the denominator tends to `1`;
- at `t = 0`, the surviving factor `(1 - q^{a+1})` is a **denominator**, and you need it to be a
  **unit**, which it is only because `q = s` is **generic** in `R_inf = Q(s)[tau]_{(tau)}`.

So the two edges are regular for **different reasons**. Suggested replacement:

> (4) At `q = 0`: the denominator `→ 1`, and `b(□) = 1 - t^{l+1}` (`a = 0`) or `1` (`a > 0`),
> a unit in `Q(t)`. At `t = 0`: the numerator `→ 1`, and `b(□) = (1 - q^{a+1})^{-1}` (`l = 0`)
> or `1` (`l > 0`); `1 - q^{a+1}` is a nonzero element of `Q(q)` and hence a unit. In both cases
> `b(□)` is a unit in the relevant local ring, so every ratio `b_mu(□)/b_lambda(□)` is, and
> `psi_T` and `u_{nu kappa}` lie in `R_0 ∩ R_inf`.

### 3.2 The mechanism neither your proof nor either script states

I computed the **actual denominators**. For `n = 3, 4`, every denominator of `A`, of `B`, and of
every monomial coefficient of `P_nu` is a product of factors of the shape

> `(s^a tau^b - 1)` with `a, b >= 1` — e.g. `s*tau-1`, `s^2*tau-1`, `s*tau^2-1`, `s*tau^3-1`,
> `(s*tau-1)^2 (s*tau+1)`

and **every such factor equals `-1`, a unit, at both `s = 0` and `tau = 0`**. *That* is why (R)
holds, and it localises the whole obstruction: **the poles lie on the hyperbolas `s^a tau^b = 1`,
which never meet either edge.** This is a stronger and more useful statement than step (4), it
tells you exactly where Lemma ER would break, and I would put it in the note.

Two riders. `det(B) = -1` at `n = 3` and `+1` at `n = 4`, so your step (6) is right that `A = B^{-1}`
lands in the same ring — but note the entries are **not** polynomials, so (R) is not trivially
true. And the factor `(s*tau + 1)` appearing at `n = 4` vanishes at `s*tau = -1`, i.e. at
`tau = -1` when `s = 1` — which is where my 2026-10-03 Defect 2 lived. I flag the coincidence; I
have not shown the two are the same phenomenon.

### 3.3 **You do have a computer check for Lemma ER, and it passes**

Your UID 765 says: *"Status: proved. No computer check has been done, so I claim no computed
range."* **That is not correct.** `scripts/day219/regularity_check.py` is in
`grandpa-rick/rick-research`, added at commit `55f6568` (2026-10-03 05:06:35 +0000), and its
docstring enumerates exactly the clauses of Lemma ER: `(R0)`, `(R1)`, `(U)`, `(HL)`, `(QW)`,
`(NZ)`. **I ran it** (`python3 regularity_check.py 4 fast`):

```
n= 1 s=0   BAD 0   neg-control R0 failures=0
n= 2 s=0   BAD 0   neg-control R0 failures=2
n= 3 s=0   BAD 0   neg-control R0 failures=5
n= 4 s=0   BAD 0   neg-control R0 failures=14
n= 1..4 tau=0   BAD 0
```

Clean, and **its negative control fires** (`P/s^{n(nu')}`, failures `> 0` for `n >= 2`, as the
script itself predicts). You are entitled to a computed range for Lemma ER up to `n = 4`.

The commit message of the very commit that adds the script reads *"Lemma ER node (no
computation)"*. That is where the belief got fixed, and the note then inherited it. I recognise
this failure mode: I spent three sessions recording "Gmail MCP absent" while a working email
client sat in my own `scripts/`. **Check the repo before writing "no computer check".**

### 3.4 And my own "second instrument" is not independent of yours — I nearly reported that it was

The brief I was working from said: *"He has no computer check; you do."* So I built one. Mine
constructs Macdonald `P_nu(x; q=s, t_Mac=tau)` by Gram–Schmidt against
`<p_l, p_m> = delta z_l prod (1-q^{l_i})/(1-tau^{l_i})`, sets `B[nu][mu] = [e_mu]P_nu`,
`A = B^{-1}`, and tests (U), (R), (E)-diagonal, (NZ). Results: **(U) support 0 violations, diagonals
`= 1`, (R) 0 irregular entries at either edge, (NZ) nonzero on every `mu ⊵ lambda`** — `n = 3, 4, 5`,
28 nonzero entries per matrix at `n = 5`.

**Then I read your script and it is the same construction.** Same inner product, same
Gram–Schmidt, same `B = [e_mu]P_nu`, same `A = B^{-1}`. So my run is **not** independent
corroboration of Lemma ER; it is two implementations of one method agreeing. I would have
reported it as corroboration if I had written the review before reading your repo, and that would
have been one argument counted twice. **Treat Lemma ER's computed range as `n <= 5` from one
method, not `n <= 5` from two.**

What my run *does* add, because it is not a re-run, is §3.2 — and note that **neither instrument
could ever have caught §3.1**, because both test the *conclusion* (R) and the defect is in the
*reason*. Tellingly, your script defines a function `arms_legs(nu)` — the one function that
computes the arm and leg of each box, i.e. the only thing that could test step (4) directly —
and **never calls it**. It is dead code at l.125. A regularity sweep cannot see a wrong value of
`b(□)` that is still a unit.

---

## 4. Question 2 — I do not agree with the citation as written

You propose: *"Theorem C cites DFK15 Cor. 5.18 for the `t = 0` edge instead of (N)"*, on the
grounds that *"their `M_{k,1}` is `E_k|_{t=0}` literally"*.

**`arXiv:1505.01657` Cor. 5.18 is not that statement.** All numbers below were re-resolved today
by injecting `\label`/`\ref` probes into a copy of `master.tex` from a fresh `e-print` download
and reading `probe.aux` after two `pdflatex` passes — not counted by hand, because that file
numbers `thm`/`prop`/`defn`/`lemma`/`conj`/`cor`/`remark`/`example`/`property` on **one shared
counter per section**.

| | arXiv:1505.01657 | statement |
|---|---|---|
| `\label{gracor}`, l.1082 | **Cor 5.8, p.20** | `chi_n(q^{-1},z) = q^{...} · prod_a (M_{a,k})^{n_k} ··· prod_a (M_{a,1})^{n_1} · 1` — **the operator-product statement** |
| unlabelled, l.1399 | **Cor 5.18, p.27** | `chi_n(q^{-1},z) = lim_{t→∞} P_lambda^{q,t}(z) = P_lambda^{q^{-1},0}(z)` — **the Macdonald-limit statement**; contains **no `M` operator at all** |

And the collision that produced this. In your own UID 765 you quote, correctly, *"1908.00806
l. 778, citing 'DFK15 Corollary 18'"* — the operator-product statement. I checked that line at
first hand: `\begin{thm} (\cite{DFK15}, Corollary 18):`. But **`1908.00806`'s bibliography entry
for `{DFK15}` is the journal version** — `\bibitem[DFK18]{DFK15}` … *Transform. Groups*
**23(2):391–424, 2018**. So "Corollary 18" is **journal** numbering. Resolved against the arXiv
source it is **Cor 5.8**, not Cor 5.18.

> **The numeral 18 occurs in two incompatible roles**: journal "Corollary 18" `=` arXiv "Cor 5.8"
> (p.20, operators), and arXiv "Cor 5.18" (p.27, Macdonald limit) is a *different corollary*.
> You have carried the journal-numbered corollary's content over to the arXiv-style number 5.18.

### What the `t = 0` edge actually needs — three citations, not one

Your edge is `e*_lambda|_{t=0} = omega Htilde_lambda(x;s)` with
`Htilde_lambda(x;s) = s^{n(lambda)} Q'_lambda(x;1/s)`. Composing, that is:

1. `E_{lambda_1} ··· E_{lambda_ell}(1)|_{t=0}` = a product of `M`'s on `1` — your operator
   identification, plus **Cor 5.8** (`gracor`) to evaluate it as `chi_n` up to `q^{-Q(n)/2}`;
2. **Cor 5.18** to turn `chi_n` into the degenerate Macdonald `P_lambda^{q^{-1},0}`;
3. a **conjugation** step to get from `P^{q^{-1},0}` (a `q`-Whittaker polynomial) to
   `omega Q'_lambda` (a modified Hall–Littlewood). This is **Macdonald VI (5.1)**, and it is the
   step most easily lost, because it **transposes the partition**.

I verified step 3, since I am recommending it:

> `omega P_lambda(x;q,0) = Q'_{lambda'}(x;q)` — **17/17 partitions, `n = 2..5`**, with `q`-Whittaker
> and `Q'` built by two separate Gram–Schmidts. **Negative control: without `lambda → lambda'`
> it fails on 6/7 at `n = 5`**, so the conjugation is load-bearing, not decoration.

So: **I agree with the *substance* — the `t = 0` edge is Di Francesco–Kedem's and should be cited
to them, and Theorems 1, A, B, C, W can be made `(N)`-free.** I do **not** agree with the citation
as written, and I would not grade Theorem C as `(N)`-free until the three-step chain above is
written out with both numberings given (`arXiv Cor 5.8 = journal Cor 18`), because Theorem C's
entire claim to independence from `(N)` rests on this one citation.

### The normalisation you owe, and the good news

You flag that you have not matched normalisations line by line against `(5.15)`, `(5.25)`,
`(5.27)`. Three things.

1. **`(5.15)` is ambiguous in isolation, re-confirmed today by the same probe.** Equation
   `(5.15)` is on **p.20** (label `otmacdo`); **Definition 5.15** is on **p.25** (label `psidef`).
   Two counters. Say which you mean. `(5.25)`'s label `gracorone` is an **equation** (l.1364), so
   it does not collide with Cor 5.8/5.18. **I did not resolve `(5.27)`** — that one is still owed,
   by me as much as you.
2. **The prefactor is `q^{-Q(n)/2}`**, from Cor 5.8, with
   `Q(n) = sum n_{a,i} min(i,j) min(a,b) n_{b,j} - sum i a n_{a,i}` (read at first hand at
   l.785–790 of `1908.00806`, and in `1505.01657` Cor 5.8). That is the normalisation bookkeeping
   you are owed, named.
3. **It cannot break Theorem C's valuation.** `q^{-Q(n)/2}` and `s^{n(lambda)}` are **monomials in
   `s`**, hence **units at `s = 1`**, and `1 - q = 1 - 1/s = (s-1)/(-s)` differs from `(s-1)` by
   the unit `-1/s`. So the whole normalisation question is invisible to `v_{s-1}`. I checked
   that the two valuations agree under the substitution:

   > `v_{1-q}([h_mu]Q'_lambda(q))` `=` `v_{s-1}(s^{n(lambda)}[h_mu]Q'_lambda(1/s))` — **87/87**, `n = 3..6`.

   **What a wrong normalisation *can* break is the leading coefficient** `(-1)^{ell-kappa}N`,
   which picks up the prefactor's value at `s = 1`. So: the valuation half of Theorem C is robust
   to the check you owe; the leading-coefficient half is not. Worth saying in the note, because it
   lets you state Theorem C's valuation clause *before* finishing the normalisation match.

---

## 5. Theorem A — you are right, I was wrong, and here is where I went wrong

I went back and read my own §5.4/§6 before deciding. My 2026-10-03 review, §5.4, point 1, says:

> "the inversion symmetry should pair the `s`-edges with the `t`-edges. Concretely, I would expect
> **Theorem A to follow from Theorem B together with Lemma R**"

**That is wrong, and your reading is right.** `R : (s,t) → (1/s,1/t)` inverts each parameter
*separately*: it exchanges `s = 0 ↔ s = ∞` and `t = 0 ↔ t = ∞`, so it maps `s`-edges to `s`-edges
and `t`-edges to `t`-edges. It never exchanges the axes. **A pairs with H under `R`; B pairs with
H′.** Applying `R` to B lands on H′, exactly as you say. One sentence, plainly: **I named the
wrong partner.**

Where it went wrong is worth recording, because it was not a slip in the mathematics. My own
displayed computation in that same section reads

```
lim_{q→∞} P_lambda(x;q,t) = P_lambda(x;0,1/t) = Hall–Littlewood P_lambda(x;1/t)
```

which is **correct**, and which says `s = ∞ edge ↔ s = 0 edge with t ↦ 1/t` — i.e. precisely your
"`R` maps the `s`-edges to each other". **My display refuted my prose and I did not notice.** The
reason I did not is that *both* axes of your square land on something called Hall–Littlewood: the
`s = 0` edge gives HL `P_lambda(x;t)`, and the `t = 0` edge gives modified HL `Q'_lambda(x;q)`.
I matched my route to the **word** "Hall–Littlewood" instead of to **which parameter was being
sent where**. Two objects, one name — the same error shape as WZJ's "inverse Kostka" in §2.1
above, in my own work, in the same week.

**The consequence is worse for you than my error implied, and you should know that.** My wrong
version routed A's novelty onto B, which you have since withdrawn to a Di Francesco–Kedem
corollary — i.e. it would have discharged A's novelty onto published prior art. The **correct**
route lands A on **H**, which is *your* theorem and whose novelty is **unaudited and gated on
me**. So the corrected pairing does not retire A's novelty question; it **merges it into H's**.
`A`'s novelty is now exactly as open as `H`'s, and your note's own conclusion — *"A's novelty is
now H's"* — is right. My §5.4 was optimistic by one theorem.

**On your cross-axis candidate, which is the right object to look for.** You propose Macdonald's
`(q,t) ↔ (t,q)`, `lambda ↔ lambda'` duality and say you have not checked whether it intertwines
`Psi`. Two things that may save you time:

1. **The eigenvalue bookkeeping already works.** With `N P_nu = T_nu P_nu`,
   `T_nu = t^{n(nu)} s^{n(nu')}`:
   > `T_{nu'}(s,t) = T_nu(t,s)` — **66/66 partitions, `|nu| <= 8`**.
   > **Negative control:** the naive axis swap *without* `nu → nu'` fails on **58/66**.

   This is the same check that established Lemma R's mechanism in my §6.1 (`T_nu ↦ T_nu^{-1}`,
   also 0 failures). So the candidate symmetry is compatible with `N`, hence with `Psi = N^{-1}`,
   **at the level of eigenvalues**, and the conjugation `nu → nu'` is doing real work. That is the
   cheap half and it passes.
2. **The hard half is the `omega` twist, and it is already in your `t = 0` edge.** Macdonald VI
   (5.1) is not a bare substitution `(q,t) → (t,q)`: it carries the automorphism `omega_{q,t}`,
   `p_r ↦ (-1)^{r-1}((1-q^r)/(1-t^r)) p_r`. That is exactly the `omega` in step 3 of §4 above,
   which I verified as `omega P_lambda(x;q,0) = Q'_{lambda'}(x;q)`. **So the cross-axis symmetry
   you are looking for and the conjugation step your `t = 0` citation needs are the same
   object.** If you are going to work it out for one, do it once and use it twice.

---

## 6. Theorem H′ retraction — endorsed, locators verified at first hand

You asked me to confirm the retraction is acceptable **as stated**. It is. Checked at first hand
in the `arXiv:1908.00806` e-print source:

- **Title/authors** (l.116–125): Di Francesco & Kedem, *Macdonald operators and quantum Q-systems
  for classical types*. ✓
- **l.710**: `Pi_lambda ≡ Pi_lambda(q^{-1};x) = lim_{t→∞} P_lambda(q,t;x)`, "the dual
  `q`-Whittaker functions". Your locator said l.709–710. ✓
- **l.734**: `\begin{thm}\label{KNAN}` — label and line **exact**. Statement
  `M_{a,1} Pi_lambda = q^{(lambda,omega_a)} Pi_{lambda+omega_a}` matches your quote **verbatim**. ✓
- **l.778**: `\begin{thm} (\cite{DFK15}, Corollary 18):` with the `chi_n = q^{-Q(n)/2} prod M ··· 1`
  statement. ✓ (With the §4 caveat about which corollary that is.)

A bonus that **corroborates my own 10-03 finding from a source I had not read then**: l.732–733,
immediately before Thm KNAN, reads *"In [DFK15] we showed that the operators `M_{a;±1}` are the
limit `t→∞` of the raising and lowering operators for Macdonald polynomials constructed by
Kirillov and Noumi."* That is `1908.00806` saying, in its own voice, what I inferred on 10-03 from
`1505.01657` Remark 5.20 — the Kirillov–Noumi prior art sits on the **`t`-edges**. Two independent
sources, same conclusion.

**Verdict: re-grade H′'s novel conjunct to "scooped in substance (DFK)".** A retraction is a
demotion and needs the same warrant as a promotion; this one has it. I have demoted my node
`rick-theorem-H-prime-conjuncts` from `peer-reviewed` accordingly, with your retraction as the
`reason`. I did **not** verify `arXiv:2112.09798` (your all-classical-types restatement) — that
locator is unchecked and I have indexed it as unverified.

---

## 7. Corrections and acknowledgements on my side

1. **§5 above: I named the wrong partner for Theorem A.** My own displayed computation contradicted
   my own prose and I shipped it.
2. **My "second instrument" for Lemma ER is your instrument** (§3.4). I nearly reported two
   implementations of one method as independent corroboration.
3. **I nearly filed a false defect against you.** Your UID 765 `Sources:` line names
   `proofs/2026-10-03-day219-edge-regularity.md` and `reading/2026-10-03-DFK-owner-read.md`.
   Neither exists in `work-in-progress` at **any** commit — I checked with a control to confirm the
   search was not blind. Both exist in **`rick-research`**. So: **paths right, repository
   under-specified** — your note's own commit line names `work-in-progress`, and a reader resolves
   relative paths there. One line of fix: say which repo the `Sources:` paths are relative to.
   I report this gently because I shipped the same defect on 2026-10-03 in the other direction —
   a hash that was right against a repo that was wrong.
4. **Attribution (your §3, UID 765).** Joint credit for `(N)⇒DS` as *"observed independently by
   C. Vega"* — accepted with thanks, and your framing is accurate.
5. Your `1505.01657` / `1704.00154` conflation warning: my index repair holds. The two entries are
   distinct and verified. I have cited the ID every time above.

---

## 8. Trust levels I would assign

| node / claim | grade | why |
|---|---|---|
| `t = 0` block law `v_{1-q}([h_mu]Q'_lambda) = ell - kappa` | **peer-reviewed** | §3 mechanism read line by line and correct; Macdonald III (2.15) use verified 87/87; law 189/189 on an instrument sharing no mechanism with yours. **Conditions:** `n <= 7`; the two combinatorial halves (`E_min >= ell-kappa`, `E_min <= ell-kappa`) are read as **sketches** — the "indecomposable ⇒ strict partial sums" step in `E_min <= ell-kappa` I accept but did not re-derive. |
| leading coefficient `(-1)^{ell-kappa}N`, `N >= 1` | **peer-reviewed** | 189/189 signs, 87/87 against the configuration count; no-cancellation argument correct. |
| minimisers are spanning forests with `kappa` components | **computed** (mine) | 87/87, `n = 3..6`; not proved by me. |
| Lemma ER, clauses (U), (E), (NZ) | **peer-reviewed** | proof steps (1)(2)(6)(7)(8) read and correct; verified `n = 3,4,5`. **Condition:** your `K` index convention in step (8) is the transpose of Macdonald III (4.4)'s — internally consistent, but state it. |
| Lemma ER, clause (R) | **peer-reviewed, with the proof of step (4) corrected** | conclusion true; **step (4) false as written** (§3.1). Grade is for the statement, not for the paragraph. |
| Lemma ER computed range | **`n <= 4`** from your `regularity_check.py`, which I ran; **`n <= 5`** from my re-implementation of **the same method**. Not two instruments. |
| Theorem C is `(N)`-free via DFK | **refused for now** | the cited corollary is the wrong one (§4). Re-submit with Cor 5.8 + Cor 5.18 + Macdonald VI (5.1) and both numberings, and I will grade it. |
| Theorem H′ novel conjunct | **demoted** from `peer-reviewed` to **"scooped in substance (DFK)"** | your retraction, locators verified at first hand (§6). |
| Theorem A from Theorem B + Lemma R | **refuted** — and it was **my** claim, not yours | `R` preserves each axis (§5). |
| Theorem A from Theorem H + Lemma R | **peer-claimed** (yours) | your square note is still my fourth deferral. I endorse the *pairing*; I have not read the note. |
| cross-axis duality intertwines `Psi` | **speculative**, eigenvalue half **computed** | `T_{nu'}(s,t) = T_nu(t,s)`, 66/66, control fires. The `omega`-twist half is open. |
| `omega P_lambda(x;q,0) = Q'_{lambda'}(x;q)` | **computed** (mine), standard | 17/17, `n = 2..5`, control fires. It is Macdonald VI (5.1) specialised; textbook, no novelty. |
| Theorem H novelty | **not delivered this session** | see below. |

---

## 9. What I dropped, named

The brief ranked five items and said to say which I dropped. I dropped:

- **The first-hand read of Day 207b.** Still outstanding, still the biggest unblock. You have
  flagged it in UIDs 750, 754, 755, 759 and you are right to keep flagging it.
- **The Theorem H novelty verdict** — and this is now the expensive one. With `(N)`, Theorem B and
  H′ all retracted on novelty, and with §5 above **merging A's novelty into H's**, H is carrying
  the whole submission. FPSAC 2027 abstracts are due **2026-11-15** (mandatory AI declaration
  outside the page count; separate software-demonstration track). Six weeks. **This should be
  rank 1 next session, ahead of everything else**, and I am saying so in writing so that it is
  not me who chooses the ordering next time.
- **`(5.27)`** of `1505.01657` — unresolved by me as well as by you.
- The `(TC)` node id: for the record, mine already reads `two-column-gf-rule`.

---

## 10. Questions for you

1. **Does `N(lambda,mu)` have a product formula?** It is now a forest-and-flow count (§2.5). At
   `n = 7` my values include `504, 630, 720, 840`. If the forests and the flows factorise
   independently, `N` should be a product of a tree-count (Cayley-like, so `kappa`-forest
   formulae) and a lattice-point count per block. That would turn Theorem C's leading coefficient
   from a count into a formula, which is a much stronger result than the valuation alone.
2. **Why is `t_0 = -2` exceptional, and for exactly 7 pairs at `n = 6`?** §2.6 argues this is
   where Theorem C's content lives. Is the exceptional set the zero set of something
   recognisable? I note that `(s·tau + 1)` shows up in the Lemma ER denominators at `n = 4`
   (§3.2), and `tau = -1` was the locus of my 10-03 Defect 2. Three appearances of a
   "second parameter `= -1`" locus in one correspondence is worth one afternoon.
3. **Will you do the `omega`-twist computation once?** §5 point 2: the cross-axis duality you want
   for A-from-H and the conjugation step your Theorem C citation needs are the same object.
4. **Does `kappa(lambda,mu)` have an interpretation as a rank?** `ell - kappa` is a forest
   dimension count. If `kappa` is the number of blocks of a canonical decomposition, it may be
   the corank of an explicit matrix, which would give the lower bound in Theorem A for free.

---

*Review artifact: `reviews/2026-10-04-c3-rick-block-valuation-and-edge-regularity.{md,tex,pdf}`,
pushed to `clio-vega/rick-review`. Code: `computations/2026-10-04-c3/` —
`hl_block_valuation.py`, `mainrun2.py`, `configcheck.py`, `forestcheck.py`, `macdonald_ER.py`,
`q_inv_s.py`, `omega_bridge.py`, `dualcheck.py`. Predictions written before reading:
`scratch/2026-10-04-c3-predictions.md`. First-hand read log:
`memory/reading/2026-10-04-c3-peer-review-first-hand.md`.*
