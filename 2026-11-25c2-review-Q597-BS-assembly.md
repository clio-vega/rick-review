# Internal review, 2026-11-25 (REVIEW c2): Q597 BS(L) assembly, cold read

Reviewer: Clio, in a separate slot, reviewing my own PROVE 2026-11-25 c2 output.

- **File reviewed:** `proofs/2026-11-25c2-Q597-BS-assembly.tex`, commit `a826964` of `clio-vega/proofs` (7 pp.).
- **Registry:** `proofs/registry/q585-ybe-train-vs-commutor.json`.
- **Mail:** the high-water mark at the start of this slot was UID 953. I listed every UID above 952 with `check --all --limit 3000`, which returns 953 messages. The only one above 952 is 953, my own health ping. There is no neighbour mail; Rick has made no commits since 11-14.
- **Code for this review:** `reviews/code-1125c2-BS/`. It holds `indep_bs_census.py`, `mos_coverage.py`, `mos_images.py`, `bridge_all.py` and `bridge_lesion.py`, written for this review, together with their `.out` files.

## Verdicts in one place

| node (PROVE c2) | PROVE's grade | review | why |
|---|---|---|---|
| `Q597-both-diverge` (Lemma both) | proved | **upheld** | §2.1: every line checked; all the cited lemmas cover the scope used |
| `Q597-dichotomy` (Prop dich) | proved | **upheld** | §2.2: the Thm local table really does have exactly two re-run rows for an `(1,a_T)` contact |
| `Q597-BS-L-all` (Thm bsall) | proved | **upheld, with condition C1** | §2.3: the case-b citation is right in substance, but the *domain* of the cited Thm bs is worded through "clean journey", an I-dependent notion |
| `Q597-BS-L` | computed → proved | **promotion upheld** | via `Q597-BS-L-all` |
| `Q597-readout-L` (Thm roleL) | proved | **upheld** | §3: it uses only Δ_L; Lemma mixed is avoided |
| `MC-iff-G3prime` (Prop mcE) | proved | **upheld, with condition C2** | §3: PQ-RIGID needs both composite boards in the class 𝓕; the proof should say so |
| `Q597-Role-from-BS-L` | proved "as corrected" | **upheld as corrected, with condition C3** | the node's `file` is the 11-22 c2 tex, whose Thm main still states the uncorrected implication |
| `Q597-Role`, `Q597-block-swap-BS` | stay computed | **agree** | the hidden-hypothesis finding is correct (§3) |
| `Q597-G3prime` | computed | **agree** | independent re-count: §5 |
| (Mos), the standing hypothesis (no node) | "evidence: bridge 520/520" | **evidence overstated, then closed at size 5** | the bridge covered 520 of the 1979 census tilings and missed 1159 one-move images. Re-run on all 1979: 1979/1979 pass (§4). Size 6 is still open |

**No demotions.** Every promoted node's theorem covers the scope it claims. The four conditions (C1–C4) are wording and registry fixes. I applied them in this slot (§6). The one substantive finding is about the *evidence* for the standing hypothesis (Mos). The cited bridge never checked most of the boards that (Mos) is about. I have now checked them at size 5, and they pass.

## 1. Summary of the claim, in one sentence

Under (S) (termination, the engine rule, and (Mos), the hypothesis that M0, M0·J_x and M0·J_y are Purbhoo–KT mosaics), every diverging B/C pair is exactly one of case a or case b. In both cases the role L satisfies the block swap BS(L). Theorem main (11-22 c2) silently assumed (MC), so (Role) is only conditional. Given PQ-RIGID, (MC) for a pair is equivalent to Δ_E = Δ_L.

I can state it in one sentence, and its four parts are logically independent of each other.

## 2. The BS(L) chain, line by line

### 2.1 Lemma both

**Part (1): divergence happens at a step.**
- p is the length of the longest common prefix, so A and A′ both stand on R_p.
- Lemma class (`2026-11-20-Q597-no-repeat.tex`) applies to *every* R_k, including a terminal one. R_p is reached by the W1 prefix steps, so η_T(u_p) ≠ 0. Hence R_p has the nest-A class or T's class 1.
- Lemma term (`2026-11-22c2-Q597-role.tex`, l.234–241) then shows that the stop test agrees on the two boards:
  - packed_at(T′, R) is None, because R carries the nest-A edge or the T edge and never T′'s edge;
  - nest A is the source, so it is skipped;
  - nest T's cells are untouched by J_o, which changes only nests A and T′.
- Both "one stops, the other steps" and "both stop" contradict maximality or divergence. ✔

**Part (2): divergence is mutual.**
- Thm fc gives a tile u ∈ H_p ∩ W_y.
- u ∈ M0 lies in H_p, so J_x removes u at step p. By Lemma nr it is never re-created, so u ∈ W_x.
- J_y removes u at some step j.
- If role y did not diverge, Lemma dinv would give X_j∖Y_j = M0∖M0·J_x ∋ u, so u ∉ Y_j.
- But the identical step j has u in its hexagon. By Lemma U a step's hexagon lies on its board, so u ∈ Y_j. Contradiction. ✔
- *Scope note.* Lemma U and Thm fc need M0·J_x to be a mosaic as well as M0. That is why (Mos) has to name all three boards. The WSlast Thm bs named only M0 (`2026-11-25-Q597-WSlast.tex` l.138), and the assembly correctly widens it.

### 2.2 Prop dich

- Lemma both supplies the hypotheses of Thm fc on both roles. Thm fc then gives (FC≤) on both, and Thm share gives (Share). Its setting (`2026-11-23-Q597-share.tex` §1) is exactly "both roles diverge with a step on both boards".
- Prop orient then gives a unique L.
- The Thm local table (`2026-11-22-Q597-first-contact.tex` l.107–125) has, for A at (1,a1), re-runs (1,b) in two rows and (1,a0) in two rows, and nothing else. By Σ-symmetry the same holds for target C.
- So "case a or case b, nothing else" is a correct reading of a proved exhaustive table. ✔

### 2.3 Thm bsall: does each cited theorem cover the scope?

**Case a.** Thm casea (`2026-11-23c2-Q597-casea.tex` l.115) has the hypotheses "(FC≤) on both roles, L's re-run takes (1,a_{T′})". Prop casea, which it invokes, also needs (Share), and Prop orient needs (Share) to define L. The assembly supplies (Share) in Prop dich, so the scope is covered. ✔
- *Minor:* Thm casea's own statement omits (Share) even though its L presupposes it. It is harmless here.

**Case b.** Thm bs (`2026-11-25-Q597-WSlast.tex` l.137) is stated for *geometric records*, which l.37 defines as "a role of a diverging B/C pair whose **clean journey** A (toward T) is at (1,a_T) at its contact and whose re-run takes (1,b)".
- "Clean journey" is defined in the 11-22 c2 setting (l.44) as *the role on I's side*. That is an I-dependent notion, and the whole point of this assembly is to avoid it.
- Read literally, then, Thm bs covers only the case-b pairs whose L is the I-side role, and identifying the two is (Role), which is now known to need (MC). The literal citation is circular.
- In substance it is not. The intended definition is the one in Remark reindex (11-22 c2, l.188ff): "a diverging B/C pair together with its role L, when L's re-run takes b".
- I grepped the WSlast tex: "clean" occurs **once**, in that definition line, and I or "one-sided" occur nowhere in its proofs.
- **Condition C1:** add a dated erratum to the WSlast definition: "clean journey A" → "journey A of the role (the role L of Prop orient)".

**Grading by tree walk** (in the JSON, not the md):
- No `proved`/`lean-verified` node in the registry has a non-proved `premise` child. I checked this by walking the whole tree, all 195 nodes.
- The descendants of `Q597-BS-L-caseb`, `Q597-Ca`, `Q597-Share`, `Q597-orientation`, `Q597-FC-le` and `Q597-local-contact-classification` are all proved. The only exception is `Q597-Share-box`, a computed *attempt* and not a premise.
- *But the tree under-records the dependencies:*
  - `Q597-BS-L-all` lists only `Q597-both-diverge` and `Q597-dichotomy` as children, and `Q597-dichotomy` has no children at all.
  - Its real premises are `Q597-Ca`, `Q597-BS-L-caseb`, `Q597-orientation`, `Q597-Share`, `Q597-FC-le`, `Q597-local-contact-classification`, `Q597-termination-agrees`, `Q597-board-difference-invariant` and `Q597-no-recreation`. They sit elsewhere in the tree, so a tree walk from the node cannot see them. I looked each one up by id: all are proved.
  - The registry has no cross-reference field, so I recorded the list in the node's `approach` text (**C4**).
- **(Mos) is not a node.** It is the one non-proved input of the whole chain, and it appears only in prose. See §4.

## 3. The hidden hypothesis, and Thm roleL / Prop mcE

**The finding is correct.**
- Lemma mixed (11-22 c2 l.70–76) assumes M0·J_x·J_y^x = M0·J_y·J_x^y.
- Thm main's proof (l.140) opens with "By Lemma mixed we may compute Δ in the role L", and its hypothesis list (l.132–138) does not include commutation.
- Without commutation, Δ_L is all that the role-L computation gives. I = supp Δ_x ∪ supp Δ_y also involves Δ_E, which nothing controls.
- So "I = ∅ in case a" and "I one-sided in case b" are proved only under (MC). The same goes for the last sentence of Thm casea. This is the [[a-cited-lemmas-hypothesis-can-be-the-goal]] pattern, caught by the author's own re-read. It deserves credit.

**Thm roleL.**
- Its parts 1–2 use only the step-sum Δ_L = Σ_{m_B}δ − Σ_{m_A}δ. The common prefix and suffix are identical steps, so they have identical removed/created triangles and identical δ.
- It also uses 11-18 Thm red, with G5 supplied by Lemma side.
- Lemma N needs only BS and the configuration table. Lemma mixed is not used. ✔

**Prop mcE.**
- Net deltas compose, so P12 − P21 = (Δ_y − Δ_x) keywise, which gives same pq ⟺ Δ_x = Δ_y. PQ-RIGID then gives equal boards. ✔
- **Condition C2:** PQ-RIGID (`2026-11-17-PRIGID.tex`, Thm pq) is stated for S, S′ ∈ 𝓕. The proof should say why the two composite boards are in 𝓕, as Thm cond of the 11-17 c2 tex does with its pool hypothesis. The PRIGID tex (l.41) says engine mosaics lie in 𝓕 by the 11-16 degree lemma. One clause citing that suffices.
- **Condition C3:** `Q597-Role-from-BS-L` keeps the grade *proved* for the corrected implication (… & boards equal ⇒ (Role)). Its `file` field, however, points at the 11-22 c2 tex, where Thm main still states the uncorrected one, and Thm casea's last sentence (11-23 c2) inherits it.
  - The assembly says "the file itself is not rewritten". Not rewriting is fine; a dated erratum line in each of the two texs is still owed, as was done for WSlast.

## 4. (Mos): what the evidence covers

(Mos) is Thm bsall's explicit hypothesis. Its evidence is the census bridge, `code-1124c2-Q597/bridge.py`, which gives 520/520 and 719/719.
- `bridge.py` iterates the distinct M0 of `roles5.pkl`, which are the states of pair records: states with ≥ 2 nest-A corners.
- Thm bsall also needs (Mos) for M0·J_x and M0·J_y. These are census states too, since the closure is closed under moves, but they may have only one corner.

`mos_coverage.py` counts the distinct tilings in the uncapped closure:

| count (size 5, uncapped closure) | value |
|---|---|
| states | 5194 |
| states with ≥ 2 corners (every one has exactly 2) | 779 |
| distinct tilings, all states | **1979** |
| distinct tilings, ≥ 2-corner states (= bridge.py's set) | **520** |
| distinct one-move images M0·J_T of pair states | 1267 |
| ... of which **outside** the bridged 520 | 544 (to B) + 615 (to C) |

So the bridge's 520/520 **does not cover** M0·J_x or M0·J_y in most pairs. The assembly's sentence "its evidence: … the exact census bridge 520/520" overstates the coverage for two of the three boards that (Mos) names. (1979 is the mosaic count in `2026-11-17-PRIGID.tex`, which pooled the 1979 into 𝓕, not into the KT bridge.)

**Closed in this slot.** `bridge_all.py` runs PROVE's `bridge.py` logic, unchanged, on all 1979 tilings. I exec'd the source with only its pickle input replaced. The result: **1979/1979** are `build_mosaic(n, ℓ)` up to translation, with every cell a Purbhoo-chirality KT piece and consistent labels (`bridge_all5.out`).
- *Negative control* (`bridge_lesion.py`): 20 bridged boards, each with one square translated by (1,0,0,0). The 20 mutated boards fail; the 20 originals pass. The injected instrument sees failures.
- So at size 5, **(Mos) holds on every census board**, exhaustively.

At size 6 the same gap is open. The 5525-state "fresh chunks 3–6" of the PROVE census are **not** covered by the 719/719 bridge, which ran on the 11-22 c2 subsample (chunks 0–2). The size-6 BS(L) census rows are therefore data on boards for which (Mos) itself is unchecked. That is no error in a theorem. It is a gap in the evidence for the hypothesis, and it should be stated next to the 1232/1232. A follow-up for PROVE: run `bridge.py` on chunks 3–6.

**Trust, honestly.**
- Thm bsall is a proved implication (S) ⇒ BS(L). The `proved` grade is right for that implication, and the registry's convention matches (Thm bs had the same standing hypotheses).
- BS(L) *as a fact about the program* is no better than (Mos):
  - on the size-5 census, it is now exhaustively computed for all 1979 boards;
  - in general, it rests on Purbhoo 0705.1184 §2.4 as cited by PROVE. I did not re-read §2.4 in this slot.
- Downstream nodes must not quote BS(L) without the "(Mos)" qualifier.

## 5. Independent census re-count

`reviews/code-1125c2-BS/indep_bs_census.py` shares with PROVE's `bsall.py` only two things: the census seeds (`code-1114c2-Q590/common.py:census`, the definition of the census) and the engine (`migrate.py`).
- It does not import `diverge.py`, `zonetest.py`, `q597lib.py` or `align.py`.
- The following are all written fresh:
  - the uncapped state closure (PROVE uses a cap-60 sampler);
  - the step log;
  - the (class, type) typing;
  - the common prefix;
  - the L / case classification;
  - MC as tile-multiset equality;
  - a direct test of the case-a two-step rigid swap;
  - a B/B control arm.

| check | PROVE (`bsall5.out`) | independent (`indep_bs_census5.out`) |
|---|---|---|
| states | 5194 (cap-60 sampler) | **5194** (uncapped closure) |
| ordered B/C pairs | 1558 | **1558** |
| diverging / non-diverging | 779 / 779 | **779 / 779** |
| both roles diverge (Lemma both (2)) | 779/779 | **779/779** |
| both journeys step at p (Lemma both (1)) | 779/779 | **779/779** |
| exactly one L | 779/779 | **779/779** |
| case a / case b / leftover | 258 / 521 / 0 | **258 / 521 / 0** |
| case a: middle is a two-step rigid swap (c−α)(a+γ) | (part of `bs_test`) | **258/258** |
| composite boards equal (MC), all B/C pairs | 1558/1558 | **1558/1558** |
| control: B/B unordered pairs, boards equal | 339 commuting / 440 not (Step 0) | **339 / 440** |

Every count agrees. The uncapped closure reproduces 5194, which confirms the earlier note that the cap-60 sampler loses nothing at size 5 ([[a-cap-that-is-never-reached-is-not-a-sample]]). The B/B arm shows that the MC comparison can come out false.
- *Not done:* I did not re-test case-b BS(L) with my own block-swap tester. Its rigid-translate comparison is the same kind as the case-a one above, which passed. I also ran no lesion of the case-a swap test (for instance, a wrong sign on α). The rigid-swap count is evidence only to the extent that set equality of translated tiles is strict, which it is by construction.
- I also did not re-run Δ_L = Δ_E with my own readout. Given PQ-RIGID it is equivalent to the MC column, which I did re-run.

## 6. Edits made in this slot

All committed to `clio-vega/proofs` (commit hash in the email).
- `2026-11-25-Q597-WSlast.tex`:
  - a dated erratum (C1) for the "clean journey" wording in the definition of a geometric record, and for (Mos) needing M0·J_o;
  - fixed the unbalanced `` quotes in PROVE c2's erratum line ("``Open item", "``rest on (Share) alone").
- `2026-11-22c2-Q597-role.tex`: a dated erratum after Thm main for the missing commutation hypothesis (C3).
- `2026-11-23c2-Q597-casea.tex`: a dated erratum after Thm casea; its last sentence is conditional on (MC) (C3).
- All three rebuild with 0 errors and 0 undefined references.
- Registry: dated REVIEW annotations on `Q597-BS-L-all`, `Q597-both-diverge`, `Q597-dichotomy`, `Q597-readout-L`, `MC-iff-G3prime` and `Q597-Role-from-BS-L`.
  - These include C4, the list of premises that are not tree children, and the (Mos) coverage result.
  - **No trust value changed.**
  - Backup: `q585-ybe-train-vs-commutor.json.bak-1125c2-review-pre`; formatting kept at indent=2, ensure_ascii=False.
- **C2** (one clause on 𝓕 in Prop mcE) is recorded here and in the registry note. I did not edit the PROVE c2 tex itself; it belongs to its author's next pass.

## 7. Step 0 and the lesion: brief remarks

- **Step 0 (commutor loop).** The caveat is honest and correctly placed: a cell-level loop does not test Purbhoo §5.2's flock-level monodromy. Grade: computed, `attempt`. Agree.
- **Frame lesion (−α shift, 180/253 C-records fire).** The lesion is live, and it points at the one theorem whose proof uses (Mos). The claim "each moved frame is a frame no mosaic has" is asserted, not checked; it would be worth one line of code.

## 8. Questions and next steps

1. **(G3′).** This is now the whole of (MC) on B/C pairs. Since Δ_L is known in closed form, one route is to show that E's re-run is determined by L's block swap through the shared square (Thm share). That route goes through the two contacts' common tile rather than through E's own middle, which the dead 11-19 inverse-BS attempt tried and failed.
2. **(Mos) as a theorem.** Is "every state reachable by single-rhombus migration from a canonical board is M0(ℓ) for a KT puzzle ℓ" a statement of Purbhoo 0705.1184 (migration preserves mosaics), or only the bijection at the level of complete flocks? The answer decides whether (Mos) is a citation or a lemma to prove. Read §2.4 and §3 for this.
3. Bridge the size-6 fresh chunks and the one-corner size-6 states (§4). `bridge_all.py` does this with SIZE changed.
