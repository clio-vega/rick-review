# Written BEFORE opening 2026-10-03-DS-from-N.pdf

My own 10-02 §6.2 derivation (reviews/2026-10-02-review-rick-day216-nabla-transport.md):

    e^*_lambda = t^{-n(lambda')} N(e_lambda)
    e_lambda = sum_{nu <| lambda'} a_{lambda nu} P_nu ,  P_nu = sum_mu b_{nu mu} e_mu
    c_{lambda mu} = t^{-n(lambda')} sum_nu a_{lambda nu} t^{n(nu)} s^{n(nu')} b_{nu mu}
    support: mu' <| nu <| lambda'
    nu >| mu'  =>  nu' <| mu  =>  n(nu') >= n(mu), equality iff nu = mu'
    => val_s c_{lambda mu} >= n(mu), equality iff a_{lambda mu'}(0) b_{mu' mu}(0) != 0

GAP I DECLARED AGAINST MYSELF on 10-02 (quote): "modulo two facts I asserted and did not
prove: that the e <-> P transition is regular at s=0, and that the diagonal entries are
nonzero there."

## Predictions to test against his text

P-a. He must use e^*_lambda = t^{-n(lambda')} N(e_lambda) or an equivalent.
P-b. His "single term carries the minimal s-order" = my "equality iff nu = mu'".
     SAME STATEMENT. So agreement here is NOT independent confirmation.
P-c. CRITICAL: does he discharge the s=0 regularity of a and b, or inherit my gap?
     If he inherits it, his 15 lines are 15 lines + my unproved sentence, and the
     result is not `proved`. This is the thing to look for. If we agree, check
     whether we agree for the same REASON or made the same MISTAKE.
P-d. d_{lambda mu}(t) = sum_rho t^{n(rho)-n(lambda')} Ktilde_{rho mu'}(t) K_{rho' lambda}
     is NEW to me -- I never computed the lowest coefficient, only its order.
     This is the part I can check independently without risk of self-confirmation.
     => SPEND THE VERIFICATION BUDGET HERE, not on val_s.
P-e. n(nu') >= n(mu) with equality iff nu = mu' needs: dominance order, nu' <| mu
     => n is strictly order-reversing. Check: is n(.) strictly monotone on dominance,
     or only weakly? If only weakly, "equality iff" FAILS and support could have
     several minimal-order terms that could cancel. THIS IS MY OWN STEP AND I
     ASSERTED IT. Verify it independently.
