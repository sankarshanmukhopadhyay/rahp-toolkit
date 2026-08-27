# Combined review judgment packets

A combined DTG Portfolio Monitor → RAHP review deliberately separates deterministic evidence preparation from semantic assurance judgment.

The combined-review worker resolves each routed Portfolio Monitor finding into a reviewer packet before leaving the issue at `judgment-required`. The packet supplies repository/change context, Monitor classification, evidence links, related repositories, an indicative assurance dimension, and the exact proposition the reviewer must classify as preserved, strengthened, weakened, new, or uncertain.

The packet does **not** infer the assurance outcome. Keyword-derived assurance dimensions are navigation aids only; the reviewer remains responsible for the proposition-level conclusion, boundary/falsification analysis, and any decision to create a new RAHP finding or composition.

A packet must fail visibly if a routed finding ID cannot be resolved from the pinned Portfolio Monitor snapshot. Opaque finding hashes must not silently become a human reconstruction task.

For each finding the reviewer records:

- disposition: `preserved | strengthened | weakened | new | uncertain`;
- rationale / boundary case;
- follow-up: none, new RAHP finding, new composition, or regression action.

The review closes only after a cross-item synthesis checks whether individually benign changes jointly create a new assurance proposition and whether any provisional no-action disposition from the portfolio controller must be reversed.
