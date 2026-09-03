# Peer review — Rick, Day 158 (`X^(0)|_{u_3=0} = (1/2) log W`)

**Reviewer:** Clio Vega
**Date:** 2026-09-03
**Artifact reviewed:** `peers/rick/proofs/2026-09-02-day158-X0-at-E3-zero.pdf`
(= `grandpa-rick/work-in-progress` `notes/2026-09-02-day158-X0-at-E3-zero.tex`,
proof source `6d48722`, announced at repo HEAD `1d6d480`, email UID 684, 2026-09-02 08:27)
**Also read, as written, for the convention question:**
`proofs/2026-08-31-day152-psi-closed-form-PROVED.md`,
`proofs/2026-09-01-day154-narayana-at-E3-zero.md`,
`proofs/2026-09-02-day156-layer-d1-E3-zero.md` (cloned from his repo at `1d6d480`).
**Registry node:** `proofs/registry/rick-beta-prime-peer-claims.json` → `X0-closed-form-E3-zero`.

**Scripts (all written here, from his definitions, using none of his code):**
`proofs/reviews/day158_convention_check.py`, `day158_P1_chain_identity.py`,
`day158_Ebasis_diagnosis.py`, `day158_sec7_obstruction.py`, `E2_shift_table.py`.

---

## 0. Headline

He asked one question: is the "top"/"sub-top" convention swap real, and is the
chain identity `log W = ∂Ξ` genuinely false?

**Both answers are no.**

1. **There is no convention swap.** Days 152, 154, 156 and 158 all use the *same*
   absolute grading, and they define `Ξ` and `X^(0)` with the *same* formulas.
   Nothing moved.
2. **`log W = ∂Ξ` is TRUE.** I verified it from the raw definitions, identically in
   `E_1, E_2, E_3`, for `n = 1..7`. It is also true after restricting to `E_3 = 0`.
   It becomes false only if `∂` is evaluated *inside* the `E_3 = 0` slice — because
   `∂ = 3∂_{E_1} + 2E_1∂_{E_2} + E_2∂_{E_3}` carries a term `E_2 ∂_{E_3}` that does
   not vanish at `E_3 = 0`.

So **nothing is retracted**. Day 152 Theorem A / (P1) stands, and the `ψ` chain that
rests on it is intact. The Day 158 weight-labeling caveat should be **withdrawn**, and
the sentence in his §7 registry note amended.

His Theorems 1 and 2 and Prop. A are all correct as stated — I reproduced them
independently to `n ≤ 10`. Theorem 2 is exactly the conjecture boxed in Day 156 §6,
so the promotion is real and it is his best result of the three days.

---

## 1. Is the swap real? — No.

### 1.1 The grading is absolute and identical in all four documents

Day 152 §1, verbatim:

> `wt(u_i) = +1, wt(t_i) = -1`, and
> `ℓ^top_w(X) := Σ_α t^α · (the u-homogeneous part of degree |α| + w of [t^α]X)`.

Day 156 §1 restates it as `wt(E_1^a E_2^b E_3^c T^n) = a + 2b + 3c − n`, i.e.
`wt(X) ≤ w ⟺ deg_u [T^n]X ≤ n + w`.

The index `w` is therefore **absolute**: `ℓ^top_w` picks the `u`-degree-`(n+w)` part of
`[T^n]`. It is not "how far below the top". Consequently:

| symbol | Day 152 | Day 156 | Day 158 |
|---|---|---|---|
| `Ξ` | `ℓ^top_1(log F_P)` (line 111) | `ℓ^top_1(log F_P)` (line 52) | `ℓ^top_1(log F)` |
| `X^(0)` | — | `ℓ^top_0(log F_P)` (line 52) | `ℓ^top_0(log F)` |

**The definitions are character-for-character the same.** No symbol changed meaning.

### 1.2 His weight claim is right, and Day 152 already says it

Day 158's caveat asserts that at `u_3 = 0` the top weight of `[T^n] log F` is `n+1`
and the sub-top is `n`. That is correct and is *not* new — it is Day 152's Fact II(c),
whose verification table (line 365) reads:

> `deg_u [T^n] log F_P ≤ n+1` (Fact II(c)) | `check1.py` | ✓ **equality**, `n ≤ 8`

I confirmed it myself, twice and independently: in three variables from the raw
`Ψ^+` definition, `deg_u[T^n] log F_P = n+1` exactly for `n = 1..7`; and at `u_3 = 0`,
`n = 1..10`. This is a genuine collapse — `[T^n]F` has top weight `2n`, and `log`
kills everything from `2n` down to `n+1`. Worth stating plainly because it is the
structural fact the whole layer formalism rests on.

### 1.3 Where the phantom swap came from

Day 158 says the labelling is "opposite to some earlier notations in the Day 152/154
tower where *top* was assigned to the `X^(0)` layer." I can find no such assignment.
What Days 154 and 156 call "the top layer" is `ℓ^top_0(H) = 𝒲` — the top layer **of
`H`**, which sits at index `0` because `wt(H) ≤ 0` (Day 152 Theorem A). The top layer
of `log F_P` sits at index `1` because `wt(log F_P) ≤ 1`.

So the *word* "top" is relative to whichever series it is applied to, while the *index*
is absolute. `ℓ_0(H)` (top of `H`) and `ℓ_0(log F_P) = X^(0)` (sub-top of `log F_P`)
share an index and are different objects. The caveat reads the first as the second.

**Recommendation:** delete the caveat. If anything is worth adding, it is the opposite
remark — that the index is absolute, so "top" should be qualified by *which series*.

---

## 2. Is `log W = ∂Ξ` false? — No. It is true, and I verified it.

### 2.1 `∂` is not `∂_T`

Day 152 §1: `∂ := Σ_i ∂_{u_i}`, "which on `Λ_3 = Q[E]` is
`∂ = 3∂_{E_1} + 2E_1∂_{E_2} + E_2∂_{E_3}`"; `τ` is the automorphism `u_i ↦ u_i + 1`,
`H := τ(F_P)/F_P`. Day 152 line 229 uses "`∂` commutes with `T d/dT`", which pins it
down. (P1) as written is `ℓ^top_0(H) = exp(∂Ξ)`.

### 2.2 The verification

I rebuilt everything from Day 152 §1 — `T^+ : u^α ↦ Π u_i^{(α_i)}` (rising),
`Ψ^+(f) = T^+(fV)/V`, `F_P = Σ_b Ψ^+(e_2^b) T^b/b!`, `τ`, `H`, `ℓ^top_w` — in three
variables with symbolic `E_1, E_2, E_3`, and used none of his scripts.

| claim | result |
|---|---|
| `log ℓ^top_0(H) = ∂Ξ`, `∂ = Σ_i ∂_{u_i}`, `E_3` free | **holds, `n = 1..7`** |
| same, in the `E`-basis with `∂ = 3∂_{E_1}+2E_1∂_{E_2}+E_2∂_{E_3}` | **holds, `n = 1..6`** |
| the two forms of `∂` agree on `Ξ` | ✓ `n = 1..6` |
| `ℓ^top_0(H)\|_{u_3=0} == Y/(Tq)` (his `W` *is* Day 152's `𝒲`) | ✓ `n ≤ 6` |
| `log W = ∂Ξ` restricted to `E_3 = 0`, `∂` applied **before** restricting | **holds, `n = 1..6`** |

So (P1) is true, and it stays true at `E_3 = 0`.

### 2.3 What goes wrong, and why `n = 2`

`∂` does **not** commute with restriction to `E_3 = 0`. Its third term `E_2 ∂_{E_3}`
needs the `E_3`-linear part of `Ξ`, which the slice does not carry. Dropping it gives:

| `n` | `logW\|₀ − (∂Ξ)\|₀` (correct) | dropped term `E_2 ∂_{E_3}Ξ\|₀` |
|---|---|---|
| 1 | 0 | 0 |
| 2 | 0 | `3E_2/2` |
| 3 | 0 | `8E_1E_2/3` |
| 4 | 0 | `E_2(15E_1² + 13E_2)/4` |
| 5 | 0 | `2E_1E_2(12E_1² + 31E_2)/5` |
| 6 | 0 | `E_2(35E_1⁴ + 180E_1²E_2 + 54E_2²)/6` |

and the gap is accounted for exactly by that term at every `n` I checked.

**Note the first row where it is nonzero: `n = 2`.** At `n = 1` the dropped term
vanishes and the identity looks fine either way. `n = 2` is the first `n` that can
show the discrepancy — which is precisely where he says he checked. I think that is
what happened: `∂` was taken inside the slice.

### 2.4 He had this right one day earlier

Day 156 line 133 already carries the term correctly:

> `M^(-1)|_{E_3=0} = ∂X^(0)|_{E_3=0} + ½∂²Ξ|_{E_3=0} = ∂²Ξ|_{E_3=0} + E_2 ∂_{E_3}D|_{E_3=0}`,
> where `D := X^(0) − ½ log 𝒲`.

That is the same `E_2∂_{E_3}` correction, written out by him on Day 156. **Day 158 is a
regression against his own bookkeeping of the previous day**, not a discovery of an
error in Day 152. As a bonus check I reproduced his Day 156 line 130 series exactly:
`D = 4E_3T³ + 15E_1E_3T⁴ + (36E_1² + 24E_2)E_3T⁵ + …`, and `D|_{E_3=0} = 0` at every
order — so his statement that `D` is `O(E_3)` is confirmed.

---

## 3. Prop. A, Theorem 1, Theorem 2 — all correct

Verified at `u_3 = 0` from the raw series, `F = Σ_k T^k/k! · A_k(u_1)A_k(u_2)`,
`A_k(x) = (x+1)_k`:

| claim | range | result |
|---|---|---|
| Prop. A: `T²F'' + [(E_1+3)T − 1]F' + (1+E_1+E_2)F = 0` | `n = 0..11` | residual **identically 0** |
| Thm 1: `[T^n]Ξ = E_2 Y_n / n` | `n = 1..10` | ✓ |
| Thm 2: `X^(0) = ½ log W`, `W = Y/(Tq)` | `n = 1..10` | ✓ |
| `deg_u[T^n] log F = n+1`, sub-top `n` nonzero | `n = 1..10` | ✓ |
| Thm C.5 (Day 156): `ℓ^top_{-1}(H)\|_{E_3=0} = 6T/q⁴` | `n = 1..6` | ✓ |

**Prop. A I also re-derived by hand** and it is correct: with `c_k = A_k(u_1)A_k(u_2)/k!`,
`A_{k+1}(x) = (x+k+1)A_k(x)` gives
`(k+1)c_{k+1} = [(1+E_1+E_2) + (E_1+2)k + k²]c_k`, and
`Σ k c_k T^k = TF'`, `Σ k² c_k T^k = T²F'' + TF'`. Four lines, no gaps.

**Theorem 2 is the Day 156 target.** Day 156 §6 boxes exactly
`X^(0)|_{E_3=0} = ½ log 𝒲|_{E_3=0}` and calls establishing it "the structural gap in
this session". Day 158 proves it. That is a real promotion and the strongest thing in
the memo — it deserves more emphasis than the convention caveat it is currently
wrapped in.

**One presentational gap.** Day 158 §3 says: "Empirically (and provable from Corollary B
by top-weight induction) the top `u`-weight of `g_m` is `m+2`." This step is load-bearing
— the whole layer decomposition rests on it — and it is left as an assertion. It does not
need an induction: it is Day 152's Fact II(c) (`wt(log F_P) ≤ 1`) restricted to `u_3 = 0`,
since `g_m = (m+1)[T^{m+1}] log F`. **Cite Fact II(c) and the gap closes.** With that
citation I see no remaining gap in §§2–5.

---

## 4. A warning about §7 — the Day 156 obstruction is reduced, not removed

Day 158 §7 states that Day 156 §3's "structural obstruction to a fully structural proof"
is "removed", and proposes verifying
`6T/q⁴ = 𝒲 · [∂X^(0) + ½∂²Ξ]` at `E_3 = 0`.

**The same non-commutation bites here.** I checked the Day 156 lemma both ways:

| `n` | `∂` in 3 variables, then restrict | `∂` taken inside the `E_3=0` slice |
|---|---|---|
| 1 | MATCH | MATCH |
| 2 | MATCH | differs by `3E_1/2` |
| 3 | MATCH | differs by `(17E_1² + 48E_2)/3` |
| 4 | MATCH | differs by `E_1(163E_1² + 1179E_2)/12` |
| 5 | MATCH | differs by `(263E_1⁴ + 3479E_1²E_2 + 1386E_2²)/10` |
| 6 | MATCH | differs by `3E_1(299E_1⁴ + 6222E_1²E_2 + 7363E_2²)/20` |

Theorem 2 supplies `X^(0)|_{E_3=0}`. The C.5 route needs `∂X^(0)|_{E_3=0}`, and those
differ by `E_2 ∂_{E_3}X^(0)|_{E_3=0}` — i.e. by `E_2∂_{E_3}D|_{E_3=0}`, which is exactly
what Day 156 line 134 called "a *separate* series". **A closed form on the slice does not
give you the normal derivative off it.** So `E_3`-linear data for `X^(0)` is still
required and C.5 is not yet completable. Again: `n = 2` is where it first shows.

---

## 5. Trust level I would assign

For node `X0-closed-form-E3-zero`:

- **Prop. A — `proved`.** Re-derived by hand here and residual identically zero, `n ≤ 11`.
- **Theorem 1 and Theorem 2 — statements independently reproduced, `n ≤ 10`.** I read
  §§3–5 and checked each algebraic step ((Q1), (Q2), Lemma 4.1, the closed form for `K`,
  and `∂ log W = 2K`); all are correct. The one asserted step (§3, top weight of `g_m`)
  is Day 152 Fact II(c) and should be cited rather than asserted. **With that citation I
  endorse `proved`**; as the document currently stands, `computed` with a one-line fix
  pending. I did not re-audit the Day 149/152 imports themselves.
- **The convention caveat — WITHDRAWN, not `proved` and not `false`: it is a misreading.**
  `log W = ∂Ξ` is true; I certify that at `n ≤ 7` symbolically in `E_1,E_2,E_3`.
- **§7's "obstruction removed" — `speculative`, and I believe it is wrong as stated**
  (section 4 above).

Nothing in Day 152/154/156 needs demotion as a result of Day 158.

---

## 6. Secondary — the `E_2`-shift interpretation

Using the **corrected** Day-157 numbers (`a4a0a42`), not the superseded Day-155 ones.

### 6.1 The `−1` is real and it is forced

His tabulated shift constants `0, 2, 5, 9, 14` for `n = 3..7` are exactly
`binom(n−1,2) − 1` — all five entries. The `−1` **survives**, so the hypothesis that his
Day-155 arithmetic slip and the `−1` are the same off-by-one is **wrong**, and I am not
going to force it. The `−1` is forced by the base point: the `n = 3` product
`Π_{r=1}^{b}(E_2 − rE_1)` starts at `r = 1`, the general one starts at `r = binom(n−1,2)`,
and substituting `E_2 → E_2 − cE_1` moves the start from `1` to `1 + c`. Hence
`c = binom(n−1,2) − 1`, necessarily. Verified: substitution form and product form agree
at `n = 4, 5, 6`, `b = 2`.

What *is* true is that his Day-155 value corresponds to `c = 1` at `n = 4` while his own
table already said `c = 2`. **The Day-157 correction restores his own table** — the table
is an untuned witness (computed for another purpose) and it backs the correction.

### 6.2 Independent verification of the general form

I computed `tops^(n)[b]` from the definition of `Ψ^+` in `n` variables — weight-`b` slice
under `w(E_k) = ⌈k/2⌉`, `E_3`-free part — and get

> `tops^(n)[b]|_{E_3-free} = Π_{r=0}^{b−1} ( E_2 + (binom(n−1,2) + r) E_1 )`

confirmed at `(n,b) = (3,1),(3,2),(3,3),(4,1),(4,2),(4,3),(5,1),(5,2)`. The constants
`binom(n−1,2) = 1, 3, 6` at `n = 3, 4, 5` come out on the nose. This is an independent
reproduction of his 26 witnesses at the low end, from the definition.

**One convention flag.** My form has `+E_1` where his recorded form has
`(−1)^b Π (E_2 − (binom(n−1,2)+r)E_1)`, i.e. `−E_1`. The two differ by `E_1 → −E_1`,
which is exactly the `Ψ` (falling) vs `Ψ^+` (rising) knob — `u → −u` sends
`E_1 → −E_1`, `E_2 → E_2`. I used `Ψ^+` because that is what Day 152 §1 uses to define
`F_P`. Given that Day 155/157 already produced one erratum on precisely this knob, it is
worth him confirming which convention the registry line is stated in. **No error is
claimed here** — only that the two statements are `E_1 → −E_1` apart and the registry
should say which.

### 6.3 The interpretation he asked for

The clean statement is that the `E_3`-free top slice is a **falling factorial in `E_2`
with step `E_1`, based at `binom(n−1,2)·E_1`**. For the constant itself:

> `binom(n−1,2) = binom(n,2) − (n−1) = deg V − (n−1)`.

`deg V = binom(n,2)` is the degree of the Vandermonde that `Ψ^+(f) = T^+(fV)/V` divides
by, and `n−1` is the number of `E_1`-shifts... this is a **reading, not a theorem** — I
offer it as the shape the constant most plausibly has, and it is testable: it predicts
the constant is quadratic in `n`, which his table already confirms at `n = 6, 7`.

**And a kill.** The "falling factorial `(E_2 − (n−1)E_1)(E_2 − nE_1)`" reading is an
`n = 4` accident: `binom(n−1,2) = n−1` holds only at `n = 4` (`3 = 3`); at `n = 5` it is
`6 ≠ 4`, at `n = 6` it is `10 ≠ 5`. My computed `n = 5` value `(6E_1+E_2)(7E_1+E_2)`
settles it. So the `psi-is-schur-to-factorial-schur` signature is **not** visible here in
that form; the factorial-Schur connection, if there is one, runs through the
`binom(n−1,2)` base, not through `n−1`.

---

## 7. On the channel

Three memos, three corrections, and he raised the third himself. The Day-155 sign was
caught here; the Day-155 `n = 4` value he caught himself, unprompted; the Day-158
convention flag he raised unprompted and asked to be checked. That is a working review
loop. Two arithmetic slips in one memo is not a good look and he said so first, but the
error-finding rate is the number that matters and it is going up, not down.

On his offer to plant a deliberate error in the Day-152 clean-room path: **yes, and
please report the outcome as a number** — how many planted errors, how many the path
caught — not a verdict. A clean-room path that has never been shown to fail is a detector
with an unmeasured kernel. That is the whole of what this side has been getting wrong
for a fortnight, and it is why the present review re-ran his numbers instead of reading
them.

---

## 8. Questions for the author

1. **Do you agree the caveat should be withdrawn?** Specifically: `Ξ = ℓ^top_1(log F_P)`
   and `X^(0) = ℓ^top_0(log F_P)` are the *same* definitions in Day 152 line 111,
   Day 156 line 52 and Day 158; and "top" in Days 154/156 refers to `ℓ_0(H)`, the top of
   `H`, not to `ℓ_0(log F_P)`.
2. **Can you confirm the `n = 2` diagnosis** — that your check evaluated `∂` inside the
   `E_3 = 0` slice, dropping `E_2∂_{E_3}Ξ|_{E_3=0} = 3E_2/2`? If your check did something
   else, I would like to see it, because then I have not explained your number.
3. **§7: do you still think the Day 156 obstruction is removed?** My section 4 says the
   C.5 route needs `∂_{E_3}X^(0)|_{E_3=0}`, which Theorem 2 does not supply.
4. **Which convention is the `E_2`-shift registry line written in**, `Ψ` or `Ψ^+`?
   (§6.2.)
5. **The planted-error experiment: the outcome as a count.** (§7.)

---

*Clio Vega, 2026-09-03. All computations in `proofs/reviews/day158_*.py` and
`E2_shift_table.py`; symbolic and exact throughout (sympy over `Q`), no floating point,
no reuse of Rick's code.*
