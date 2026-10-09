# COLD READING of Theorem 6.6 — written 2026-10-09 BEFORE opening any other part of the draft

Source: rendered image of p. 10 (`pdftoppm -r 200 -f 10 -l 10`) of
`2026-10-09-rick-fpsac2027-draft-0dcdc5e.pdf`, md5 87d0868788f38cbf3f19506c0518030a.
At the time of writing I have read: the title block (pdfinfo), Example 6.5 and the
paragraph above it (both on p.10, unavoidable — they share the page), and Theorem 6.6.
I have NOT read: his code, §§1-5, §7+, the definitions of kappa, Phi_a, [a], M, Prop 3.3.

## Verbatim transcription of the printed statement

**Theorem 6.6** (Closed l = 3, kappa = 1 leads). *Let lambda = (a,b,c) be any ordering of a
length-3 partition, mu = (x,y) with kappa(lambda,mu) = 1, n = x+y, m_xy as in Example 6.5. Put*

    Xi_a(r,q) := lin_e T_a(p_r p_q) = (-1)^{r+q} ([a+r+q]/[a]) [a]_{t^r} [a]_{t^q}

*and U_a(b,c;x,y) := ( (-1)^n Phi_a(p_b p_c; x,y) - Xi_a(b,c) ) / m_xy. Then*

    [(s-1)^2] c_{lambda mu}
       = (-1)^{b+c} U_a(b,c;x,y)
       + SUM over { 1 <= r < b , {b-r, a+r+c} = {x,y} }  of  (-1)^{r+c} Xi_a(r,c)
       + SUM over { 1 <= q < c , {c-q, a+b+q} = {x,y} }  of  (-1)^{b+q} Xi_a(b,q)
       + [e_x e_y] D_a(M_bc),

*with D_a the derivation D_a(e_j) = M_aj of Proposition 3.3.*

## What I, as a cold reader, take the statement to DENOTE

A formula for one specific coefficient -- the coefficient of (s-1)^2 in the (s-1)-adic
expansion of c_{lambda mu} -- in the case where lambda has three parts and kappa(lambda,mu)=1,
with mu having two parts. The RHS has four pieces: a "main" term U_a built from Phi_a, two
finite correction sums indexed by splittings of a part, and a derivation term.

## Findings from the cold read, in order of seriousness

### C1 (SERIOUS). "any ordering" asserts an unstated and non-obvious invariance.
The LHS depends only on the partition lambda as a multiset: c_{lambda mu} is indexed by a
partition. The RHS is **manifestly not symmetric in a, b, c**. The letter `a` is distinguished
everywhere -- Xi_a, U_a, Phi_a, D_a all carry it as a subscript; b and c appear only as
arguments. I checked the b<->c symmetry and it holds:
  - Xi_a(r,q) is visibly symmetric in (r,q);
  - the two correction sums map to each other under b<->c together with r<->q
    (first sum term (-1)^{r+c}Xi_a(r,c) -> (-1)^{r+b}Xi_a(r,b), second is
     (-1)^{b+q}Xi_a(b,q); equal since Xi is symmetric and the signs agree);
  - U_a(b,c;.) is symmetric in b,c provided Phi_a(p_b p_c;.) is (p_b p_c is);
  - (-1)^{b+c} and (presumably) M_bc are symmetric.
So the RHS is symmetric in **b,c** but the printed hypothesis allows a to be ANY of the three
parts. Therefore Theorem 6.6, as printed, silently asserts the extra theorem
**"the RHS is independent of which part is named a"**. Either that is the "box symmetry" of
the title, in which case it must be invoked by name AT THIS POINT, or it is not proved, in
which case "any ordering" is an overclaim and the hypothesis should pin a down.
This is the single thing I would most want the author to answer.

### C2 (SERIOUS). The title of the theorem says "kappa = 1" but the LHS extracts (s-1)^2.
"Closed l = 3, kappa = 1 leads" + hypothesis kappa(lambda,mu) = 1, yet the displayed quantity
is the coefficient of (s-1)^**2**. If kappa is the (s-1)-adic valuation -- which the paper's
title ("The (s-1)-adic valuation of Hikita's *-product") invites a reader to assume -- then
kappa = 1 means the LEAD is the coefficient of (s-1)^1, and [(s-1)^2] is the SUB-lead.
Either kappa is not the valuation, or the valuation is kappa+1, or there is an off-by-one.
A cold reader cannot tell which, and the word "leads" in the theorem title makes the reading
"[(s-1)^2] is the lead" the natural one -- which forces valuation = kappa + 1.

### C3. m_xy is imported from an Example whose other hypotheses are FALSE in Theorem 6.6.
Example 6.5 is headed "(Two rows)" and its sentence reads "for lambda = (lambda_1,lambda_2),
y <= x, and m_xy = 2 if x = y, 1 otherwise". So the sentence that defines m_xy also fixes
ell(lambda) = 2 and y <= x. In Theorem 6.6 lambda has length 3, so the surrounding hypotheses
of the defining sentence do not hold. The intended import is clearly only the *value*
"m_xy = 2 if x=y, else 1", and that value is well defined independently -- but "as in
Example 6.5" is doing the work of a Notation block and should be replaced by one.
Does "y <= x" come along? It does not matter for m_xy, and the set conditions
{b-r, a+r+c} = {x,y} are order-insensitive, so I believe nothing breaks. Flagged as a
presentation defect, not (as far as I can see) a mathematical one.

### C4. m_xy changes ROLE between 6.5 and 6.6, and is applied non-uniformly.
In Example 6.5, m_xy is an **additive** term ("m_xy - (1-t)t^{lambda_2-1}"). In Theorem 6.6 it
is a **divisor** of U_a. A value imported by cross-reference, used in a different algebraic
role, is worth one line of justification. Sharper: U_a is divided by m_xy but the two
correction sums are **not**. If m_xy corrects for double counting of the class (x,y) when
x = y, why does the correction not apply to the Xi sums as well? If it instead corrects the
coefficient-extraction convention for [e_x e_y] when x = y, then it should sit with that term,
not with U_a. As printed the placement looks asymmetric and I cannot reconstruct the reason.

### C5. Hidden integrality claim at x = y.
U_a = (...)/m_xy with m_xy = 2 when x = y. If [(s-1)^2]c_{lambda mu} is an integer (or a
polynomial with integer coefficients), the theorem silently asserts that
(-1)^n Phi_a(p_b p_c;x,y) - Xi_a(b,c) is divisible by 2 whenever x = y. That is a real claim
and a good self-test; it should be remarked on, or the diagonal case checked explicitly.

### C6. The base of the unsubscripted bracket [.] is not determined by the page.
In Xi_a(r,q) = (-1)^{r+q} ([a+r+q]/[a]) [a]_{t^r} [a]_{t^q}, two brackets are subscripted
`t^r`, `t^q` and two are bare. The paper carries at least two parameters: s (the (s-1)-adic
variable of the title and the LHS) and t (Hall-Littlewood, all of Example 6.5 and the
preceding paragraph). A cold reader cannot tell whether bare [m] means [m]_s, [m]_t, or
[m]_q in some third variable. This is exactly the normalisation the author predicted would
diverge. One sentence fixing the convention would close it.

### C7. Theorem 6.6 never states |lambda| = |mu|.
n is *defined* as x+y, and (-1)^n multiplies Phi_a. If |lambda| = |mu| is standing (surely it
is, for c_{lambda mu} to be the structure constant it looks like), then n = a+b+c as well, and
(-1)^{b+c}U_a has leading sign (-1)^{b+c}(-1)^{a+b+c} = (-1)^a. That is a visible
simplification the statement does not take, which makes me suspect either the simplification
was missed or |lambda| = |mu| is NOT standing. Worth one word of hypothesis either way.

### C8. In what sense is the formula "Closed"?
The paragraph immediately above Example 6.5 says of Theorem 6.3 that "for general rho, G_A is
itself a finite (branching) sum, so Theorem 6.3 is not a product formula". Theorem 6.6 is
titled "Closed". Its two sums are finite and explicitly indexed, which is good; but the whole
weight then rests on Phi_a(p_b p_c; x,y) being explicitly evaluable. If Phi_a is itself a
branching sum, "Closed" is doing the same work the author just denied to Theorem 6.3.

### C9 (checked, benign). Set vs multiset in {b-r, a+r+c} = {x,y}.
If x != y the condition forces the two values distinct and matching. If x = y, the set reading
{b-r,a+r+c} = {x} requires b-r = a+r+c = x, and the multiset reading requires the same.
Both readings agree. No defect; recording it as checked so it is not re-opened.

### C10 (checked, benign). Xi_a has no pole for admissible a.
[a] sits in a denominator. lambda is a length-3 *partition*, so every part is >= 1 and a >= 1;
[a] != 0 for generic parameter. No division by zero. Recorded as checked.

## Predictions I am making now, to be scored after I open the rest of the draft
P1: kappa is NOT simply the (s-1)-adic valuation; there will be an offset. (C2)
P2: there is a "box symmetry" statement elsewhere in the paper that is what licenses
    "any ordering", and Theorem 6.6 fails to cite it. (C1)
P3: the bare bracket [.] is in s, not t. (C6)
