# N2 participant booklet

For each task, decide the warranted status before solving the terminal response:
`direct_gate`, `conditional_candidate`, or `refuse`. Give one brief structural
reason. No route is assigned, and the training sheet is not available.

## Sequence A1

| Order | Phase | Task |
| ---: | --- | --- |
| 1 | immediate_unassisted | N2-I-C |
| 2 | immediate_unassisted | N2-I-G |
| 3 | immediate_unassisted | N2-I-R |
| 4 | delayed_same_topology | N2-D-C |
| 5 | delayed_same_topology | N2-D-G |
| 6 | delayed_same_topology | N2-D-R |
| 7 | unseen_topology | N2-U-C |
| 8 | unseen_topology | N2-U-G |
| 9 | unseen_topology | N2-U-R |

## Sequence A2

| Order | Phase | Task |
| ---: | --- | --- |
| 1 | immediate_unassisted | N2-I-R |
| 2 | immediate_unassisted | N2-I-G |
| 3 | immediate_unassisted | N2-I-C |
| 4 | delayed_same_topology | N2-D-R |
| 5 | delayed_same_topology | N2-D-G |
| 6 | delayed_same_topology | N2-D-C |
| 7 | unseen_topology | N2-U-R |
| 8 | unseen_topology | N2-U-G |
| 9 | unseen_topology | N2-U-C |

## Task bank

### N2-I-C

A reciprocal conductance network has links `L-C:1`, `R-C:1`, `C-A:1`,
`C-B:1`, `A-ground:1`, `B-ground:1`. Terminals are fixed at `L=1`, `R=0`.

### N2-I-G

A reciprocal two-terminal network has one hidden junction joined equally to `L`
and `R`.

### N2-I-R

A directed linear-response network has
`K=[[1,0,-1],[0,1,-2],[-3,-1,4]]`.

### N2-D-C

A reciprocal conductance network has links `L-C:1`, `R-C:1`, `C-A:1`,
`C-B:1`, `A-ground:2`, `B-ground:2`. Terminals are fixed at `L=2`, `R=0`.

### N2-D-G

A reciprocal two-terminal network has one hidden junction and both link
conductances are 3.

### N2-D-R

A directed linear-response network has
`K=2[[1,0,-1],[0,1,-2],[-3,-1,4]]`.

### N2-U-C

A reciprocal conductance network has links `L-C:1`, `C-D:1`, `D-R:1`,
`C-A:1`, `D-B:1`, `A-ground:1`, `B-ground:1`.

### N2-U-G

A reciprocal path `L-A-B-R` has unit conductance on every link and no other link.

### N2-U-R

A reciprocal coupled-mode packet has one boundary and hidden block
`[[0,1],[1,0]]`.

Select one of the three statuses and give the structural reason. Do not compute the
terminal value.
