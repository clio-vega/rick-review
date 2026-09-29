# Is Rick's Step-H functional QJ(n,p) = sum_k f_k q_{n+k} q_{p-k} equal to
# Jing's / Macdonald's Hall-Littlewood Q_{(n,p)} for the two-part composition (n,p)?
R.<t> = QQ[]
Sym = SymmetricFunctions(R.fraction_field())
HLQ  = Sym.hall_littlewood(t).Q()
HLQp = Sym.hall_littlewood(t).Qp()
m    = Sym.monomial()
s    = Sym.schur()

def q(n):
    # one-row HL function q_n = Q_{(n)};  q_0 = 1
    if n < 0: return Sym.zero()
    if n == 0: return Sym.one()
    return Sym(HLQ([n]))

def f(k):
    return R.fraction_field()(1) if k == 0 else R.fraction_field()(t**k - t**(k-1))

def QJ(n,p):
    return sum(f(k)*q(n+k)*q(p-k) for k in range(0, p+1))

print("n p | QJ(n,p) == Q_{(n,p)} ?   (Q_{(n,p)} = HL Q at partition (n,p), n>=p)")
allok=True
for n in range(1,7):
    for p in range(1,n+1):
        lhs = QJ(n,p)
        rhs = Sym(HLQ([n,p]))
        ok = (lhs == rhs)
        allok &= ok
        print(f"{n} {p} | {ok}")
print("ALL (n>=p):", allok)

print()
print("Now the straightening range n < p (composition, not partition):")
for n in range(1,5):
    for p in range(n+1,6):
        lhs = QJ(n,p)
        # Macdonald's straightening for two-row Q: Q_{(n,p)} = -Q_{(p-1,n+1)} when n<p ; Q_{(n,n+1)}=0
        if p == n+1:
            guess = Sym.zero(); label="0"
        else:
            guess = -Sym(HLQ([p-1,n+1])); label=f"-Q_({p-1},{n+1})"
        print(f"n={n} p={p}: QJ == {label} ?  {lhs == guess}")
