# Paper acquisition and evidence

Use public full text online by default; this repository is not a PDF mirror.
Try reasonable legal sources: IACR ePrint, arXiv, author homepages, institutional
repositories, conference preprints and public technical reports. Check that the
version includes the proof, appendix or supplement actually needed.

Search snippets, citation pages, blogs and generated summaries are DISCOVERY,
not final EVIDENCE for technical claims. Prefer primary papers, author revisions,
full versions/appendices, official artifacts, then follow-up papers. Never infer
a theorem from an abstract or substitute a secondary summary for required evidence.

If important full text remains unavailable, mark **EVIDENCE MISSING**, add an entry
to `MISSING_SOURCES.md`, and report **MISSING CRITICAL SOURCE** to the human with
its exact title, authors, venue/year, identifier, inaccessible part, dependent
hypothesis, missing evidence, retrieval attempts, and whether work can continue.
Do not request copies of sources that are not materially needed. Continue only
independent work; stop the blocked technical verification until evidence arrives.

- `notes/`: durable reading notes and exact source locations.
- `supplied/`: exceptional human-supplied critical full text; see its README.
- `local/resource_buffer/`: ignored temporary downloads and acquisition work.

Public full text → read online → do not store PDF by default.
Critical inaccessible full text → report + record → human supplies → check storage
permission → store under `papers/supplied/` → verify readability → resume.

Use this human-facing report, and persist the same details in `MISSING_SOURCES.md`:

```text
MISSING CRITICAL SOURCE
Paper: exact title; authors, venue/year and identifier if known
Needed For: dependent hypothesis or technical claim
Missing Evidence: exact section, proof, appendix or experiment
Why retrieval failed: public sources/versions attempted and their limitations
Impact: what is blocked; whether independent work can continue
Human Action: exact full text/supplement to obtain, subject to storage permission
```

When this blocks the active hypothesis, briefly link its `MISSING_SOURCES.md` entry
from STATE.md's Main Uncertainty and set Next Action to obtain/read the source, then
verify the specific claim. Do not copy the full request into STATE.md.
