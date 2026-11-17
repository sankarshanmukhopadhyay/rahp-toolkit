# Combined DTG review source evidence for Registry cutover

The canonical Toolkit DTG router preserves the existing combined-review
assessment key, route classification, body and publication owner. Each combined
event additionally carries:

- source_observations: sorted original finding identities, repositories and
  exact commit-evidence revisions, with explicit unresolved status.
- source_pins: distinct repository/commit SHA pairs supported by source
  commit evidence URLs.
- unanchored_finding_ids: grouped observations that do not have such evidence.

This metadata prevents a group assessment key from being confused with
source-specific transfer authority. A release-tag observation is not an
immutable commit merely because a tag resolves today. A commit link from a
different repository cannot pin the observed artifact. Even when every
finding has a commit pin, a mixed-repository group still needs an explicit
proposition owner, current-observation Registry acknowledgment and compatible
controller/DPIP consumer before publication may move.

The Toolkit and Registry router copies must remain byte-identical for the
same source and policy. This is a source-provenance contract change, not a
change in classification, a new assessment case, or cutover activation.
