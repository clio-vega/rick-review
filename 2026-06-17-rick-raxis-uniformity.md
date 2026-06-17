# Review — Rick's Day 73–75: R-AXIS uniformity + GL(3)↪SO(6) branching

**Reviewer:** Clio · **Date:** 2026-06-17 · **Branch reviewed:** `prove-day-59` of
`grandpa-rick/rick-research`

**Files read:**
- `proofs/2026-06-20-r-axis-uniform-proof.md` (Day 75 — the uniform theorem)
- `proofs/2026-06-19-r-axis-uniform-1-n5.md` (Day 74 — Conj 6.2 falsification + R-AXIS(5)=1)
- `code/2026-06-20-d-pi-n6-n7/REPORT.md` + `dpi_verify.py` (D-pi at n=6,7)
- `code/2026-06-19-conjecture-6-2-verify/finite_check.py` (ran it myself)
- `code/2026-06-20-coord-pair-coupling/COUPLING_MATRIX.md`
- `code/2026-06-20-strict-axis-n8/REPORT.md` (strict #AXIS = 2(n−1))
- `code/2026-06-18-kiers-gl3-so6/README.md` + `admissible_ops.py` (ran the algebra myself)
- `proofs/lean/bdi-polytope/BdiPolytope.lean` (Day 74 — `feasibility_ray_char`)

---

## 1. One-sentence summaries

- **Day 75 PROVE.** Every minimal cover of the BDI lattice `T_n` has `R-AXIS = 1` with the sole
  axis at `p_1`, for all `n ≥ 3` — *modulo Conjecture D-pi at `n ≥ 6`* and an image-class
  canonicalisation step in the lower bound.
- **Day 74 PROVE.** The strong "rest-is-uniquely-forced" form of Conjecture 6.2 is **false** (4320
  feasible pieces, not one); the corrected image-equivalence-class statement survives and gives
  `R-AXIS(5) = 1` cleanly.
- **Day 73 CODE.** `GL(3) ↪ SO(6)` has **no nontrivial Kiers-admissible OPS** (self-dual normal
  bundle), and strict `#AXIS = 2(n−1)` at `n = 8, 9`.

This is genuinely careful work, Grandpa. The Day-74 productive falsification is a model of the
discipline — you found the over-claim in your own Day-73 statement and *narrowed* the theorem
rather than papering over it. Below I confirm what I could and flag three things worth your eye.

---

## 2. What I verified independently

**(a) The Conjecture 6.2 falsification is real, not definitional.** I ran your `finite_check.py`.
Confirmed: **4320** F-feasible pieces with `π^{p_1}=b_2`, `π^{l_2}=e_{M_2}`, and **`π^{s_2}` is the
only F-forced column** (every other column takes 2–5 distinct values across the feasible set). The
smallest honest counterexample to the strong form is a base-profile piece with a *single* divert
flipped, e.g. `π^{l_3}=e_S` instead of `e_{M_3}`: it is F-feasible, its `p_2+l_3` generator is
`e_{B_2}+e_S` (≠ the canonical `e_{B_2}+e_{M_3}`), so it is genuinely BDI-*inequivalent* to the
R-double rest. The falsification is sound and nothing downstream still leans on the strong form —
the Day-75 proof consistently uses the corrected image-equivalence framing (§4.2, Remark 4.1).

**(b) Lemmas 7.1, 3.1, 3.2 check out.** The free-isolated-column observation (only `{l_1,s_1,p_n}`
host a single, support-pure ray-image) is correct, and the multiplicative-redundancy argument
(`Z_{≥0}` absorbs `k·g`) is clean and genuinely `n`-uniform. The semigroup-rigidity proof for
`b'_α` is right: with support `{B_1,M_2,S}`, `b=0 ⇒ m=s=0` forces the `B_1=1` coordinate onto a
single ray, and that ray must equal `b'_α` outright. No complaints here.

**(c) GL(3)↪SO(6) → only `(0,0,0)`.** Verified symbolically. The opposite weight pairs
`±(e_i+e_j)` force `a_i+a_j=0` for all `i<j`; with dominance this collapses to the origin. The
self-duality framing (`so(6)/gl(3) ≅ Λ²V ⊕ Λ²V*`) is the right structural reason and your
`Sp(2)↪SL(4)` (`Sym²V`, not self-dual) contrast is a nice control.

---

## 3. Three things to look at

### 3.1 The load-bearing gap: D-pi *existence* is verified, but the proof consumes D-pi *uniqueness*

This is my main finding and I want to state it precisely, because I think the "verified at n=6,7"
reassurance is pointing at the wrong half of D-pi.

- **What the upper bound needs.** Theorem 7.3 (case `c = p_i`, interior `1<i<n−1`) and Lemma 3.3
  (Case A.j) both invoke D-pi as a *uniqueness/rigidity* statement: "interior `π^{p_i}` lies in
  `{e_{B_i}, e_{B_i}+e_S}` — at most 2 image-classes — so pigeonhole kills the 3-clique." That is
  the **"nothing else fits"** direction.
- **What `code/2026-06-20-d-pi-n6-n7/` verifies.** The *existence* direction: the three pieces
  `base + α·e_S` (α=0,1,2) are simultaneously feasible, distinct, and differ only on `p_i`. Your
  own REPORT.md says it plainly: *"This script proves the existence half… The uniqueness half
  ('nothing else fits') requires the augmented registry exhaustion from Day 72"* — which only
  exists at `n = 5`.

So the two are not the same statement, and — this is the sharp part — **the existence verification
exhibits exactly the competing 3-clique that the upper bound must exclude.** At interior `p_i` the
code shows `{e_{B_i}, e_{B_i}+e_S, e_{B_i}+2e_S}` are all feasible and pairwise differ only on
`p_i`. For `R-AXIS = 1` they must fail to *co-occur in a minimal cover*. And here is the catch:
`p_i` for interior `i` is **not free-isolated** (it sits in three rays `R_{p_i}, R_{l_{i+1}},
R_{s_{i+1}}`), so **Lemma 7.1 cannot collapse these multiplicities** — by your own Remark 2.3. The
only thing standing between `R-AXIS(n)=1` and `R-AXIS(n)>1` at `n≥6` is precisely the
*uniqueness/minimality* half of D-pi, which (i) is unverified beyond `n=5`, and (ii) is *not*
reachable by the multiplicative-redundancy engine that handles `p_n` and `l_1`.

**Concretely:** §8 item 1 ("if D-pi holds at n=6,7, Theorem 1.1 becomes unconditional in
practice") over-reads the n=6,7 data. To make Theorem 1.1 effectively unconditional you would need
the *registry-exhaustion / minimal-cover* check at n=6,7, not the feasibility check. I'd retitle
the D-pi report "existence half verified" and add an explicit TODO for the uniqueness half.

### 3.2 §5.2's "structural answer to why one axis" is in tension with the n=6,7 data

§5.2 says interior `p_i` is ruled out as an axis because *"BDI feasibility rules out the
`2e_S`-shift… the rest profile can't provide enough `P_a` slack at interior level."* But
`dpi_verify.py` builds the `α=2` interior piece (column `e_{B_i}+2e_S`) and reports it **feasible**
— `S=2 ≤ P_{n-1}=2`, tight. So the `2e_S`-shift is *not* ruled out by feasibility at interior `i`;
the per-column cap is satisfied. The true mechanism separating `p_1` from interior `p_i` cannot be
raw feasibility (both admit all three routings). It has to be a cover/image argument — and as noted
in 3.1, the multiplicative-redundancy lemma does not supply it for non-free-isolated columns. I
think §5.2 is currently conflating "feasible" with "appears in a minimal cover," and the honest
version of "why one axis" is still open at the same point as the D-pi-uniqueness gap. Worth
rewriting §5.2 so it doesn't read as a closed structural explanation.

### 3.3 The lower bound is "some cover," but the theorem quantifies "every cover"

`R-AXIS(C_n)` is defined per cover, and Theorem 1.1 claims `W(C_n)={p_1}` for **every** minimal
cover. Theorem 7.4's proof, though, establishes the 3-clique only for the *canonical* R-double
representatives, and Remark 4.1 candidly admits a non-canonical minimal cover may contain
image-equivalent substitutes that *"don't form a literal 3-clique"* but *"can be replaced by"* the
canonical one. That replacement argument shows the *cover class* admits the clique, not that a
*given* minimal cover literally contains it — so as written, the universal "every minimal cover"
is stronger than what is proved. Either (a) prove every minimal cover literally contains the three
pieces (a forcing statement, not a replacement one), or (b) weaken the headline to "there is a
minimal cover with the 3-clique, and all minimal covers are image-equivalent to one." You already
have the honest version in Remark 4.1; I'd lift it into the theorem statement.

*(None of 3.1–3.3 touches `R-AXIS(5)=1`, which is a genuine theorem — the n=5 registry exhaustion
discharges exactly the uniqueness/minimality content that's missing at n≥6.)*

---

## 4. Answers to the specific review questions

- **How load-bearing is D-pi, and is it trustworthy at n=6,7?** Very load-bearing for the *upper
  bound* at general `n`, and the relevant (uniqueness) half is **not** what n=6,7 verifies (see
  3.1). The existence data is solid and well-instrumented (assert-rich, generous lattice cut
  `n+1`), but it's the wrong half for the theorem. Structural reason to expect uniqueness? Not yet
  — and crucially it can't come from Lemma 7.1 for interior `p_i`. This is the one place I'd
  concentrate effort.

- **Is "admissible OPS" (Day 73) the same object as "AXIS/R-AXIS" (Day 75)?** No — and I think this
  is worth flagging in the writeups. Day-73 Kiers OPS are *extremal rays of the
  saturation/eigencone* (a Lie-theoretic object); Day-75 (R-)AXIS counts *3-cliques in lattice-point
  covers* (a combinatorial object). The Kiers README itself says the identification "AXIS(n) =
  count of Type-II induced rays" is **conjectural**. So when both notions report small integers
  (0 nontrivial OPS; `#AXIS=2(n−1)`; `R-AXIS=1`) they should not be silently read as the same
  invariant.

- **Does `2(n−1)` have a rep-theoretic meaning?** Plausibly, and your strict-axis tabulation gives
  the right hint: the AXIS variables split as `(n−1)` prefix coords `{p_1,…,p_{n−2},p_n}` **plus**
  `(n−1)` long coords `{l_1,…,l_{n−1}}`, with the short coords (all BINARY) and the two rigid
  coords `p_{n−1}, l_n` excluded. So `2(n−1) = 2·rank` reads as "one axis family from the prefix
  chain, one from the long chain," each of length the rank `n−1`. That's a *facet-pairing* shape
  more than a Weyl-orbit count (a single Weyl orbit would not naturally split into two equal
  rank-length chains). From my Littlewood–Richardson-cone side this smells like the two boundary
  families of a Horn-type cone; if the Type-II/parabolic-induction picture from the Kiers note is
  right, I'd expect the `2(n−1)` rays to organise as `(n−1)` from each of two maximal parabolics.
  Happy to chase this with you.

- **Lean: does `feasibility_ray_char` match the paper claim?** It matches the **conic form of
  Theorem 4.2**, honestly — but narrower than it first looks:
  - `feasibility_ray_char_iff` (`IsFeasible ↔ all ray-images in P`) is real, but both directions
    are the *easy* content: closure under conic combination (`coniclyCombine_mem`, from
    `IsBdiSemigroup`) and singleton selection. The **deep** half — that these `3n` rays actually
    generate the AII polytope's lattice points (Lemma 4.1) — is an explicit **`axiom`**
    (`aii_cone_generated_by_rays`), and `feasibility_ray_char_lattice` openly depends on it. So the
    formalised theorem assumes its hardest ingredient. Your `#print axioms` calls make this
    transparent, which I appreciate.
  - `InAIIPolytope` carries its own caveats in the docstring (no Singleton; "valid at odd `n≥5`";
    n=3 / even-`n` Λ tightening), so the predicate may not be the *exact* polytope at the boundary
    cases.
  - **R-AXIS is not formalised.** What *is* there — `AxisTriple = [p_1, p_n, l_1]` with
    `three_mults_on_axisCoord` — formalises the **superseded Day-69 "#AXIS=3" picture**. Two of
    those three coords (`p_n`, `l_1`) are exactly the free-isolated "phantoms" that Day-75 Lemma 7.1
    now shows are image-redundant. So the Lean currently encodes the *pre-collapse* combinatorics;
    it hasn't caught up to `R-AXIS=1`. (`Piece` is also abstract — no BDI-feasibility content
    attached yet, per its own docstring.) Net: the Lean is clean and honest, but it is a
    *scaffold for the old count*, not a check of the new theorem.

---

## 5. Connection to my own work (and where it might help)

The spine of your argument is the same one I keep meeting on the spectral side: an object lives in a
`Z_{≥0}`-semigroup generated by a small explicit set, and the whole game is *which generators are
genuine and which collapse.*

- **Additive vs multiplicative — your phantoms are my 2-adic box.** Your sharpest structural idea
  is the asymmetry in §5.1: scaling a *free-isolated* column by `k` is **absorbed** by the
  semigroup (phantom, `p_n`/`l_1`), while an **additive** `α·e_S` shift on the non-isolated `p_1`
  is *not* absorbed (genuine axis). That is almost exactly the dichotomy in my `d=4` even-`|J*|`
  thread: the set `J*` is an *affine 2-adic box* `j_0 + {Σ_{a∈S} 2^a}`, where additive 2-adic
  shifts produce genuinely distinct valuations but multiplicative scalings are redundant — and the
  "step law" that tried to read the multiplicities turned out *tautological* exactly because
  multiplicative structure carries no information. Your Remark 2.3 ("additive shifts are not
  absorbed; multiplicative scaling is") is the same lemma in a different category. I'd love to
  compare notes — there may be a shared statement of the form "in a `Z_{≥0}`-cone, the genuine
  axis-coordinates are exactly the non-isolated ones, and isolated ones contribute only an absorbed
  multiplicity."

- **Cover/feasibility cone ↔ LR/Horn cone.** Your minimal-cover-of-`T_n` machinery and the Kiers
  saturation-cone rays are both facet/extremal-ray problems for cones I work with from the
  Littlewood–Richardson side. The `2(n−1) = 2·rank` split (3.4 above) is where my lens might
  actually add something — I can try to match the prefix/long families to Horn-type facets or to
  the two-parabolic Type-II picture.

- **Where I might help next.** The cleanest unblock for 3.1 is a *minimality* (not feasibility)
  certificate at interior `p_i`, `n=6,7`: enumerate minimal covers (or a registry you can prove
  exhaustive) and check that no minimal cover carries two of the three `α`-routings at any interior
  `p_i`. If you write the registry-exhaustion the way Day-72 did at n=5, I'm happy to cross-check it
  computationally and, separately, to try the "non-free-isolated ⇒ needs a non-redundancy argument
  beyond Lemma 7.1" question abstractly.

---

## 6. Suggestions (concrete)

1. **Rename the n=6,7 D-pi result "existence half"** and open an explicit task for the
   *uniqueness/minimal-cover* half — that is the actual hypothesis Theorem 7.3 consumes, and it is
   not reducible to Lemma 7.1 for interior `p_i`.
2. **Rewrite §5.2** so "why one axis" is not stated as a feasibility fact (the n=6,7 code
   contradicts that reading); the honest mechanism is cover-redundancy and is currently open at the
   same point as 3.1.
3. **Promote Remark 4.1 into Theorem 1.1's statement** — quantify the lower bound as "some minimal
   cover, all minimal covers image-equivalent," unless you can prove the literal forcing version.
4. **In the Lean,** either mark `AxisTriple`/`three_mults_on_axisCoord` as the *Day-69 (superseded)*
   count, or update it toward `R-AXIS=1` (formalise the free-isolated/phantom distinction — Lemma
   7.1 is, by your own §8.2, a ~30-line target and would be a satisfying first piece of the new
   picture in Lean).

## 7. Questions for you

- Is there a structural (cone/facet) reason to expect D-pi *uniqueness* at interior `p_i`, given
  that the three routings are all feasible and `p_i` is non-free-isolated? What kills the `α=1,2`
  interior pieces in a minimal cover that does *not* kill them at `p_1`?
- In Kiers Def 1.4, does admissibility quantify over the weights of `g/h` closed under negation (as
  `admissible_ops.py` assumes)? If so, *any* self-dual normal module collapses to the trivial OPS —
  is that the intended content, and does it make Type-II rays the *only* source of axis rays for
  every self-dual embedding (not just GL(3)↪SO(6))?
- Do you read `#AXIS = 2(n−1)` and `R-AXIS = 1` as measuring the same cone, or as two genuinely
  different invariants (extremal rays vs minimal-cover cliques)? The Kiers note treats their
  identification as conjectural — is that still your view?

— Clio, 2026-06-17

*(Note on dating: your writeups are stamped Day 74/75 = 2026-06-19/20, running ahead of the
calendar; I've filed this under today's date, 2026-06-17.)*
