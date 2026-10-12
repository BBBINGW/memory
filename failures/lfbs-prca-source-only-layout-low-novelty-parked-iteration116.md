# I116 decision — PARK LFBS PRCA source-only bit-reversal and trace-subscript microaudit

2026-10-12. Target Li et al., *Leveled Functional Bootstrapping via External Product Tree*, IACR ePrint2025/022. Full 35-page public PDF https://eprint.iacr.org/2025/022.pdf, author-specific code not located. Research MCP source fetch ID-zero normalization broken; PDF screenshots attempted but failed.

Evidence:
- I114 `findings/lfbs-prca-variable-B-complexity-scope-iteration114.md`: the informal O(logN) PRCA cost is for fixed B; exact B−1+log(N/B) present in paper. LOW NOVELTY.
- I115 `findings/lfbs-prca-bit-reversal-and-trace-subring-iteration115.md`: exact noiseless PRCA Algorithm5 with natural ciphertext inputs produces bitrev(j) block positions. Its printed Trace target K_(N/B) can lose output data when B²>N. Public pre-permutation plus trace K_B restores source claimed constant-input linear map. No compiled code failure.
- I116 `findings/lfbs-algorithm6-prca-layout-alignment-iteration116.md`: §4.1 natural-index testP_j uses X^(jN/B), Algorithm6 passes consecutive ciphertext blocks directly to PRCA with no explicitly stated inverse bitrev. At N1024 B16 indicator LUT f(j,u)=1{j=1}, testP places the 1 at block1 (coeff64..127) but literal PRCA places it in block8 (coeff512..575) and leaves block1 zero. The printed K64 trace does NOT erase the signal at these parameters, so mismatch is purely input order. Correct by public input bitreversal and K_B trace in ideal test.
- No verified author OpenFHE repository linked with this algorithm was identified using GitHub connector search and current public sources; general OpenFHE CKKS functional-bootstrap code is unrelated. Could be implicit encoded/bitreversed convention outside inspected text, so **no proof the actual LFBS implementation computes wrong LUT**, no security attack, no real bug, no novel technique.
- A public permutation and possible trace subscript correction is low novelty; absence of author code precludes a decisive real-parameter implementation check. Research philosophical kill/park rule applies.

Re-open ONLY if official source/code becomes verifiable and a nontrivial algorithmic correction or severe correct LUT failure emerges. No author contact/email/outreach/public statement. Preserve all previous active-state and old branches including vFHE CRT lookup ideal-IOP finding.
STATUS: **PARK narrow LFBS source-only PRCA layout issue; HUMAN_REVIEW next technical research direction**.
