# Independent raw-recurrence audit of M01

Verdict: **reproduced**.  Starting only from `(j,q,k,r)=(7,4845,4,204)`, the
canonical Macaulay recurrence gives the actual state
`(h,b,u,c)=(7168,4849,207,1)`.  Both adjacent rank-2 decompositions are valid,
so `c=1` is actual rather than assigned.

The full orbit gives

- `gamma3=-18772`, `gamma4=-2350`;
- first positive tails `(alpha,beta)=(1524,2138)`;
- second positive tails `(p,v)=(7794,26150)`, hence actual `++ -> ++`;
- raw and tail computations agree at `gamma5=245481>0`.

For the proposed cubic strengthening, `alpha=C(55,2)+39` and
`e=v-p=18356<C(54,3)=24804`, with gap `-6448`.  Nevertheless the weaker gate
has `U_3(e)-U_2(alpha)-1=183083>0`.  Thus this one actual row decisively
refutes M01 while preserving both the G++ conclusion and the next raw
recurrence value.

The checker is standalone and imports no author evidence.  It ran with a
512 MiB virtual-memory ceiling and a 120-second timeout (wall time below
0.1 seconds), without Lean.  Script SHA-256:
`29c4eaf134d6869caafdcd0a52dece29b89209e9874c493458a46676c13c0a2d`.

This audits only the stated witness and does not close the public problem.
