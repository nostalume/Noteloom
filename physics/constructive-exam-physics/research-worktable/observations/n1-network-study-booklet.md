# N1 participant booklet

Use the route printed in your assigned sequence. Every link label is a conductance.
Find the current injected at `L` and include one boundary-law check. The sparse
local strip appears in the separate protocol and is visible only when the schedule
says so.

## Sequence N1

| Order | Phase | Variant | Route |
| ---: | --- | --- | --- |
| 1 | immediate_assisted | N1-I2-A | direct |
| 2 | immediate_assisted | N1-I3-B | direct |
| 3 | immediate_assisted | N1-I2-B | sparse |
| 4 | immediate_assisted | N1-I3-A | sparse |
| 5 | delayed_same_topology | N1-D2-A | direct |
| 6 | delayed_same_topology | N1-D3-B | direct |
| 7 | delayed_same_topology | N1-D2-B | sparse |
| 8 | delayed_same_topology | N1-D3-A | sparse |
| 9 | unseen_topology | N1-US-A | direct |
| 10 | unseen_topology | N1-UC-B | direct |
| 11 | unseen_topology | N1-US-B | sparse |
| 12 | unseen_topology | N1-UC-A | sparse |

## Sequence N2

| Order | Phase | Variant | Route |
| ---: | --- | --- | --- |
| 1 | immediate_assisted | N1-I2-B | direct |
| 2 | immediate_assisted | N1-I3-A | direct |
| 3 | immediate_assisted | N1-I2-A | sparse |
| 4 | immediate_assisted | N1-I3-B | sparse |
| 5 | delayed_same_topology | N1-D2-B | direct |
| 6 | delayed_same_topology | N1-D3-A | direct |
| 7 | delayed_same_topology | N1-D2-A | sparse |
| 8 | delayed_same_topology | N1-D3-B | sparse |
| 9 | unseen_topology | N1-US-B | direct |
| 10 | unseen_topology | N1-UC-A | direct |
| 11 | unseen_topology | N1-US-A | sparse |
| 12 | unseen_topology | N1-UC-B | sparse |

## Problem bank

### N1-I2-A

A reciprocal conductance network has links `L-C:1`, `R-C:1`, `C-A:1`,
`C-B:1`, `A-ground:1`, `B-ground:1`. Fix `L=1 V`, `R=0 V`.

### N1-I2-B

Links: `L-C:2`, `R-C:2`, `C-A:2`, `C-B:2`, `A-ground:1`,
`B-ground:1`. Fix `L=1 V`, `R=0 V`.

### N1-I3-A

Links: `L-C:1`, `R-C:1`, `C-A:1`, `C-B:1`, `C-D:1`,
`A-ground:1`, `B-ground:1`, `D-ground:1`. Fix `L=1 V`, `R=0 V`.

### N1-I3-B

Links: `L-C:2`, `R-C:2`, `C-A:2`, `C-B:2`, `C-D:2`,
`A-ground:1`, `B-ground:1`, `D-ground:1`. Fix `L=1 V`, `R=0 V`.

### N1-D2-A

Links: `L-C:1`, `R-C:1`, `C-A:1`, `C-B:1`, `A-ground:2`,
`B-ground:2`. Fix `L=2 V`, `R=0 V`.

### N1-D2-B

Links: `L-C:3`, `R-C:3`, `C-A:3`, `C-B:3`, `A-ground:1`,
`B-ground:1`. Fix `L=1 V`, `R=-1 V`.

### N1-D3-A

Links: `L-C:1`, `R-C:1`, `C-A:1`, `C-B:1`, `C-D:1`,
`A-ground:2`, `B-ground:2`, `D-ground:2`. Fix `L=2 V`, `R=0 V`.

### N1-D3-B

Links: `L-C:2`, `R-C:2`, `C-A:2`, `C-B:2`, `C-D:2`,
`A-ground:3`, `B-ground:3`, `D-ground:3`. Fix `L=1 V`, `R=-1 V`.

### N1-US-A

Links: `L-C:1`, `C-D:1`, `D-R:1`, `C-A:1`, `D-B:1`,
`A-ground:1`, `B-ground:1`. Fix `L=1 V`, `R=0 V`.

### N1-US-B

Links: `L-C:2`, `C-D:1`, `D-R:2`, `C-A:1`, `D-B:1`,
`A-ground:2`, `B-ground:2`. Fix `L=1 V`, `R=-1 V`.

### N1-UC-A

Links: `L-C:1`, `R-C:1`, `C-A:1`, `A-B:1`, `C-D:1`,
`B-ground:1`, `D-ground:1`. Fix `L=1 V`, `R=0 V`.

### N1-UC-B

Links: `L-C:2`, `R-C:2`, `C-A:1`, `A-B:2`, `C-D:1`,
`B-ground:1`, `D-ground:2`. Fix `L=2 V`, `R=0 V`.

No numerical answer is printed in this booklet.
