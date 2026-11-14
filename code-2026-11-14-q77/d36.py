from dims import *
import sys
which = sys.argv[1]
if which == 'A': print('(3,6) |monoid|,dimA mod p =', dimA(3, 6, P1), flush=True)
else: print('(3,6) U,dimB mod p =', dimB(3, 6, P1), flush=True)
