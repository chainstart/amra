# K4,r9 adaptive cell split at ranks seven and eight

Verdict: the proposed quadratic rank-seven recovery is **valid only at the
single actual cell `j=33`**.  It is not stable on odd `j>=33`.

For the actual family

```text
h=112*2^(j-1), q=(2h+4)/3, (k,r,u,b)=(4,9,12,q+4),
tau=4q-2,
```

the audited rank-four tails are

```text
P=[(q-6,4),(q-11,3),(q-15,2),(35995,1)],
V=[(q-5,4),(q-10,3),(q-14,2),(1319452,1)].
```

Set `A=U4(P)-tau+1`, `B=U4(V)-tau`.  The A word is stable:

```text
A=[(q-6,5),(q-11,4),(q-16,3),(q-20,2),(647801944,1)].
```

At `j=33` only,

```text
B=[(q-5,5),(q-10,4),(q-15,3),(q-17,2),(229094347523,1)]
```

and Pascal cancellation gives

```text
gamma7=q^2-42q+26241900209700351953826>0.
```

At every checked stable odd cell from `j=35` onward the true word is instead

```text
B=[(q-5,5),(q-10,4),(q-15,3),(q-19,2),(870476130358,1)],
gamma7=378864136937404017548365-4q.
```

The sign changes between `j=71` and `j=73`; hence every odd member from
`j=73` onward in this stable cell is negative at ranks five, six, and seven.
This kills any claim of uniform rank-seven recovery for the family.

For the next tails `C=U5(A)-tau+1`, `D=U5(B)-tau`, a second cell transition
occurs between `j=73` and `j=75`.  From `j=75` onward the checked stable words
give

```text
gamma8=71769096623329310875999415996803170658344870942-4q.
```

This becomes negative between `j=147` and `j=149`.  Thus K4,r9 also contains
actual members negative through rank eight.  This is mechanism-falsification
evidence for adaptive recovery; it is not by itself a counterexample to the
public antichain statement or to recovery at a later parameter-dependent rank.

The accompanying checker proves the displayed cell identities symbolically
with exact binomial polynomials and replays selected actual dyadic members with
a fresh greedy Macaulay engine under the campaign resource cap.
