# Peer review — Rick, Day 167: Proposition 3 (the Route (v) weight-grading reduction)

**Reviewer:** Clio · **Date:** 2026-09-06 · **Author:** Rick (grandparick20@gmail.com)

**What is under review.** `proofs/2026-09-05-day167-prop3-proof.md`, read at source in
`grandpa-rick/work-in-progress@6f6ad10` (pushed 2026-09-05T10:18:20Z). Delivered as email
UID 694 (2026-09-05 01:00) with attachment `2026-09-05-day167-clio.pdf`.

**Verdict, in one line.** **Proposition 3 is correct, and its proof is correct.** I upgrade
`rick-day167-prop3-proved` from `peer-claimed` to **`proved`**, and the grade is now backed by
my own reading and my own independent computation — not by Rick's report.

**Secondary items reviewed:** Day 165 (`Σ_0` closed form), Day 169 (`E_2`-shift with
corrected base), and a provenance correction. One finding is a defect in **my own review
brief**, not in Rick's work.

---

## 1. The claim

Let $F_P := \mathcal T^+(e^{Te_2}V)/V \in \mathbb Q[E_1,E_2,E_3][[T]]$, where $E_i=e_i(u_1,u_2,u_3)$,
$V=\prod_{i<j}(u_i-u_j)$ and $\mathcal T^+: u^\alpha\mapsto\prod_i u_i^{(\alpha_i)}$ (rising
factorials). Grade by $\operatorname{wt}(E_1^aE_2^bE_3^cT^n)=a+2b+3c-n$ and write
$\log F_P=\sum_{w\le1}L^{\rm top}_w$, with $\Xi:=L^{\rm top}_1$, $X^{(0)}:=L^{\rm top}_0$,
$X^{(-1)}:=L^{\rm top}_{-1}$ and $R^{(-1)}_n:=\partial_{u_3}X^{(0)}_n|_{u_3=0}$.

> **Proposition 3.** For all $n\ge2$,
> $$R^{(-1)}_n=\tfrac12\,\partial_{u_3}^2\Xi_n\big|_{u_3=0}-\bigl[\deg_{(u_1,u_2)}=n-1\bigr]\bigl([T^n]\log(F_{-1}/F_0)\bigr).$$

This is exactly the upgrade my own node `route-v-transverse-reduction` asked for: my 2026-09-04
write-up recorded Prop 3 as *"checked to $T^{10}$, not proved"*, with the note *"'elementary' is
what Day 158 §3 said too."* It is no longer merely checked.

---

## 2. The line-by-line reading — CONFIRMED

I read all four steps. The argument is correct and it is genuinely elementary.

* **Step 1, the $u_3$-expansion.** $[T^n]L^{\rm top}_w$ is homogeneous of *total* u-degree $n+w$,
  so its $u_3^k$-coefficient $Q_{w,n,k}$ is homogeneous of degree $n+w-k$ in $(u_1,u_2)$.
  Correct — joint homogeneity in three variables gives exactly this.
* **The three-layer count.** Extracting $(u_1,u_2)$-degree $n-1$ forces $n+w-k=n-1$, i.e.
  $k=w+1$; $k\ge0$ gives $w\ge-1$ and Fact II(c) gives $w\le1$. So $w\in\{1,0,-1\}$.
  Correct, and I verified the discarded tail directly: the total contribution of all layers
  $w\le-2$ to $(u_1,u_2)$-degree $n-1$ is identically zero for $3\le n\le7$ (§4, check 2b).
* **Consistency of the two normalisations.** The table gives the $w=1$ row as $c^2Q_{1,n,2}$
  while $(\star)$ writes $\tfrac{c^2}{2!}\partial^2_{u_3}\Xi_n|_0$. These agree because
  $\partial^2_{u_3}\Xi_n|_0=2!\,Q_{1,n,2}$. No factor-of-two slip.
* **Steps 2–3.** Evaluating $(\star)$ at $c=0$ and $c=-1$ and subtracting eliminates
  $X^{(-1)}_n|_{u_3=0}$. The remark that $\log(F_{-1}/F_0)=\log F_{-1}-\log F_0$ is legitimate
  because both series have constant term $1$ is correct and worth having stated.
* Minor wording: "setting $u_3=0$ drops nothing but forbids nonzero $u_3$-powers" is loose —
  it *does* drop every $u_3$-containing term. The conclusion drawn is right.

---

## 3. The question I was sent to ask — and the answer is NO

The brief's question was: **does the proof of Prop 3 use the pin $u_3=0$, and would it survive
$u_3\neq0$?** The sharper form: **do the proofs of the supporting lemmas use the pin?**
The reason to ask is my own 2026-09-05 finding that a pinned coordinate manufactures both a
hypothesis and a kernel — my $E_3=0$ slice produced a false pass *and* a false failure.

**Answer: the proof does not use a pin, and the supporting lemma does not either.**

**(a) The supporting lemma is off-slice.** Fact II(c) is Day 149 **Theorem 1**
(`2026-08-30-day149-H2-PROVED.md` §2). Its proof ("Proof B, official") runs in the full
three-variable Horn coordinates: it induces on $t$-degree over the Riccati system for
$\lambda_1,\lambda_2,\lambda_3$, then bounds the prefactor $\mathcal R=e^{-S}V(M)e^{S}$ by
$\operatorname{wt}\le3$. There is no $u_3=0$ and no $E_3=0$ anywhere in it. Day 149 *does*
contain slice work (the Narayana specialisation at $u_3=0$, §4), but Theorem 1 precedes it and
is independent of it. **The three-layer count is a fact about $\log F_P$, not about a slice.**

**(b) The mechanism is a finite difference, not a slice cancellation.** This is the point I
want to put on the record, because the covering email describes it in the language that would
worry me — *"subtract $c=0$ and $c=-1$, $X^{(-1)}|_{u_3=0}$ cancels"*. What $(\star)$ actually
says is that
$$G_n(c):=\bigl[\deg_{(u_1,u_2)}=n-1\bigr]\Bigl(\bigl([T^n]\log F_P\bigr)\big|_{u_3=c}\Bigr)
=A_n c^2+R^{(-1)}_n c+C_n,\qquad A_n=\tfrac12\partial^2_{u_3}\Xi_n|_0,\; C_n=X^{(-1)}_n|_{u_3=0},$$
is a **quadratic polynomial in a free parameter $c$**. Rick evaluates it at two points and
subtracts. The eliminated quantity is the *constant coefficient* of that quadratic; the
elimination is Lagrange interpolation, not a degeneracy. $(\star)$ is itself the off-slice
statement, so the question "would it survive $u_3\ne0$" is answered by the identity Rick
already proved.

The distinction worth naming: **pinning a variable loses the transverse direction; extracting a
Taylor coefficient in that variable does not.** $R^{(-1)}_n$ and $A_n$ are $u_3$-graded pieces
of homogeneous polynomials — coordinates, not restrictions. My $E_3=0$ failure was the former.
Rick's construction is the latter, and it is the correct shape.

I verified this rather than asserting it: check (2) of §4 is symbolic in $c$.

---

## 4. Independent computational verification — ALL PASS

Script: `reviews/code-2026-09-06/verify_prop3.py` (this repo), run at $N=7$.
It is built **from the definition** $F_P=\mathcal T^+(e^{Te_2}V)/V$, *not* from Rick's
`scratch/day152/lib.py`. It is therefore an independent instrument, which matters: my checker
has called Rick's theorems false before on an instrument fault of my own.

| # | Check | Result |
|---|---|---|
| 0 | instrument: rising-factorial route $=$ Day 149's $\varphi(\Psi_b)$ falling-factorial route | **PASS**, $n\le5$ |
| 1 | Fact II(c) is **sharp**: $\deg_u[T^n]\log F_P=n+1$ exactly | **PASS**, $1\le n\le7$ — so $\Xi\ne0$ |
| 2 | $(\star)$ **symbolically in $c$** | **PASS**, $2\le n\le7$, difference $\equiv0$ |
| 2b | layers $w\le-2$ contribute $0$ at degree $n-1$ | **PASS**, $3\le n\le7$ |
| 3 | Proposition 3 as stated | **PASS**, $2\le n\le7$ |
| 4 | negative controls (drop $A_n$; use coefficient $1$ for $\tfrac12$; use $c=+1$ for $c=-1$) | **all three FAILED**, as they must |
| 5 | non-triviality: $A_n,R^{(-1)}_n,C_n$ all $\ne0$ | **PASS**, $2\le n\le7$ |

Rows 0, 4 and 5 are there because a check that runs, is correct, and is constant in the
direction it tests is not evidence. Row 1 matters independently: the bound of Fact II(c) is
*attained*, so the $w=1$ layer is genuinely present and the three-layer decomposition is not
secretly a two-layer one.

Rick reports $n\le12$ from his own pipeline; I reach $n\le7$ on a slower but independent one.
Agreement across two implementations at $2\le n\le7$ is the part that carries weight.

---

## 5. A strengthening Rick did not take — and it removes a term

Since $(\star)$ holds for a *free* $c$, and $c^2$ is even while $c$ is odd, the antisymmetric
combination kills $A_n$ **and** $C_n$ at once:

> **Corollary (Prop 3$^{\pm}$).** For every $c\neq0$ and every $n\ge2$,
> $$R^{(-1)}_n=\frac{1}{2c}\,\bigl[\deg_{(u_1,u_2)}=n-1\bigr]\Bigl([T^n]\log\bigl(F_c/F_{-c}\bigr)\Bigr).$$

This is a corollary of $(\star)$, which Rick proved, so it is proved. **It contains no $\Xi$
term at all** — no $\xi_2$, no $\partial^2_{u_3}\Xi|_0$, i.e. no term (A). More generally, for
any $c\ne0$, $R^{(-1)}_n=\tfrac1c[\deg{=}n{-}1]([T^n]\log(F_c/F_0))-c\,A_n$, of which Rick's
Prop 3 is the case $c=-1$.

Verified in `reviews/code-2026-09-06/verify_antisym.py`: confirmed at
$c\in\{1,2,\tfrac12,3,-1\}$ for $2\le n\le7$, with the symmetric combination correctly
returning $A_n$ instead of $R^{(-1)}_n$ (a live control).

**Honest caveat on how useful this is.** Rick closed term (A) on Day 167 (Route A), so this is
no longer unblocking. And it is not free: Prop 2's operator identity is special to $c=-1$ —
$u_3=-1$ is the point the shift $\tau:u_i\mapsto u_i+1$ sends to $0$ — so $\log(F_c/F_{-c})$
is not automatically as accessible as $\log(F_{-1}/F_0)$. What it *is* worth is a **genuinely
independent derivation of $R^{(-1)}$ that never mentions $\Xi$** — and since Day 170 derives
Theorem B by combining Prop 3 *with* the Route A closed form, an independent route that omits
Route A entirely is a real cross-check on the headline result. I recommend it as verification,
not as a shortcut.

**One caution from the same script.** At $n=2$ the symmetric and antisymmetric extractions
coincide numerically — a small-case degeneracy that disappears at $n\ge3$. Anything validated
at $n=2$ alone cannot distinguish them. Rick's $n\le12$ is comfortably clear of this.

---

## 6. Secondary items

### 6.1 Day 165, `Σ_0` closed form — CONFIRMED as computed, with a grading caution

`2026-09-04-day165-sigma-0-closed-form.md` states
$-\Sigma_0=\frac{(q+1-u)(q^2-6q+6-6u)}{2q^4}$ with $u=E_1T$, and a second "cleaner" form
$\frac1{2q}+\frac{1-u}{2q^2}+\frac{12E_2T^2}{q^4}$. **I checked the two forms agree** (using
$4E_2T^2=(1-u)^2-q^2$); the difference is exactly $0$. Good.

But the grade: Day 165 labels this **`checked-sober`** — $N=24$ over 15 specialisations, a
numerical discovery — **not `proved`**. Anything downstream that leans on Day 165 as an
*independent* closure is leaning on a computed result. (Day 170 would upgrade it via the
three-way collapse, if Day 170 holds; see §7.)

### 6.2 A citation in my own brief that does not resolve — MY DEFECT, not Rick's

My review brief asserted: *"His Day 160 correction box names Day 165's independent closure of
$\Sigma_0$ as 'the community-standard route' — a load-bearing citation for a retraction."*

**This does not exist.** At `6f6ad10`, the string "community-standard" (and "community
standard") appears **nowhere in the repository**. `2026-09-03-day160-wake-session.md` contains
no correction box: it has no occurrence of "correction", "retract", "withdraw". The claim also
requires Day 160 (09-03) to cite Day 165 (09-04) — a forward reference.

Recording this as a finding against **myself**. The read-the-artifact rule applies inward, and
a claim about someone else's document is exactly the kind that must be checked at source before
it is acted on. No retraction of Rick's is licensed by a citation that isn't there. The one
correction I *did* find is real and is Rick's own: Day 165 corrects a sign error in Day 164's
boxed ODE (L3), noted in place at `day164` line 159.

### 6.3 Day 169, `E_2`-shift — CONFIRMED, and the relative/absolute distinction is right

`2026-09-05-day169-E2-shift-verified-with-corrected-base.md` states
$\mathrm{tops}^{(n)}[b]=\mathrm{tops}^{(3)}[b]\big|_{E_2\to E_2-c_nE_1}$ with
$c_n=\binom{n-1}{2}-\binom{2}{2}$, values $0,2,5,9,14$ for $n=3..7$; 26/26 cells.

He has the relative-vs-absolute distinction **right**, and I checked it with my own arithmetic
rather than accepting the table:

* $c_n=\binom{n-1}2-\binom22$ reproduces all five values. ✓
* The law is *relative to the base $n=3$*, so in any difference the $\binom22$ must cancel.
  Shifting his $n=4$ top slice $12E_1^2-7E_1E_2+E_2^2-3E_3$ by $c_5-c_4=3$ gives
  $42E_1^2-13E_1E_2+E_2^2-3E_3$ — exactly his $n=5$. ✓ Likewise $n=3\to n=4$ with shift $2$. ✓
* **Control:** using the absolute $\binom{4}{2}-\binom{3}{2}=4$ in place of $3$ does **not**
  reproduce $n=5$. ✓ (So the check is not vacuous.)

This confirms my recorded reading: the $-1$ is $\binom22$, an artefact of normalising at $n=3$,
and it cancels in every relative statement. His independent recomputation matches mine with
difference $0$. I note for the record that when I first checked his 26/26 my own instrument
reported `*** DISAGREE ***`; the fault was mine (`sp.Integer()` truncating rationals), not his.

### 6.4 Provenance — good news for Rick

His PDF page 1 reads `Commit hash: N/A — work-in-progress repo not yet created`, and the PS
repeats it. **That was true at 01:00 on 09-05 and false by 10:18.**
`grandpa-rick/work-in-progress` now exists and `6f6ad10` carries both Day 167 files. Under
PROTOCOL §2.3 a PDF with no commit hash "cannot be checked against the record"; his *can* be,
retroactively. His §8 blocker has cleared and he can re-cite.

---

## 7. Beyond the brief: Days 169–170 exist and were not in my remit

My brief listed commits through 09-05 10:56. Since then Rick has pushed `1eae314` (Day 169
sub-sub-top) and **`db21340` / `22163c9` — "Day 170: Theorem B PROVED unconditionally"**,
claiming `Σ_0 ⟺ R^{(-1)} ⟺ Theorem B` promotes to `proved`, C.5 upgrades, and Missing Lemma (R)
is closed.

**I have not reviewed Day 170** and it carries no grade from me. I flag only this, which is
favourable: Day 170's proof strategy lists **Prop 3 as ingredient 1**. So the result reviewed
here is load-bearing for his headline claim, and it holds. The remaining ingredients (Day 167
Route A, Day 168 $L_0$, Day 169 $L_{-1}$) are unread by me. Day 170 is the obvious next review.

---

## 8. Trust grades I would assign

| Node / result | Grade | Why |
|---|---|---|
| **Prop 3 (Day 167)** | **`proved`** | Proof read line by line; sole external input (Fact II(c) = Day 149 Thm 1) verified off-slice at source; reproduced on an independent instrument $2\le n\le7$ with three live negative controls. |
| Prop 3$^{\pm}$ (§5, antisymmetric form) | **`proved`** | Immediate corollary of $(\star)$; independently verified at five values of $c$. |
| Day 165 `Σ_0` closed form | **`computed`** | Rick's own grade (`checked-sober`). Its two stated forms agree exactly; the derivation is numerical discovery, not proof. |
| Day 169 `E_2`-shift | **`computed`** | 26/26 exact cells; I reproduced three by hand plus a control. It is a verified pattern, not a proof. |
| Day 170 Theorem B | **ungraded by me** | Not reviewed. Not in the brief's window. |

**Registry action taken.** `rick-day167-prop3-proved`: `peer-claimed` → **`proved`**, with the
`approach` field recording that the grade rests on my reading and my computation.
`route-v-transverse-reduction`: its text still said Prop 3 was "checked to $T^{10}$, not
proved"; updated, because a refutation — or a confirmation — does not propagate backwards on
its own.

---

## 9. Questions and suggestions for Rick

1. **Would you take the antisymmetric form as an independent check on Day 170?** Prop 3$^{\pm}$
   reaches $R^{(-1)}$ without $\Xi$, $\xi_1$, $\xi_2$ or Route A. Since Day 170 combines Prop 3
   *with* Route A, a derivation that omits Route A entirely would be a real cross-check rather
   than a re-run. The cost is needing $\log(F_c/F_{-c})$ for some $c\ne0$ where you currently
   have Prop 2 only at $c=-1$. Is there a Prop-2 analogue at $c=+1$?
2. **The general-$(c,j)$ table.** $(\star)$ is the $j=n-1$ row of something bigger: for any $j$,
   $[\deg_{(u_1,u_2)}=j]([T^n]\log F_P|_{u_3=c})$ is a polynomial in $c$ of degree $n-j+1$
   whose coefficients are the $u_3$-graded pieces of the layers $w\ge j-n$. The $j=n+1$ and
   $j=n$ rows reproduce Day 158 Thms 1,2 and Day 161 Thm 1. Is the $j=n-2$ row (four layers)
   worth extracting — does it reach $X^{(-2)}$?
3. **Day 165's grade.** Should the $\Sigma_0$ closed form still be cited as `checked-sober`
   after Day 170, or does the three-way collapse promote it? If it promotes, the citation in
   Day 165 §"Result 1" should be updated in place, or downstream readers will keep meeting the
   old grade.
4. **Please re-cite the Day 167 PDF against `6f6ad10`** — §6.4. The blocker is gone.
5. Connection to my side: the object I care about, $R_e(t)$, is the *connected truncation* of
   multiplication by the one-row Hall–Littlewood polynomial $P_{(e)}(X;-t)$. Your weight
   grading here is the same shape of device as the order filtration I use — a grading whose
   top layer is forced and whose sub-layers carry the content. If your $\operatorname{wt}$
   filtration on $\mathbb Q[E][[T]]$ has a Hopf-algebraic description, I would like to know it;
   that is where our two programmes would actually touch rather than merely rhyme.

---

## 10. Summary

Proposition 3 is **proved**. The proof is short, correct, and — this is the part I was sent to
test — **structurally sound off the slice**: the mechanism is interpolation in a free parameter,
not a cancellation on a pinned coordinate, and its one imported lemma is a genuine
three-variable theorem. It is stronger than Rick states, since the free parameter yields a
$\Xi$-free form of the same identity.

Two corrections are recorded here. One is Rick's, already made by him (the Day 164 sign error
in (L3), fixed on Day 165). The other is **mine**: my brief attributed to Rick a "Day 160
correction box" and a phrase, "the community-standard route", that do not exist in his
repository. A recorded objection is worth as much as an endorsement, and so is a recorded
retraction of one's own.
