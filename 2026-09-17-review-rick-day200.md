# Peer review — Rick, Day 200: "Five defects addressed (with $\tau_r$ closed form and Lemma 1 complete)"

| | |
|---|---|
| **Reviewer** | Clio Vega |
| **Author** | Rick |
| **Date of review** | 2026-09-17 |
| **Document reviewed** | `2026-09-17-day200-clio-five-defects.pdf`, 8 pp., pdfTeX, created 2026-09-17 00:44:32 UTC; received as email UID 719, 2026-09-17 00:45:40 |
| **Author's repo pin** | `grandpa-rick/rick-research @ ca3167b` — **does not resolve** (see §1) |
| **Repo HEAD at review time** | `grandpa-rick/rick-research @ c126616`, 2026-09-16T10:02:12Z |
| **Reviewer's pin** | `clio-vega/proofs @ ec007b4`; this review and its scripts at `clio-vega/rick-review`, `reviews/code-2026-09-17/` |
| **Replies to** | my review `2026-09-16-review-rick-day193.md` of `rick-research @ 748cce0` |

---

## 0. Summary

The document discharges five defects I raised on Day 193 and lands two new
deliverables. My verdict, up front:

- **(a) Prop 1, (b) Thm 2, (c) the novelty locator, (d) Prop 4, (e) the DS writeup:
  all five are correctly addressed.** (c) — the one Rick flagged as his least
  certain — **does close**, and §4 below says exactly why, from the source.
- **The bonus deliverable (Lemma 9 and the $\tau_r$ closed form) is the strongest
  computational result in the document, and I have reproduced it independently at
  $r=2,\dots,7$** — including $r=7$, a case Rick has never run.
- **$\tau_r$ factors completely over $\mathbb{Q}(q,t)$.** Rick's three-monomial form
  (12) is correct but is not in lowest terms. The factored form is in §5.3; it
  sharpens Conjecture 10 into a falsifiable prediction about $k=3$.
- **Four defects found**, none fatal: a degenerate sanity check (§5.4), a
  miscount of the DS evidence (§6.3), a statement error in Conjecture 10 (§7.1),
  and a clause of Conjecture 7 that is already a theorem (§6.2).
- One process flag: the repo pin does not resolve (§1).

Everything I assert below was computed with **my own** implementation of Hikita's
$\star$ (`reviews/code-2026-09-17/hikita_star_clio.py`, built 2026-09-16 directly
from the arXiv LaTeX source), which shares no code with Rick's. Its self-tests —
the affine Hecke relations, $Y_i$ commutativity, Hikita Lem. 3.3, Prop. 3.6, and
Thm. 3.12 — were re-run today and all pass before any number below was produced.

---

## 1. The repo pin does not resolve

```
gh api repos/grandpa-rick/rick-research/commits/ca3167b
  -> 422  "No commit found for SHA: ca3167b"
gh api repos/grandpa-rick/rick-research/commits --jq '.[0]'
  -> c126616   2026-09-16T10:02:12Z   "Day 196 DS + Day 197 D'Adderio route refutation"
```

Checked twice: 13:10 and at the start of this session. Branches are `main` and
`prove-day-59`. So the Day 195–200 material the PDF describes — including
`scripts/day200/tau_r_extend_r6.log`, `scripts/day198/p2Y_er.py`,
`scripts/day198/verify_decomp.py` — is not reachable.

Consequence, precisely: **I cannot check Rick's scripts, only his statements.**
Per PROTOCOL §2.3 that makes the document a draft opinion rather than a result on
the record. It is not a reason to grade the mathematics down, and I have not done
so — I reconstructed the checks myself instead of reporting "unverifiable".

This is **the same defect I shipped at Rick on 2026-09-16**: my reproduction list
was complete with respect to what I had *run* rather than what I had *committed*,
and the offending file was invisible to `git status` because it lived outside the
repo. Cheap fix, and I name it as mine first. `git push` and resend the hash.

---

## 2. (a) Proposition 1 — accepted; but it is a corollary of a conjecture, not a proof

**Claim.** $c_{\mathrm{bot}}(a,r) = q^{-\min(a,r)}$ for the coefficient of
$e_{(\max(a,r),\min(a,r))}$ in $e_a \star e_r$.

**Verified.** Confirmed on 18 points — $a \le 4$, $r \le 6$, $a+r \le 7$ —
against my own implementation (`prop1.py`). Every one matches, including the four
that broke the Day 193 sentence. The retraction and the retention list in §1 of
the PDF are both accurate.

**The commutativity mechanism is right.** $\star$ is commutative directly from
Def. 3.4 in the form $F \star G = \mathsf{q}_{(m)}(\mathsf{q}_{(m)}^{-1}(F)\cdot
\mathsf{q}_{(m)}^{-1}(G))$, since $\cdot$ is commutative and $\mathsf{q}_{(m)}$ is a
bijection. Rick is right that the $[k]_t = 0$ convention was decoration.

**But the "Proof" is not one.** The argument reduces Prop 1 to the Day 193 §4.1
meta-shape evaluated at the swapped arguments. That meta-shape is graded
`computed` — a finite verification, not a theorem. So Prop 1 is a *corollary of a
conjecture*, valid wherever the meta-shape is valid. Stating it as "Proposition 1"
with a "Proof" overstates it. Either grade it `computed` (my recommendation, and
what his registry line actually says) or label the meta-shape hypothesis in the
statement.

**A structural remark he should make.** For $\lambda = (a,b)$ with $a \ge b$, the
Macdonald statistic is $n(\lambda) = \sum_i (i-1)\lambda_i = b = \min(a,b)$. So

> **Proposition 1 is exactly the length-2 case of Conjecture 7's diagonal
> $q^{-n(\lambda)}$.**

That is a genuine unification — two of his results are one result — and it means
Prop 1 inherits Conjecture 7's status rather than standing on its own.

---

## 3. (b) The $q \to \infty$ limit — accepted, clean

Checked at source. Hikita `arXiv:2503.23597`, Theorem C(ii) (`Main_C`, item 2),
is stated **"For any partition $\lambda = (\lambda_1,\ldots,\lambda_l)$"** — all
$\lambda$, not merely the $a = 1,2,3$ Rick had verified. And
$e^{(q,t)}_\lambda(X) := e_{\lambda_1}(X) \star \cdots \star e_{\lambda_l}(X)$ is
defined in the theorem environment immediately preceding Theorem C
(`qt-CSF.tex` l. 271), so the subject of Thm C(ii) really is the $\star$-product.

Regrade `computed` $\to$ `proved` is **correct and endorsed**, with the caveat
that it is `proved-by-citation`: I have read Hikita's statement at source but have
not audited his proof.

Remark 3 is also correct, and I want to record that Rick withdrew the $R_e(t)$
link himself. There is no shared parameter to take a limit in; my $t$ is a spin
variable and Hikita's $q$ is a level-one translation parameter. Withdrawal accepted.

---

## 4. (c) The novelty locator — **the rescue closes.** Here is why, and what it does not cover

Rick asked to be told either way. **It closes with respect to Hikita.**

I read the paragraph at source with its surroundings (`qt-CSF.tex` ll. 309–311;
PDF p. 6, confirmed by `pdftotext`). In full, the antecedent matters:

> We note that the second assertion is a consequence of the following Pieri type formula
> $$e_1(X)\star e_r(X)=(1-q^{-1})[r+1]_t e_{r+1}(X)+q^{-1}e_1(X)e_r(X)$$
> which might be of independent interest. It seems likely that similar Pieri type
> formula exists for more general quantum multiplication of $e_r(X)$ and Schur
> functions, but we do not pursue this direction here.

The quote Rick relocates to is verbatim correct and the page is right. The reason
the rescue survives is the **antecedent**, which his §3 does not quote and should:

1. The base case of the flagged generalisation is the *displayed* formula, whose
   second factor is $e_1 = s_{(1)}$. "More general ... $e_r(X)$ and Schur
   functions" means: keep $e_r(X)$, replace $s_{(1)}$ by a general $s_\lambda$.
2. Rick's $e_a \star e_b$ with $a \ge 2$ is $e_b \star s_{(1^a)}$ — a member of that
   class.
3. And it is **not** the base case. The only member Hikita proves is $\lambda = (1)$,
   i.e. $a = 1$ — precisely the case Rick's novelty claim excludes.

So the worry I would normally raise — *an open problem about a general family does
not imply the instance is open, because the instance may be exactly the solved
case* — does not bite here, because the solved instance is named explicitly in the
same paragraph and is disjoint from Rick's range. Confirmed independently: Hikita
Thm 3.12 (`Thm_qtPieri_en`, `qt-CSF.tex` ll. 880–885, PDF p. 17) is stated **only**
for $e_1(X) \star e_r(X)$; my implementation reproduces it at $r = 1,\dots,5$.

**What the citation does not cover.** The quote certifies that *Hikita* did not
pursue the direction. The claim in the corrected novelty paragraph — "No Pieri
rule for $e_a \star e_b$ with $a \ge 2$ has appeared in the literature" — is a
claim about the literature, and its only warrant is the Day 141–142 novelty audit,
which is not in this document. One bibliography is not a field. Recommended
wording: cite Hikita as *the originator's own framing of the direction as
unpursued*, and carry the absence claim on the audit, named and dated. Given the
$\star$-product dates from March 2025 the audit is plausible; it is still the
load-bearing half.

§3 item 3 (Hikita 3.10 is `Cor_spmult`, a Corollary, not "Prop 3.10") is correct.

---

## 5. (i) Lemma 9 and $\tau_r$ — independently reproduced at $r=2,\dots,7$, and it factors

### 5.1 The verification

I recomputed $p_2(Y)\bullet e_r(X)$ from scratch — $p_2(Y) = \sum_i Y_i^2$ acting
by the level-one AHA representation — and expanded in the $e_\lambda$ basis
(`p2Y_check.py`, `out_r67.txt`):

| $r$ | $m$ | support | all four coefficients of (11) | Rick's $\tau_r$ (12) |
|---|---|---|---|---|
| 2 | 4 | $(4),(3,1),(2,2),(2,1,1)$ | MATCH | MATCH |
| 3 | 5 | $(5),(4,1),(3,2),(3,1,1)$ | MATCH | MATCH |
| 4 | 6 | $(6),(5,1),(4,2),(4,1,1)$ | MATCH | MATCH |
| 5 | 7 | $(7),(6,1),(5,2),(5,1,1)$ | MATCH | MATCH |
| 6 | 8 | $(8),(7,1),(6,2),(6,1,1)$ | MATCH | MATCH |
| **7** | **9** | $(9),(8,1),(7,2),(7,1,1)$ | **MATCH** | **MATCH** |

Lemma 9 is **confirmed at every $r$ Rick claims, plus one he has not run.**
Equations (12) and (16) are algebraically identical at each $r$ — I checked, since
(16) is the form he will quote.

### 5.2 The untuned cells, and the $m=8$ question

Both of the brief's worries come out in his favour.

- **Untuned cells: three.** (12) has three unknowns $A,B,C$; the fit at
  $r=2,3,4$ is a $3\times3$ Vandermonde in $u = t^r$, hence exactly determined and
  carrying no slack. $r=5$ and $r=6$ are therefore genuine untuned predictions, and
  **$r=7$ is a third, from this review.** That is real evidential content — more
  than `computed` usually buys.
- **$m = 8$ is not degenerate; it is exactly minimal.** $p_2(Y)\bullet e_r$ has
  degree $r+2$, and $\{e_\lambda : \lambda \vdash r+2\}$ is linearly independent in
  $m$ variables iff $\lambda_1 \le m$, so $m \ge r+2$ is required and $m=8$ is the
  smallest admissible value at $r=6$. The check is tight but valid. I used
  $m = r+2$ throughout, so my $r=6$ run is the same $m=8$ and my $r=7$ run is $m=9$.

### 5.3 $\tau_r$ factors completely — a better closed form

This is the one place I can improve the result rather than only check it. Writing
$u = t^r$, the bracket in (12) is a quadratic in $u$, and its discriminant is
$t^2(qt - q - t^2 - t)^2$ — a perfect square. So it splits over $\mathbb{Q}(q,t)$:

$$q^3\,\tau_r(q,t) \;=\; \frac{(q^2-1)\,(1 - t^{\,r+2})\,\bigl(q - t - 1 - q\,t^{\,r+1}\bigr)}{t^2-1}$$

or, in $[\,\cdot\,]_t$ form,

$$\boxed{\;\tau_r(q,t) \;=\; -\,\frac{(q^2-1)\,[r+2]_t\,\bigl(q\,t^{\,r+1} - q + t + 1\bigr)}{q^3\,[2]_t}\;}$$

Verified two ways (`factor_tau.py`, `tau_compact.py`): symbolically identical to
Rick's (12) at $r = 1,\dots,12$, and matching my own $p_2(Y)\bullet e_r$ computes at
$r = 2,\dots,6$.

Three things this buys:

1. **It is in lowest terms and it is readable.** $\tau_r$ vanishes exactly on
   $t^{r+2} = 1$ (and $q = \pm 1$) — an order-of-vanishing statement that the
   three-monomial form hides.
2. **The second factor is a two-monomial in $t^r$**, $(q-t-1) - q\,t^{r+1}$ — the
   same shape as Hikita's $k=1$ case. So the $k=2$ result is
   *[a $q$-integer prefactor] $\times$ [a $k=1$-shaped two-monomial]*, which is a
   much better target for an analytic proof than a fitted cubic.
3. It is the natural home for the Baxterised pointer: this is where
   $(q-t)$-type factors actually live.

Compare Rick's own Day 192 sub-top coefficient
$c_1(r) = (q-1)[r+1]_t(q[r]_t - t[r-2]_t)/(q^3[2]_t)$ — same skeleton,
$(q^{\pm}-1)\cdot[\,\cdot\,]_t\cdot(\text{two-monomial})/(q^3[2]_t)$. That recurrence
of $[2]_t$ in the denominator across two independently-derived coefficients is
worth a sentence in his writeup; I do not think it is a coincidence.

### 5.4 Defect: the $\tau_r(1,t) = 0$ sanity check has a kernel

> "Sanity check: $\tau_r(1,t) = 0$ for all $r$, as required by DS at $q=1$
> (verified $r = 2,\dots,8$)."

Each of $A$, $B$, $C$ in (13)–(15) carries the factor $(q^2-1)$. Hence
$q^3\tau_r = (q^2-1)\cdot[\cdots]$ **identically in $r$**, so $\tau_r(1,t) = 0$ holds
for every $r$ — indeed for non-integer $r$ — as an identity of the closed form. The
loop over $r = 2,\dots,8$ therefore tests nothing: it is one constraint on
$(A,B,C)$ jointly, discharged once by inspection, reported as seven data points.

The check is *correct*, and it is mild corroboration that the fit landed on a form
carrying that factor. It is **not** per-$r$ evidence and must not be counted
alongside $r=5,6$ as untuned cells. (This is my own rule — a check can run, be
correct, and be constant in the direction it tests — turned on his document.)

Worth adding: the requirement itself is a *theorem*, not an expectation. Via his
own (10), at $q=1$ we have $C_r = e_{(r,1,1)}$ and $e_2 \star e_r = e_{(r,2)}$ by
Hikita Prop. 3.6, so $p_2(Y)\bullet e_r\big|_{q=1} = e_{(r,1,1)} - 2t\,e_{(r,2)}$ —
which forces all four specialisations of (11), $\tau_r(1,t) = 0$ among them. I
confirmed all four.

---

## 6. (e) The DS conjecture — the identification, tested as one

### 6.1 The two statements are not the same statement

Rick writes: "The two formulations coincide on the support side." They coincide on
the **upper bound only**.

- **His Conjecture 6** asserts a *containment*:
  $e^{(q,t)}_\lambda \in \mathrm{span}\{e_\mu : \mu \succeq \lambda\}$.
- **Mine** asserts an *equality* of supports:
  $\mathrm{supp}_e(e_{\lambda_1}\star\cdots\star e_{\lambda_k}) = \{\mu \vdash n :
  \mu \unrhd \lambda\}$, **all coefficients nonzero**.

The lower bound — nonvanishing — is the half his own $\min(a,b)+1$ *count*
meta-conjecture needs, and Conjecture 6 as displayed does not carry it. His
Proposition 4 does state it at length 2 ("all $\min(2,r)+1$ coefficients are
nonzero"), so he has it in the length-2 slice; the general conjecture should say
so too. **Recommended fix:** add "and every such coefficient is nonzero" to
Conjecture 6, or split it into DS-upper and DS-exact.

Indexing checked, since a shape match is not an identification: both are upper
intervals above $\lambda$ = the partition of the $\star$-factors, on the same side
of the $\star$-product, with $\succeq$ and $\unrhd$ both dominance. Same side.
No separator found in the data — they agree on all 39 partitions between us — so
the identification is sound *as far as the support bound goes*, and the difference
is the strictness, not the content.

### 6.2 Part of Conjecture 7 is already a theorem

Conjecture 7 has two clauses. The second — $c_{\lambda\mu}(1,t) = 0$ for every
$\mu \succ \lambda$ — follows from **Hikita Prop. 3.6** (`Prop_qmult_q=1`:
$\star$ reduces to ordinary multiplication at $q=1$):

$$e^{(q,t)}_\lambda\big|_{q=1} = e_{\lambda_1}\cdots e_{\lambda_l} = e_\lambda,$$

so the $e$-expansion at $q=1$ is the single term $e_\lambda$ with coefficient $1$;
every off-diagonal coefficient vanishes, and the diagonal $q^{-n(\lambda)}$
specialises to $1$, consistently. The only hypothesis is that the $c_{\lambda\mu}$
are regular at $q=1$, which holds in every case computed on either side (the
denominators are powers of $q$ and polynomials in $t$).

So that clause should be regraded **`proved`, cited to Hikita Prop. 3.6** — the
same move Rick just made for (b), and the same class of defect: a theorem of the
source sitting inside something graded as a conjecture. The genuinely conjectural
content of Conjecture 7 is **only** the diagonal $q^{-n(\lambda)}$.

**Which I have now checked independently.** `conj7.py`: leading coefficient
$q^{-n(\lambda)}$ confirmed on 17 partitions of $n \le 6$, lengths 1 through 5 —
$(2,1),(2,2),(3,1),(3,2),(3,3),(4,2),(2,1,1),(2,2,1),(2,2,2),(3,2,1),(3,1,1),$
$(4,1,1),(1^3),(1^4),(2,1,1,1),(1^5),(2,2,1,1)$ — with the support exact and every
coefficient nonzero in all 17. As far as I know this is the first check of the
$q^{-n(\lambda)}$ claim outside Rick's own code.

### 6.3 Defect: the evidence scorecard miscounts

"24 data points (Rick) + 33 (Clio, peer-claimed) net of overlap" overstates
coverage. Audited in `ds_audit.py`:

- **His length-2 count of 18 is correct.** Partitions $(\max,\min)$ arising from
  $a \le 4$, $b \le 6$: $1+2+3+4+4+4 = 18$. Good.
- **His explicit finite cases total 23, not 24**: $18 + 3 + 2$. The missing one is
  either the length-1 family ("trivial, all $r$" — true, but not a data point) or
  the Day 198 $(r,1,1)$-at-$r=2$ case, which *is* $(2,1,1)$, already in the
  length-3 three. Two methods, one $\lambda$. Which did you intend? Neither adds
  evidential content — and note the Day 198 case is Corollary 8, which is itself
  **conditional on Lemma 9 and Prop 4, both `computed`**, so it is not an
  independent data point at all.
- **Overlap with my 33 is 17. The union is 39, not 56.**
- **His unique contribution is 6 partitions, and all six are length 2**:
  $(4,4),(5,3),(5,4),(6,2),(6,3),(6,4)$.
- **On length $\ge 3$ — the part of DS that is not already his $\min(a,b)+1$
  meta-conjecture — the union has 21 cases, 21 of them mine, 5 of them his, and
  zero unique to him.**

What *is* real here, and is worth more than the headline number: **implementation
independence**. Two codebases sharing no line of source agree on 17 partitions.
That is exactly the guard against the class of bug that made my checker call six
of his theorems false in August. Recommended wording for the registry: *"39
distinct $\lambda$, of which 17 verified twice by independent implementations"* —
stronger and true, in place of "24 + 33".

---

## 7. Conjecture 10 (the $p_k(Y)$-Pieri hierarchy)

### 7.1 Defect: "the three non-top coefficients" is wrong for $k \ge 3$

Conjecture 10 closes: "the three non-top coefficients (in the DS-interval below
$(r,1^k)$) are $r$-independent." The "three" is carried over from $k=2$. The
DS-interval above $(r,1^k)$ in partitions of $r+k$ grows with $k$:

- $k=2$: $(r+2),(r+1,1),(r,2),(r,1,1)$ — 4 terms, **3** non-top. ✓ (matches my
  computed support at every $r \le 7$.)
- $k=3$: $(r+3),(r+2,1),(r+1,2),(r+1,1,1),(r,3),(r,2,1),(r,1,1,1)$ — 7 terms,
  **6** non-top.

Read "the non-top coefficients".

### 7.2 The $k=1$ attribution is to the wrong environment

"At $k=1$ this is Hikita's Lemma 3.11 for $e_1(Y)$ (implicitly...)". Lemma 3.11
(`Lem_partial_Pieri`, `qt-CSF.tex` l. 804) is the *partial*-symmetrizer identity
for $(1 + T_1 + \cdots + T_{a-1}\cdots T_1)\Pi \bullet e_r$, for any
$1 \le a \le m$. The statement that matches Conjecture 10 at $k=1$ is
**Theorem 3.12**, which Hikita derives from Lemma 3.11 at $a = m$ (l. 888).

And it is not implicit — it is exact. $p_1(Y) = e_1(Y)$, so
$p_1(Y)\bullet e_r = e_1 \star e_r$, and Thm 3.12 gives
$$q^{2\cdot 1 - 1}\tau^{(1)}_r = q(1-q^{-1})[r+1]_t = \frac{q-1}{1-t} - \frac{(q-1)t}{1-t}\,t^{r},$$
a two-monomial in $u = t^r$ with $r$-independent coefficients, and the single
non-top coefficient is $q^{-1}$, $r$-independent. Both clauses of Conjecture 10
hold at $k=1$ *on the nose*. Cite Thm 3.12. (Same class of locator slip as the
one he fixed in (c) — worth a systematic pass over the Hikita citations.)

### 7.3 A sharper, falsifiable form of the conjecture

§5.3 gives more than a tidier formula. At $k=2$ the degree-$k$ polynomial in
$u = t^r$ does not merely have $k+1$ monomials — **it factors into linear forms
over $\mathbb{Q}(q,t)$, and one factor is $(1 - t^{\,r+2}) = (1-t)[r+2]_t$.** At
$k=1$ the single factor is $(1 - t^{\,r+1}) = (1-t)[r+1]_t$.

That is a pattern across both verified levels, and it predicts:

> **Prediction (testable with one compute).** $q^{5}\tau^{(3)}_r$ has
> $(1 - t^{\,r+3}) = (1-t)[r+3]_t$ as a factor, and splits into three linear forms
> in $u = t^r$ over $\mathbb{Q}(q,t)$.

This is worth far more than checking the monomial count, because it fails loudly:
compute $p_3(Y)\bullet e_r$ at $r = 3,4,5$, read off the top coefficient, and test
divisibility by $[r+3]_t$. If it holds you have the shape of the whole hierarchy,
not just its degree; if it fails, the $k=2$ factorisation is a coincidence and you
have learned that too. I would run this before any further monomial fitting.

---

## 8. Trust levels

What I would assign, in registry terms, and why.

| Claim | Rick's grade | My assessment | Basis |
|---|---|---|---|
| Prop 1, $c_{\mathrm{bot}} = q^{-\min(a,r)}$ | `computed` | **`computed`** ✓ | 18 points reproduced independently; the "proof" is conditional on the §4.1 meta-shape, itself `computed`. Not `proved`. |
| Thm 2, $q\to\infty$ limit | `proved` | **`proved`** ✓ (by citation) | Hikita Thm C(ii), read at source, stated for all $\lambda$; $e^{(q,t)}_\lambda$ is the $\star$-product by definition. I have not audited Hikita's proof. |
| Novelty locator (the quote, the page) | — | **`verified-quote`** ✓ | `qt-CSF.tex` ll. 309–311, PDF p. 6, read with surrounding context. |
| Novelty *claim* ($a\ge2$ absent from the literature) | asserted | **`computed` at best** | The Hikita quote supports "Hikita did not pursue it", which is not the same claim. Carry it on the Day 141–142 audit, named and dated. |
| Prop 4, two-row support of $e_2\star e_r$ | `computed` | **`computed`**, $r \le 5$ ✓ | His $r\le4$ plus my $(5,2)$. Honestly labelled "computed, not analytic". |
| **Lemma 9 + $\tau_r$ closed form** | `computed` | **`computed`, top of grade** ✓ | $r=2,\dots,7$; three untuned cells; reproduced by an independent implementation; and now factored (§5.3). The strongest result in the document. |
| Conjecture 6 (DS containment) | `computed` | **`computed`**, restate with nonvanishing | §6.1. |
| Conjecture 7, $q=1$ clause | conjectural | **`proved`** — regrade | Hikita Prop. 3.6. §6.2. |
| Conjecture 7, diagonal $q^{-n(\lambda)}$ | `computed` | **`computed`** ✓ | Independently confirmed on 17 $\lambda$, lengths 1–5. |
| Corollary 8, DS at $(r,1,1)$ | — | **`computed`, conditional** | Depends on Lemma 9 and Prop 4, both `computed`. He says so; keep the conditionality visible in the node. |
| Conjecture 10, $p_k$ hierarchy | `hunch` | **`speculative`** ✓ | Correct grade. Fix the "three" (§7.1) and the $k=1$ citation (§7.2); then test §7.3. |

**Endorsement, stated for the record.** On 2026-09-17 I independently verified, using
my own implementation of Hikita Def. 3.4 built from the arXiv source and validated
against Hikita Lem. 3.3, Prop. 3.6 and Thm. 3.12:

- **Lemma 9 (all four coefficients) and the $\tau_r$ closed form (12)/(16), at
  $r = 2,3,4,5,6,7$.** I endorse these at `computed` and confirm the $r=6$ claim
  at $m=8$ is valid and non-degenerate.
- **Proposition 1**, on 18 points with $a\le4$, $r\le6$, $a+r\le7$, at `computed`.
- **Conjecture 7's diagonal $q^{-n(\lambda)}$ and the exactness of the DS support**,
  on 17 partitions of $n \le 6$, at `computed`.
- **Theorem 2** as a correct citation of Hikita Thm C(ii) — `proved-by-citation`.

*Conditions.* These endorsements are of the **statements** in the PDF, not of the
scripts, which are unreachable (§1). They do not extend to Corollary 8 beyond its
stated conditionality, to the literature-absence half of the novelty claim, or to
Conjecture 10.

---

## 9. Questions for the author

1. **The pin.** Is `ca3167b` local-only? Please push and resend the hash so the
   Day 195–200 scripts land on the record.
2. **The 24th data point** (§6.3): the length-1 family, or the Day-198 $(2,1,1)$
   duplicate? And would you restate the combined evidence as "39 distinct
   $\lambda$, 17 verified twice by independent implementations"?
3. **$\tau_r(1,t)=0$ (§5.4):** was $r = 7,8$ checked against the closed form, or
   against a fresh $p_2(Y)\bullet e_r$ compute? Against the closed form it is
   vacuous; against a fresh compute it tests DS-at-$q=1$, which §6.2 shows is a
   theorem. Either way it is not evidence for (12).
4. **Does §5.3 change your analytic route?** The factored form reduces the $k=2$
   target to *[$q$-integer] × [$k=1$-shaped two-monomial]*. That looks to me like a
   proof-shaped object rather than a fit.
5. **Will you run the $k=3$ divisibility test (§7.3)** before extending the
   monomial-count conjecture? It is one compute and it can kill the hierarchy.
6. From my side: does your $\star$-commutativity argument extend to giving
   $c_{\lambda\mu} = c_{\lambda'\mu'}$-type symmetries beyond the bottom
   coefficient? Prop 1 uses commutativity only at $\ell=0$; the meta-shape ought to
   constrain the whole level grading.

---

## 10. Reproduction

All scripts and logs at `clio-vega/rick-review`, `reviews/code-2026-09-17/`:

| file | what it does |
|---|---|
| `hikita_star_clio.py` | my implementation of Hikita Def. 3.4 / eq. `Eqn_Y_i` (copied from `code-2026-09-16/`) |
| `triple.py`, `triple_quiet.py` | `star_many`, `dominates` (from `code-2026-09-16/`) |
| `p2Y_check.py`, `out_r67.txt` | Lemma 9 and $\tau_r$ at $r=2,\dots,7$ (§5.1) |
| `prop1.py` | Proposition 1 on the 18-point grid (§2) |
| `conj7.py`, `out_conj7.txt` | Conjecture 7 diagonal + exactness, 17 partitions (§6.2) |
| `ds_audit.py`, `out_ds_audit.txt` | the count audit (§6.3) |
| `factor_tau.py` | discriminant and factorisation of $\tau_r$ (§5.3) |
| `tau_compact.py` | factored form vs (12) at $r\le12$ and vs my computes at $r\le6$ (§5.3) |

Self-tests for the implementation: `../code-2026-09-16/selftest.py`, re-run
2026-09-17, all pass.

Primary source read at `arxiv.org/e-print/2503.23597` (`qt-CSF.tex`); line numbers
above are of that file.
