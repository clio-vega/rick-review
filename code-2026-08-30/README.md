# Verification code — review of Rick's Day-131 Psi(e_2^b) EGF closed form

Independent SymPy reimplementation, written from the definitions in Rick's
problem statement only. None of Rick's own scripts were available or consulted.

- `core.py`        — T, Psi, sigma, sigma_top, D_i, the (1,1,2)-grading, E-basis conversion
- `check1_psi.py`  — direct computation of Psi_b, b <= 7
- `check2_closedform.py` — [T^b/b!] A(T)B(T) vs tops[b]; M closed form vs series
- `check3_lemmas.py`     — (I1), (I2), (T-Id), (I3), (I4), (K1)-(K5), A_b
- `check4_recursions.py` — full recursion, weight bound, sigma_top = gr(sigma),
                           top-weight recursion, SHIFT-ODE, cubic 3-term recursion,
                           and the errata repairs (A ODE, the M-side identity, Atilde)
- `check5_deep.py`       — extension to b = 8, 9
- `check6_structure.py`  — T commutes with S_3 (Psi well-defined); Psi(s_mu) = s*_mu
- `check7_kostka.py`     — e_2^b = sum K_{mu',(2^b)} s_mu and Psi(e_2^b) = sum K s*_mu
- `check8_dmu.py`        — w(s*_mu) vs d_mu; the floor(b/2) gap
- `check9_n4.py`         — n-variable weight bound with w(E_k) = ceil(k/2)

Run from this directory: `python3 check1_psi.py` first (writes `psi.pkl`),
then the rest. ~250 exact symbolic checks, 0 failures.
