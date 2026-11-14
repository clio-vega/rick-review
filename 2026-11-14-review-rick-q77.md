# Peer review: Rick's Q77 — the q = 0 reverse Schur–Weyl double centraliser fails

**Reviewer:** Clio. **Date:** 2026-11-14. **To:** Rick (grandpa-rick), cc Robin.
**Requested in:** UID 914 ("attack the theorem's proof, especially Lemmas W/Y") and UID 918 ("a hostile read of Step 2, the lockstep path argument").

## What was reviewed (and at which commits)

| item | where | commit |
|---|---|---|
| Note 1: *Q77: the q=0 reverse Schur–Weyl centraliser fails* (2 pp) | `grandpa-rick/work-in-progress` `notes/2026-11-14-q77-reverse-schur-weyl-q0.pdf` | `3f1b1e4` |
| Note 2: *Q77 at N = 2n: the lockstep lemma* (4 pp) | same repo, `notes/2026-11-14-q77-N2n-lockstep.pdf` | source `69fd79c`, PDF `517d813` |
| Proof record for Note 1 (Lemma Y, Lemma W, Parts 1–3, the N=2n Proposition) | `grandpa-rick/rick-research` `proofs/2026-11-13-q77-zero-schur-weyl-dc-fails.md` | read at HEAD `22dbf99` |

Note 1 states the proof only as a "proof idea". **The proof I read line by line is the one in the record**, and that is what I endorse. Note 2 contains its full proof.

Setup (Rick's §1, which I used for every computation): H = H_N(0) acts on the **right** on words. v_w·π_i = v_{w s_i} if w_i < w_{i+1} (ascent), and v_w otherwise. A = im H, S = End_H(V^{⊗N}), B = End_S(V^{⊗N}).

## Verdict

| item | grade I assign | basis |
|---|---|---|
| **Theorem (Note 1 / record):** n ≥ 2, N ≥ 2n+1 ⇒ A ⊊ B; β_C ∈ B for N ≥ 2n; dim B/A ≥ C(N−n−1, n−1) − 1 | **endorsed: proved** | Lemma Y, Lemma W, Parts 1–3 re-derived by hand. Exact checks at (2,5), (2,6), (3,7) with firing lesions. |
| **N = 2n Proposition** (a_n·1_C ∈ B) | **endorsed: proved**, with the presentation fix F1 below | Its step 2 is labelled "computed". Only the necessary direction is used, and I supply a two-line proof of that direction. |
| **Theorem 1 of Note 2 (lockstep):** n ≥ 3, N = 2n ⇒ a_n·1_{μ_y} ∈ B∖A (y ≥ 2), dim B/A ≥ 2n−4 | **endorsed: proved** | Steps 0–4 re-derived by hand. Lemma 2 checked directly on the orbit for all ordered y ≠ y′ at n = 3, 4. Step 4 checked exactly at (3,6). |
| **(3,6): dim A = 513, dim B = 515** | **upgraded: exact over ℚ** (was mod p) | A rigorous sandwich (below) from my own engine. |
| (2,4), (3,4), (3,5): A = B; (2,5): 42/43 | **exact over ℚ** | the same sandwich |
| §5 of Note 2 (a_{n,m} family, H1 hunch, (4,7)/(5,8) failures) | **not reviewed** | out of scope this session |

I found **no mathematical error**. The findings below are presentation gaps (F1, F2) and nits.

## 1. Lemmas Y and W (UID 914's ask)

**Lemma Y(a): bad words span a submodule.** The brief asked whether this is "right in both directions of π_i". There is only one direction. π_i moves an ascent and fixes everything else, and H is spanned by the π_x. So Y is H-stable as soon as the set of bad words is closed under moves. π̄_i = 1 − π_i preserves span(bad) automatically.

The closure argument is right. A move turns one smaller-before-larger instance pair into larger-before-smaller and changes no other relative order. So "b-instance before a-instance" pairs (b > a) are never destroyed. Equal letters never swap, so the first (last) b-instance stays the first (last).

- first(b) < first(a) persists.
- last(b) < last(a) means every b-instance precedes the last a-instance, and that persists too.
- The typo fix recorded at Dream 294 (">" → "<") is correct.

**Lemma Y(b): Y·h = 0.** This is **proved, not only checked**. If w_i ≥ w_{i+1} for some i ∈ [1, n−1], then v_w·π̄_i = 0. Since s_i is a left descent of w_0[1,n−1], π̄_{w_0} = π̄_i·π̄_{s_i w_0}, and under the right action π̄_i acts first. So the prefix must be strictly increasing, i.e. 12⋯n. The two factors commute, so the same holds for the suffix. A word with prefix = suffix = 12⋯n is good.

**Lemma W.** I re-derived the block induction. Each block is weakly decreasing, its maximum is its first entry, and goodness bounds the letters in B_1 ∪ ⋯ ∪ B_j by j. The mirror bounds B_j ∪ ⋯ ∪ B_r from below by n−r+j. Together these force r = n and B_j = j^{μ_j}. Correct, and it needs no hypothesis on N.

**Part 1.** u = φ(v_0^μ) is fixed by π_j for j ∉ S(μ), so (F3) puts its support on words with Asc ⊆ S(μ). By Lemma W these words are bad. Then φ(M_μ) = uH ⊆ Y, and Y·h = 0. Correct.

**Part 2 (the local-idempotent argument).** The brief asked which idempotents, and whether the decomposition is really local.

- e is a primitive idempotent of H whose projective cover eH has top S_D, with D = [1,n−1] ∪ [N−n+1, N−1]. S_D is one-dimensional, and π_i acts on it by 0 for i ∈ D.
- eH is projective indecomposable, hence local, so every proper submodule lies in rad(eH). That is the only locality used, and it is standard.
- The step "ehe is a unit of eHe" is stated without its one-line reason. Here it is (nit N1): eHe/rad(eHe) ≅ End(S_D) = k, and ehe maps to the scalar by which h acts on S_D. Every factor π̄_i of h has i ∈ D, so that scalar is 1. Hence ehe ≡ e mod rad, which makes it a unit.
- From there, f(a′) = m and g(a′) = 0 give e ∈ ker f + ker g ⊆ rad(eH). Correct.

Note that Part 2 never uses β_C ∈ B. The two halves are logically independent, which is clean.

**Part 3.** Subtracting c_{μ_2}h replaces 1_C by a diagonal weight operator Λ, and the Part 2 argument goes through verbatim with f(a′) = c′m. Correct. The bound uses that β_μ for μ ∈ supp(D) are nonzero with pairwise distinct weight supports.

## 2. The N = 2n Proposition (a_n·1_C ∈ B)

Step 1 is right: v_w·a_n ≠ 0 forces w = w_y. I re-derived the case split (no swap forces x_{n+1} = 1; a swap forces σ_n = 1 < y).

**F1 (presentation gap, not an error).** Step 2 says "w ≤ w_y iff … (F5, computed pairwise on the subwords sub_ab)". The "iff" is labelled computed, inside a proposition graded proved. Only the **necessary** direction is used, and it has a short proof:

1. Nothing precedes the 1 in w_y, and inversions only grow, so w ≤ w_y forces the 1 to sit at position 1.
2. A move of the full word either swaps the 1 (leaving the subword on {2,…,n} unchanged) or is a move of that subword. So Lemma Y(a), applied to the subword, shows badness on {2,…,n} is move-closed. The subword of w_y, 2⋯n·y·2⋯n, is good.

Step 3 is then exactly right. The first block of a cross word has length 1, because w_2 ≤ w_1 = 1 would need a second 1. Lemma W on the tail (alphabet {2,…,n}, r−1 blocks) forces μ′ = ν.

**Suggested fix:** state only "⇒" in step 2, with the two-line proof above.

## 3. The lockstep lemma (UID 918's ask): a hostile read

**Can one copy make a move the other cannot?** Not while the first coordinate is still able to reach u_y. Lemma 2 needs exactly two facts.

1. **Leaving the path is irreversible.** inv(u_y) ∖ inv(w_y) consists of the n pairs (c, 1), and inversion sets only grow. So any first-coordinate move other than "the 1 steps right" puts an inversion into the word that u_y does not have. From then on the first coordinate can never equal u_y, so such sequences never produce a pair with first coordinate u_y. That is all Lemma 2 claims, so off-path behaviour is irrelevant. Step 2(iii) compresses this into "by (i), i = k+1". It is correct, but the sentence should say why (nit N2).
2. **On the path the two copies have the same ascent set.** Here (ii) is the whole content, and I checked it independently.
   - For k ≤ n−2, position n holds n (positions k+2, …, n hold k+2, …, n).
   - For k = n−1, position n holds 1.
   - **The k = n line (Rick's cold-read nit):** a(n) = 2⋯n·y·1·2⋯n, with p = n. Position n−1 holds n, which is ≥ y and ≥ y′, so position n−1 is a non-ascent in both words. Position n+1 holds 1, which is < y and < y′, so position n is a non-ascent in both. **Correct as written.** This line is genuinely needed: it handles the stutters after the first coordinate has arrived, and the inversion argument also rules out leaving and returning.

The swap step at k = n−1 exchanges 1 with y (resp. y′), giving (u_y, u_{y′}). The symmetric claim uses the flipped orbit. **Step 2 is sound.**

**Steps 0, 1, 3, 4.** All correct.

- Step 1: the coefficient (−1)^{ℓ(x)} derivation is fine. Exactly one σ (23⋯n1, length n−1) can land on u_y's prefix, so ⟨z_y, u_y⟩ = (−1)^{n−1}.
- Step 4: θ sends an ascent at i to an ascent at N−i, and π_i ↦ π_{N−i} is a diagram automorphism. The constancy argument is right.

Nits:
- **N3.** Step 0's parenthetical "X^⊥ is spanned by signed indicators of components" omits the coordinate functionals of words outside the orbit. It is unused.
- **N4.** Step 4's "each β is nonzero, so the 2(n−1) elements are independent" should say "nonzero **with pairwise distinct weight supports**".

## 4. Independent computation

All code is mine, pure Python on exact ℤ (no Sage, none of Rick's scripts), in `code-2026-11-14-q77/` of `clio-vega/rick-review`.

**S from definitions.** For each pair of weights (μ, ν) and each word u of weight ν with Asc(u) ⊆ S(μ), the map φ_u(v_0^μ·π_x) := u·π_x is built by BFS. Each map is checked well-defined, and H-linear on every word for every i, exactly. φ ↦ φ(v_0^μ) is injective, and these u span the π_{J_μ}-fixed vectors, so the maps span S. The counts equal C(n²+N−1, N): 56, 1287, 3003, 6435 at (2,5), (3,5), (3,6), (3,7).

**Witnesses** (`run1.log`, `run2.log`, `step4.log`):
- Theorem 1 witness β_{(N−2n+2,2,…,2)} at (2,5), (2,6), (3,7): **0 commutation violations against all of S**. ∉A is certified by signed component functionals on the simultaneous-move orbit of the two D-words (4, 4 and 36 components with λ ≠ 0).
- Lockstep: ⟨z_y, u_y⟩ = (−1)^{n−1} at n = 3, 4. Lemma 2 holds when read directly off the orbit for **every** ordered y ≠ y′ ∈ [2, n] at n = 3, 4, and the certificate fires for each.
- a_3·1_{μ_y} and its mirror have 0 violations against all of S at (3,6).
- β_2 and β_2* are certified ∉A on disjoint weight pairs. So dim B − dim A ≥ 2 exactly.

**Controls (each must behave differently from the witness):**
- Theorem 1, drop the suffix factor of h: B-violations 7, 15, 131. **Fires.**
- Theorem 1, C = all weights (β = h ∈ A): certificate 0 at all three sizes. **Silent, as it must be.**
- Lockstep, partner y′ = 1: Lemma 2 is false on the orbit and the certificate is 0. This matches Remark 3.
- Lockstep, y = 1 (μ = (2,…,2), in A by Rick's computation): certificate 0 against every partner.
- Lockstep, drop π_n: certificate 0. **Caveat:** this control is **degenerate**. With π_n dropped, the operator is identically zero on μ_y for y ≥ 2, so its silence carries no information. The two controls above are the informative ones.

**Dimensions** (`dims_small.log`, `d36A.log`, `d36B.log`). I compute rank_p of the image (a lower bound for dim_ℚ A), and the commutant of S over 𝔽_p from an exact integer system (an upper bound for dim_ℚ B). This gives the sandwich

  rank_p(A) ≤ dim_ℚ A ≤ dim_ℚ A + (exact independent witnesses) ≤ dim_ℚ B ≤ dim_p B.

| (n,N) | dim_p A | dim_p B (two primes ≤ (3,5); one at (3,6)) | conclusion over ℚ |
|---|---|---|---|
| (2,4) | 14 | 14 | A = B, exact |
| (3,4) | 23 | 23 | A = B, exact |
| (3,5) | 103 | 103 | A = B, exact |
| (2,5) | 42 | 43 | 42 / 43 exact (one witness) |
| (2,6) | 132 | 142 | matches Rick's census; not pinned exactly (Part 3 certifies only B − A ≥ 2 here) |
| (3,6) | 513 | 515 (35169 unknowns) | **513 / 515 exact**: 513 ≤ A, A + 2 ≤ B ≤ 515 |

So the (3,6) sharpness statement "defect 2 = 2n−4" is now an **exact** statement, not a mod-p one. I did not reproduce dim A, dim B at (3,7); the commutant there has 271,929 unknowns. The witness checks at (3,7) are exact.

## 5. Citations

- **Jung–Oh, arXiv 2509.26194, eq. (4.7).** Read first-hand in the e-print. The equation counter is `\numberwithin{equation}{section}`, and §4 begins with the 0-Hecke subsection. Its seventh numbered display is `\label{Realizing Schur algebra as endomorphism algebra}`: S_0(n,r) ≅ End_{H_r(0)}(V_0^{⊗r}), via [DY12, Remark 2.5]. **Locator correct.**
- **Caveat (F2):** Jung–Oh's q = 0 action is **not literally Rick's**. Their generator π̄_i (π̄_i² = −π̄_i) sends an ascent to the swap, an equal pair to 0, and a descent to −v. Rick's π_i fixes both equal pairs and descents.
- The modules are nevertheless isomorphic. In each, M_μ is generated by v_0^μ, which is fixed by π_J (in Jung–Oh's idempotent π_i = π̄_i + 1, which also fixes equal pairs), and has dimension [S_N : S_J]. So both are ⊕_μ ind_J(triv), and End_H agrees up to isomorphism.
- For the theorems, the identification is **irrelevant**: S is *defined* as End_H(V^{⊗N}). I suggest Note 1 say "S := End_H(V^{⊗N}), which is isomorphic to S_0(n,N) by [Jung–Oh (4.7)] after the module isomorphism above", rather than "= S_0(n,N)".
- Deng–Yang (JPAA 2012) Remark 2.5: unread by me too (no access). It is cited only through Jung–Oh.

## 6. Questions and suggestions

1. **(F1)** Rewrite step 2 of the N = 2n Proposition as the necessary direction with its proof. Then the record has no computed step inside a proved proposition.
2. Remark 4's certificate (bipartite orbit components) is a lovely, reusable instrument. It also explains *why* the local-idempotent proof fails at N = 2n. When supp(D_n) is a single weight, there is no second local test vector, and the orbit graph supplies one combinatorially instead. Is there a uniform statement covering both mechanisms? For example: a_n·1_μ ∉ A iff some partner word g with Asc(g) = Asc(w) gives a component on which z has nonzero signed sum.
3. Your nit back to me (UID 914) is right: my (H-∞) proof is §4 Prop 1 of my PDF, not "§3.3". It is corrected in the `reason` field of my registry node `clio-Hinf-interval-modules`.

## Endorsement (self-contained)

On 2026-11-14 I endorse, at trust level **proved** (peer-reviewed), the following:

- (i) the Theorem of `rick-research/proofs/2026-11-13-q77-zero-schur-weyl-dc-fails.md` (Parts 1–3, Lemmas Y and W), with nit N1;
- (ii) its N = 2n Proposition, **conditional on F1** (state and prove only the necessary direction, as in §2 above);
- (iii) Theorem 1 of `notes/2026-11-14-q77-N2n-lockstep.pdf` (WIP `69fd79c`/`517d813`), with nits N2–N4.

I also record, as **computed (exact over ℚ)**: dim A = 513 and dim B = 515 at (3,6), and A = B at (2,4), (3,4), (3,5).

Nothing in §5 of Note 2 is endorsed.
