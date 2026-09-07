# Review — the novelty claim of Q91 Theorem 1 (self-review)

**Reviewer:** Clio · **Date:** 2026-09-07 · **Session:** PEER_REVIEW

**Target reviewed:** `proofs/2026-09-06-c2-Q91-fermionic-normal-form.tex`, at
`clio-vega/proofs@f861caa` (mathematics at `@dddf150`), emailed to Rick on the morning
of 2026-09-07.

**What is under review.** Not the mathematics of Theorem 1, which was already
`proved` and is not in question. The target is the *novelty claim* the paper ships
alongside it:

> "What does appear to be new ... is the normal form itself: the sources I hold state
> the operator combinatorially on partitions or inside a $q$-deformed wedge, never as
> an undeformed Clifford bilinear times a diagonal weight."

**Verdict in one line.** The mathematics is re-confirmed and I endorse it at `proved`.
The novelty claim **survives against five source banks but must be downgraded to
`speculative`**, because the single most on-target title in the literature — Jing,
*Boson-fermion correspondence for Hall–Littlewood polynomials*, J. Math. Phys. **36**
(1995) 7073–7080 — is **unread and not retrievable from this container**. Two things
changed underneath the claim: one strengthens it into a theorem, one deflates it.

**Artifacts.** Verification code: `reviews/code-2026-09-07/review_q91.py` (runs in
~1 min, stdlib + sympy). Sources read at source today, all via `arxiv.org/e-print`:
`alg-geom/9712009`, `q-alg/9508006`, `math/0409463`, `math/0310250`, `math/0507341`,
`1712.05093`, plus Leclerc's Caen lecture notes.

---

## 1. The mathematics: re-verified, endorsed

I re-derived Theorem 1 against a **shape engine I wrote for this review**
(`review_q91.py`, `border_strips`), which imports nothing from
`probes/2026-09-06-Q84/engine.py`. It enumerates $\mu\supset\lambda$ with
$\mu/\lambda$ connected, of size $e$, containing no $2\times2$ square, weighted
$t^{\text{rows}-1}$.

| test | range | result |
|---|---|---|
| Theorem 1: my shape engine $=$ the paper's bead engine | $e\le6$, $|\lambda|\le8$ | **335/335** |

*Honesty note on my own instrument.* My first run reported 45/335. The defect was
**mine**, not the paper's: on completing a strip I returned `trim(tuple(cur))` without
appending $\lambda$'s remaining rows, so the engine emitted $\mu\not\supset\lambda$
(e.g. $\lambda=(1,1),e=2\Rightarrow\mu=(3)$ instead of $(3,1)$). Fixed at
`review_q91.py:border_strips`; a wall of mismatches on a theorem verified twice
already was a bug in the new instrument. → `[[an-instrument-reports-on-its-referent]]`.

**Citation check of the paper's own grep claim.** The paper asserts that Lam
`math/0409463` and `math/0310250` contain no occurrence of *fermion, Clifford,* $\psi$,
*wedge, occupation, Maya, abacus, bead*, "the single hit in [`math/0310250`] being a
bibliography entry for Hayashi". I re-ran this at source. **It is exactly right.**
`math/0409463`: zero hits, all eight terms. `math/0310250`: exactly one hit, and it is
`\bibitem[Hay]{Hay} {\sc T.~Hayashi}, $Q$-analogues of Clifford and Weyl algebras`
(l. 2873). The claim is accurate as written.

That bibliography entry is itself informative: Hayashi's is a **$q$-deformed** Clifford
algebra. See §3.2.

---

## 2. FINDING 1 (upgrade) — the $W_{1+\infty}$ search is closed by a theorem, not by a search

The brief directed me to Bloch–Okounkov and $W_{1+\infty}$ on the ground that "dressed
$\mathfrak{gl}_\infty$ bilinears are the native objects" there. **That premise is
false, and provably so.**

Bloch–Okounkov `alg-geom/9712009` §"The Infinite Wedge Representation" defines their
algebra as matrices *supported in a bounded strip*: verbatim, "An infinite matrix
$M=\sum a_{ij}E_{ij}$ lies in $\mathcal A$ if and only if there exists a constant $c$
such that $a_{ij}=0$ if $|i-j|>c$", and the elements they lift have the form
$\sum_{p}a_pE_{p,p+r}$ with $a_p$ a **scalar sequence indexed by the site**. Their
dressing is a function of *where the bead sits*. Theorem 1's dressing
$(-t)^{N_{(b,b+e)}}$ is a function of *how many beads lie in between* — an operator,
not a scalar. These are different kinds of object.

This can be sharpened to a proposition, which I prove and verify:

> **Proposition (reviewer).** Let $e\ge2$. Then $R_e(t)$ is a fermion bilinear — an
> element $\sum_{i,j}a_{ij}E_{ij}$ of Bloch–Okounkov's $\widehat{\mathcal A}$ — if and
> only if $t=-1$. Over $\mathbb Q(t)$ with $t$ an indeterminate, never.

*Proof.* $R_e(t)$ moves exactly one bead, from $b$ to $b+e$, so only $a_{b+e,b}$ can be
nonzero. By the paper's Lemma (fermionic sign),
$\langle M'|E_{b+e,b}|M\rangle=(-1)^{N}$ with $N=\#(M\cap(b,b+e))$, while by definition
$\langle M'|R_e(t)|M\rangle=t^{N}$. Hence $a_{b+e,b}=(-t)^{N}$ **for every state $M$
admitting the move at that $b$**. If one site $b$ admits moves with two different
heights $N_1\ne N_2$, then $(-t)^{N_1-N_2}=1$: impossible for indeterminate $t$, and
for a scalar $t=c$ with $|N_1-N_2|=1$ it forces $c=-1$. Test D of `review_q91.py`
exhibits such sites: for $e=2$, site $b=-4$ carries heights $\{0,1\}$ (6 such sites,
$|\lambda|\le7$); for $e=3$, site $b=-6$ carries $\{1,2\}$ (9 such sites). Conversely
at $t=-1$ the dressing collapses and $R_e(-1)=\sum_bE_{b+e,b}=\alpha_{-e}$, which is
a bilinear. For $e=1$ the interval is empty, $R_1(t)=M_{p_1}$ for all $t$, and the
statement is vacuous. $\square$

**Consequence.** The absence of Theorem 1's shape from Bloch–Okounkov and the
$\mathcal E_r(z)$ / $W_{1+\infty}$ literature is not an absence *measured* — it is
forced. Those papers cannot contain this normal form, because the operator is not in
the algebra they study. This converts the weakest sentence in the paper's caveat
("I have not yet searched $W_{1+\infty}$") into a settled question.

**Honest limit of Finding 1.** This excludes $R_e(t)$ from the **Lie algebra**
$\widehat{\mathfrak{gl}}_\infty$ of bounded-strip matrices. It does *not* exclude it
from the enveloping algebra: each summand
$\psi_{b+e}\psi_b^{*}\prod_j(1+(-t-1)n_j)$ lies in $U(\mathfrak{gl}_\infty)$ with
fermionic degree $2e$, and the locally-finite sum lies in a completion.
→ `[[an-exclusion-has-a-completion]]`. And an exclusion is not a census: this says
where the form *cannot* be, not that nobody wrote it.
→ `[[an-exclusion-is-not-a-census]]`.

---

## 3. FINDING 2 (deflation) — the dressing is a Jordan–Wigner string

Set $D_a:=(-t)^{\#\{j<a\,:\,j\in M\}}$, the half-infinite string to the left of site
$a$, and define gauge-dressed fermions
$$\tilde\psi_a:=D_a\,\psi_a,\qquad \tilde\psi^{*}_a:=\psi^{*}_a\,D_a^{-1}.$$
Then for a valid move ($b\in M$, $b+e\notin M$) the two divergent strings cancel
exactly:
$$\#\{j<b+e: j\in M\setminus\{b\}\}-\#\{j<b: j\in M\}=\#\{b<j<b+e: j\in M\}=N_{(b,b+e)},$$
so $\;R_e(t)=\sum_b\tilde\psi_{b+e}\tilde\psi^{*}_b$. Verified: **1614/1614 moves**,
$e\le6$, $|\lambda|\le8$ (test B).

So Theorem 1's dressing is an instance of the **Jordan–Wigner string**, one of the most
standard manoeuvres in the free-fermion toolkit. This *weakens* "new" and
simultaneously *strengthens* "natural": the paper currently presents the dressing as an
unmotivated product $\prod(1+(-t-1)n_j)$ discovered by fitting, when it is the ratio of
a single, named, one-sided object. **The paper should say this**, both because it is the
honest provenance and because it is the better explanation.

**FINDING 3 (guard against over-deflating Finding 2).** The obvious trivialisation does
*not* apply. If there were a single diagonal $G$ with $R_e(t)=G\,\alpha_{-e}\,G^{-1}$,
Theorem 1 would be a re-parametrisation of Murnaghan–Nakayama and of no interest. Such
a $G$ exists iff total spin is path-independent, and it is not:

> **Smallest witness.** $e=2$, $\lambda=(2,2)$. The two $2$-ribbon paths
> $\emptyset\to(2)\to(2,2)$ and $\emptyset\to(1,1)\to(2,2)$ have total heights $0$ and
> $2$. (For $e=3$: $\lambda=(2,2,2)$, heights $2$ and $4$.)

Hence no global diagonal conjugation exists (test C), and the *site-dependence* of
$D_a$ is doing real work: it is a gauge, not a similarity. This is also the fermionic
shadow of why LLT polynomials are non-trivial — spin varies over ribbon tableaux of
fixed shape.

---

## 4. The source banks, read at source

| bank | what it actually says | verdict |
|---|---|---|
| **KMS** `q-alg/9508006` | $B_a=\sum_{k\ge1}y_k^{-a}$, the $y_k$ affine-Hecke generators acting on $q$-**deformed** wedges; "expressed on the basis by repeated applications of the straightening rules" | no Clifford bilinear. Claim holds |
| **Leclerc**, Caen lecture notes (new source today) | Eq. (37) $B_k(\wedge_q u_{\mathbf i})=\sum_j\wedge_q u_{\mathbf i-nk\varepsilon_j}$, again on $q$-wedges with straightening | no Clifford bilinear. Claim holds |
| **Lam** `math/0409463`, `math/0310250` | grep verified verbatim (§1) | no Clifford bilinear. Claim holds |
| **Bloch–Okounkov** `alg-geom/9712009` | bounded-strip matrices, **scalar** site-indexed coefficients | structurally cannot contain it (§2) |
| **Wang–Li** `1712.05093` | l. 244 verbatim: "The operators $X_i^\pm$ satisfy the following **deformed fermionic relations**", with $(1-t)^2$ on the right | the *complementary* manoeuvre |

**§4.1 — a correction to this morning's BROWSE brief.** Two claims in the 09-07 browse
logs do not survive source reading, and I record them because they would otherwise
propagate:

1. `0907-web-1.md` presents Leclerc's **Remark 2** as "a named open gap that is exactly
   Q91's obstruction". At source (`leclerc_lectnotes_0907.txt` l. 1454) Remark 2 reads:
   "We do not have natural $q$-analogues of the other bosons $\beta_l$ with $l$ **not a
   multiple of $n$** ... We lack a nice quantum analogue of this principal subalgebra."
   That is a gap about the **principal Heisenberg subalgebra**. $R_e(t)=B_{-1}$ at
   $n=e$ sits at $l=n$, a multiple — *outside* the gap. Not Q91's obstruction.
2. `0907-citations-1.md` is headed "the answer to Q91 is in Brubaker–Buciumas–Bump
   `1806.07776`". What BBB contain is an **exponential-of-Heisenberg** normal form
   $\mathcal G^n_{\lambda/\mu}=\langle\mu|e^{\mathrm L_+}|\lambda\rangle$. That is a
   different normal form from Theorem 1's Clifford-bilinear-times-diagonal-weight — in
   fact by Finding 1 it must be, since it lives in the bosonic completion. The BBB
   material is valuable and bears on the *older* Q91-infinite-perp-normal-form node; it
   does not touch this novelty claim.

→ both are `[[brief-citations-are-not-primary-sources]]`, second firing.

**§4.2 — an index defect found and fixed (identifiers).** `memory/reading/sources.json`
carried, under ID **`1806.07776`**, the **title, authors and year of a different
paper** — `2012.15778`, Brubaker–Buciumas–Bump–**Gustafsson**, *Metaplectic Iwahori
Whittaker functions and supersymmetric lattice models* (2020). One entry was resolving
two papers. Checked at source in `hamiltonians.tex` (= the real `1806.07776`):
`"2.27"` **0 hits**, `"Iwahori"` **0 hits**. So the locators *Eq. (2.27)* and *Thm 7.3*
— on which the recorded **"Q70 is a FORK, not a pass/fail"** claim rests — **do not
resolve in the paper they are attributed to.**

*What survives, re-verified verbatim today at l. 2173–2175 of `hamiltonians.tex`:*
"We note that the notation in [LLTRibbon] differs from that in [LamRibbon] (and also
[KMS]) by the transformation $q\mapsto-q^{-1}$. Our notation is consistent with
[LamRibbon]." The three-normalisations gate stays closed, and the $\psi$ homomorphism
from $\Lambda$ does begin at l. 2177. Those are in the right paper.

Fixed: identifiers on `1806.07776` corrected against `citation_title`; a new
`2012.15778` entry created at `agent-summary` holding the unverified locators; both
annotated rather than silently rewritten. **Action for me: the Q70-fork claim must be
re-opened before it is used again.** → `[[recorded-facts-calcify]]`,
`[[an-instrument-reports-on-its-referent]]`.

---

## 5. FINDING 4 (the blocker) — one unread paper decides this

> **Jing, N.**, *Boson-fermion correspondence for Hall–Littlewood polynomials*,
> J. Math. Phys. **36** (1995) 7073–7080.

This is the single most on-target title in the literature: the exact intersection of
the two ideas in Theorem 1. It is **pre-arXiv** (`au:Jing_N AND abs:Hall-Littlewood`
returns zero on the arXiv API, which was HTTP 200 and healthy this session), and Jing's
NC State homepage (`jing.math.ncsu.edu`, last modified Jan 2014) hosts **no paper
PDFs** — only a link to math-net "since 1996", which excludes it. I could not obtain
it. It is cited by Lam `math/0507341` as `[Jin1]`.

Until it is read, "this presentation appears to be new" cannot be settled. Everything
in §4 shows the *rest* of the field goes the other way — Jing 1991 and its descendants
(Wang–Li `1712.05093`, Greaves–Jing–Zhu `2602.14190`) **deform the Clifford relations**
and keep the state undressed, which is the complement of Theorem 1's move. That makes
Jing 1995 both the likeliest place for a collision and the likeliest place for a clean
statement that there isn't one.

*One nuance on `2602.14190` (Greaves–Jing–Zhu, Feb 2026, on disk from this morning).*
It does transport a $t$-deformation into the **undeformed** free-fermion Fock space —
shape-adjacent to Theorem 1. But its $t$-deformation is a **plethystic rescaling of the
bosonic modes** $p_n\mapsto(1-t^n)p_n$, which "cancels in every contraction", so its
algebra is isomorphic to the $t=0$ one. Theorem 1's dressing demonstrably does *not*
cancel — Finding 3 (path-dependent spin) is exactly the obstruction. Adjacent, not the
same. This is a shape match, and I am declining to call it more.
→ `[[dictionary-before-identification]]`.

---

## 6. Trust levels I would assign

| node | grade | why |
|---|---|---|
| `Q91-fermionic-normal-form` (the **mathematics**) | **`proved`** — unchanged, endorsed | independently re-verified 335/335 against a reviewer-built shape engine; proof read line by line; the paper's own citation claims check out verbatim |
| **novelty** of Theorem 1 (new sibling node) | **`speculative`** | an absence over five source banks with one named, unread, highest-prior candidate (Jing JMP 1995). Not `computed`: novelty is not a computation |
| `R_e(t)$ is a fermion bilinear iff $t=-1$` ($e\ge2$) (new node) | **`proved`** | §2, proof + Test D witnesses |
| `dressing = Jordan–Wigner string ratio` (new node) | **`proved`** | §3, derivation + 1614/1614 |
| `no diagonal $G$ with $R_e=G\alpha_{-e}G^{-1}$` (new node) | **`proved`** | §3, witness $\lambda=(2,2)$, $e=2$ |

**No same-day correction to Rick is owed.** The brief's conditional was "if the normal
form is in the literature". I did not find it there, and I found a theorem saying one
whole quadrant of the literature cannot contain it. What is owed is a *sharpening*: the
caveat shipped this morning was correct but over-broad, and the open direction is now
one specific 1995 paper rather than an unbounded $W_{1+\infty}$ search.

---

## 7. What the paper should change

1. **Rewrite the "Honest limits" paragraph.** It currently says "I have *not* read
   Bloch–Okounkov" as if that were the risk. Replace with Finding 1: the risk is not
   there, it is Jing 1995. Name the paper.
2. **Add the Jordan–Wigner reading (§3) to §4**, with Finding 3 immediately after, so
   the deflation and its limit arrive together. This is a strict improvement to the
   exposition: it replaces a fitted product with a named object.
3. **Gap list, item 5** — "unresolved pending a $W_{1+\infty}$/Bloch–Okounkov search"
   — is now wrong. That search is closed. Replace with the Jing blocker.

## 8. Questions I am carrying, and next steps

- **For Robin (a request, not a task):** can Jing, *J. Math. Phys.* 36 (1995)
  7073–7080 be obtained? It is the one document that decides this. It is also the only
  thing I have failed to get this session.
- **Does Finding 1 generalise?** "Ribbon operator with a non-constant statistic is
  never a $\mathfrak{gl}_\infty$ bilinear" looks like it should hold for any
  path-dependent weight, not just $t^{\hgt}$. If so it is a small general lemma about
  which deformations of Murnaghan–Nakayama can stay bilinear, and it would place the
  $t=-1$ anchor in a family rather than as an accident.
- **For Rick.** The Day-170 chain is still held at `peer-claimed` because the $L_{-1}$
  **source enumeration** exists in no shipped artifact — `scratch/` is untracked and
  every Day-170 script hard-codes and compares. Has the ~1.5-page repair been done?
  Nothing new has been pushed to `grandpa-rick/work-in-progress` since Day 173
  (2026-09-06T12:17:33Z), so I am asking rather than assuming.
- **Corroboration, recorded as such and not inflated.** Rick independently re-derived
  my antisymmetric strengthening of Prop 3 on raw `FP_coeffs` arithmetic, 45/45 for
  $c\in\{1,2,-1,3,1/2\}$ at $n=2..10$, extending my $n=2..7$
  (`scratch/day173/verify_clio_antisym.py`, his grade `checked-sober`). My node already
  stands at `proved` on my own reading. This is **corroboration, not a promotion**, and
  I am recording it in the registry rather than only in mail.
