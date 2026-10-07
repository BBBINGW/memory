# Human-supplied critical sources

Only store full text here when it is technically important and a reasonable search
failed to find an accessible complete equivalent. Do not collect every relevant PDF.

This repository was verified public on 2026-10-07. Before each upload, check current
visibility. For a public repository, the human must confirm redistribution is
permitted; otherwise do not upload. Private storage must also be legally permitted.
Never change visibility automatically. Obtaining access does not imply redistribution rights.

Use a stable relative path, e.g. `papers/supplied/author-year-short-title.pdf`.
Record the exact path in `MISSING_SOURCES.md` along with the requested missing part.
After receipt, check that the file exists, opens, matches the paper/version, and
contains the needed theorem/proof/appendix. Only then mark SUPPLIED; mark RESOLVED
when the dependent research question is resolved. Preserve useful request history.

## Reading through GitHub Notes MCP

Use `list_repo_files(path="papers/supplied")` to discover supplied PDFs, then
`read_repo_pdf(path="papers/supplied/author-year-short-title.pdf")` to read actual
server-extracted text. The default returns the first 3 physical pages (or fewer).
Use `start_page` and `end_page` for a targeted, inclusive, 1-based page range.
Physical page numbers may differ from printed page labels. Results include path,
filename, Git blob SHA, page range, total pages and numbered page text.

Limits: 20 MiB per PDF, at most 5 pages and 64 KiB of JSON per call. Oversized
requests fail explicitly; nothing is silently truncated. Request smaller ranges.
A single oversized page requires manual reading. Empty pages report
`TEXT EXTRACTION UNAVAILABLE FOR PAGE N`. Encrypted PDFs are not supported.

This is text extraction, not perfect visual reading: equations, tables, columns,
figures and font encodings may be incomplete or reordered. There is no OCR or
page-image tool. Verify that the specific required evidence is legible before
marking SUPPLIED; if not, keep the check blocked and request human verification
or an authorized, checked transcription. Never infer missing equations or proofs.

PDF reading is restricted to `papers/supplied/`; text write/append tools still
reject PDFs. The human uploads an authorized PDF using Git/GitHub. The MCP cannot
access `local/`, upload binary files, or execute scripts.

Production HTTPS MCP verification passed on 2026-10-07 using a self-created PDF:
listing, text extraction, page-range reads, MISSING → SUPPLIED, and a fresh
OAuth/MCP session reread. The test used the official MCP client, not the ChatGPT UI.
Temporary research-repository test files were removed afterward.
