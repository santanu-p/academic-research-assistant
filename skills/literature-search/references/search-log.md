# Search-log schema

Use one query row for each executed query or separately documented search operation. Preserve exact syntax in a text field or linked file; do not reduce it to the topic label. Unknown counts remain unavailable rather than zero.

| Field | Meaning |
|---|---|
| search_id | Stable local identifier for this operation |
| purpose | Orientation, formal review retrieval, update, or gap check |
| source_and_interface | Database or repository plus the interface actually used |
| executed_at | Execution date and relevant timezone |
| exact_query | The complete query, including field tags and operators |
| filters | Applied dates, languages, types, and other restrictions |
| count_reported | Count displayed by the source, if available |
| count_exported | Records actually exported or captured |
| export_location | Local artifact or available export reference |
| limitations | Access caps, unavailable fields, failed exports, or coverage issues |

For citation chaining, add the seed identifier, direction, source used to retrieve citations, and screening boundary. For an update search, link the earlier search, record changes in syntax or coverage, and state how overlap was handled.

Keep a separate candidate table with record identifier, bibliographic identity, persistent identifier, originating search IDs, screening status, reason, and linked study ID where known. A duplicate can be marked and linked without erasing its retrieval provenance. A study ID should not be inferred merely from similar titles.

The coverage note should answer: which questions guided retrieval; which sources and dates were covered; which restrictions were deliberate; which sources were unavailable; what supplemental discovery was performed; and what the retrieved set cannot establish. For a rapid search, state the time or scope limit explicitly. Do not fabricate full-text screening or independent review to complete the schema.
