# N1 independent network-key reviewer packet

Review the twelve prompts in the participant booklet without consulting the
administrator answer key, authored sparse orders, or another reviewer. For each
variant:

1. independently compute the current injected at `L`;
2. write a shortest competent direct nodal solution;
3. apply the printed sparse local strip and write its pivot order;
4. judge whether both routes preserve the same target and physical assumptions;
5. judge whether the direct route is a fair competent baseline rather than a
   deliberately inflated method.

After submitting those materials to the administrator, compare against the sealed
answer key and record one TSV row. `exact_answer_agrees` refers to your independent
answer. `direct_route_valid` and `sparse_route_valid` refer to mathematical and
physical validity. `baseline_competent` is false if the authored direct instruction
systematically forces avoidable work. Explain every false value in `notes`.

Record real expertise and provenance. A reviewer who saw authored routes or peer
work is retained but cannot satisfy the independent-review count.
