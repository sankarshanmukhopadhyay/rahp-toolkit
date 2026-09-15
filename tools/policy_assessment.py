#!/usr/bin/env python3
"""Compatibility entry point for the experimental RAHP policy workflow (#662).

The reviewed v2 research workflow is implemented in ``policy_assessment_v2``.
This module preserves the original import/CLI path used by tests and research
notes while keeping the stable RAHP controller untouched.
"""

from policy_assessment_v2 import (  # noqa: F401
    ASSESSMENT_SCHEMA,
    evidence_work_queue,
    main,
    render_markdown,
    review_subject,
    synthesize_assessment,
)


if __name__ == "__main__":
    raise SystemExit(main())
