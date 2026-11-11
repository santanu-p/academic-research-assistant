---
name: search-strings
description: "Write expert Boolean search strings and database-specific queries for Google Scholar, Semantic Scholar, Scopus, Web of Science, JSTOR, ERIC, SSRN, arXiv, IEEE Xplore, ProQuest and library catalogs. Use when the user needs a search query."
---

# Search Strings


## Building blocks
- **OR** joins synonyms inside one concept: ("remote work" OR telework OR "work from home").
- **AND** joins different concepts: (remote work terms) AND (productivity terms).
- **NOT** excludes, used sparingly.
- **Quotes** for exact phrases: "hybrid work".
- **Truncation** with an asterisk: employ* finds employee, employees, employment.
- **Parentheses** group each concept.
- **Field tags** narrow to title or abstract where the database supports them.

## Database notes
| Database | Tips |
|---|---|
| Google Scholar | Keep it short; supports quotes, OR, minus and intitle:; no truncation |
| Semantic Scholar | Natural-language queries work; filter by field, year and venue |
| Scopus | TITLE-ABS-KEY( ) field; full Boolean and truncation |
| Web of Science | TS= for topic; NEAR/x for proximity |
| JSTOR | Humanities and social sciences; use advanced search fields |
| ERIC | Education; use the ERIC thesaurus descriptors |
| SSRN, arXiv | Preprints in economics, law, physics, computer science and math |
| IEEE Xplore | Engineering and computing; use the command search |

## Output format
1. The concept table with synonyms.
2. A full Boolean string.
3. Adapted versions for 2 or 3 databases that fit the topic.
4. Suggested filters (years, document type, language) and tips if results are too many or too few.
