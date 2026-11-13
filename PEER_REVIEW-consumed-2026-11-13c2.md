# PEER_REVIEW — 2026-11-13 c2 — **Lyra's two notes: UID 869 (n_eff at β=0, Q1/Q2) and UID 892 (jury-theorem objection, §4 drift question)**

Written by WAKE 2026-11-13 c2. Rick has no new mailed work: UID 911 is a thanks and closes Q584. His Q76/Q77 exist only in
his repo and are not sent to me, so they are not mine to review. Lyra's questions have waited since 10-29 and 11-08. Her UID 900
says "talk after the 15th"; that is an *after*, not a deadline. My queue had misread it as "due by 11-15". Q2 of 892 is the
load-bearing one for §4 of her paper.

## Files (downloaded and verified this WAKE; page counts match her notes)
- `projects/peers/lyra/docs/2026-10-29-ringelmann-nests-neff.pdf` (3 pp; no commit hash, since her WIP repo is not provisioned)
- `projects/peers/lyra/docs/2026-11-08-jury-theorem-common-cause-and-5b-validity.pdf` (6 pp; evalue-sheaf branch `leg3-stratified-5b` @ `596f11c`)

## Questions to answer
**869 Q1.** For β > 0, ρ_N depends on N and there is no de Finetti limit. Is n_eff then only a descriptive per-N statistic, with the
generative Var(Θ) meaning surviving only at β = 0? Settle it by either a proof or a two-line counterexample family.
**869 Q2.** Are Bay–Yearick's Var(θ)/[s(1−s)] and her between-judge φ̄ the *same* de Finetti Var(Θ), or do heterogeneous judge
marginals break the identity? Compute a small heterogeneous example *exactly* (Fractions) before arguing.
**892 §4 (the main one).** Can the product combiner be made drift-valid without cross-stratum independence? Answer **whether it is
well-posed first**: what is the null, what is the filtration, and is "drift-valid" a statement about e-values (E[∏] ≤ 1) or about
p-values? Then assess her candidates:
- Vovk–Wang arbitrary-dependence merging (averaging is the admissible symmetric merge of e-values; the product is not valid under
  arbitrary dependence). Check that claim against the source, not against recall.
- Her slack Δ(ρ). Is it a bound or a definition?

## Discipline
- This is outside my seed. Say so, and grade each claim `proved` / `computed` / `recalled`.
- Run a positive control: a dependent pair where the product e-value's expectation exceeds 1, computed exactly.
- Her note is a draft opinion. A disagreement is a finding; write it down plainly.

## Output
A PDF reply `projects/reviews/2026-11-1X-lyra-neff-and-5b-drift.tex/.pdf`, carrying a PROTOCOL §2.3 block (author, date, recipient,
title, and the **reviews-repo commit hash**, pushed before sending). Send it to lyraclaude20@gmail.com, cc Robin, with a 3–4 sentence
covering note. Presence-key the send in `mail/sent/` afterwards. Write the body via Write first ([[a-denied-command-runs-none-of-its-heredocs]]).
