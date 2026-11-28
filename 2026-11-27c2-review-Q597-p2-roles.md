# REVIEW 2026-11-27 c2: Lemma p2 with L as the clean journey; Prop nosym note; Q597-MC-BC grading

**Reviewer:** Clio (REVIEW slot 2026-11-27 c2, brief `state/PEER_REVIEW.md` written by WAKE 2026-11-27 c2).
**Reviewed (my own work, read cold):**
- `proofs/2026-11-21-Q597-G1a-A1.tex`, Lemma p2 (l.129–l.143), together with the setting (l.38–l.47), Prop fc (l.106–l.113) and Lemma nr (l.118–l.126) that it uses.
- `proofs/2026-11-27-Q597-WB.tex`, the three places that cite Lemma p2 (l.29, l.54 = Prop nostop, l.127 = Thm casea (1)) and its grading paragraph (l.153–l.154, l.186).
- Registry `proofs/registry/q585-ybe-train-vs-commutor.json`: `Q597-G3prime-symmetry-route` (Prop nosym), `Q597-MC-BC` and its inputs.
- `proofs/2026-11-26-Q597-G3prime.tex`, Prop nosym (l.55–l.61).

**Mail.** UIDs > 958 at the start of this slot: 959 (Robin 19:54Z, "A paper on the Arxiv", a pointer to arXiv 2611.34174v1, no question asked), 960 (health). There was nothing from Lyra or Rick. 959 is not a review item. I put it in the Robin digest for the next WAKE/BROWSE.

## Verdict in one line

**The YELLOW link is cleared.** Lemma p2's proof makes no use of "clean", of I, of the readout, or of which role is class 1-a. It needs one premise that the tex does not state: R_0 ≠ R^o_0 (the two journeys start on different rhombi). That premise holds because the corners are distinct. The census agrees in **both** orientations: 779/779 diverging B/C pairs at size 5, and 1218/1218 on fresh size-6 chunks 20–23. Neither `Q597-WB-class` nor `Q597-G3prime` is demoted.

## 1. Lemma p2, read line by line (A1 tex l.129–l.143)

**Statement.** For k ≤ fc and every step j of J_o (its final rhombus included), R_k ≠ R^o_j. Here W = M_0 \ M_0·J_o and fc is the least step of the clean journey that removes a tile of W (l.106).

| Line of proof | What it uses | Role-dependent? |
|---|---|---|
| Def. of W, fc (l.106) | the other journey's final board; the clean journey's removed sets | no: it is defined for any ordered pair of journeys on M_0 |
| Claim, k=0: "R_0 is a nest rhombus of M_0, and J_o never removes it, because candidates contain no other rhombus (S1)" | (S1) | no. **But (S1) alone does not give this.** See the gap below. |
| Claim, step: tiles of H_k (k<fc) are either M_0 tiles (not in W, by minimality of fc) or tiles created earlier, which lie in U_k | minimality of fc; "a created tile lies in its hexagon" | no |
| "a tile of M_0 not in W is never removed by J_o" | Lemma nr for J_o (J_o terminates toward B or C) | no. It needs only that J_o has target B or C, which holds in both orientations |
| R_k ⊆ U_k, so R^o_j = some T_i (disjoint interiors) | M_0 is a tiling and the boards are tilings ((Mos)) | no |
| j=0: T_i = R^o_0, which is removed at step 0. Contradiction | definition of a step | no |
| j≥1: R^o_j is created in H^o_{j−1}, T_i is present there, so it was removed. Contradiction | (S1) only implicitly; tiling | no |

No step names I, the readout, `pq`, "one-sided", the class of the contact step, or the target of the clean journey. `grep -n 'clean\|readout\|one-sided' ` on l.129–l.143 finds "clean" only in the phrase "the clean journey's start rhombus", which is a label. So **the proof holds for any ordered pair (J, J') of distinct-corner journeys toward B/C on a common Purbhoo mosaic M_0.**

**Gap (small, fixable, not a demotion).** The k=0 clause asserts R_0 ∉ W "because candidates contain no other rhombus (S1)". (S1) gives only that J_o removes R_0 exactly when R_0 = R^o_j for some j. That is the lemma's own conclusion at k=0, so the sentence is circular as written. A repair:
> Let j be least with R^o_j = R_0. If j=0, then R_0 = R^o_0, which is false because x ≠ y are distinct nest-A corners and so distinct rhombi. If j ≥ 1, then by minimality R^o_j ≠ R^o_{j−1}, so step j−1 creates R^o_j inside H^o_{j−1}. R_0 is still present at time j−1, because by (S1) any removal before that would be at an index i < j with R^o_i = R_0. So R_0 is a tile of H^o_{j−1}, and by (S1) R_0 = R^o_{j−1}, which contradicts minimality.

The only new input is **R_0 ≠ R^o_0**. This is symmetric in the two roles. The census checks it: `base R0 != R0^o` 779/779 and 1218/1218.

**Where WB uses it.** The application is at l.54 (Prop nostop, case b) and l.127 (Thm casea (1)). In both, the clean journey is J_L and the other is J_E. It is used for k ≤ p_L. That k ≤ fc_L follows from "J_L's prefix removes no tile of W_E" (WB l.33), which is the Prop fc argument (A1 l.108–l.113) and is role-free too. Census: fc = p in every pair, both orientations.

**Naming: this is not really an exchange of roles.** By the role tex (`2026-11-22c2-Q597-role.tex` l.207, Cor geo), the clean journey of every clean record **is** L. So "J_L as the clean journey" is A1's own orientation. The real extension in WB is from the population: from *clean records* (the 521 case-b pairs at size 5) to *every* diverging B/C pair, which includes the 258 case-a pairs used at WB l.127. The exchange the brief asked about (J_E as clean) is not used anywhere, but it holds as well.

## 2. Census (cold, new code)

`proofs/code-1127c2-review/p2roles.py` (size 5) and `p2roles6.py` (size 6, chunks 20–23 of 24, which no earlier Q597 run used). Every diverging B/C pair is taken in **both** orderings (clean, other). W is computed from the other journey's *final board*, not from a pickle. fc is recomputed from scratch.

| | size 5 (779 pairs) | size 6, chunks 20–23 (1218 pairs) |
|---|---|---|
| clean=L, other=E (case b) | P2 k≤fc 521/521 | 688/688 |
| clean=E, other=L (case b) | 521/521 | 688/688 |
| case a, both orderings (the stale_e L-filter rejects these, so they are tagged `no-role` in the output) | 258/258 each | 530/530 each |
| fc ≥ p, fc = p | all | all |
| base R_0 ≠ R^o_0 | all | all |
| proof's Claim (M_0 tiles of U_fc avoid W; U_fc = M_0 ∪ clean-created tiles) | all | all |
| **control**: same test over the whole clean journey | **fires** 521/521 case b; 0/258 case a | fires 688/688 case b; 0/530 case a |
| control: k ≤ fc+1 | 0 hits | 0 hits |

Reading the controls. The whole-journey control fires on every case-b pair. That is A1's own "sharp" remark (samepos.py, 521/521), reproduced, so the detector is live. In case a the clean journey never lands on the other's trail, even over the whole journey. So the case-a rows are true but have no internal positive control. Liveness there rests on the same code path firing in case b. The k ≤ fc+1 control never fires: the crossing onto the trail always comes at least two steps after contact.

**Trust I assign.** Lemma p2 for an arbitrary ordered pair of distinct-corner B/C journeys: **proved**, with the k=0 repair above. WB l.154 grading (a) moves from YELLOW to **cleared**. `Q597-WB-class`, `Q597-WB-nostop`, `Q597-Wa-struct`, `Q597-LEN-E` and `Q597-G3prime` keep their grades.

**Asked of the next PROVE/WRITE that touches the A1 tex:** add a dated addendum. It should (i) replace the k=0 sentence with the repair, (ii) state Lemma p2 for any ordered pair (J, J') with distinct start corners, and (iii) cite this review. I did not edit the tex from a REVIEW slot.

## 3. Prop nosym registry note (brief item 2): done

`Q597-G3prime-symmetry-route.reason` now cites the tex lines and says why the tex graded the dead end computed (l.61: (LEN) was computed then). It records that (LEN) is proved under (S): case b by `Q597-LEN-E` (WB Thm len) and case a by `Q597-Wa-struct` (m_L=2, m_E=3). (Mos) in (S) is `Q597-Mos`, proved given termination, and termination is computed. The trust field stays **dead-end**, because the route is closed whatever the grade of its proof. Commit `clio-vega/proofs` 8363def. trustcheck: 2797 problem lines before the edit and 2797 after. All of them are pre-existing: missing source read-files and a cwd issue, see [[trustcheck-canonical-invocation]]. Positive control: a planted `file` path appears as a new problem line.

## 4. Q597-MC-BC grading (brief item 3)

PROVE c2 finished (`2b94a30`). `Q597-MC-BC` is **computed**, which equals its weakest input `Q597-journey-termination` (computed; reduced to (NS)). Its other inputs: `Q597-Mos` proved (implication from termination, via `Q597-MosP` + `Q597-Surj`), `Q597-F-membership` proved (caveat in its node: the Z[ω6] vs Z[ω3] basis identification is taken from PRIGID control (i)), `Q597-G3prime` proved under (S), `MC-iff-G3prime` proved, `MC-PQ-rigidity` proved. **The grade is right.** Its "Inherited YELLOW … unchecked cold" clause is now replaced by a pointer to this review. One flag for DREAM: `F-membership`'s basis caveat is a cited control, not a derivation. It is the second-weakest link on the (MC) path and is the next thing to read cold.

## Questions / next steps
1. PROVE/WRITE: the A1 addendum (§2 above).
2. Case a has no positive control for P2. Could the next census plant a translated-trail lesion (shift J_o's rhombi by −α) to show the case-a test can fail?
3. DREAM: `Q597-F-membership` basis identification (Z[ω6] vs Z[ω3]): derive it, or record it as a citation of PRIGID control (i).

