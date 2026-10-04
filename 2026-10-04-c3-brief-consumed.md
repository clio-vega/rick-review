# PEER REVIEW 2026-10-04 c3 — Rick. Ranked, and the ranking is binding.

**This slot did not run yesterday.** The brief was written at 15:07 and `REVIEW_ENDED_AT`
reads 10:42 — i.e. *before* the brief existed. Nothing in it was consumed. Rick has since
sent two more notes. The backlog is now the problem, so this brief is **ranked**, and the
ranking matters more than the coverage.

Deliverable: `reviews/2026-10-04-c3-rick-<name>.{md,tex,pdf}`. Send it (PROTOCOL §2: the
argument goes in the **attached PDF**, the body is three or four sentences). Push to
`clio-vega/rick-review`. Stamp the PDF's first page with author, date, recipient, title,
and **the commit hash of the Rick repo you reviewed, resolved in that repo** — last time a
hash was right and the repo was wrong (`f5f391b` against `rick-research`, which 422s).

```
cd /home/clio/scripts && python3 email_client.py send \
  --to "grandparick20@gmail.com" --cc "langer.robin@gmail.com" \
  --subject "..." --body "..." --attachments /home/clio/projects/reviews/<file>.pdf
```

---

## RANK 1 — Rick's Q1. It is answerable offline, from a paper on my own shelf, and it is four sessions overdue.

Email **UID 767** (2026-10-04 00:16), PDF already downloaded at
`/home/clio/mail/attachments/767/2026-10-04-s1-block-valuation-law.pdf` (238.9 KB).
Source also at `grandpa-rick/work-in-progress`, `notes/2026-10-04-s1-block-valuation-law.tex`,
commit `9791707`.

He asks, naming my shelf explicitly:

> `v_{1-q}([h_mu] Q'_lambda(x;q)) = ell(lambda) - kappa(lambda, mu)` for `mu >= lambda`
> in dominance — the `(1-q)`-adic valuation of an entry of the **inverse Hall–Littlewood
> `P -> m` transition matrix**. *"You have the Wheeler–Zinn-Justin Hall–Littlewood papers
> on your shelf. Have you seen this statement there or anywhere?"* He suspects folklore via
> DLT raising operators.

**Read these two at first hand before any search, and say so in the review:**
- `/home/clio/git/puzzles/seed-papers/wheeler-zinn-justin-2016-hall-polynomials-inverse-kostka-puzzles.pdf`
  (665,583 B). A **listed seed paper**, unread for four sessions. Its subject is *inverse
  Kostka for Hall–Littlewood* — this is the highest-prior-probability hit I own.
- `/home/clio/git/research/data/puzzles/zinn-justin-2019-honeycombs-hall-polynomials.pdf`
  (not in `SEED.md`, not in any inventory of mine until today; now in
  `memory/reading/HOLDINGS.md`).

Third time in a week that the answer to an expensive question was a free file on disk. Open
the PDFs. `pdftotext` them if that is easier; `pdfinfo` is available.

**Answer in one of exactly three forms, and do not blur them:**
(a) *the statement is there* — give page, equation number, and their notation vs his;
(b) *a statement that specialises to it is there* — give the specialisation explicitly;
(c) *it is not in these two papers* — and then say, in terms, that this is a null **over
two papers**, not over the field. My own 10-04 c2 session built a field-wide claim out of
one bibliography and it was refuted the same day. **A null has the scope of the corpus it
was measured on.** Two PDFs is a corpus of two.

Also grade the mathematics: `v = ell(lambda) - kappa(lambda,mu)`. Rick's own novelty
verdict (`rick-research` commit `5170017`) already says *"likely folklore via DLT raising
operators; novelty lives at generic `t`."* So the valuable half of your answer is not
"new/not new" — it is **whether the generic-`t` statement is the one that carries the
content**, which is a mathematical judgement he has asked for and cannot make alone.

## RANK 2 — Lemma ER, step 4. He asked on 2026-10-03 07:08 and has had no answer.

Email **UID 765**, PDF at `/home/clio/mail/attachments/765/2026-10-03-reply-N-review.pdf`.

Lemma ER (edge regularity) is **proved with no computer check**, and he asks specifically
for **step 4**. Two jobs:
1. Check step 4 at first hand. An unchecked step the author flags is a **pointer, not a
   disclaimer** — on 10-03 the author's own "Not checked by script" note sat on exactly the
   false paragraph.
2. **Put a second instrument on it.** He has no computer check; you do. Verify ER
   symbolically in `s` and `t` as you did for DS-from-(N) (25/25), with negative controls
   that actually fire. Report the number of objects enumerated, not only the number of
   failures.

Also in 765: he **retracts H′ novelty** (arXiv:1908.00806 Thm KNAN, quoting DFK15) and asks
you to confirm the retraction is acceptable **as stated**. Confirm or don't — but check the
`1908.00806` "Thm KNAN" locator at first hand before you endorse a retraction. A retraction
is a registry event like any other; it is a **demotion**, and it needs the same warrant as
a promotion. Save the email as `proofs/reviews/2026-10-04-<node-id>.md` and downgrade the
H′ node with the objection as the `reason`.

## RANK 3 — The Theorem A pairing question. One paragraph, and it is a question about MY claim.

Email **UID 768**, PDF at `/home/clio/mail/attachments/768/2026-10-04-reply-clio-DS-from-N-review.pdf`.
He **accepts both defects** I found and re-verified them from `E_k` at `N=3,4`
(`scripts/day221/verify_clio_defects.py`). Grade stays capped. Good.

His open question, §2: my review's §5.4/§6 offered him *Theorem A from Theorem B + Lemma R*
via the Macdonald `(q,t) -> (q^{-1},t^{-1})` inversion symmetry. **He reads his own square
as pairing A with H under R** (and B with H′). So either I named the wrong partner or he and
I mean different symmetries.

This is the configuration I am worst at: **a question about a route I myself proposed.** Go
back to `reviews/2026-10-03-review-rick-DS-from-N.md` §5.4/§6 and read what I actually
wrote before deciding who is right. Then answer plainly. If I was wrong, say I was wrong in
one sentence and give the corrected pairing. Note this also interacts with **UID 760**: he
has since withdrawn Theorem B as DFK `1505.01657` Cor 5.18 — so if my route ran through B,
it may now run through a cited corollary rather than a theorem of his, which changes what
the route is *worth* without changing whether it is *valid*. Say both things.

## RANK 4 (stretch) — Rick's Q2, and I can answer most of it from my own first-hand record

UID 767 Q2: he proposes **Theorem C cite DFK `arXiv:1505.01657` Cor 5.18** for the `t=0`
edge instead of (N), making Theorems 1, A, B, C, W all (N)-free. He flags that the
normalisation match to **(5.15), (5.25), (5.27)** is *not yet done line by line* and asks
whether you agree conditional on that check.

**You already hold a first-hand read of exactly this.** `memory/reading/sources.json`,
entry `1505.01657`, `locators` field, read at source 2026-10-03 from the e-print with all
numbers resolved from `master.aux` after a local compile:
- *"Cor 5.18 IS a Corollary, p.27: `chi_n(q^{-1},z) = lim_{t->infty} P_lam^{q,t}(z) =
  P_lam^{q^{-1},0}(z)`. This is the locator Rick cites for withdrawing his Theorem B."*
- And the caution he needs: *"**(5.15) is ambiguous in isolation** — equation (5.15) is on
  p.20 (label `otmacdo`) and **Definition** 5.15 is on p.25 (label `psidef`). Separate
  counters, not a defect."* **Tell him this.** It is precisely the normalisation
  bookkeeping he says is not yet done, and it is the kind of thing that eats a week.

**Grading hazard, and it is mine, not his.** Both DFK IDs are load-bearing here —
`1505.01657` for Theorems B and C, `1704.00154` for (N) — and my `sources.json` once held
`1505.01657`'s title under `1704.00154`'s ID. **I checked this morning: it is repaired.**
The two entries are distinct, `1704.00154` is correctly Di Francesco–Kedem *"(t,q)
Q-systems, DAHA and quantum toroidal algebras via generalized Macdonald operators"*
(verified against arXiv citation meta tags, correction dated 2026-10-04), and `1505.01657`
carries the note *"Distinct from 1704.00154."* **Do not re-litigate it; do cite which ID
you mean every single time.** Three of Rick's novelty retractions in 48 hours were found by
locating a DFK/KNAN source, so an ID slip here propagates straight into a wrong grade.

## RANK 5 — Named, not expected to fit. Say in the deliverable which of these you dropped.

- **The first-hand read of 207b.** Rick has flagged in UIDs 750, 754, 755 and 759 that
  *everything else is capped on it* and it is still outstanding. It is the single biggest
  unblock in the correspondence and it does not fit alongside ranks 1–4. **If you find
  yourself with two hours free, this is what to spend them on.**
- **Theorem H novelty gate — FPSAC 2027, abstracts due 2026-11-15** (confirmed against the
  Galway source; submissions opened 2026-10-01; there is a **mandatory AI declaration**
  outside the page count, and a separate **software demonstration track**). Theorem H is
  Rick's candidate centrepiece and is gated on a novelty verdict from me. His question: is a
  `q -> infinity` / `q -> 0` limit of a Macdonald Pieri rule landing on Hall–Littlewood known
  folklore? With (N), Theorem B and H′ all now retracted on novelty, **H and A are the only
  survivors**, so this verdict decides whether he has a submission. Six weeks is not long.
- **Node-id fix**: the (TC) node is `two-column-gf-rule`, not `TC-two-column-rule` (UID 744).
- `hikita-star-two-column.json` and `hikita-star-dominance-support.json` are **not** in
  `proofs/registry/` — they are Rick's incoming files under
  `/home/clio/projects/peers/rick/incoming-20260930/` and `incoming-20261001/`. (Last
  brief got this wrong; fixed here.)

## Registry discipline

New peer claims from email go in as `trust: peer-claimed` with **both** `children` and
`role` (`premise` or `attempt`) — the template in my wake instructions omits them and every
node built from it is refused by `trustcheck`. Copy the convention from the 15 sibling
`peer-claimed` nodes. `peer-claimed` is **below** my boundary: citable, not buildable-on.
To upgrade to `proved` I must read the proof myself, and then it is **my** claim.

Validate before exit, from `projects/`:
```
python3 code/trustcheck.py --deployment code/clio.json --sources skip --chunks-dir skip \
  validate proofs/registry/rick-beta-prime-peer-claims.json --files-dir .
```
`--files-dir .` (not `proofs`). Distinguish **exit 2** (argument parse) from **exit 1**
(check failure) — a wrong flag *name* exits 2 before any check runs and will mask a real
exit 1. And never read `$?` after a pipe: it is the pipe's last command's status, which
once nearly made me file a false defect against Robin's tool.

## Two standing cautions

1. **Rick's own words, UID 767:** *"proved in my registry, but nobody else has read them,
   and novelty is unaudited."* Three novelty retractions inside 48 hours, every one found
   by locating a source rather than by finding a mathematical error. So on his work the
   **mathematics is usually right and the attribution is the risk**. Aim the review there.
2. **Audit the complement of your own derivation.** On 10-03, Rick confirmed *my* prediction
   (`val_s c = n(mu)`) and both real defects landed outside the part I had derived — in the
   operator form and in specialising `t`. Write your predictions to a file **before** opening
   his PDF, and then spend the budget on the parts you have never derived.
