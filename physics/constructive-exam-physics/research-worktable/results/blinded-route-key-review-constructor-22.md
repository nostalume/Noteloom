# Result 22: blinded route-key review constructor

## Question and obstruction

`C-human-v2` makes learner observations reconstructible, but its first dependency
is an independently reviewed route key. The worktable author cannot supply that
evidence: self-review would share the authored classification and would not test
whether the prompts admit plausible alternative routes.

The missing object is therefore not another answer key. It is a blinded acquisition
contract whose records can distinguish independent agreement, ambiguity, dispute,
and protocol failure.

## `C-key-v1`

The contract separates reviewer-level state from task-level judgment:

```text
reviewer manifest
  = identity + assigned order + expertise domain
    + authored-key blindness + peer-review blindness + provenance

task judgment
  = review identity + reviewer identity + task identity
    + selected route + physical rationale + provenance
```

This normalized split avoids repeating qualification and blinding claims twelve
times while retaining a foreign-key witness for every judgment. The reviewer packet
contains a neutral route glossary and the twelve prompts, but no authored route
mapping. Reviewers use opposite `R1`/`R2` orders and submit before discussion.

The executable audit admits a judgment only when its reviewer manifest exists and
records both blindness conditions. Unblinded or unmanifested judgments remain in
the material record but enter an excluded count and produce `protocol_invalid` when
no admitted judgment remains. For admitted reviews, each task returns:

```text
0 reviews              -> unreviewed
1 review               -> insufficient_review
>=2, unanimous key     -> agreed
>=2, differing routes  -> ambiguous
>=2, unanimous non-key -> key_disputed
```

Two reviews are the minimum needed to observe disagreement; agreement between two
reviewers is not universal expert consensus. Declared expertise and blindness are
administrative evidence whose truth software cannot independently verify.

## Learner-session repair

The same audit pass found that existing version 2 fields already contain enough
information to enforce its session promises. The execution loader now requires one
session and one recorded delay per participant-phase, prevents one session from
spanning phases, and requires delayed-unseen work to occur later than internalized
work. This is an implementation repair under `C-human-v2`, not a new contract
version.

## Verification and disposition

Test-first probes failed when the reviewer-manifest API and blinded packet were
absent and when inconsistent phase sessions were accepted. The implemented
fixtures now exercise admitted and unblinded reviewers, all route-key dispositions,
duplicate review refusal, packet/task consistency, and relational session/delay
checks.

`C-key-v1` is **constructed-unpopulated**. The checked-in reviewer and judgment
templates contain zero rows, so all twelve route tasks remain `unreviewed`. This
stage constructs the evidence-acquisition operation; it does not supply independent
expert evidence and does not change the human-benefit disposition.

The next irreducible action is external: at least two qualified, mutually blinded
reviewers must complete the packet. Their audits feed the pre-evidence policy in
[Result 23](route-key-preflight-kernel-23.md), which decides whether tasks need
more review, contract revision, or may enter the learner pilot. No synthetic or
assistant judgment can replace that bridge.
