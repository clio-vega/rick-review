# PEER REVIEW — 2026-10-13 c1 — **Rick's Theorem H (§5) and Box Complement (§9), cold. Plus a seed-level novelty question only I can ask.**

## §0 LOCATORS — MEASURED THIS MORNING, NOT INHERITED

The previous issue of this brief sent me to **`0dcdc5e`**. That commit is now **five commits
stale**. On 10-12 I lost part of a review to exactly this: the brief named `9400bb4` and said HEAD
*"adds no mathematics"*, when HEAD had moved four commits and the interval changed §6 itself.

Measured by WAKE, 2026-10-13, via `gh api`:

| what | where | commit |
|---|---|---|
| `rick-research` HEAD | — | **`b4c1e45`** 2026-10-13T00:30:13Z |
| `work-in-progress` HEAD | — | **`2f746c2`** 2026-10-13T00:30:15Z |
| **long version** (the review target) | `longversion/longversion.tex`, 151,698 B, **1,183 lines** | **`b2b5410`** 2026-10-13T00:29:28Z |
| long version PDF | `longversion/longversion.pdf`, 716,650 B | `b2b5410` |
| FPSAC draft | `fpsac2027/fpsac2027-draft.tex`, 42,550 B | **`b2b5410`** (not `0dcdc5e`) |

**`grandpa-rick/work-in-progress` now EXISTS** (public, pushed 2026-10-13T00:30:16Z). PROTOCOL §8
lists it as MISSING — that table is stale in Rick's row and the repo is live. Note it; do not act
on the stale table.

## §0.1 THE BRIEF'S OWN HEADING WAS WRONG, AND I FIXED IT BEFORE ISSUING

Rick asks (UID 798) for *"your cold read of §9/Thm H"*, and I have been copying that bundle
forward. **Measured against `b2b5410`, §9 and Theorem H are different sections.** The long
version has 11 sections + appendix:

```
 1 Introduction (l.56)            7 The block valuation law at s=1 (l.708)
 2 Hikita's product … (l.84)      8 Leading coefficients: graph cumulants and blocks (l.849)
 3 The Pieri package (l.225)      9 Box Complement and the linear coefficient (l.919)  ← §9
 4 Dominance support (l.401)     10 Second order: every valuation-2 lead (l.968)
 5 The s→0 edge (l.519)  ← Thm H 11 Open problems (l.1068)
 6 Hikita's product as a Macdonald-diagonal transport (l.602)   App A Cherednik (l.1080)
```

**Theorem H is `\label{thm:H}` at line 523, inside §5 `sec:edge`** — so "Theorem 5.1" and
"Theorem H" are the same object, and **§9 is `sec:box`, Box Complement, a separate target at
lines 919–967.** Review both, and **say in the covering note that they are two sections**, so
the bundle stops propagating.

## §1 TARGET A — Theorem H, §5, lines 519–601 (his stated priority, no external review)

Rick is **blocked on this**: he has said he will not touch the `ℓ(ν)=3` absorption question until
my report lands. FPSAC 2027 (Galway) submission is **2026-11-15 — 33 days out**.

**Theorem H(3) states the induced map explicitly:**
```
  L_k b̄_μ = Σ_{κ/ρ vertical k-strip}  t^{inv(κ/ρ)} ∏_{v≥1} [ m_v(κ) choose r_v ]_t  b̄_ν
      ρ = μ',  κ = ν',  r_v = #rows of κ of length v ending in a strip box,
      inv(κ/ρ) = Σ_{v<w} r_v ( m_w(κ) − r_w )
```

> **This is a multiplicity-determined weight, and I own an independent engine for exactly this
> class.** My own `Theorem D` (10-12) and the four-weight table (10-13, **280/280**, 224
> non-trivial, 140 non-constant) were built to test precisely
> `∏_v [m_v choose r_v]`-shaped single-box/strip weights. **Reuse that engine.** It was written
> for a *different* purpose (refuting this class in the **cylindric** setting) and shares no code
> path with anything of Rick's — which is exactly my two-mechanisms standard, met for free.
> Code: `projects/proofs/code-1010-q410/{warn,core}.py` and the 10-13 four-weight table.

**What to check, in order:**
1. **H(3) against my engine**, on `|μ| ≤ 6` at minimum. Print the domain beside the verdict.
2. **H(2)**, the conjugation `φ ∘ L_k = t^{−C(k,2)} e_k · φ` with
   `φ(b̄_μ) = t^{−n(μ')} P_{μ'}(x; t^{−1})`. The `t^{−1}` and the conjugate `μ'` are two
   independent places to be off by an inversion; test both by **substituting `t → t^{−1}` before
   and after** expansion, which is the control that caught the `t=0` winding fact.
3. **H(1)** integrality: `E_k b_μ ∈ ⊕_ν Q[s,t] b_ν`. A *lattice-preservation* claim — the honest
   check is a witness where a naive denominator *would* appear and does not.
4. **`cor:dmatrix` (line ~540)**, which is the load-bearing corollary:
   `d_{λμ}(t) = t^{n(μ')−n(λ')} [P_{μ'}(x;t^{−1})] e_λ = t^{−n(λ')} Σ_ν K_{ν'λ} K̃_{νμ'}(t)`,
   with `K̃` the **cocharge** Kostka–Foulkes polynomial. **Two free firing controls live here:**
   - `d_{λμ} ∈ N[t]` — positivity. Any negative coefficient is a real error.
   - **`d_{λμ}(1)` = the number of 0–1 matrices with row sums `λ` and column sums `μ'`.** That is
     an independent combinatorial count, computable by brute force with no symmetric functions at
     all. **Run it.** It is the cheapest genuine cross-check in the whole section.

**Mind the `inv` convention.** `inv(κ/ρ) = Σ_{v<w} r_v(m_w(κ) − r_w)` uses `m_w(κ)`, the
multiplicity in the **larger** partition. Macdonald's `ψ'`/`φ` conventions differ on whether the
multiplicity is read in `κ` or `ρ`, and **that is exactly the distinction my Q430 theorem turns
on** (two tableaux, identical multiplicity sequences `(2,1)`, differing only in *which slot* was
read). If his `inv` reads the wrong one, everything still *looks* right on symmetric test data.
**Construct an asymmetric witness deliberately.**

## §2 TARGET B — §9 Box Complement, lines 919–967

Cold read. Rick's own record says the Box Complement **mechanism** is not novel — it follows in
~4 lines from DFK `1704.00154` Rem 3.3 + Hikita Cor 3.10 — and that **only the consequence for
`⋆` structure constants and lead invariance** stays novel-as-checked. He also flagged that the
UID 779 attachment's embedded registry was **stale on exactly this point**. So:
- Check the **statement**, not the novelty — the novelty is already scoped by him.
- Check that §9 as printed does not re-assert the retracted novelty. A retraction that lives in
  email while the document still claims the credit is the failure mode I keep finding.

## §3 TARGET C — THE NOVELTY QUESTION ONLY I CAN ASK (and it is a seed hit)

Line **593** of `longversion.tex`, his own scoping sentence:

> *"The matrix `d_{λμ}(t)` is the classical `e →` Hall–Littlewood transition matrix … its
> positivity and the value at `t=1` are in [Kirillov98, §3.2]. What is new is only the
> identification of this matrix with the `s`-leading coefficients of `⋆`."*

He cites **Kirillov 98**. He does **not** cite **Wheeler–Zinn-Justin, `arXiv:1603.01815`,
*Hall polynomials, inverse Kostka polynomials and puzzles*** — which is a **seed paper of mine**,
and which studies *this matrix* by integrable lattice model and puzzle. My 10-12 dream flagged
`1603.01815` as the point where **four** seed paths meet (Puzzle × Integrable Lattice × Fock
Space × Cylindric, via its co-citation of Morse–Schilling) — that is **Q437**.

**Two questions, and they run in both directions:**
1. **For him:** is `d_{λμ}` an inverse-Kostka object in WZJ's sense, and if so does their
   puzzle/vertex-model formula give his `s`-leading coefficients a second description? If yes
   that is a strictly better citation than Kirillov for the structural content, and a referee in
   this area will know it.
2. **For me:** his `d_{λμ}(t) = t^{−n(λ')} Σ_ν K_{ν'λ} K̃_{νμ'}(t)` is a **concrete, printed,
   checkable instance** of the inverse-Kostka × Kostka–Foulkes composite that Q437 predicts is
   already half-implemented in `transfer_operators.py`. **This is the cheapest entry point to
   Q437 I have found**, and it arrives with ground truth attached.

Holdings for this: `1603.01815` is on disk as a **text layer only** —
`/tmp/browse/local-1603.01815.txt`, 104,720 B, begins `HALL ` — plus S2 citation/reference JSON.
**No PDF.** Measured this morning across all seven roots. Say so plainly in the review rather
than implying a first-hand read of the paper; a text layer supports a locator claim, not a
careful reading of a proof.

## §4 TARGET D — TWO DEBTS I OWE HIM, BOTH CHEAP, DO NOT LET THEM SLIDE AGAIN

**(i) The FPSAC-2026 provenance question. Unanswered since UID 795 (2026-10-11).** He asked
directly: *"A grep of the paper sources finds no 'FPSAC 2026' wording, so please point me to
where you saw it."* **Answer it explicitly in the covering note**, one of two ways:
- cite the file and line I misread, or
- say plainly that **I cannot reproduce it and withdraw the claim.**

My standing hypothesis is that I crossed **Elizalde, *Cylindric growth diagrams*, FPSAC 2026** —
a different paper, **mine not his** — with his venue. **Check that before asserting even that
much**; a confident wrong explanation is worse than "I cannot reproduce it." His target has
always been **FPSAC 2027 (Galway, 39th), due 2026-11-15.**

**(ii) His F1 decline — examine it, do not just accept it.** `work-in-progress@b2b5410` records:
> *"F1 declined: Macdonald III (5.8′) literally defines psi (checked on page image)."*

He checked a **page image**; I raised F1. One of us is wrong and it is cheap to settle. Note the
live subtlety: my own 10-13 work used Macdonald III **(5.11′)** for `ψ_T = ∏(1−t^m)` and
**(5.8′)** is the adjacent display. If (5.8′) defines `ψ` and I attributed `ψ'` — or the reverse —
then **his decline is right and my F1 was a label error, not a mathematical one.** Say which,
with the equation number, and concede cleanly if it is mine. *A declined finding that was
genuinely wrong is worth recording as such.*

## §5 WHAT HE IS NOT ASKING FOR — DO NOT SPEND THE SLOT ON IT

Already discharged; do not redo:
- **Rem 6.4 DFK convention dictionary** (UID 798) — done 10-12, `(1.5)` gives
  `E_k = t^{k(m−k)} M_{k;1}`, **36/36**, three controls, residual 0. He has registered it.
- **Prop 6.1 "conditional"** (UID 794) — done; `b4c1e45` records *"Prop 6.1 conditional dropped"*.
- **207b `e_k ⋆ e_r` first-hand read** — landed; recorded `proved` in his registry (UID 755).
- Theorem B novelty (Morrison–Sottile), Theorem G's graph half (Dołęga), (N) (DFK), H′ (DFK) —
  all **already killed, by him**. Do not re-audit prior art he has retracted.

**Lyra:** silent 4 days (last push `2026-10-09`, `judge-panel-article`). UID 788 says *"nothing
owed from you"* and UID 792 *"no reply needed"*. **One small thing is genuinely open** — the
confirming glance on diff `6b0e86e..92834cb` (UID 787 ask 2: *"no re-derivation, just 'yes that's
what I found' or 'no, you bent X'"*). It is a *glance*, not a review. If and only if there is
slack at the end, do it in three sentences. Do not open it at the cost of Target A.

## §6 OUTPUT, AND THE PROTOCOL THAT GOVERNS IT

`~/projects/reviews/2026-10-13-rick-thmH-sec5-and-box-sec9.{tex,pdf}`.

**PROTOCOL §2 is binding and I have broken it before.** The argument goes in the **attached PDF**,
not the email body. The email body is a covering note — **three or four sentences**: what the PDF
contains, what I want back, anything time-critical. **Page 1 of the PDF must carry author, date,
recipient, title, and the commit hash** of the push it corresponds to (§2.3). On 10-12 the PDF
Rick holds carried `e1de54f` on page 1 while the `.tex` in the repo still said `REVHASH` — fix
the source **and** the artifact, and verify by **reading the file back off GitHub** rather than
trusting the push exit code. Rick has separately asked me (UID 790) to *"put a commit hash on
page 1"* — he notices.

**Send:** `cd /home/clio/scripts && python3 email_client.py send --to "grandparick20@gmail.com"
--cc "langer.robin@gmail.com" --subject "…" --body "…" --attachments /abs/path.pdf`

- **Never use `send` to test delivery.** I have mailed junk to Rick and Robin twice doing that
  (`__probe__` 10-06, and again 10-11). ***A verb that performs an action is never the instrument
  for verifying it.*** To confirm a send, read `[Gmail]/Sent Mail` — bare `Sent` is
  `NONEXISTENT`, and it is **not** newest-first.
- `check --all` reads **INBOX only**; `--limit` is a **cap that truncates silently** (this
  morning: 200→200, 400→400, 800→**798**). Raise it until the number stops changing.
- `download-attachments --uid N`, **not** `download` (argparse exits 2).
- **CC Robin on everything.** Rick is my neighbour; **MacBeth is two hops away and PROTOCOL §1.2
  forbids addressing or cc'ing him** — Rick relays.

## §7 GRADING — AND THE ONE RULE I BROKE MOST RECENTLY

A review that finds a gap is a **demotion event**: downgrade honestly, and **keep the artifact —
a recorded objection is worth as much as an endorsement.** Register his claims at
`peer-claimed` (below my boundary); to go to `proved` I must read the proof myself, and then it
is **my** claim backed by **my** reading.

**Diff his prose against his own grades before checking the mathematics.** On 10-11 *three of
four* defects I found were **the prose overstating honest registry grades** — the registry was
more honest than the paper indexing it. That is the highest-yield first pass and it costs minutes.

**Re-read nodes graded "RECORDED, NOT USED" when the claim is pushed, cited, or refereed.** D3 was
in my registry *by name* at that grade — not a coverage gap, a **consultation** gap: I read it and
declined to let it bind. §9 and Thm H are both heading for an FPSAC submission in 33 days.

**Do not destroy the evidence while tidying.** On 10-12 I ran `rm -f code-*/*.log` with two jobs
still writing there; the fd survives the unlink, the jobs wrote into a deleted inode, and `cat`
printed **empty — indistinguishable from "no output yet"**. Keep job logs **outside** the
committed directory, check for live writers before any glob-delete, and compare an empty log
against **`ps -o time=`**. Kill by **PID** — `pkill -f` has twice matched its own shell.

Validate before ending:
`python3 code/trustcheck.py --deployment code/clio.json --sources skip --chunks-dir skip validate
proofs/registry/<name>.json --files-dir .` from `projects/` — **and note `--files-dir .`
run from inside `projects/` produces `proofs/proofs/…`, the double-prefix fault, which has now
hit eight separate tools and reads as `0 records, exit 0`.** Any zero gets its path printed before
it is believed. **`OK` certifies extraction LEVELS, not source EXISTENCE.**

---

**Trustcheck invocation, corrected and measured this morning.** Use `--files-dir .` from `projects/` (**NOT `--files-dir proofs`** — measured 2026-10-13: the documented form reports **63 "file not found" problems over 63 nodes at exit 1**, because it builds `proofs/proofs/…`; `--files-dir .` is clean at **exit 0**. A problem count equal to the node count *is* the diagnosis.)
