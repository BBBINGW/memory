# FHE Research State — After Iteration 184

**I184 COMPLETED; I185 NOT STARTED.** Research protocol: read `START_RESEARCH_SESSION.md`, `RESEARCH_PHILOSOPHY.md`, `AGENT.md` and this file. One falsifiable claim and one decisive test. PI makes final research choices.

## CURRENT TARGET

Okada–Takagi, *Low Communication Threshold FHE from Standard (Module-)LWE*, ASIACRYPT 2025, ePrint **2025/409**. Verified full 40pp Research MCP mirror PDF SHA256 `98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301`; official latest parity VERSION_UNVERIFIED. In source §1.2 p4, removing the decryption count bound `LDec` is explicitly open. Algorithm6 p26 and Algorithm7 p29 require fresh pre-shared Shamir Gaussian padding per decryption; per-party storage grows linearly with `LDec`. Existing per-party PRF seeds generate a separate masking term and do not supply correlated Gaussian padding.

**I184 primary hypothesis — FAIL:** independently deriving each party's Gaussian padding through its existing PRF seed cannot directly replace the jointly Shamir-shared padding for arbitrary eligible active sets. At T2,N3, Shamir interpolation at indices 1,2,3 requires any one global session pad to satisfy `z3=2z2-z1` modulo prime q. For independent uniform local values this equality occurs with probability `1/q` (exact enumeration 49/343 at q7). Even if requiring only matched variances for all sets, in a relaxed real-centered independent-noise interpolation model the equations force one negative party variance: `v1=V/3,v2=-V/3,v3=V` for target variance V>0. This restricted variance model does not rule out other finite-field correlated PRSS schemes or modified simulators. No claimed flaw in paper.

**STATUS:** FAIL naive independent-PRF replacement; PASS exact Shamir reconstruction test and conditional variance calculation; UNCLEAR correlated secret-dependent Gaussian PRSS. Finding `findings/threshold-fhe-independent-prf-padding-shamir-correlation-gate-iteration184.md` SHA `74f281bec1b64b54c097fa8f57ffc6e8c99017cc`.

## NEXT_ACTION — I185

Check existing PRSS and distributed discrete-Gaussian prior art for **correlated per-session padding** that depends on hidden secret norm, and for module-LWE on secret covariance `Bpub² I−Σ_s`, while meeting simulation security for arbitrary qualified active sets. Only formulate a construction if source compatibility and cost improvement versus O(LDec) pre-shares can be justified. Avoid repeating elementary independent-noise tests. PI decides continue/refine/park. **STATE_UPDATE YES.**

## PREVIOUS ARCHIVES

I183 GBFV few-slot automorphism without BFV detour: bare masking FAIL; source admits scaling condition. I182 GBFV-CKKS integer output bound: no missing overflow condition. I178–181 naive dBFV-to-BGV ports: PARK pending new mechanism. I175–176 Park C-MT binary jumps already in LLKN23. I171–174 SHIP trivial selector compression PARK. vFHE 2025/286 P1 latest revised proof remains SOURCE-GATED. Earlier findings and failures remain archived; consult `findings/OPEN_RESEARCH_BRANCHES.md`.
