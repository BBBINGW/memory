# Iteration 110 decision: park narrow Carousel generic p-nondivisible rounding microaudit

Date: 2026-10-12.
STATUS: **PARKED** narrow paper-technical-overview rounding-scope microaudit (ePrint 2024/2032), not a blanket failure of Carousel theory or author code.

Source research record: `findings/carousel-blind-rotation-nondivisible-p-rounding-slack-iteration108.md` and `findings/carousel-paper-vs-code-lookup-rounding-scope-iteration109.md`; archived full original `STATE.md` as `logs/carousel-state-pre-sparse-sab-handoff-iteration110.md` SHA256 repository file sha `1fe028f86c0c1ef64524feaf1c7c3f4a964c13f0`.
- I108: exact scalar phase-lookup insufficient noise condition `|e|<N/(2p)` for generic p∤N; one rounded-phase offset δ_m requires budget, no encryption failure. Initial toy M829,p5,N92 does not satisfy conjugate-invariant slot restriction (odd order 9).
- I109: corrected cyclotomic toy M449,p5,o14 even,N32 with p∤N; paper pointwise LUT and actual code-style offset-filled LUT both have strict-bound scalar errors but at DIFFERENT message/noise pairs. The pinned Go `SNUCP/carousel` commit `21d5800462920d63afcc58873446455642588297` requires N,p powers of two and presets N2048,p4/8/16, which satisfy p|N and produce zero such errors in exact model. Formal Theorem4 states rotated LUT output and has NOT been falsified. Not 128-bit secure executable param.
- Realistic contribution: a trivial general-scope first-round rounding slack, with author released parameters explicitly excluding problem, no nontrivial FHE primitive needed. Recommended park and seek technically substantive source-grounded issue. No authors contacted or public disclosure.

New independent target for I110: ePrint 2025/686 Guimarães–Pereira *Fast amortized bootstrapping with small keys and polynomial noise overhead*, a CCS2025 paper with confirmed research MCP full-text. Specific test: do the definition of `diff(s)` with terminal `d[h]=-j_last` and Algorithm2's exact Horner shifts produce `b-a s`, or a shifted negacyclic variant? Separate printed pseudocode error from functioning public C implementation. No claim of published implementation bug absent verification.
