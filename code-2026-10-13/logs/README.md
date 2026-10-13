# Run logs for the 2026-10-13 review of Rick's Theorem H (§5) and Box Complement (§9)

Extension is **`.txt`, not `.log`, deliberately.** This repo's `.gitignore` ignores `*.log` and
`*.out` because here both are LaTeX byproducts (the file says so in its own header, and warns that
in `proofs/` the same extensions mean computational evidence). Renaming respects both conventions
without editing a shared ignore file. A `git add` of `*.log` here silently adds nothing.

| file | script | what it shows |
|---|---|---|
| `t1.txt` | `t1_ncount.py` | `eq:ncount` 1772/1772; wrong-convention control fails 885/885 on the asymmetric witnesses; 887 strips blind |
| `t2_n6.txt` | `t2_run.py 6` | four mechanisms for `d_{λμ}` agree 209/209, `n ≤ 6`; positivity 209/209; control C1 (HL norms) 44/44 through `n ≤ 7` in the sibling `n=7` run |
| `t3.txt` | `t3_run.py 5` | `thm:subset` M1=M2; Hikita Thm 3.12; `thm:DS` divisibility/support; `cor:dmatrix` end-to-end; Hikita Lemma 6.3 corner |
| `t4.txt` | `t4_rest.py 5` | Theorem H(1) 173/173 (66 biting); H(2) 39/39; controls C3, C4, C5 |
| `t5b.txt` | `t5_box.py` | §9: `thm:box` 12/12, `cor:column` 12/12, `cor:pieri` 23/23, `thm:lin` 18/18, printed `Lead` example 3/3 |
| `t6.txt` | `t6_n6.py` | `n = 6` extension: M1=M2 11/11, `cor:dmatrix` 121/121, support 121/121, `d(0)=1` 64/64 |
| `t7.txt` | `t7_kirillov.py` | the factorisation `rem:H` attributes to Kirillov98, as printed: 88/88; `rem:H` ≡ `cor:dmatrix` 88/88 |

Two harness bugs of mine showed up in earlier runs and are recorded here so the numbers above are
read correctly. In `t5_box.py` I first looked up complemented partitions with their zero parts
retained (the dicts are keyed without zeros), producing three spurious `thm:box` failures; and in
its `thm:lin` arm I first fed `e^⋆_{(k,J)}` where the theorem is about `e_k ⋆ (e_{j_1}···e_{j_p})`
with an *ordinary* product inside, producing nine spurious failures. Both were mine, both are fixed
in the committed scripts, and neither was a defect in the paper.

`t3.txt`'s `r=0` line for Hikita Thm 3.12 is a third such case: at `r=0` the predicted value needs
both terms, `(1−s)[1]_t e_1 + s·e_1·e_0 = e_1`, and my harness suppressed the second when `r=0`.
The theorem holds at `r=0`; the harness did not.
