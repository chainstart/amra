# Independent audit: base-retaining/top-index rank-five candidate

## Verdict

The proposed implication is algebraically correct as a **conditional
sufficient lemma**.  Independent Macaulay arithmetic also reproduces the
stronger top-index margin statistics on all 823,476 accepted rows of the
author's stated adaptive finite domain.  No counterexample is found there.

This is not an all-parameter proof of the top-index inequality.  The adaptive
windows are not exhaustive inside a fibre when carry patterns re-enter, and
the candidate does not close every c=1 chamber, produce a uniform seed before
rank 42, or solve Erdős #776.

## 1. Macaulay definitions

For `N>=0`, independently form its canonical rank-`k` word greedily:

```text
N=C(a_k,k)+C(a_(k-1),k-1)+...+C(a_1,1),
a_k>a_(k-1)>...>a_1>=0.
```

Then

```text
U_k(N)=C(a_k,k+1)+...+C(a_1,2),
top_k(N)=a_k.
```

If `c=top_3(p)`, then

```text
C(c,3)<=p<C(c+1,3),
C(c,4)<=U3(p)<=C(c+1,4)-1.
```

The upper bound follows from monotonicity of Macaulay raising below the next
cap; it is deliberately not the sharp value at `C(c+1,3)-1`.  Similarly, for
`d=top_3(v)` and `a=top_2(alpha)`,

```text
U3(v)>=C(d,4),
U2(alpha)<=C(a+1,3)-1.
```

The independent implementation checks greedy reconstruction and both cap
bounds on 40,000 positive `(N,k)` rows as a software guard.  The displayed
bounds themselves follow directly from the definition and are not inferred
from this finite check.

## 2. Conditional deduction

Put

```text
D=U3(v)-U3(p)-U2(alpha).
```

The cap inequalities give

```text
D >= C(d,4)-C(c+1,4)+1-U2(alpha).
```

Therefore the base-retaining condition

```text
C(d,4)-C(c+1,4)-U2(alpha) >= 0
```

implies `D>=1`.  Since the exact rank-five surplus in this chamber is

```text
gamma5=D-1,
```

the conclusion is `gamma5>=0`.  Thus the claimed implication is correct,
including the otherwise easy-to-miss unit supplied by
`U3(p)<=C(c+1,4)-1`.

The stronger top-index condition is

```text
T=C(d,4)-C(c+1,4)-C(a+1,3) >= 0.
```

Using `U2(alpha)<=C(a+1,3)-1` gives `D>=T+2`, hence in fact
`gamma5>=T+1>=1`.  This stronger condition is sufficient but remains
unproved universally.

## 3. Independent actual-state reconstruction

No author function or Macaulay engine is imported.  For every tested
`(j,k,r)`, the verifier independently reconstructs

```text
h=112*2^(j-1),
(k-1)q=2h-C(k-1,2)-2+r,
u=r+k-1,                 b=q+k,
alpha=C(r+1,2)-kq-C(k,2),
beta=alpha+C(u,2)-C(r,2)-1,
tau=kq+C(k,2)+1-r,
p=U2(alpha)-tau+1,       v=U2(beta)-tau,
gamma4=v-p-alpha-tau+1,
gamma5=U3(v)-U3(p)-U2(alpha)-1.
```

It retains only legal `(++ -> ++)` rows with `gamma4<0`, independently
locates one sign-change wall, and evaluates the declared target and wall
windows.

## 4. Finite adaptive statistics

The reconstruction uses

```text
j=6,...,60,70,80,90,100,
4<=k<=300.
```

It obtains exactly:

```text
accepted actual (++ -> ++) rows : 823,476
fibres with an accepted window  : 7,812
base-leading counterexamples    : 0
top-index counterexamples       : 0
```

Both independently minimized margins occur at

```text
(j,k,r)=(6,4,145), h=3584, q=2436,
alpha=835, p=1160, v=11075,
top_2(alpha)=41, top_3(p)=20, top_3(v)=41,
base-leading margin=84520,
top-index margin=83805,
gamma4=-525, gamma5=89319.
```

The independent run also rediscovers the first p-free failure in the accepted
windows at `(j,k,r)=(21,4,26466)`, with

```text
p-free margin=-136419183,
base-leading margin=742028295195,
top-index margin=741991397675,
gamma5=859354068710.
```

The independent wall locator queried 181,573 raw centring points, 74 more than
the author's 181,499 bookkeeping count.  This comes from a separately coded
first-target binary search.  The accepted row count, fibre count, extrema,
absence of counterexamples and p-free witness agree exactly; raw locator call
count is not treated as a mathematical statistic.

## 5. Evidence boundary

The finite scan does not prove the sufficient inequality for every legal
dyadic strip and offset.  Binary wall centring is explicitly nonexhaustive
when carries make the sign pattern nonmonotone.  Moreover the condition is
only one rank-five chamber lemma; global closure still needs exhaustive actual
routing, a seed before rank 42 and composition with the antichain construction.

Accordingly:

- the conditional cap deduction passes;
- the reported finite top-index evidence passes;
- universal rank-five closure is open;
- the public problem is unchanged.

## Reproduction

```sh
env AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-776-c1-round3/audit/independent_verify_top_index_rank5.py
```

The successful run completed in about 134 seconds, with no Lean. SHA-256:

- verifier: `91e4a51904b7540766513e1563791f0217042709f10eb6164bd9be3046b9e127`
- result JSON: `8277c5fbfb60021d1034cbbc090a64517772b1d164766a4a0e25684e2453e0fd`

