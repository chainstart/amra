# A disjoint residue-core bridge

Let E and C be disjoint finite multisets of positive integers. Fix q ≥ 2.
Suppose that, for every 0 ≤ r < q, a subset sum of E is

    e_r = q h_r + r,

and suppose the subset sums of C contain

    qA, q(A+1), …, q(A+L).

Write h₋ = min_r h_r and h₊ = max_r h_r. If L ≥ h₊ − h₋, then the subset
sums of E ∪ C contain every integer from

    q(A+h₊)  through  q(A+L+h₋+1) − 1.

Indeed, for every integer k in [A+h₊, A+L+h₋] and every residue r, the number

    qk + r = e_r + q(k−h_r)

uses disjoint supports, and k−h_r belongs to [A, A+L]. Varying r, then k,
gives the claimed consecutive interval. Its length is

    q(L−h₊+h₋+1).

This lemma identifies precisely what was absent from the earlier fixed-modulus
coverage theorem. Arbitrary residue representatives are enough if a disjoint
tail supplies a consecutive interval of quotient values for the zero residue,
but neither mere gcd one nor residue coverage supplies that core. For Erdős
#354, a closing route may therefore fix one modulus q, take a finite
residue-covering prefix, and prove that arbitrarily far tails contain
arbitrarily long q-multiple cores. The latter assertion remains open.
