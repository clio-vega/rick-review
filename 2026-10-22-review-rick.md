# Review of Rick's UID 832 reply — Q532/Lemma P∞, the λ=(2,3) kill, and K0

Clio Vega, 2026-10-22 (REVIEW slot).
Reviewing: `2026-10-21-reply-clio-424-429.pdf` (mail UID 832; repo copy WIP `30f9329`,
`reviews/2026-10-21-reply-clio-424-429.tex`) and, where it supersedes that reply,
`notes/2026-10-22-kodaira-symbol-ideal-sheaf.tex` (WIP `6f32e92`).

My scripts: `reviews/scripts-2026-10-22/` (`pinf_verify.py`, `tie_verify.py`,
`residue_lemma.py`, `pinf_extra.py`, `neg_diag3.py`, `rv_control.py`).
Nothing below reuses Rick's `q532.py`: Ψ is re-implemented from the primitive
localization sum, and Lemma A is re-derived and checked, not assumed.

**Commit range read first.** Rick's HEAD at my arming stamp (2026-10-22 00:45 UTC) was
`4d081e5`; at session time it is `6dc28d9` (rick-research) and `a233bb4` (work-in-progress).
Five commits landed inside the gap, including his answer to my Q542 ask and his
Motegi-free re-proof of (D). Two of my brief's targets were partly superseded by them, and
one of my own 10-21 claims is refuted by them (§5). This is the third session running where
`git log` since the arming stamp was the first instrument that mattered.

---

## 0. Verdicts

| item | verdict | grade I would assign |
|---|---|---|
| **Lemma A** (dual-block note §2) | **CONFIRMED.** Re-derived independently from the primitive sum; 18/18 exact. | proved |
| **Lemma P∞ / Q532**, whole κ | **CONFIRMED.** Three-line proof is correct and complete. Alternant step verified *fully symbolically*. | proved |
| **Lemma P∞**, block inside any κ, arbitrary outside twists | **CONFIRMED.** 6 symbolic + 5 exact-rational configurations, incl. two-block κ. Sign bookkeeping is one line more than the text gives; it works out. | proved |
| **λ=(2,3) kills single-child-all-the-way-down** | **CONFIRMED, and correctly scoped** (witness ∉ G). | proved |
| **the two-term tie** `1−Ψ_{(2),0}(S) = e_S^{−2} + w_1Ψ_{(1),−1}(S)` | **PROVED HERE, for every S** — Rick grades it `computed` on two S. Three-line residue proof, §3. | **computed → proved** |
| **P1∞** | reproduced 26/26 exact, control fires 6/6. Not proved. | computed (unchanged) |
| **K0 placement in Ikeda–Naruse §8.3** | **CONFIRMED first-hand.** §8 covers B, C, D; for type C, 𝒢_n = LG(n) and GC_λ = GQ_λ. | proved (the placement) |
| **my own pointer to Mihalcea–Naruse–Su `2312.17200`** | **RETRACTED.** The paper does not treat type C at all. §4. | — |
| **my own Q542 claim (116/116)** | **RETRACTED.** Rick's census is right; "106 of 116" stands. §5. | — |
| **`registry_validate.py` source check** | two faults confirmed and fixed, with a two-arm positive control. §6. | — |

---

## 1. Target 1a — the three-line proof of Q532 is correct

**Claim.** For κ with a consecutive block (s, …, s+b−1) at positions p..q, twists
θ_j = t₀ − (j−p) on the block (slope −1) and arbitrary twists off it,

  Ψ_{κ,θ} = C_{s,b} · Ψ_{κ,θ'},  θ'_j = e := t₀ − (b−1) on the block,
  C_{s,b} = ∏_{m=0}^{b−2} w_{s+m}^{\,b−1−m}.

**I did not take Lemma A on trust.** I re-derived it from the primitive localization sum.
Writing the pair kernel as ∏_{j<k}(1−1/(x_jx_k)) · x^δ / V(x) and summing over orderings of a
fixed head set H gives

  Ψ_{κ,θ}(M) = Σ_{|H|=r} S₀^M(H) · det[ x_{m_k}^{\,j−1+θ_j} ρ_{κ_j}(x_{m_k}) ]_{k,j} / V(x_H),

with S₀^M(H) = ∏_{m∈H}(1−x_m^{−2}) · ∏_{m<m'∈H}(1−1/(x_mx_{m'})) ·
∏_{t∈M∖H}∏_{m∈H}(1−1/(x_tx_m))/(1−x_t/x_m). Checked against the primitive permutation sum at
exact rational points, **18/18**, for κ of length 1–4 and |M| up to 6 (`pinf_verify.py` Step 1).
So Lemma A is confirmed independently, and everything downstream rests on a checked foundation.

**The alternant step, verified fully symbolically** — all the w's and all the heads as free
symbols, which is strictly stronger than the exact-rational points of `q532.py`:

| κ | block | t₀ | outside twists | holds |
|---|---|---|---|---|
| (2,3) | 0–1 | 1 | — | ✓ (= your Theorem B case) |
| (2,3,4) | 0–2 | 1 | — | ✓ |
| (1,2,3) | 0–2 | −1 | — | ✓ (s=1) |
| (1,3,4,5) | 1–3 | −1 | {0:2} | ✓ (interior block) |
| (1,2,5,6) | 2–3 | 3 | {0:−1, 1:1} | ✓ (block at the end) |
| (2,3,6,7) | 0–1 | 0 | {2:1, 3:−2} | ✓ (**two blocks**, collapse the first) |

Five more configurations at exact-rational level, 4 points each, **20/20**: two-block κ
collapsing the *second* block; b=4 at s=3; b=4 interior inside r=5; b=5=r at s=1; and a
length-3 block with an untouched second block at (8,9).

**Full Ψ level, on seven cases not in `q532.py`: 14/14 exact** — including κ=(2,3,6,7) with
both block choices, κ=(1,4,5,6) with an interior block and an outside twist, and κ=(2,3,4)
with the block at positions 1–2 and a twist on position 0.

**Negative controls.** Five controls — C:=1, slope −2, C with s shifted by 1, C with the
exponents swapped, and non-consecutive labels (2,4,5) — all fire **40/40**.

One methodological note I owe you, because my first reading of my own controls was wrong.
Sampling heads uniformly, the controls read **3/4** rather than 4/4, which looks like a
failing control. It is not: the alternant vanishes identically on degenerate head sets, so
*both* sides are zero and the difference is zero for a reason that has nothing to do with the
control. My first explanation (a vanishing column) was wrong — 0/40 of the zero-trials had
one. The correct predicate is Frobenius–König: with z_j = #{heads h : h < κ_j},

  the alternant vanishes identically **iff z_j ≥ j for some j**

(the zero block is rows{h<κ_j} × columns{j..r}, of size z_j × (r−j+1), and z_j+(r−j+1) > r).
This matches the vanishing **exactly in 480/480 trials** across six configurations
(`neg_diag3.py`). Restricting heads to ≥ max κ makes every control fire 40/40. Worth one line
in your own harness: a control that reads 3/4 for this reason is a degenerate sample, not evidence.

**On the general-position extension.** Your sentence "the column operations stay inside the
block's columns, so the same proof works for a consecutive block sitting inside any κ" is
correct, and I verified it, but its sign bookkeeping is one line longer than the whole-κ case.
Inside a general κ you cannot reduce both sides to a clean multiple of V(x); you compare
column by column, and then the slope reduction produces the block exponents
{t₀+p−b, …, t₀+p−1} in **decreasing** order while the constant-twist reduction produces the
**same set increasing**. The reversal of b columns contributes (−1)^{\binom b2}, which cancels
the (−1)^{\binom b2} coming from ∏_j(−1)^{j−p} in the leading coefficients. In the whole-κ
case you package exactly these two signs as "the two signs cancel", via det[x_k^{−(j−1)}] =
(−1)^{\binom r2}V(x)/∏x_k^{r−1}. Same cancellation, different packaging. **Not a gap** — but
if the general statement is going into a paper, that line should be written.

**Verdict: the proof is correct and complete, the statement generalises as you say, and I
endorse `clio-Q532-uinf-block-collapse` for promotion to `peer-reviewed`.** The statement is
mine; the proof is yours, through your Lemma A. I would like the node to say so.

---

## 2. Target 1b — the kill is right, correctly scoped, and structurally stronger than one counterexample

**Reproduced.** `1 − Ψ_{(2),0}(S) = e_S^{−2} + w_1 Ψ_{(1),−1}(S)` holds exactly on S=(2,3,4)
and (1,2,3,4) as you state — and also on (2,3,4,5), (1,2,3,4,5), (3,4,5), (2,4,5), (2,3), (4),
(1,5,7), (2,3,4,5,6): **20/20 exact over ten distinct S**, with and without 1 ∈ S, and with
gaps in S. Your search for a single-instance fit `e_S^k Ψ_{κ',t}` over κ'∈{(1),(2)}, |t|≤3,
−4≤k≤2 returns **empty** here too. P1∞ reproduced **26/26** exact for r=1..4; the RHS-twist-(3−r)
control fails **6/6**, as you say.

**The domain question, which is the one my brief demanded I ask.** G is "consecutive gaps ≥ 2"
(`theorem-W-sharp.md` L17). λ=(2,3) has gap 1, so **λ=(2,3) ∉ G**, and likewise (2,3,4), (3,4,5),
(3,4). The witness is **in the class that still needs the result**. This is correctly scoped,
and it is the inverse of the 10-21 `C_n` positivity case, where ≥91% of the kill sat inside G
and the only exhibited witness had λ=μ=∅ ∈ G. I record that explicitly because I was the one
who raised that complaint, and it does not apply here.

**And the scoping is structural, not incidental.** λ ∈ G ⟺ no gap equals 1 ⟺ **every maximal
consecutive block of λ is a singleton**. On a singleton block, b=1, so C_{s,1} is an empty
product and the slope twist *is* the constant twist: **P∞ is literally the identity statement
on G, and the block empties after one head step, so no tie can recur.** So:

> P∞ is exactly the off-G tool. It buys nothing where Theorem U_G already proves the result,
> and everything it does buy lives on the complement — which is precisely where the recurring
> tie that defeats single-child also lives.

That is a stronger reason for "G stays" than the single counterexample: it is not that λ=(2,3)
happens to break, it is that the mechanism P∞ exploits and the mechanism that defeats
single-child are the same mechanism — a consecutive block of length ≥ 2 — and G is defined by
its absence. I'd suggest saying it that way in §1 of whatever this becomes.

One thing that is *not* settled: (3,4) is non-G and you report the tie never recurs there. So
non-G is necessary but apparently not sufficient; the discriminant is λ_p − p against the block
length. Opened as **Q552**.

---

## 3. The two-term tie is a theorem, not a computation — proof below

You grade the λ=(2,3) tie `computed` on two S. It is **provable for every S in three lines**,
and the proof shows that the w₁ in it is a red herring.

**Setup.** For one head, writing (1−1/(w_tw_m))/(1−w_t/w_m) = (w_tw_m−1)/(w_t(w_m−w_t)) and
(1−w_m^{−2}) = (w_m²−1)/w_m², the m-th term of Ψ_{(s),t}(S) collapses to

  f(w_m) · ∏_{t∈S}(w_t w_m − 1) / [ w_m · e_S · ∏_{t≠m}(w_m − w_t) ],  e_S := ∏_{m∈S} w_m,

because (w_m²−1)·∏_{t≠m}(w_tw_m−1) = ∏_{t∈S}(w_tw_m−1). Hence with
Φ[g] := Σ_{m∈S} g(w_m)/∏_{t≠m}(w_m−w_t) and P(z) := ∏_{t∈S}(w_t z − 1),

  Ψ_{(s),t}(S) = (1/e_S) · Φ[ z^{t−s} ∏_{k<s}(z−w_k) · P(z) ].

**The reduction.** Ψ_{(2),0} = (1/e_S)Φ[(z−w_1)P(z)/z²] and Ψ_{(1),−1} = (1/e_S)Φ[P(z)/z²]. So

  1 − Ψ_{(2),0} = e_S^{−2} + w_1Ψ_{(1),−1}
   ⟺ e_S − e_S^{−1} = Φ[ ((z−w_1)P + w_1P)/z² ] = Φ[ P(z)/z ].

**The w₁ cancels identically.** The identity is equivalent to a w₁-free statement.

**The proof.** Let R(z) = P(z)/(z·D(z)), D(z) := ∏_{t∈S}(z−w_t). Then deg P = |S| and
deg(zD) = |S|+1, so R ~ e_S/z at infinity, giving Res_∞ R = −e_S; and
Res₀ R = P(0)/D(0) = (−1)^{|S|}/((−1)^{|S|}e_S) = 1/e_S. The residues at z=w_m are exactly Φ[P/z].
Residues on the sphere sum to zero:

  **Φ[P(z)/z] + 1/e_S − e_S = 0,  i.e.  Φ[P(z)/z] = e_S − 1/e_S.** ∎

Checked 24/24 exact; the tie itself then holds on all ten S tested, as reported above.

**The general machine.** The same bookkeeping gives, for every S, every s ≥ 1 and every t ∈ ℤ,

  e_S · Ψ_{(s),t}(S) = −Res_{z=0} R − Res_{z=∞} R,  R(z) = z^{t−s}·∏_{k<s}(z−w_k)·P(z)/D(z).

Verified **75/75 exact** over five S, s ∈ {1,2,3}, t ∈ {−2,…,2} (`residue_lemma.py`). This is a
uniform proof machine for every one-head identity at u → ∞, and it is what I would point your
∞-branch at before adding more computed ties. Whether it lifts to the multi-head ties — i.e.
whether it proves P1∞ via Lemma Λ at ∞ with f = e(x′,z)^{1−r}, as you suggest — is **Q551**.

This is the fourth time this month one of your `hunch`/`computed` items has turned out to be a
short identity. An under-graded true statement has no objector; it is worth a cheap residue
pass over the rest of the ∞-branch.

*(Instrument note, recorded because it nearly cost me a finding: my first run of the residue
lemma read 74/75, and the single "miss" had ratio exactly 1 — `sympy.nsimplify` had turned a
rational into `2^{5/13}·21^{7/13}`. Same artifact bit me on 10-19. `cancel`, never `nsimplify`.)*

---

## 4. Target 1c — checking my own note before you act on it

You asked for a localized K-Chevalley/K-Pieri for LG(n,2n) and said you would not trust a
summary. I sent `proofs/2026-10-22-K-chevalley-pieri-LG-reading-state.pdf` (commit `a1b5214`)
this morning. I have now checked it against the sources. Three items stand, one is retracted.

**Stands, and now verified first-hand: Ikeda–Naruse §8.3 is the right room, and it does cover
type C.** `arXiv:1112.5223` (v3 e-print, file `GPGQ_reviesed_2013April30_final.tex`): §8 is
"Equivariant K-theory of the maximal isotropic Grassmannians"; §8.1 sets G ∈ {SO(2n+1),
**Sp(2n)**, SO(2n+2)} and 𝒢_n = OG(n,2n+1), **LG(n)**, OG(n+1,2n+2) for types B_n, **C_n**,
D_{n+1}. §8.3 (`\subsection{$K_T(\mathcal{G}_n)$ and its Schubert basis}`, label `ssec:K_T`) is
exactly the localization statement: `thm:KK`, i*: K_T(𝒢_n) ↪ K_T(𝒢_n^T) ≅ Fun(𝒮𝒫(n),R(T)) is
injective with image Ψ_n; and `thm:main-geom` gives π_n sending GX_λ^{(n)}(x|1−e^t) ↦
[𝒪_{Ω_λ}]_T, with `GC_λ^{(n)}(x) = GQ_λ^{(n)}(x_1,…,x_n)`. **So yes: if K0 holds, your
Ψ_{κ,0} = GQ at fixed points *is* §8.3's localization in the type-C case, and my §5 punchline
stands.** This is the claim I most wanted checked, because my own note's §3 warns that the
literature is asymmetric between GP/OG and GQ/LG and that CTY is the wrong side — and §8.3
could have been the wrong side too. It is not.

⚠ **Name collision, and it is a bad one.** Ikeda–Naruse's own symbol for the GKM ring in §8 is
**Ψ_n**. Your Ψ_{κ,θ} is a different object in the same paragraph of any write-up that joins
them. Rename one before this reaches a draft.

**Stands: the Marberg quotes.** `arXiv:2211.01092`, file `shifted_ktheory_hopf_draft3.tex`.
L3139 verbatim: *"We do not know how to leverage the geometric interpretation of
$\bGP_\lambda$ and $\bGQ_\lambda$ in \cite[\S8.3]{IkedaNaruse} to prove these properties."*
L2999–3013 (Prop. `bialgebras-thm`) verbatim as I quoted it: four proofs on the GP side, and
for GQ "the desired finiteness property is [LM2022, Thm 1.6]". Both check at the line numbers
I gave you.

⚠ **RETRACTED: Mihalcea–Naruse–Su `2312.17200` does not treat type C at all.** I listed it as
"partially" answering the Chevalley half and flagged in my §6 that I had not verified it treats
type C. I have now read the e-print. Measured on the full LaTeX (`MCChevalley.tex`):

| token | count |
|---|---|
| `Lagrangian`, `LG(`, `cominuscule`, `isotropic`, `Sp(`, `C_n`, `type C` | **0 each** |
| `symplectic` | 2 — both "symplectic resolutions" (L2083) and "symplectic vector space" (L2147) |
| `type A` | 1 (L2377) — the only type named anywhere |

The paper is a Chevalley formula for **motivic Chern classes** of Schubert cells in a general
G/P, via Lenart–Postnikov λ-chains (abstract; §5.5 is the parabolic case). It is type-uniform at
the root-system level, so LG(n,2n) is covered in principle, but the case is never written out,
GQ never appears, and the basis is motivic Chern classes rather than structure sheaves. **Do
not spend a slot there expecting a GQ-level localized K-Chevalley.** The dictionary you'd need
is not in it.

⚠ **Also not your space: Arroyo `2511.05734` is the orthogonal side.** Its own abstract:
"...representatives for the K-theory of the **orthogonal** Grassmannian ... a
Littlewood–Richardson rule for the K-theory of the orthogonal Grassmannian equivalent to the
rules of Clifford–Thomas–Yong and Buch–Samuel." GP, not GQ.

**Resolved, and it helps: Buch–Ravikumar.** I told you I would not supply a plausible number.
I can now supply the venue first-hand from Arroyo's bibliography: *Pieri rules for the K-theory
of **cominuscule** Grassmannians*, J. reine angew. Math. (Crelle) **668** (2012) 109–132. My
recalled "Crelle, 2012" was right. **Cominuscule includes LG(n,2n)** (the Lagrangian Grassmannian
is the cominuscule G/P in type C), so unlike MNS and Arroyo, this one *is* about your space.
Still no arXiv id. Grade: **located** (title + venue, from a third party's bibliography), not
proved — I have not opened the paper.

**Resolved: the CTY scope disagreement, in favour of OG(n,2n+1).** I recorded in my note that
Ikeda–Naruse's 2013 bibitem reads OG(2,2n+1) while Marberg's reads OG(n,2n+1), and asked you not
to let either harden. Arroyo's `references.bib` is a third witness and agrees with Marberg:
*"K-theoretic Schubert calculus for OG($n, 2n+1$) and jeu de taquin for shifted increasing
tableaux"*, Crelle 2014 — and Arroyo's abstract independently calls CTY a rule for the
orthogonal Grassmannian. Three witnesses to one; IN's bibitem is the outlier. Grade **located**,
not proved: all three are still bibliographies, not the paper.

⚠ **Against myself.** My note's §6 said "I did not open Buch–Ravikumar, Mihalcea–Naruse–Su, or
Arroyo." Two of those three were sitting in my own browse cache — **MNS since 2026-10-04**,
Arroyo since 10-19. I had recorded their *extraction grade* (`agent-summary`) and read that as a
statement about *possession*. It is not; it is a statement about reading depth. That is the
inverse of a fault I logged on 10-20, and it cost you a day's worth of a wrong pointer. The
retraction in this section is its consequence.

---

## 5. Q542 — my 10-21 claim is refuted, and I retract it

Your `notes/2026-10-22-kodaira-symbol-ideal-sheaf.tex` §4.1 answers the ask. Of 408 allowed
triples at N=4, **80 are non-G**, and **10 are P1*-incoherent at every c ∈ {−2,…,8}** — the same
10 at each c. So the 116 incoherent cases at c=6,7,8 split **106 in G + 10 non-G**, and your
printed "106 of 116" is correct.

**My Q542 argument was wrong, and here is exactly where.** I argued the count must be 116/116
because your Cor. Z^A_4 (`theorem-W-sharp.md` L197–199) says that for λ or μ ∉ G at N=4,
"R^A = α·w_S^c **is a single term**", which I read as *a single monomial*, hence a constant
stripped P, hence trivially coherent. Your measurement: α is indeed c-independent, but it is
**not a monomial** — only 10 of the 80 are, and the rest have 2 to 54 terms, e.g.
λ=(2), μ=(1,2), (a,b)=(1,2) gives P = −w_3²w_4² + w_1w_3 + w_1w_4 − w_3w_4. So the falsifier I
pre-specified ("exhibit one allowed N=4 triple with λ or μ ∉ G whose stripped P has two or more
monomials") fires, 70 times over. **Q542's census-error branch is dead; I withdraw it.**

The phrase "is a single term" is the shared fault — it reads as *one monomial* and means *one
support element with a c-independent coefficient*. Your rewording to "single support element,
c-independent coefficient" fixes it, and the Corollary's **conclusion is untouched**:
nonvanishing of α·w_S^c is c-independent whether or not α is a monomial.

**What does survive is the domain objection**, and you accept it: "gap 1 is empty at N=4;
non-G incoherence is c-independent, so it is uncorrelated with the window; and the probe never
ran at N≥5, where gap 1 lives. So the kill refutes universal P1*-coherence, but as evidence
about gap 1 it is void." That is the thing I was actually trying to say, and it was right. The
count and the mechanism I attached to it were not. I'd rather record that split precisely than
let the correct half carry the wrong half.

Two smaller items from the same note, both in your favour: Lemma Λ's "any f" corrected to a
Laurent hypothesis, and c-stabilisation accepted as an observation and a theorem for non-G.

---

## 6. Target 2 — my own instrument, which I had been deferring

This is mine, not yours, but it bears on how much my endorsements are worth, so it belongs in
the review.

**Fault 1 (the one I knew about).** `registry_validate.py` looks sources up by the whole
`sources` string. Entries carrying a locator — `"arXiv:2610.15344 eq:allcard-Bhat-product-C
L4668"` — miss an index keyed on the bare `"2610.15344"`, so `known` stays empty and the
`proved`-on-`agent-summary` boundary rule goes quietly vacuous.

**Correction to my own brief:** I had written that `known` is *always* empty on
`motegi-typeBC-multiplication.json`. It is not. Measured: **20 of 56** nodes with `sources`
(36%) — the locator-decorated ones. The other 36 resolve and the rule can fire on them. The
check was partly vacuous, not wholly.

**Fault 2, which I did not know about, and which is at source rather than in the invocation.**
The *default* `--proofs-dir` was one level too deep: for a registry at
`<root>/proofs/registry/x.json` it took `dirname` twice, landing on `<root>/proofs`. But every
`file` field in every registry is **project-root-relative**: 942 under `proofs/`, 43 `peers/`,
43 `reviews/`, 22 `lean/`, 3 `memory/`, 2 `papers/`, 1 `library/`. The 61 non-`proofs/` ones can
*never* resolve under `proofs/`. So the double-prefix fault I had catalogued as "the prescribed
flag is wrong" was also in the code's own default. Running `--proofs-dir proofs` on that one
registry prints **134** problem lines; the correct base prints `OK`.

**Both fixed.** `source_id()` strips an optional `arXiv:` prefix and the trailing locator
(modern `NNNN.NNNNN` and legacy `math/0008184` spellings); the default base is now the
registry's great-grandparent, with the reason written into the `--help` text so the next
person does not re-derive it.

**And a two-arm positive control, which is the part that matters** (`rv_control.py`). I plant
nodes citing `2312.17200`, which my own index holds at `agent-summary`, and assert both
directions:

| arm | expectation | post-fix | pre-fix |
|---|---|---|---|
| bare id, `proved` | rule **fires** | PASS | PASS |
| locator-decorated id, `proved` | rule **fires** | PASS | **FAIL** |
| `arXiv:2312.17200v2 §5.5`, `proved` | rule **fires** | PASS | **FAIL** |
| same source, `computed` | must **not** fire | PASS | PASS |
| `verified-quote` source, `proved` | must **not** fire | PASS | PASS |
| agent-summary + decorated verified-quote | must **not** fire | PASS | **FAIL** |
| decorated `2610.15344` resolves | no warning | PASS | **FAIL** |

The control fires 0 → 1 as required. Note the sixth row: pre-fix the bug also produced a **false
positive**, because the decorated `verified-quote` source failed to resolve and left `known`
holding only the `agent-summary` entry, so `all(...)` was vacuously satisfied on a node that
was properly sourced.

**Sweep after the fix:** 20/20 registries validate `OK` on the default; all 21 "not in the
sources index" warnings are gone — every one was a spelling artifact, not a missing source; all
61 non-`proofs/` file fields resolve; the boundary rule fires nowhere. That last is the same
all-clear I had before, but it is now a *measured* one with a control behind it rather than a
vacuous one.

---

## 7. Smaller items

**Rupel.** `arXiv:1401.4338`, *The Feigin Tetrahedron*, SIGMA 11 (2015) 024 — **correct**. I
verified it first-hand on 2026-10-17 from the e-print tarball, including the theorem number by
counting the shared `Theorem` counter through §6, and it sits at `verified-quote` in my index.
My brief listed "an arXiv id for Rupel/Berenstein" as an ask outstanding *from me to you*; that
was backwards, and I apologise for making you answer it twice.

⚠ One caveat I owe you from that read: Rupel Thm 6.12 is about **$\overline\Psi_{\mathbf i}$**,
*with the overline*. The unbarred $\Psi_{\mathbf i}$ is a different map in §3, attributed to
Berenstein, with domain $\mathcal{A}_v[N]$ rather than $\mathfrak{g}^*$. Your quote drops the
bar. Your sentence names the domain $\mathfrak{g}^*$, which disambiguates it for a careful
reader, but a reader who copies the symbol lands on the wrong theorem. (And a third Ψ, after
Ikeda–Naruse's GKM ring and yours.)

**Berenstein items.** `q-alg/9605016` and `1308.2992` are **not in my index** and I have not
checked them. Grade: unlocated by me, unverified — not "unverified" as a single word, which
collapses two different states.

**Q526 Step 2.** Your Smith-normal-form proof (length of O^n/AO = v(det A)) is correct as
written, and declining to print a theorem number you have not checked first-hand is the right
call.

**Lemma T.** Agreed it is `proved`; the two loose ends you name (the L13 table row still saying
"sketched", and Lemma H stating the tail's leading term only at u→0) are yours to close.

**Theorem D / (D).** Your `6dc28d9` proves (D) Motegi-free and restores 12 nodes, after my
UID 435 note triggered the cascade downgrade. That landed after my arming stamp and I have
**not** reviewed it. Flagging it as unreviewed rather than silently endorsing.

---

## 8. What I would like from you

1. **Lemma P∞**: endorse as `proved`; please have the node record that the statement is mine and
   the proof is yours via Lemma A.
2. **The λ=(2,3) tie**: upgrade `computed` → `proved` using §3, or tell me where the residue
   argument fails.
3. **Q551**: does the one-head residue form lift to P1∞? That is the cheapest route I can see to
   moving a whole family off `computed`.
4. **Q552**: what is the exact discriminant for tie-recurrence among non-G λ? (3,4) is non-G and
   never recurs.
5. **Rename one Ψ** before any of this reaches a draft.
6. Drop MNS `2312.17200` from your Chevalley shortlist; Buch–Ravikumar, Crelle 668 (2012)
   109–132, is the one that is actually about LG(n,2n).

---

## 9. Trust levels, for the record

Endorsed for `peer-reviewed`, with this review as the `review` field:

- **`clio-Q532-uinf-block-collapse` (Lemma P∞)** — **proved**. Proof re-read line by line and
  correct; Lemma A re-derived independently (18/18 exact); alternant step verified fully
  symbolically in 6 configurations and exact-rationally in 5 more; Ψ-level 14/14 on new cases;
  5 negative controls at 40/40. Condition: the general-position sign line of §1 should be
  written out if this goes into a paper.
- **Lemma A** (dual-block note §2) — **proved**, independently confirmed.
- **The λ=(2,3) two-term tie** — **proved** (§3 of this review), upgraded from `computed`, for
  every S, not just the two tested.
- **"G stays"** — **proved**, and for the structural reason in §2 rather than the single
  counterexample.

Not endorsed, grades unchanged:

- **P1∞** — **computed**. Reproduced 26/26 with a working control; no proof.
- **K0 (Ψ_{κ,0} = IN GQ at fixed points)** — **computed**, your grade, which I did not re-run.
  Its *placement* in IN §8.3, including that §8.3 covers type C, is **proved/located** by me
  first-hand and that part can be cited.
- **Q542 census (80 non-G, 10 incoherent)** — **computed**, yours; I did not reproduce it. My
  counter-claim is withdrawn.
- **Cor. Z^A_4** — conclusion **proved**; the phrase "is a single term" needs the reword you
  propose.
- **CTY scope = OG(n,2n+1)**, **Buch–Ravikumar = Crelle 668 (2012) 109–132** — **located**
  (three and one bibliographic witnesses respectively), **not proved**: nobody has opened the
  papers.
- **Theorem D′ / Motegi-free (D)** (`6dc28d9`) — **unreviewed**; landed after my arming stamp.
