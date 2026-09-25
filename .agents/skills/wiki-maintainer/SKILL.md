---
name: wiki-maintainer
description: >-
  Use this skill to maintain the project's knowledge base and wiki. 
  It defines the directory layout, page conventions, and operations 
  for ingesting new sources, querying information, and logging decisions.
---

# Wiki Maintainer Skill

This skill allows you to act as the persistent knowledge base maintainer for the project. 

## The Core Philosophy
The Knowledge Base (Wiki) is a structured repository tracking architecture, design decisions, and domain concepts as the project grows.
You (the LLM) write and maintain the notation, structure, citations, index, and logs.
**The user owns the frame-bearing sentences, what counts as central, and all `[[wikilinks]]`** — you suggest links, but never make them.

## Directory Layout
Maintain the following structure in the Obsidian vault at `/home/sahaj/obsidian_vault/projects/knowledge_engine`:
```text
raw/               ← immutable source documents (papers, docs, references). Never modify.
wiki/              ← LLM-maintained markdown pages
  index.md         ← catalog of all pages (update on every ingest/decision)
  log.md           ← append-only history of setup/ingests/decisions/lints
  architecture/    ← system design, data flow, component boundaries, diagrams
  concepts/        ← domain concepts 
  decisions/       ← design choices with reasoning (why X over Y) + resistance logs
  queries/         ← filed Q&A sessions worth keeping
  sources/         ← summaries of ingested docs/articles
```

## Page Conventions
- All wiki pages live in `wiki/` or subdirectories of it.
- Filename: lowercase, hyphenated. e.g. `evaluation-protocol.md`
- Every page starts with a `# Title` and a one-line summary below it.
- Add YAML frontmatter with `tags` and `updated` date.
- Cross-reference related pages with `[[page-name]]` — **The user makes these**; you only suggest candidates in prose.

## Operations

### 1. Ingest
When the user drops a file in `raw/` and says "ingest this":
1. Read the source.
2. Discuss key takeaways briefly with the user.
3. Write a summary in `wiki/sources/`.
4. Update `wiki/index.md`.
5. Update relevant architecture/concept/decision pages.
6. Append to `wiki/log.md`: `## [DATE] ingest | <title>`

### 2. Query
When asked a conceptual question about the project:
1. Read `wiki/index.md` first.
2. Drill into relevant pages.
3. Synthesize the answer with citations to the wiki files.
4. File valuable answers in `wiki/queries/`.
5. Append to `wiki/log.md`: `## [DATE] query | <summary>`

### 3. Lint / Health Check
If the user asks for a health check:
Flag contradictions, stale claims, orphan pages, concepts lacking a page, missing cross-references; suggest new questions/sources. 
Append `## [DATE] lint | health check` to `wiki/log.md`.
