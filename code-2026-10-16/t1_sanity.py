from qsym_indep import *
# rank 1, phi=0: his stated normal form M_a*M_b = M_ab + q^{ab} M_ba + M_{a+b}
S = Setup([[1]], [[0]])
got = qs_product(S, ((2,),), ((3,),))
print("M_2 * M_3 =")
for w, c in sorted(got.items()):
    print("   ", w, c)
want = {(((2,),(3,))): {0:1}, (((3,),(2,))): {6:1}, (((5,),)): {0:1}}
print("matches his rank-1 formula M_ab + q^{ab}M_ba + M_{a+b}:", got == want)
