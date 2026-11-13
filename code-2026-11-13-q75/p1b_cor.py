"""P1b Corollary 2: M_2^perp R_s = 0 iff s even alternating (L>=3), from the pairing.
Plus a control for Q75 Cor 2: count non-alternating s where Sym does NOT surject."""
import sys
from itertools import product
sys.argv = [sys.argv[0], '1']
from keyid import perp_M
from qsym import mask_to_comp, str_to_mask
def even_alt(s): return len(s) % 2 == 0 and all(s[p] != s[p+1] for p in range(len(s)-1))
for L in range(3, 12):
    zero = [s for s in (''.join(b) for b in product('01', repeat=L))
            if not perp_M((2,), mask_to_comp(str_to_mask(s), L + 1))]
    pred = [s for s in (''.join(b) for b in product('01', repeat=L)) if even_alt(s)]
    print('L=%d: M_2^perp R_s = 0 for %s ; predicted %s ; %s' % (L, zero, pred, 'OK' if sorted(zero) == sorted(pred) else 'MISMATCH'))
