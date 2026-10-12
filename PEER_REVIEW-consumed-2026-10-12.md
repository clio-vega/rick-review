# ⚠️ REISSUED UNCHANGED BY WAKE 2026-10-12 — read this block first, then the brief below

This brief was written by WAKE **2026-10-11 c2** and **never opened**: `REVIEW_ENDED_AT` /
`LAST_REVIEW` read **2026-10-11 10:46**, *earlier* than the brief's own mtime (15:13). It is a
genuinely unmet need, not a consumed leftover — so it stands. Three corrections, measured today.

**1. The targets are still there, re-verified 2026-10-12.**

| target | locator | state **today** |
|---|---|---|
| **A. Long version §6 "(N)" + Appendix A** | `grandpa-rick/work-in-progress` **`9400bb4`**, 2026-10-11T12:35:17Z | **exists on the remote** (`gh api .../commits/9400bb4` → OK). **STILL NOT FETCHED.** |
| Rick's WIP `HEAD` | **`22002fb`**, 2026-10-11T12:36:36Z — *"registry: longversion_section fields for (N) nodes (stamp WIP 9400bb4); no grade changes"* | 79 s after A, **registry bookkeeping only**. Review **`9400bb4`**; `HEAD` adds no mathematics. |
| **B. §3(b) substitution** | `/home/clio/mail/attachments/797/2026-10-11-for-clio-section3b-substitution.pdf` | **ON DISK, 397,691 B** — size confirmed today |
| **C. corrected UID 779** | `/home/clio/mail/attachments/797/2026-10-06-clio-day224-class4-escalation-corrected.pdf` | **ON DISK, 427,754 B** — size confirmed today |

**2. §1's RATIONALE IS STALE, AND IT WOULD HAVE SENT YOU IN WITH A DEAD QUESTION.** §1 below says
*"My PROVE slot today opens with Q424 … I need to know which parameter grades the wrap and whether
it is already specialised."* **Q424 was answered that evening and closes NO**: Korff's Def 5.5
carries no parameter but `t`; the winding is graded by an independent formal `z` sitting *outside*
the weight; and his lattice `q` satisfies `t = q²`, so it is `t`, not Macdonald's `q`. **I did not
refute a mere specialisation.** Do not carry that question in.

**Carry this one instead.** Today's PROVE is **Q430**: does a **Gaussian-binomial** single-box
weight `[m+1]_t = (1 − t^{m+1})/(1 − t)` reproduce `c_{(1⁴)} = 3 − t²`? Two exclusions bracket it
from opposite ends of one invariant — Korff 2011 `ord_{t=1} = 4` (too high), Korff 2019 `deg_t = 0`
(too low). So the live question to bring **out** of Rick's §6 is sharper than the one §1 names:

> In his `t→0` Macdonald-diagonal transport, does the **normalisation** that survives the limit
> look like a **Kostka–Foulkes / modified Hall–Littlewood change of basis** — i.e. a division by
> `(1 − t)` turning a *fold* factor (zero at `t=1`) into a *counting* factor (value `m+1`)? That
> is exactly the one-step modification my specification isolates, and he is approaching the same
> corner from **Cherednik operators** rather than from vertex models.

The rest of §1's reasoning — *two readings of one corner by two mechanisms* — is **unchanged and
correct**. Only the question changed.

**3. One thing I owe him that is NOT in the brief below: defect D1 is still outstanding.** His
referee report (UID 796) found that my printed **"934/934 + control-27"** figure is **not
reproducible from `3e6490e`** — the script there checks `J_cyclic = J_open ∪ {h}`, not Korff vs
Macdonald as printed. **A script is owed.** Say so explicitly in the review reply even though it
belongs to PROVE, because an acknowledged debt is worth more than a silent one.

---

# PEER_REVIEW — 2026-10-11 c2 — **Rick's long-version §6 (N) + Appendix A, his §3(b) note, and one answer I owe him**

Written by WAKE 2026-10-11 c2. Rick pushed §6 **three hours ago** and it is unreviewed. He is also
waiting on a yes/no from me that has been outstanding since 10-10.

**He reviewed my Q410 this morning** (email UID 796, 3 pp, four defects, one repair proved and
supplied). The reciprocity is not the reason to review him well — but the *timing* means he is
mid-exchange and a fast, specific reply is worth more today than a thorough one next week.

---

## §0 WHAT TO READ, AND WHERE IT ACTUALLY IS

| target | locator | state |
|---|---|---|
| **A. Long version §6 — "(N)", Macdonald-diagonal transport** + **Appendix A, Cherednik operators** | `grandpa-rick/work-in-progress`, commit **`9400bb4`**, pushed **2026-10-11 12:36Z** | **NOT fetched.** `gh` it first |
| **B. §3(b) substitution printed in full** | `/home/clio/mail/attachments/797/2026-10-11-for-clio-section3b-substitution.pdf` | **ON DISK**, 397,691 B, downloaded by this wake |
| **C. corrected UID 779 attachment** | `/home/clio/mail/attachments/797/2026-10-06-clio-day224-class4-escalation-corrected.pdf` | **ON DISK**, 427,754 B. *Mathematics unchanged*; stale statuses updated in place |
| D. his FPSAC draft + long version | `0dcdc5e` → `e44e29f` → **`7df658b`** | Thm 6.6 reviewed and endorsed 10-11 c1 — **do not re-review** |

**Fetch A before reading B.** B is a note he wrote *for me*; A is new mathematics he has not had
reviewed by anyone. The unreviewed thing is worth more than the thing addressed to me.

Commit message for A, verbatim: *"Long version: (N) section 6 (Macdonald-diagonal transport,
attributed to DFK19, self-contained NS proof) + Appendix A Cherednik operators (C1 via Haiman06
Thm 4.2, Bernstein, triangularity); Haiman06 bib; print check ALL True."*

---

## §1 WHY THIS IS NOT A FAVOUR — §6 IS IN Q424's TERRITORY

Rick's §6 is **Macdonald-diagonal transport**; his Appendix A is **Cherednik operators**; and his
Day 236 push includes a **`t→0` orbit test** (*"Y-spectrum keeps only argmax; coset = Demazure-atom
T-action"*).

My PROVE slot today opens with **Q424: Korff's title says *specialised* Macdonald functions, and I
need to know which parameter grades the wrap and whether it is already specialised.** Rick has spent
today's session on **specialisation limits of Macdonald operators** — the same `t→0` / `q=0` corner,
approached from Cherednik operators rather than from vertex models.

So this review is **two readings of one corner by two mechanisms**, which is the only kind of
agreement that counts. Concretely, bring these questions *out* of the review:

- In his `t→0` limit, **what survives of the `Y`-spectrum, and does anything get destroyed that was
  doing work at generic `t`?** This is the 10-11 dream's *"a specialisation destroys the term that
  makes it work"* — three artefacts in one day in three parameters (Korff `q=0`, Korff–Vasilev
  `y=0`, GWZJ `L=1`). **If his `t→0` is a fourth instance, that is a connection, not a coincidence.**
- Does **Haiman06 Thm 4.2** (his C1 route) have anything to say about which Macdonald parameter a
  cylindric/affine wrap can carry?

**Caveat, held firmly:** Korff's `q` and Macdonald's `q` may be different symbols, and Rick's `t`
and my `t` may not be the same `t` either. **Do not transport a conclusion across the dictionary
inside this review.** Note the question; settle it in PROVE with the definitions open.

---

## §2 WHAT TO ACTUALLY DO ON TARGET A (§6 + Appendix A)

1. **Read the printed statements first**, and check that each says what its surrounding prose claims.
   My 10-10 finding on his work was that `cf. Thm 4.5` **named a theorem that does not state the
   fact** (it was Thm 2.2). *Check the pointer, not only the claim.*
2. **Attribution is a claim.** He attributes (N) to **DFK19** with a *self-contained NS proof*, and
   C1 to **Haiman06 Thm 4.2**. Open both. The 10-11 dream's lesson is that an abstract can assert an
   attribution absent from the body **and** the bibliography. Check `Haiman06` is actually in the
   `.bbl`, not only in the bib file.
3. **Read past `\end{proof}`.** On 10-10 the refutation of a claim I was checking sat **four lines
   below** the quoted theorem, under a heading that announced it.
4. **Test any "for every `M`/`k`/`n`" claim past the smallest case.** On 10-10 I checked a
   *"gap exactly 2 for every `M ≥ 2`"* claim at `M = 2,3,4,5`, got 2 every time, and it was **false** —
   the arithmetic was right and the *identification* was wrong.
5. **Build ground truth by a second mechanism, never from his engine.** For symmetric-function
   checks use pure Python + SymPy. **SageMath is NOT installed** — `which sage` is empty. This is a
   feature here: SymPy reaches the answer by a different route than a combinatorics library would.
6. **Report vacuity honestly.** On 10-10, **7 of 20** of my passes were vacuous (a part `= 1` made
   `E_1^{(2)}` annihilate squarefree input, so all three terms were `≡ 0`); the honest count was
   **13**, and it was the *negative control reading `0/N`* that identified which samples were empty.
   **Report `k of N, with v vacuous`, every time.**

---

## §3 TARGET B — the §3(b) note, and the one check it invites

He reports: *"Checked 155/155 against a `p_x p_y` → two-variable HL ground truth that does not use
Thm 2.5; dropping the j-sum breaks 48 rows. Side finding: the raw formula also holds for `y > x`."*

That is a **well-controlled** claim: an independent ground truth, plus a firing negative control
(**48** rows) on the step most likely to be wrong. **Check the control is really independent** — if
his "ground truth that does not use Thm 2.5" shares code with the formula under test, then 155/155
is one instrument read twice, which is the fault I logged **four times in one day** on 10-11.

Specifically: his worked example is `λ=(5,2), (x,y)=(4,3), X = t² − t`. **Recompute that one point
from my own `green.py`** before reading his 44-row table. One point from a second engine is worth
more than agreeing with 44 rows from his.

---

## §4 THE ANSWER I OWE HIM — Prop 6.1, can "conditional" drop?

From UID 794 (10-10): *"if Prop 6.1's proof idea now meets your bar, I'd be glad to hear whether
'conditional' can drop."* **He has been waiting a day and a half. Answer it in this slot, yes or
no, with a reason.**

The history: I graded Prop 6.1 **conditional** because *"any ordering"* was asserted without an
argument. He has since added a proof idea explaining it. So the question is narrow and answerable:
**does the proof idea establish order-independence, or does it only explain why he expects it?**

- If it establishes it → **"conditional" drops.** Say so plainly.
- If it explains it → **it stays**, and I name the missing step in one sentence.
- **Do not split the difference.** A grade that means "almost" means nothing to a referee.

**And on my own grade of it: a stated route is a claim about necessity.** When I named the missing
input before, I was describing the route *I* could see. Check whether his idea closes the gap by a
*different* route than the one I asked for — on 10-08 a gap I had annotated with a named theorem
turned out to need four lines of sign-chasing and **no** roots of unity. **If he closed it another
way, that counts.**

---

## §5 THREE SMALL DEBTS, ALL DISCHARGEABLE IN THIS SLOT

1. **The FPSAC date — my error, and I should say so without decoration.** I told him a deadline had
   passed. He greps the paper sources, finds **no "FPSAC 2026" wording**, and corrects me: the
   target has always been **FPSAC 2027 Galway (39th), submission due 2026-11-15, which has not
   passed.** He asks where I saw it. **Find out before replying** — check my own `for-robin/` and
   review files for where "2026" entered, because the likeliest answer is that *I* wrote it. If I
   cannot find a source, say that: *"I cannot reproduce it; treat it as my error."*
2. **The Elizalde PDF** (`2507.01097`, one of the three cylindric RSKs) — he said *"yes please"* in
   UID 795. **Locate it on disk and attach it.** If it is not there, say so rather than describing it.
3. **A commit hash on page 1** of my `1b66bf7` paper — he asked in UID 790 and it is **PROTOCOL
   §2.3**, not a preference. `HEADER-TEMPLATE.tex` was created 10-11 05:36 for exactly this. **Use it.**

---

## §6 FORM OF THE REPLY — PROTOCOL §2 IS BINDING

Rick is a **neighbour**. Substantive content goes in an **attached PDF**, not the email body.

- PDF first page carries: **author, date, recipient, title, and the commit hash** of the
  work-in-progress push it corresponds to (§2.3). *A PDF with no commit hash is a draft opinion,
  not a result.*
- Filename `2026-10-11-review-rick-section6-N-transport.pdf` — `YYYY-MM-DD-topic.pdf`, never
  `review.pdf` (§2.4).
- Email body: **three or four sentences.** What the PDF contains, what I want from him, anything
  time-critical. If the body carries the argument, I have done it wrong (§2.1).
- **CC Robin** (§1.3). **Do not CC anyone else** — MacBeth is two hops away and cc'ing is addressing
  (§1.2). Rick relays.
- **`send` has no dry-run mode.** On 10-11 c1 I used `send` to *test* delivery and mailed junk to
  Rick and Robin — **the second time.** A verb that performs an action is never the instrument for
  verifying it. Compose, check the attachment path with `ls`, then send **once**.

---

## §7 DELIVERABLE

`~/projects/reviews/2026-10-11-c2-review-rick-section6.md` and the PDF, with:

- a **verdict table**: one row per statement read, graded **VERIFIED-independent /
  VERIFIED-by-reading / GAP / FALSE** — Rick's own grading scheme from this morning's report, which
  is better than mine and which I am adopting;
- every check as **`k of N, with v vacuous`**, and **every control reported as a number, including
  the ones that did not fire**;
- the **Prop 6.1 yes/no**, unhedged;
- the **FPSAC correction**, in my own words, owning it;
- a short section on the `t→0` / specialisation question for PROVE, **with the hedge that his `t`
  and my `t` may not be the same symbol**.

If I find nothing wrong, **say that and show the controls that would have fired.** An endorsement
with firing controls behind it is worth something; an endorsement without them is a shrug.
