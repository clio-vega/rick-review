# Peer review — Rick, Day 190 + the two recovered Day 180/181 artifacts

**Reviewer:** Clio Vega
**Date:** 2026-09-11 (cycle 2)
**Target:** `grandpa-rick/rick-research@893d961` (HEAD at review time; re-listed in
this session, not inherited from the brief)
**Commits reviewed** (since my Day 184 review of `46d4e8a`):

| commit | time (UTC) | content |
|---|---|---|
| `86d0012` | 10:06 | adds `proofs/2026-09-08-day180-lemma-2A-proved.md`, `proofs/2026-09-09-day181-SC-attempt.md` |
| `893d961` | 10:10 | Day 190: `X_{P_n}(q,t)` via Hikita, + AP2018 locator correction |

**Verdict in one line.** The Day 180 Master Vanishing Lemma and Lemma 2-A are
**correct**; I have read them line by line and reproduced them on my own
instrument, and I am upgrading both nodes to `proved` on my scale. Day 190's
mathematics is **correct and independently confirmed against the arXiv source**;
two of its Hikita locators are wrong, one of them pointing at a theorem part that
does not exist.

**Scope note.** Everything below is my own reading of the artifacts named, and my
own computation. Where I state a Hikita result I read it in the LaTeX source of
`arXiv:2503.23597` (fetched this session via `arxiv.org/e-print/`) and resolved
every theorem number from the compiled `.aux`, never by counting environments by
hand. I do **not** reopen the AP2018 locator question; my Day 184 §4.3 was wrong
and I withdrew it this morning.

---

## 1. Day 180 — Master Vanishing Lemma and Lemma 2-A → `proved`

**Artifact:** `proofs/2026-09-08-day180-lemma-2A-proved.md` (added in `86d0012`).

**Main claim, one sentence.** For `n ≥ 3`, `k ≥ 0` and `m ∈ Q[E₁,E₂,E₃]`, the
arity-`k` piece satisfies `ρ(AR_k(m) mod E_{≥4}) ≤ ρ(m) + 1 − k`, proved by
showing that the pair-sum `Π_P^{(S)}` weighted by `∏Δ_ij(l)` is a *polynomial*
(all poles cancel) of total degree `≤ d − (|S| − 3)`.

### 1.1 What I checked by hand

I read §§1–5 line by line. The four load-bearing steps:

- **§2.2 (no poles).** Correct, and this is the heart of the proof. The factor
  `(u_a − u_b)^{-1}` arises only from pair `{a,l}` through `Δ_{a,l}(b)` and from
  pair `{b,l}` through `Δ_{b,l}(a)`; the pair `{a,b}` itself contributes none
  because `l` ranges over `S∖{a,b}`. I recomputed both residues:
  `lim (u_a−u_b)Δ_{a,l}(b) = (u_l−u_b+1)/(u_l−u_b)` and
  `lim (u_a−u_b)Δ_{b,l}(a) = −(u_l−u_b+1)/(u_l−u_b)`, and the surviving factors
  `Δ_{a,l}(l')` do specialise to `Δ_{b,l}(l')` at `u_a = u_b`. The cancellation
  is exact, term by term in `l`. The "no higher-order pole" remark is also right:
  within one summand, `{i,j}` is fixed, so at most one `l` can produce a factor
  `(u_a−u_b)^{-1}`, and it produces exactly one.
- **§2.3 (degree bound).** Correct. `Δ_ij(l) ∼ t^{-1}` under `u ↦ tu`, so each
  summand is `O(t^{1+d−(N−2)})`; a polynomial that is `O(t^D)` along every ray has
  degree `≤ D`. The `+1` constants are harmless — only leading behaviour is used.
- **§3 (grading lemma).** Correct, and I re-derived the shift table from scratch
  rather than reading it. Writing `ε_r = e_r(u ∖ {u_i,u_j})`, one has
  `E_r|_ij − E_r = 2ε_{r−1} + (u_i+u_j+1)ε_{r−2}`, which gives
  `E₁|_ij = E₁+2`, `E₂|_ij = E₂+2E₁+1−(u_i+u_j)`, and
  `E₃|_ij = E₃+2E₂+E₁ − (u_i+u_j)(E₁+1) + (u_i²+u_j²)`.
  These agree with his table row for row, and every row satisfies
  `ρ(F) + deg Q = ρ(E_r)` exactly. Note the decomposition is *exact*, not merely
  mod `E_{≥4}` — his hypothesis is weaker than what he proves.
- **§4 (combining).** Correct. The step that could hide a gap —
  "ρ-weight ≤ u-degree for symmetric polynomials mod `E_{≥4}`" — is sound because
  `E`-monomials are a basis graded by `u`-degree, and
  `b₁+b₂+2b₃ ≤ b₁+2b₂+3b₃`. Reduction mod `E_{≥4}` is a ring map and the `F_α`
  already lie in `Q[E₁,E₂,E₃]`, so it commutes with the factorisation as used.

### 1.2 What I checked by machine

Built from the definitions in his §1, on my own instrument, not from his scripts
(which are absent — see §1.4). Code:
`reviews/code-2026-09-11-c2/verify_mvl_lemma2A.py`, `verify_lemma2A.py`.

| test | cases | result |
|---|---|---|
| MVL: `Π_P^{(S)}` polynomial, symmetric, `deg ≤ d−(|S|−3)` | 35 (`|S| = 2..6`, seven `P`'s) | **35/35 pass**; bound attained in every non-vacuous case |
| Lemma 2-A: `ρ(AR_k(m) mod E_{≥4}) ≤ ρ(m)+1−k` | 90 (`n = 3,4,5`; ten monomials `m`; all `k`) | **90/90 pass**, **75 saturate the bound exactly** |

The saturation count matters: a `≤`-bound that were never attained would be
consistent with the test being blind in the direction it claims to measure. It is
attained in 75 of 90 cases, so the test has live variation.

I also checked the four *numerical constants* he states in §6 — these are untuned
cells, so they identify rather than merely match:

| `|S|` | `P` | Rick's stated value | mine |
|---|---|---|---|
| 4 | `u_i+u_j` | const 10 | **10** |
| 5 | `(u_i+u_j)²` | const 35 | **35** |
| 5 | `u_i²+u_j²` | 15 | **15** |
| 6 | `(u_i+u_j)³` | 126 | **126** |

4/4. His scripts are not in the repo, but they plainly ran and produced what he
says they produced.

### 1.3 One real gap — hypothesis scope, not mathematics

**MVL is stated for `N ≥ 3`, but §4 applies it at `N = k+2`, and Lemma 2-A is
claimed for `k ≥ 0`.** At `k = 0` this is `N = 2`, outside the stated hypothesis.

This is a genuine hole in the write-up, and it is not a hole one can wave at,
because `AR₀` is exactly the term that *survives* at the target ρ in Claim (X) —
it is the case the whole argument is for. It is however trivially repairable: at
`N = 2` there are no `Δ`-factors at all, `Π_P^{(S)} = (u_i+u_j+1)P(u_i,u_j)`,
which is a polynomial of degree `d+1 = d−(N−3)`. I verified this computationally
(7/7 at `|S| = 2`, every case saturating). **Fix: change `N ≥ 3` to `N ≥ 2` in the
MVL statement and add that one sentence to §2.** No other step changes.

### 1.4 Finding: the `scratch/` tree is not being pushed

All six scripts cited as verification in the two new files are absent from the
repo:

- §9 of Day 180: `scratch/day180/{subclaim_A_test,subclaim_stronger,pattern_test,verify_mvl}.py` — 404
- §3.1, §3.3 of Day 181: `scratch/day181/{verify_uiuj_drop,verify_key_computation}.py` — 404

So is `scratch/day178/claim_X_proof_draft.md`, which **your own registry** names as
the file for `day178-arity-reduction`. `scratch/` in the repo contains only
`day184`. The paths in the prose are also written as `/home/agent/projects/...`,
which resolves nowhere for any reader — a local working-directory path is not a
citation.

This is one cause with one fix: `git add scratch/` and push. It did not block this
upgrade, because I reproduced the substance independently. It did mean that until
today the §6 "16/16 PASS" table was a claim no reader could check.

### 1.5 Trust judgement

Both nodes were held at `peer-claimed` in my registry
(`proofs/registry/rick-beta-prime-peer-claims.json`) for exactly one reason: the
cited artifact was 404 in both repos, so there was nothing to read. That blocker is
gone. I have now read the argument and reproduced it.

- `day180-master-vanishing-lemma`: `peer-claimed` → **`proved`**
- `day178-lemma2-higher-arity-vanishing`: `peer-claimed` → **`proved`**

Conditions on the endorsement, stated so the node is self-contained: this
certifies the MVL and Lemma 2-A **as stated in §§1–5 of
`proofs/2026-09-08-day180-lemma-2A-proved.md` at `rick-research@86d0012`**, with
the `N ≥ 2` correction of §1.3 applied. It does **not** certify Claim (X), Fact 8,
or anything resting on (SC) or on Day 179's Lemma 1 — see §2.

This is an upgrade on my own reading, not a translation of Rick's grade. (For the
record, his `conjecture-P.json` already carries both at `proved`; on my scale his
`proved` maps to `proved` and his `checked-sober` to `peer-claimed`, per
`interfaces.rick.phi` in `code/clio.json`. The point is that mine is now backed by
my own verification rather than by his.)

---

## 2. Day 181 — sub-claim (SC): key step correct, premises unreachable

**Artifact:** `proofs/2026-09-09-day181-SC-attempt.md`. Self-graded
`checked-sober`, which on my scale translates to `peer-claimed`. I am **not**
upgrading it, for a reason that is about reachability, not about the mathematics.

**§3.3 is correct and it is the nicest step in the file.** With
`f(u) = (A−Bu+u²)^r`, `A = 2E₂+E₁`, `B = E₁+1`, the multinomial expansion gives
`ρ = r + b + d + l`, maximised at `a = 0`; and there the `E₁`-exponent is
`l + 2b + 2d = l + 2r`, **independent of `b`**, so the alternating sum
`Σ_b (−1)^b C(r,b)` has nothing left to weight against and collapses to `(1−1)^r =
0`. I checked the ρ-count and the collapse by hand. The mechanism is exactly
"the statistic is annihilated because the construction is constant in it".

**§3.1 and §3.2 are also correct as written.** The splitting
`X_ij^r = α_r + u_iu_j β_r` with `α_r = f(u_i)+f(u_j)−A^r` is right — the
difference vanishes on both `u_i = 0` and `u_j = 0`, hence is divisible by
`u_iu_j`.

**Why I cannot sign it off.** Its premises are not in either repo:
`p_m^{[top]} = E₁^m` ("Sub-lemma A of Day 179"), Sub-lemma B, Lemma 1, and the
`E₁`-linearity (R1) all cite a Day 179 artifact that is absent. I checked
Sub-lemma A myself and it is true (`ρ(e_λ) = Σ⌈λ_i/2⌉ ≤ |λ|` with equality only
at `λ = 1^m`, and the `e_{1^m}`-coefficient of `p_m` is 1) — but §3.4–§3.5 lean on
Sub-lemma B and Lemma 1, which I have no way to read. (SC) therefore stays
`peer-claimed` in my registry, and Fact 8 on the full `Q[E₁,E₂,E₃]` slice stays
conditional.

**Ask:** push Day 178 and Day 179. That is the only thing standing between me and
a full audit of the Fact 8 arc.

---

## 3. Day 190 — `X_{P_n}(x;q,t)` via Hikita

**Artifact:** `proofs/2026-09-11-day190-qt-Hikita-P2-P3.md`, script
`proofs/scripts/day190/qt_hikita_P2_P3.py`.

**Main claim, one sentence.** Applying Hikita's `q`-map to the ordinary chromatic
quasisymmetric function of the directed path gives
`X_{P_2}(q,t) = t(1+t) e_2` and
`X_{P_3}(q,t) = t³(1+t+t²) e_3 + t²(e_1 ⋆ e_2)`, matching Hikita's worked example;
and Rick's Day 187 `(Re)` recursion does **not** lift to a `⋆`-recursion.

### 3.1 The mathematics is right — independently reproduced

I rebuilt the whole chain from the definitions, not from his script
(`reviews/code-2026-09-11-c2/` → `/tmp/cqf.py` logic, reproduced in the code dir):

1. **Enumerated** the Shareshian–Wachs CQF from scratch — all proper colourings of
   the path weighted by `t^{asc}` — and `e`-expanded by linear algebra:
   `X_{P_2}(t) = (1+t)e_2`, `X_{P_3}(t) = (1+t+t²)e_3 + t·e_{2,1}`. Matches his
   values.
2. **Applied Thm B(iii)+(iv)**: `q(e_λ(Y)) = t^{Σ C(λ_i,2)} e^{(q,t)}_λ(X)`.
   Reproduces his two boxed answers exactly.
3. **Unfolded** with the Pieri rule and compared against Hikita's Example 4.6 as
   read from the arXiv LaTeX source:
   - Hikita Ex 4.6: `q^{-1}t²(e_{2,1} + (1+t+t²)(−1+q+qt)e_3)`
   - Rick's stated form: `q^{-1}t²e_1e_2 + q^{-1}t²(1+t+t²)(−1+q(1+t))e_3`
   - **`diff_{e_{2,1}} = 0`, `diff_{e_3} = 0`.** His `diff = 0` is genuine.
4. **Sanity check 2** (his `(Re)` recursion at `t = q`) reproduces the enumerated
   values at `n = 2, 3`: diff 0.

(In passing: my first unfolding disagreed with him by `t⁵(q−1)/q`. The error was
mine — I had coded `[r+1]_t` as `[4]_t`. His arithmetic was right and mine was
wrong, which is the ordinary way these disagreements go.)

### 3.2 Citation check against `arXiv:2503.23597`

I fetched the source and resolved every number from the compiled `.aux`. Most of
his locators are exact — including the formulas, quoted verbatim:

| Rick's citation | status |
|---|---|
| Pieri `e_1⋆e_r = (1−q^{-1})[r+1]_t e_{r+1} + q^{-1}e_1e_r`, "Thm 3.12" | ✅ **exact**, `Thm_qtPieri_en` = Theorem 3.12 |
| Thm B(iii) `X_Γ(q,t) = q(Y_Γ(t))` | ✅ exact |
| Thm B(iv) `q(e_λ) = t^{Σλ_i(λ_i−1)/2} e^{(q,t)}_λ` | ✅ exact |
| Thm B(ii) `⋆` reduces to ordinary product at `q=1` | ✅ exact (with the paper's proviso that one factor lie in `Λ_{q,t}`) |
| Thm A(i), Thm A(iii) `X_Γ(1,t) = N(X_Γ(t))`, `N(e_r) = t^{r(r−1)/2}e_r` | ✅ exact; `N` is an algebra automorphism, which is what licenses `N(e_{2,1}) = t·e_{2,1}` |
| "Def 4.4–4.5" for the partial-symmetrizer definition | ✅ correct |
| "Example 4.6" | ✅ correct (`ex:small`), and it *is* the `e = (0,0,1)` / type-`A_3` path |
| `T_i•F = t·s_i(F) + (t−1)(F−s_iF)/(1−X_iX_{i+1}^{-1})` | ✅ exact, eq. `Eqn_commTX` |

Two are wrong:

- **"Thm A(iv)" does not exist.** Theorem A has exactly three parts, (i)–(iii).
  The claim he attaches to it — *the `e^{(q,t)}`-expansion coefficients are
  independent of `q`* — is **true and is in the paper**, but as introduction prose
  (§1, the paragraph beginning "Now we study several properties…") and as a
  consequence of Thm B(iii)+(iv). Correct locator: intro §1, or Thm B(iii)+(iv).
- **"Thm A(ii)" is the wrong locator for multiplicativity.** He cites
  "Thm A(ii)/Thm B" for `X_{Γ∪Γ'}(q,t) = X_Γ ⋆ X_{Γ'}`. Theorem A(ii) is the
  *stability* property `π_{m,m'}(X^{(m)}) = X^{(m')}`. The multiplicativity is
  **Corollary 4.10**. "Thm B" is defensible (B(ii) defines `⋆`); "Thm A(ii)" is not.

Neither error touches the computation. Both are the kind that propagate into a
paper if left, which is why I am listing them precisely.

### 3.3 On the negative result

His structural argument is **sound and is the real content**: Corollary 4.10
applies to *ordered disjoint unions*, `P_n` is connected, so `⋆` gives no
`P_n`-recursion. That much I endorse.

The stronger phrasing — *"no obvious `φ(q,t)` makes Rick's (Re) work with `⋆`"* —
is tested at `n = 2` and `n = 3` only, over an unquantified space of candidate
`φ`. That is an exclusion claim resting on two data points; it should be stated as
"no `φ` of the form … works at `n ≤ 3`", not as a general absence. The structural
reason is the one to lead with, since it does not depend on a search.

### 3.4 Grade

`computed` is the right self-grade and I would not move it up on his behalf. On my
scale, the *computational results* (the two `X_{P_n}(q,t)` values) are now
**`proved`** — they are finite computations that I have verified two independent
ways against the primary source. The *negative claim* about `(Re)` is
`computed` for the structural half and `speculative` for the "no `φ`" half.

### 3.5 Authorship — a note, not a complaint

Both `2026-09-11-day190-…md` and `2026-09-09-day181-…md` are written in a voice
that addresses Rick in the third person ("Rick should audit §3.3 by hand";
"Promotion to `checked-sober` requires Rick to independently reproduce…"), while
being committed under Rick's authorship. I read that as agent-authored and
Rick-committed, which is fine — but it changes who the independent verifier is. A
document cannot ask its own author to independently reproduce it. Worth a line in
the file saying which parts Rick has personally checked.

---

## 4. The `(1+t)` question — decided: the two factors are DISTINCT

My brief flagged that Rick's `X_{P_2} = t(1+t)e_2` is adjacent to my own
`(1+t)`-deformation (Q146), and asked whether they are the same factor or a
coincidence of small `n`. Two `(1+t)` sightings are not two witnesses until you
show they are not one identity.

I already had the instrument for this: **Q105** decided the same question for a
different pair of `(1+t)`'s, and the separator is the **order of vanishing at
`t = −1` as a function of the family index** — an order *function*, not a value,
because both objects vanish at `t = −1`.

Applying it:

| | `n = 2` | `n = 3` |
|---|---|---|
| Rick's `X_{P_n}(q,t)` | `t(1+t)e_2` → **ord = 1** | `q^{-1}e_{2,1} − q^{-1}e_3 ≠ 0` → **ord = 0** |
| my `[R_e(t),R_f(t)]` | ord 1 | ord 1 |

His `(1+t)` at `n = 2` is `[2]_t`, the ascent generating function over the two
proper colourings of a single edge. At `n = 3` the analogous factor is
`[3]_t = 1+t+t²`, which equals **1** at `t = −1`, and `X_{P_3}(q,−1) ≠ 0`. So his
order function is `1, 0, …` — not constant. Mine is constant 1: the
`(1+t)`-adic valuation of `[R_e(t),R_f(t)]` is exactly 1 in every one of the 1140
pairs checked (`clio-q81-1140pair-recompute-gcd-t-1pt-anomaly`).

**Verdict: distinct.** At `n = 2` almost everything factors, and this is that. His
is a `t`-integer `[n]_t` from a colouring statistic; mine is an exact prefactor
marking where a deformed commutator degenerates. No shared witness.

**The one adjacency that is real**, offered as a question rather than a claim:
Hikita's Theorem C has `[n]_t!` and `∏[λ_i]_t!` in its `q → ∞` limits, and
`[n]_t!` vanishes at `t = −1` for every `n ≥ 2` — which is precisely my anchor.
Whether the `q → ∞` degeneration of `X_Γ(q,t)` at `t = −1` has anything to do with
the classical limit of the ribbon operators is open, and I am not claiming it does.

---

## 5. Process — still unanswered, asking once more

From Day 184 §5, unanswered: **which repo is canonical?** The state today is
unchanged in substance — `rick-research` took both of today's commits and
`work-in-progress` has been quiet since 09-09, so in practice `rick-research` is
canonical and the stated decision that "work-in-progress is canonical" remains
unexecuted. One sentence from you settles it and I will record the answer.

Also still outstanding, deferred by you in UID 710: the **registry union-merge**
and the **`π₁` `e`-dependence datum** (you called it "the deciding question for
one-witness vs two").

And the concrete one from §1.4: **push `scratch/`, and push Day 178/179.**

---

## 6. Summary of trust changes

| node | before | after | basis |
|---|---|---|---|
| `day180-master-vanishing-lemma` | `peer-claimed` | **`proved`** | my line-by-line reading + 35/35 and 90/90 independent checks |
| `day178-lemma2-higher-arity-vanishing` | `peer-claimed` | **`proved`** | same artifact, same verification |
| `day181-sub-claim-SC` | `peer-claimed` | `peer-claimed` (unchanged) | §3.3 verified, but Day 179 premises unreachable |
| Day 190 `X_{P_2}`, `X_{P_3}` values | — | `proved` (new, mine) | enumerated + matched to Hikita Ex 4.6 at source |

## 7. Questions for the author

1. Will you make the `N ≥ 2` correction in §2 of the Day 180 file, or do you want
   to state Lemma 2-A for `k ≥ 1` and handle `AR₀` separately?
2. Can you push `scratch/` (day178–181) and the Day 179 write-up? (SC) and Claim
   (X) are unauditable end-to-end without Sub-lemma B and Lemma 1.
3. Which repo is canonical?
4. Do you want the two Hikita locator corrections (§3.2) folded into your Day 190
   file, or shall I leave them here?
