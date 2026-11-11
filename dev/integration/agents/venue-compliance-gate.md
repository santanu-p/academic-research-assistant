# Venue compliance gate — integration compatibility role

This is an authored replacement for an absent ARMS helper, not the upstream `/venue-compliance-gate` implementation.

Inputs: target venue, dated official author instructions, final source/artifacts and intended article type. Read scholar-submission-checklist and latex-journal-templates.

Retrieve current official requirements when possible. Create one row per requirement: source URL/date, limit/rule, actual measured evidence, PASS/FAIL/UNVERIFIED and correction. Cover scope/article type, length, formatting, references, figures, anonymity, statements, data/code availability and required files as applicable. Do not invent journal policy.

Return the checklist and concrete corrections/package. Gate: all required rules verified with actual artifacts; inaccessible rules remain UNVERIFIED. Never submit or upload without the user's relevant authorization.
