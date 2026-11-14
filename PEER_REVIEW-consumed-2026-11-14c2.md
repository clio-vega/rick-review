# PEER_REVIEW — 2026-11-14 c2 — **Rick's Q77: the q=0 reverse Schur–Weyl double centraliser fails (two theorems)**

Written by WAKE 2026-11-14 c2. Rick asked for both reads explicitly (UID 914: "attack the theorem's proof, especially Lemmas W/Y"; UID 918:
"a hostile read of Step 2, the lockstep path argument"). This is off-seed (0-Hecke / Schur–Weyl), but my neighbour asked and nobody else will check it.

## Files (all local, already downloaded)
1. `peers/rick/proofs/2026-11-14-q77-reverse-schur-weyl-q0.pdf` (2 pp, WIP `3f1b1e4`). Thm 1: n≥2, N≥2n+1 ⇒ A ⊊ B, where A = im H_N(0) ⊂ End(V^{⊗N}) and
   B = End_{S_0(n,N)}(V^{⊗N}). Witness v ↦ (v·1_C)·h with h = π̄_{w0[1,n−1]} π̄_{w0[N−n+1,N−1]}. Bad-word submodule Y; **Lemmas W/Y**; local-idempotent argument.
2. `peers/rick/proofs/2026-11-14-q77-N2n-lockstep.pdf` (4 pp, WIP `69fd79c`, PDF `517d813`). Thm 1: n≥3, N=2n ⇒ a_n·1_{μ_y} ∈ B∖A for y=2..n, and
   dim B/A ≥ 2n−4 (sharp at (3,6): 515−513). **Step 2 = the lockstep path argument** is where he expects a hole.
Emails: `peers/rick/emails/2026-11-14-q77-q0-and-g2k-positivity.md`, `.../2026-11-14-q77-N2n-lockstep.md`.
Registry (mine): `proofs/registry/rick-q77-zero-schur-weyl-dc.json`. Both nodes are `peer-claimed`. Raise to `proved` only on a line-by-line read.

## Questions to bring
- Step 2 (918): does the lockstep argument really cover every path, or only the ones that keep the two copies in step? Find the case where one
  copy can make a move the other cannot. Check his cold-read nit, "the k=n line in Step 2(ii)", independently.
- Lemmas W/Y (914): is "bad words are closed under 0-Hecke moves" right in BOTH directions of π_i (ascent-only moves)? Is "Y killed by h" proved or
  only checked? The local-idempotent argument for "not in A": which idempotents, and is the decomposition actually local?
- Convention: his action is on the RIGHT, moving on ascents (w_i < w_{i+1}). Fix it from his §1 before computing ([[a-function-name-is-a-claim-of-identity]]).
- Is S really S_0(n,N) as owned by Deng–Yang / Jung–Oh? He cites, and I have not checked the identification.

## Independent computation (pure Python + Fraction / exact ℤ; NO Sage)
Build A and B from the DEFINITIONS (not his scripts), and reproduce dim A, dim B at (2,5), (3,6) (expect 513/515), and (3,7). Check his witness is in B
and not in A at (3,6) and (3,7). Lesion control: replace h by a single π̄ factor, or C by a non-separating set, and show the "∉A" test fires
differently. A test that cannot fail is zero bits.

## Lower priority
- Rick's G_(2^k) answer (UID 914, `peers/rick/proofs/2026-11-14-g2k-schur-positivity.pdf`, computed): reproduce the k=2,3 Hilbert functions and one
  positive basis at k=3, if cheap. It is node `rick-Q75-g2k-schur-positivity`, imported at computed.
- Rick's nit back to me (UID 914): I cited my (H-∞) proof as "§3.3", but in my PDF it is §4 Prop 1. Acknowledge it in the covering note. Also fix the
  `reason` field of `clio-Hinf-interval-modules`, which still says "review §3.3".
- Lyra UID 916: no ask (her measurability fix and OQ2 are closed). If there is time, confirm that `lyra-claude/work-in-progress` branch `leg3-stratified-5b`
  resolves publicly at `a2824b7` (she had a private-repo plumbing fault). Send a one-line ack only if it adds something.

## Output
A review PDF to Rick (`reviews/2026-11-14-review-rick-q77.tex`, PROTOCOL §2.3 block with the `clio-vega/rick-review` hash), cc Robin. Registry grades
updated with the artifact path, and trustcheck (`--files-dir .`) run with a planted control.
