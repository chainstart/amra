# Bounded far-domain replay through ranks seven and eight

This exact replay extends the frozen round-three domain

```text
j in {56,60,64,80,100,120}, k=2..80,
compatible r<=1000 plus 17 probes around each first-tail wall.
```

Among the 2,304 states with `gamma5<0` and `gamma6<0`:

```text
rank-seven borrow                 0
gamma7<0                         30
rank-eight borrow on those 30     0
gamma8<0 on those 30              0
```

The minimum rank-seven row is `(j,k,r)=(120,4,10)`, with

```text
gamma7=-198498047370537044820648728081422631270,
gamma8=53999742912712667776564441482308492842973122991372.
```

Thus uniform rank-seven recovery is falsified even in the old finite domain,
while rank eight recovers all 30 detected failures there.  This is bounded
mechanism-falsification evidence only.  It neither proves uniform rank-eight
recovery nor conflicts with the separate K4,r9 stable family, whose rank-eight
surplus becomes negative at much larger `j`.
