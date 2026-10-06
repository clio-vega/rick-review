import sympy as sp
from kostka_d_matrix import (partitions, conj, kostka, n_stat,
                             kostka_foulkes, kostka_foulkes_tilde)
t = sp.symbols('t')

def rick_d(lam, mu, parts, KT):
    s = sp.Integer(0)
    for nu in parts:
        k = kostka(conj(nu), lam)
        if k: s += k * KT[(nu, conj(mu))]
    return sp.simplify(sp.expand(s * t**(-n_stat(conj(lam)))))

def kirillov_M(lam, mu, parts, KF):
    """Kirillov verbatim: M(e,P)_{lam mu} = sum_nu K_{nu lam} K_{nu' mu}(t)"""
    s = sp.Integer(0)
    for nu in parts:
        k = kostka(nu, lam)
        if k: s += k * KF[(conj(nu), mu)]
    return sp.expand(s)

print("TESTING:  d_{lam mu}(t) == t^{n(mu')-n(lam')} * M(e,P)_{lam mu'}(1/t)\n")
grand_ok = grand_tot = 0
for n in range(2, 6):
    parts = list(partitions(n))
    KF={}; KT={}
    for a in parts:
        for b in parts:
            KF[(a,b)]=kostka_foulkes(a,b); KT[(a,b)]=kostka_foulkes_tilde(a,b)
    ok=tot=0; nonconst=0
    for lam in parts:
        for mu in parts:
            lhs = rick_d(lam,mu,parts,KT)
            M   = kirillov_M(lam, conj(mu), parts, KF)
            rhs = sp.simplify(sp.expand(t**(n_stat(conj(mu))-n_stat(conj(lam))) * M.subs(t,1/t)))
            tot+=1
            good = sp.simplify(sp.expand(lhs-rhs))==0
            ok+=good
            if lhs!=0 and sp.simplify(lhs-lhs.subs(t,0))!=0: nonconst+=1
            if not good and tot<200:
                print(f"   MISMATCH n={n} lam={lam} mu={mu}: d={lhs}  rhs={rhs}")
    print(f" n={n}: {ok}/{tot} agree   (nonconstant d entries: {nonconst})")
    grand_ok+=ok; grand_tot+=tot
print(f"\nTOTAL {grand_ok}/{grand_tot}")

# Negative control: drop the t-power prefactor
print("\nNEGATIVE CONTROL: same relation WITHOUT the t^{n(mu')-n(lam')} prefactor")
for n in [4]:
    parts=list(partitions(n)); KF={}; KT={}
    for a in parts:
        for b in parts:
            KF[(a,b)]=kostka_foulkes(a,b); KT[(a,b)]=kostka_foulkes_tilde(a,b)
    ok=tot=0
    for lam in parts:
        for mu in parts:
            lhs=rick_d(lam,mu,parts,KT)
            rhs=sp.simplify(sp.expand(kirillov_M(lam,conj(mu),parts,KF).subs(t,1/t)))
            tot+=1; ok += (sp.simplify(sp.expand(lhs-rhs))==0)
    print(f"  n=4 without prefactor: {ok}/{tot}  => {'CONTROL FIRED' if ok<tot else 'BLIND'}")
