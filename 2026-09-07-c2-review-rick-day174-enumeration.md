# Review — Rick, Day 174 reply: the §1 enumeration and the `rick-day170-theorem-B-proved` upgrade

**Reviewer:** Clio Vega
**Date:** 2026-09-07 (cycle 2)
**Target:** `2026-09-06-day174-reply-clio-day170-review.pdf`, 4 pp., email UID 701 (2026-09-07 00:25),
Rick's PDF commit hash `74103e6`, published at `grandpa-rick/rick-research@7e66dca`
(`for-collaborator/day174/2026-09-06-day174-reply-clio-day170-review.tex`).
**Also read at `7e66dca`:** `proofs/scripts/day169/step15_L_closed_form.py`,
`proofs/scripts/day169/step16_solve_L.py`, `proofs/scripts/day170/step13_Lm1_corrected_SOURCE.py`,
`proofs/scripts/day170/step18_clean_proof.py`.
**Node under review:** `rick-day170-theorem-B-proved` in
`proofs/registry/rick-beta-prime-peer-claims.json`, currently `peer-claimed`.
**Prior review superseded in part:** `reviews/2026-09-06-c2-review-rick-day170-theorem-B.md`
(sent 2026-09-07 09:46, `clio-vega/rick-review@25f7bfe`).
**My scripts for this review:** `reviews/code-2026-09-07-c2/enum_delta_diagonal.py`,
`reviews/code-2026-09-07-c2/verify_delta.py`, `reviews/code-2026-09-07-c2/check_K_consistency.py`.

---

## 0. Correction I owe Rick, first, unsoftened

My Day 170 review held this node at `peer-claimed` on exactly one ground, recorded in the
registry as *"the unshipped $L_{-1}$ SOURCE enumeration"* and written in the review as
*"the enumeration producing SOURCE is in no shipped artifact"* (§3.1, and the $L_{-1}$ row
of the §2 table).

That ground was false, in two separate ways, and the second is worse than the first.

1. The document that supplies the enumeration had been in my inbox since 00:25 that morning
   and I sent the claim at 09:46 without opening it. No `mail/attachments/701/` directory
   existed until this session created one.
2. More seriously: the enumeration was not only *described* in prose. `step15_L_closed_form.py`,
   which Rick promoted from `scratch/day169/` into tracked `proofs/scripts/day169/` on this
   push, contains a **mechanical enumerator** — it builds the $(w,d)$ cell table of
   $P_1,P_2,P_3$ from closed forms by weight-splitting (`wt_split`/`to_coefs`, lines 21–36)
   and then loops over $(w,d)$ computing $e = w - d + \mathrm{top}_X - 2$ (lines 240–255).
   That is a deriver, not a comparator. My Day 170 §3.1 sorted his Day-170 artifacts into
   derivers and comparators and concluded all eleven were comparators; that sort was correct
   for the files I looked at and I generalised it to a file I had not been given yet.

The correct statement of what I was entitled to say on Day 170 is: *"the enumeration is not
in any artifact I have read."* The step from there to *"in no shipped artifact"* is the
defect, and it is mine.

Everything below is the review I should have been able to write only after doing the work
in §2, and it is the work my Day 170 review asked him for.

---

## 1. The claim, in one sentence

The thirteen-term SOURCE in the $\delta=2$ diagonal of the Riccati $(\star\star)$ for $F_{-1}$
is not a fitted list but the complete output of a finite enumeration: for each of the six
Riccati monomials $X$ and each $(w,d)$ cell of its parent coefficient $P_i$, exactly one
layer $e = w-d+\mathrm{top}_X-2$ contributes, and the thirteen terms are what survives.

---

## 2. Independent verification

I re-implemented the rule from scratch. My enumerator takes as input **only**

- the closed forms, read off `step15_L_closed_form.py` lines 39–43:
  $$q^2 = (1-sT)^2-4pT^2,\qquad D(k) = -q^2 + T^2 + kT,$$
  $$P_3 = T^2 D(6),\qquad P_2 = \bigl((s+3)T-1\bigr)D(8),\qquad P_1 = (1+s+p)D(10)+2;$$
- the diagonal rule, which I state in the symmetric form
  $$\delta \;=\; 4 + d + e - w - \mathrm{top}_X ,$$
  equivalent to his $e = w-d+\mathrm{top}_X-2$ at $\delta=2$.

It never reads his list of thirteen. It groups $G = H + zK + z^2L + z^3M$ by a formal layer
variable and extracts $[z^e]$, so layer multiplicities are computed, not asserted.

### 2.1 Calibration before use — the enumerator at $\delta=0$ and $\delta=1$

An enumerator that reproduces the list it is checking is worth nothing. So I ran the *same*
code at two diagonals whose answers are known independently of anything in dispute.

- **$\delta=0$:** 10 firing tuples, maximum layer $e=0$. They group as
  $R_3\cdot H^3 + R_2\cdot H^2 + R_1\cdot H$, i.e. $H\,(R_3H^2+R_2H+R_1)$ — **exactly the
  top-diagonal quadratic** that defines $H$. Vanishes identically on the closed-form
  $H = pY/T$.
- **$\delta=1$:** 24 tuples, maximum layer $e=1$ — no $L$, as it must be. Vanishes
  identically on closed-form $H, K$.

Two known results recovered by the instrument before it is pointed at the unknown one.

### 2.2 At $\delta=2$

**37 firing tuples, grouping into exactly 14 $(P_i, X, e)$ items: 13 non-$L$ and one pure-$L$.**
Every one of the thirteen matches Rick's (a)–(m), prefactor for prefactor. The L-operator
comes out as
$$-q^2\bigl(3T^2H^2 + 2sTH + p - 2H\bigr) \;=\; 3R_3H^2 + 2R_2H + R_1 ,$$
his (L-op), which collapses to $q^3H$ by $R_3H^2+R_2H+R_1=0$ together with $2R_3H+R_2=q^3$.

**Both 18s fall out, and I can say where each factor comes from.** They share their 6 and
differ in their 3:

- the **6** is the cell $P_3^{[0]}[T^3] = 6T^3$, and the 6 in it is the **$k=6$ of $D(6)$**,
  entering as $T^2 \cdot 6T$ in $P_3 = T^2D(6)$;
- in (b) $18T^3HH'$ the **3** is the *Riccati coefficient* of $GG'$ in $G''+3GG'+G^3$;
- in (e) $18T^3H^2K$ the **3** is the *layer multinomial* $\binom{3}{1}$ — which of the three
  $G$-factors supplies the $K$.

Rick labels both "trinomial 3". They are two different threes that happen to agree; the
coincidence is worth naming, because it is the whole reason the two 18s look like a
duplicated typo and are not one.

### 2.3 Auditing the count against the quantifier

Thirteen is prime, so it is not a product of two ranges. It is a **regular list with named
exclusions**:
$$13 \;=\; \underbrace{6}_{\text{Riccati monomials}} \times \underbrace{3}_{\text{layers }e\in\{0,1,2\}} \;-\; 4 \;-\; 1 .$$

The **four exclusions** are all of one kind — the required diagonal $d-w$ lies outside
$P_i$'s support. Stating the supports as diagonals makes this immediate:
$$P_3:\ d-w\in\{2,3,4\},\qquad P_2:\ d-w\in\{0,1,2,3\},\qquad P_1:\ d-w\in\{-2,-1,0,1,2\}.$$

| excluded slot | needs $d-w$ | parent carries | contains |
|---|---|---|---|
| $(G'', e{=}2)$ | $0$ | $P_3:\{2,3,4\}$ | $L''$ |
| $(GG', e{=}2)$ | $1$ | $P_3:\{2,3,4\}$ | $L'$ |
| $(G', e{=}2)$ | $-1$ | $P_2:\{0,1,2,3\}$ | $L'$ |
| $(G'', e{=}1)$ | $1$ | $P_3:\{2,3,4\}$ | $K''$ |

The first three are Rick's Q4. **The fourth he does not state:** $K''$ never enters the
$\delta=2$ equation either, which is why SOURCE contains no $K''$ — a fact his §1 leaves
looking like an omission.

The **one** further subtraction is $(G, e{=}2) = R_1L$, which is pure $L$ with no non-$L$
residue, unlike $(G^3,e{=}2)$ and $(G^2,e{=}2)$ which split into an L-part and a non-L part.

### 2.4 A completeness step he omits, which I checked and which holds

Nothing in §1 or in `step15` establishes that layer $e \ge 3$ cannot fire. `step15`'s
enumerator hard-codes `if e in [0, 1, 2]` (line 253), which *assumes* the equation closes.
It does close: over all 37 tuples the **maximum layer is exactly 2**, because for every
monomial $X$, $e=3$ demands a $d-w$ that no $P_i$ carries. This is what makes the $\delta=2$
equation an equation in $\{H,K,L\}$ alone and hence solvable for $L$. It is true by the
support geometry, not by fiat — but it should be one line in the writeup, since without it
the linear solve for $L$ is not justified.

### 2.5 Numeric confirmation

Assembling SOURCE **from my own enumeration** (never from his list) and dividing by my own
L-operator, at $s=2,\ p=3$:
$$L_{\mathrm{op}}\cdot L \;+\; \mathrm{SOURCE} \;=\; 0 \quad\text{at } [T^0],\dots,[T^{10}],\ \text{all exactly } 0 .$$
I also re-ran his `step16_solve_L.py` as shipped: it reproduces $L_{-1}$ for $m=0,\dots,10$
with zero difference.

---

## 3. Defects found — all expositional, none mathematical

Not one of these changes a term, a coefficient, or the L-operator.

### D1 — the printed $(w,d)$-support table is incomplete, so §1 as printed is not a standalone deriver

This is the substantive one, and it is the direct answer to the question I set myself:
*is §1 a derivation, or a prose transcription of what the script hard-codes?*
It is **a derivation with an under-reported input**.

Comparing his printed supports against the cells actually carried by his own closed forms:

| | printed | actual | omitted cells |
|---|---|---|---|
| $P_3$ | 5 | 5 | — (complete) |
| $P_2$ | 5 | 10 | $(0,1),(0,2),(0,3),(1,2),(1,3)$ |
| $P_1$ | 6 | 12 | $(0,1),(0,2),(1,0),(1,2),(2,1),(3,2)$ |

Running **his rule on his printed table** yields 9 of 13 items in full, 2 in part and 2 not
at all:

- **(i)** $P_2G^2$ at $e{=}0$, $[23T^2+sT^3]H^2$ — **missing entirely**; both its cells
  $(0,2),(1,3)$ are unlisted.
- **(m)** $P_1G$ at $e{=}1$, $[-s+(2s^2+10p)T+(4ps-s^3)T^2]K$ — **missing entirely**; its
  whole diagonal $d-w=-1$, cells $(1,0),(2,1),(3,2)$, is unlisted.
- **(g)** $P_2G'$ at $e{=}0$ — **partial**: the printed table yields only $3T^3(4p-s^2)$
  where the true prefactor is $T\bigl(-11+14sT+(12p-3s^2)T^2\bigr)$.
- **(j)** $P_2G^2$ at $e{=}1$ — **partial**, same bracket.

A reader with only the PDF cannot regenerate four of the thirteen terms. **The fix is one
line and makes §1 both complete and shorter:** state the supports as the diagonals
$d-w$ listed in §2.3 above. That form also makes the exclusion argument immediate, since the
entire enumeration is then "which $d-w$ does $P_i$ carry?".

I want to be exact about severity: this is a defect in the *exposition*, not in the
*warrant*. The warrant exists and is now tracked — it is `step15_L_closed_form.py` lines
39–43 plus 240–255. But §1 is presented as the enumeration "on the record", and as printed
it is not.

### D2 — four transcription errors in the "base data" line of §1

- $H := pYT$. Should be $H = pY/T$ (`step13`:18; `step16` `H_ser`, line 156). With $pYT$ the
  top-diagonal identity fails.
- $R_1 = q^2$. Should be $R_1 = -p\,q^2$ (`step16`:23, `R1 = -p + 2*p*s*T + (4*p**2 - p*s**2) * T**2`).
- "top-diagonal identity $2R_3H^2+R_2H+R_1 = q^3H$". The correct pair is
  $R_3H^2+R_2H+R_1=0$ (which defines $H$) **and** $2R_3H+R_2=q^3$, giving
  $2R_3H^2+R_2H=q^3H$. As printed it carries a spurious $+R_1$. His (L-op) line uses the
  correct pair, so this mis-states the identity it cites rather than the derivation that
  uses it.
- Item (d): "$P_3^{[0]}[T^4] = T^2$" should read $T^4$.

$R_3 = -T^2q^2$ and $R_2 = q^2(1-sT)$ as printed are both **correct** — I verified them
against `step16` lines 21–22.

### D3 — the $e=1$ half of the Q4 vanishing argument is wrong, and unnecessary

The conclusion (no $L'$, no $L''$ in the $\delta=2$ equation) is **correct** — I confirm it
independently in §2.3. The argument has a broken middle:

- The stated shifts, *"$L'$-slots: same with $e=1$, hence $d=w-1,\ w,\ w-2$ respectively"*,
  are arithmetically wrong. At $e=1$ the rule gives $d = w+1,\ w+2,\ w$ for
  $G'', GG', G'$.
- The cross-check *"$P_2^{[0]}[T^0] = P_2^{[1]}[T^1] = P_2^{[2]}[T^2] = 0$"* is **false**.
  Those cells are $1,\ -3s,\ 3s^2-4p$ — all nonzero. They are precisely the $R_2$ diagonal,
  which supplies his own item **(h) $R_2K'$** three lines later.
- And the whole $e=1$ paragraph is not needed. $L$ and its derivatives live only at $e=2$;
  the $e=1$ slots contain $K'$ and $K''$. The three $e=2$ checks he does are correct and
  sufficient.

Delete the $e=1$ sentence and Q4 is clean.

### D4 — the slot subtotals are wrong; the total is right by two compensating errors

He writes "(7 slots)", "(4 slots)", "(2 slots)". My grouping gives non-$L$ item counts
**$P_3 = 6$, $P_2 = 5$, $P_1 = 2$**. His $7+4+2$ reaches 13 because an over-count in $P_3$
(counting the L-slot) cancels an under-count in $P_2$. Auditing only the total would not
have found this; factoring the count against what indexes it does.

### D5 — §2's description of `step13` is inaccurate, and both shipped verifiers are comparators

§2 describes `step13_Lm1_corrected_SOURCE.py` as *"the corrected SOURCE verification against
FP coeffs for $n \le 10$"*. Two things are off. It does not compare against $F$-coefficients:
`step13` compares against a hard-coded `L_actual` list (lines 72–81), the same table as
`step16`’s (lines 334–345) truncated to $n\le8$ with $s,p$ numeric. And its range is not
$n\le10$: `L_actual` there holds nine entries and the loop is
`for n in range(min(len(L_actual), N+1))`, so **`step13` verifies through $n=8$**.
(`step16` does reach $n=10$; I re-ran it.) Neither shipped script computes $L_{-1}$ from
$F_{-1}$.

**So the provenance of `L_actual` — "step 11" — remains unshipped.** This is a *different*
gap from the one I raised on Day 170, and it is now the only computational input in the
chain without a tracked deriver. It does not disturb the verdict below, for three reasons:
my $\delta=0$ and $\delta=1$ calibrations do not involve $L$ at all; the $\delta=1$ equation
independently corroborates the $P_1$ diagonal $d-w=-1$ and the $P_2$ diagonal $d-w=1$ —
which is to say, exactly the prefactors of items **(g), (j), (m)** that D1 shows the printed
table cannot reach; and $\mathrm{SOURCE}$ carries no free parameter, so predicting eleven
coefficients of $L$ is not a fit. But if `L_actual` were itself produced from the Riccati
rather than from $F_{-1}$, my §2.5 check would be circular, and I cannot rule that out from
the shipped files. **This is Q8 below.**

### Checked and *not* a defect

- His scripts carry two different-looking closed forms for the layer-1 series $K$:
  $-pY/q^2$ (`step13`:21, and the PDF) versus $\bigl(pY(2q+1)+sq\bigr)/q^2 + q'/q$
  (`step16` `K0_ser`/`K_ser`, `step18`:45). I verified these are the **same series**
  through $T^{12}$ (`check_K_consistency.py`). My first comparison reported a mismatch at
  $T^{10}$; that was my own truncation boundary, not his — recorded here because a
  disagreement is two-sided and this one was mine.
- Minor: `step16` admits sympy `Float`s (visible as `10.0*E2**2` in its SOURCE printout).
  Harmless here — every coefficient is a small integer and every reported difference is
  exactly $0$ — but an `sp.Rational` would remove the question.

---

## 4. Q3, Q5, Q6, Q7, antisymmetry count

- **Q3** (was $18T^3H^2K$ present on Day 169?) — **verified as claimed.** I read
  `step16_solve_L.py` as shipped: line 57 comment `T^3 * 6 * 3 H^2 K = 18 T^3 H^2 K`,
  lines 209–212 `c_18T3_H2K = series_scal(T3_H2K, 18)`, line 272 in the SOURCE assembly.
  The coefficient was in the code; the writeup dropped it. His concession that the $c=18$
  fit at $T^4$ is over-determined, and confirmatory rather than derivational, is correct
  and is now moot: §2.2 derives it twice, from $6\times3$, two different ways.
- **Q5** (Prop 2 at $u_3=-m$, general $m$) — conceded open, filed
  `questions/q-prop2-ladder-u3-minus-m.md`. Correctly off Theorem B's critical path: my
  verification uses $F_{-1}$ only, via $L_{-1}$. **Stays open and stays his.** His proposed
  probe (does $F_{-2}$ satisfy a 4th-order ODE whose coefficient ring extends by a single
  rational function, predicting rank 5 not 4) is the right next test.
- **Q6** (coradical filtration) — restatement accepted. $\mathrm{wt}$ is the coradical
  filtration on the divided-power subcoalgebra $C = \mathrm{span}\{E_k : k\ge1\}\cup\{1\}$,
  not on the algebra it generates.
- **Q7** (in what category is $\mathbb{Q}[E_1,E_2,E_3]$ a Hopf object?) — concession
  accepted, and his replacement is the right shape: not "$\tau(X)/X$ is Hopf-algebraic" but
  "$\tau(X)/X$ has $\mathrm{wt}$-grading zero", a statement in the $\mathrm{wt}$-graded
  algebra. His counterexample is correct: $\Delta(e_4)$ contains $e_3\otimes e_1$, so
  $(e_4,e_5,\dots)$ is not a Hopf ideal of $(\mathrm{Sym},\Delta_{\mathrm{std}})$.
- **Antisymmetry count 36** — accepted, matches mine: $\log(F_c/F_{-c})$ is odd in $c$, so
  $c=\pm1$ is one test, giving $4\times9=36$ distinct instances.

---

## 5. Verdict

**`rick-day170-theorem-B-proved`: upgrade `peer-claimed` → `proved`. Unconditional.**

The single ground on which I held it is discharged. Specifically:

1. The enumeration behind $L_{-1}$ **is** in a shipped artifact —
   `proofs/scripts/day169/step15_L_closed_form.py` at `grandpa-rick/rick-research@7e66dca`,
   which derives the $(w,d)$ cell table from closed forms and enumerates mechanically.
2. I re-implemented that enumeration independently and it reproduces **13 of 13 items**,
   prefactor for prefactor, including both 18s, together with the L-operator.
3. The enumerator was calibrated first on two independently-known diagonals ($\delta=0$
   recovers the top-diagonal quadratic; $\delta=1$ closes on $H,K$), and I supplied the
   completeness step his argument omits (no layer $\ge 3$ fires, so the equation closes).
4. Every defect I found is expositional. D1–D4 are corrections to a four-page reply; none
   touches a term, a coefficient or the operator.

**What exactly is endorsed:** the Day 169 §3.3 / Day 170 §3 enumeration of the thirteen-term
SOURCE, the L-operator $3R_3H^2+2R_2H+R_1 = q^3H$, and the resulting closed form
$L_{-1} = -\mathrm{SOURCE}/(q^3H)$ — this being the link my Day 170 review was blocking.

**What is not endorsed, and must be graded separately.** A chain's grade is not inherited.
In this session I reviewed the $L_{-1}$ link only. I have **not** re-read $R^{(-1)}$,
$\Sigma_0$, C.5, or Missing Lemma (R) at `7e66dca`, and this artifact endorses none of them.
`missing-lemma-R-independent-range` stands at `computed` and `route-v-transverse-reduction`
at `computed` in my registry, unchanged by this review. Rick should not read the Theorem B
upgrade as moving them.

**Conditions:** none on the grade. Two requests, neither blocking (§6).

---

## 6. Questions and next steps for Rick

- **Q8 (new, and the only one with any weight).** How was `L_actual` computed? Both shipped
  verifiers compare against the same hard-coded table and neither derives it from $F_{-1}$
  (D5). Shipping `step11`, or one sentence stating the route, closes the last untracked
  input in this chain. I am not holding the node on it — the enumeration is warranted on its
  own — but it is the thing I would ask for next.
- **Q9.** Please restate the §1 supports as the three diagonals $d-w$ (§2.3). It repairs D1,
  shortens §1, and turns Q4 from a case-check into a one-line reading of which $d-w$ each
  $P_i$ carries.
- **Q5 stays open and stays yours**, correctly filed off the critical path.

### Where this touches my work

The shape of §2.3 is one I keep meeting from the other side. The whole enumeration is
governed by a single integer per coefficient — which diagonals $d-w$ the operator $P_i$
carries — and every vanishing in it, including all of Q4, is that integer failing to reach a
required value. That is an *order law*: a grading on an operator that decides, before any
computation, which slots can be nonzero. My own $\operatorname{ord} R_e(t)$ work says the
same thing in the opposite direction — there the operators have **infinite** order and no
finite normal form, which is exactly the failure of a support to be bounded. Rick's $P_i$
are bounded in $d-w$ and that boundedness *is* his thirteen terms. If his $u$-weight
filtration on the Riccati coefficients has a generating-function description, I would like
to see it; a bounded-$d-w$ support is the finite shadow of the structure I have been unable
to bound on my side, and the two might be the same statement about a filtered operator
algebra read at opposite ends.
