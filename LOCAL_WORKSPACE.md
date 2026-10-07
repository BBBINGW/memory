# Local workspace and durable research memory

`local/` is working memory: high-churn intermediate work that stays on this machine.
GitHub is long-term memory: compact research state and results that may influence future decisions.

| Local directory | Purpose |
| --- | --- |
| `local/scratch/` | Rough equations, temporary thoughts and transient notes |
| `local/derivations/` | Intermediate algebra, proof attempts, noise derivations and parameter calculations |
| `local/experiments/` | Temporary scripts, benchmarks, raw outputs and test artifacts |
| `local/parameter_sweeps/` | Raw CSV, JSON and TXT sweeps and parameter tables |
| `local/temporary_notes/` | Temporary paper notes awaiting review |
| `local/resource_buffer/` | Temporary downloads, partial files and acquisition metadata |

These directories are ignored by Git. In a new checkout, create them with:

```sh
mkdir -p local/{scratch,derivations,experiments,parameter_sweeps,temporary_notes,resource_buffer}
```

The current GitHub Notes MCP accesses GitHub only; it cannot access this local workspace.
Use local tools for scratch work and promote selected results manually.

## Manual promotion

```text
local work → minimal verification → useful for future decisions?
                                   ├─ no: keep local or delete
                                   └─ yes: summarize and promote into GitHub
```

Promote only useful or verified findings, surviving hypotheses (label uncertainty),
informative negative results, stable derivations, concrete obstructions, important
parameter conclusions, reproducible experiments/scripts, human research decisions,
or information needed to update `STATE.md`.

Do not commit temporary derivations, large sweeps, raw experiment outputs, or duplicate
or speculative notes by default. Keep only the minimal supporting scripts/artifacts
needed for reproducibility when they are necessary; place those outside `local/`.
No promotion automation is used.

Examples:

- `local/derivations/tmp_scaled_ep_block.md` → `findings/scaled_ep_block_correctness.md`
- `local/experiments/noise_test_raw.txt` → `findings/noise_bound_observation.md`
- An informative failure → `failures/scaled_ep_block_noise_failure.md`
- Reviewed paper notes → `papers/notes/`

Do not preserve full chain-of-thought-style reasoning traces as long-term research records.
Instead preserve a concise record: parent idea if relevant, technical hypothesis,
motivation, minimal test, evidence and source locations, PASS / FAIL / UNCLEAR,
concrete reason, implication, and next action. The human/research agent decides
importance; no script makes scientific promotion decisions.
The goal is reproducible research memory, not conversational history.

## Keep recovery state compact

`STATE.md` remains the minimum information needed for the next session to resume.
Only compact conclusions belong there, not detailed derivations, raw outputs or logs.
For example, record a derived parameter threshold and link to its evidence rather than
copying all 127 tested parameter sets. Keep durable evidence in `papers/`, `findings/`,
`failures/`, or an appropriate reproducibility file.

Missing critical evidence belongs in `MISSING_SOURCES.md`. Exceptionally, legally
storable human-supplied full text belongs in `papers/supplied/` when public retrieval
fails; see `papers/README.md`. Do not mirror publicly accessible papers.
