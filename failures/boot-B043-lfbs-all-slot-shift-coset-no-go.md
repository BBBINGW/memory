# BOOT B043 failure archive: LFBS all-B PRCA output-slot position shift no-go

TRACK_ID BOOT | ITERATION B043 | 2026-10-20 | STATUS FAIL_PUBLIC_MONOMIAL_SHIFT | STATE_UPDATE YES

Original paper Li et al., Leveled Functional Bootstrapping via External Product Tree, ePrint 2025/022 §4.2 Algorithm5 PRCA / Algorithm6; generic B-ary LFBS PRCA must preserve B independent branch messages at j*N/B coefficients before subring HomTrace and public temp block replication.

Proof: let K=N/B. Normalized relative trace into Zq[X^K]/(X^N+1) has T_K(X^i)=X^i for i divisible by K, otherwise0. For P=sum_(j=0)^(B-1) m_j X^(jK) and shift delta: when delta not divisible K, trace(X^delta P)=0 and every input branch is lost. When delta divisible K, output is just a bijection of all B preserved slots; precisely one branch still maps to constant index0. Odd Galois automorphisms cannot change this conclusion. Any scheme avoiding 0 while keeping B generic independent outputs would need new representation, extra ciphertext, publicly provable branch relation, or nontrivial computation not present in this shortcut. This is not a universal impossibility result for LFBS improvements.

Exact modular toy q257 N32/64/128 B2/4/8/16 tested 12 compatible pairs; 896/896 monomial trace checks PASS. Exhaust 896 shifts: 90 legal preserving all B and with one constant slot, 806 kill all B, no partial survivors. temp multiplication exact per-block replication. Reproducer /tmp/boot_b043_trace_shift.py SHA256 de094ddb06a9a03d9c6ca03e4777a0194016690aafe74a4a695beb527bbf6045.

New prior art Han Xia 2026 paper doi:10.62056/a69n5txl7s already studies coefficient noise of scaled FULL trace; its source hxialab/ErrTrace trace estimator differs from LFBS PARTIAL relative trace. Do not assert constant is empirically worst in LFBS or claim direct DFR impact. Source's earlier B041 B042 findings exist but full read tool response empty, and PDFs screenshot fetch failed 403. No actual native LFBS keys, security/noise/latency benchmark; no paper-worthy new primitive.

FULL finding findings/boot-B043-lfbs-trace-coset-saturation-output-noise-placement-gate.md

NEXT B044: different BOOT paper and substantive core mechanism, one minimal falsifiable test; no repeated B041/B042 trace micro-ideas. SHIP remains PAUSED_BY_PI after I407, no cross-track modification.