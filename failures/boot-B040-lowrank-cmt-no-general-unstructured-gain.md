# BOOT B040 failure archive — Matrix-low-rank CMT is not a general random-LUT bootstrapping improvement

TRACK_ID: BOOT
ITERATION: B040
DATE: 2026-10-20
STATUS: FAIL_UNIVERSAL_UNSTRUCTURED_LUT_COST_ADVANTAGE / PASS_CONDITIONAL_EXACT_BILINEAR_LOW_RANK_EVAL / LOW_STANDALONE_NOVELTY
STATE_UPDATE YES
SHIP paused after I407; no cross-track writes.

Source: Dumezy et al., "Evaluating Larger Lookup Tables using CKKS" TCHES 2026(1):559–591, DOI10.46586/tches.v2026.i1.559-591, full original paper mirror ePrint2025/1301 35 physical pages SHA256 048ba3ae4fe97eae0417138b816572b1c79b503727db54ce76576a4d38190b19 VERSION_UNVERIFIED, §5.1 Eq5/Alg6 pp19–20, §7 lazy rescale/relin pp23–24, §8 source random LUT experiments pp25–27. Authors p1 footnote implementation available upon request for research, so source code for specific CMT not accessible and no native run claimed.

Primary proposal: factor the PUBLIC CMT LUT matrix Y of dimensions A×B (A≈B≈√P), into rank r factor UV^T, then compute Σ_{t≤r}(Σ_i U_it L_i)(Σ_j V_jt R_j) using same encrypted Kronecker digit-selector inputs as paper CMT. This equals L^T Y R for ALL selector vectors, even if selector plaintexts imperfect/noisy, because matrix identity holds. In ideal arithmetic existing noise sensitivity identical. New CKKS rounding/key-switching noise, levels, scale and full DFR unproved.

Operation-count test: original final CMT contraction AB=P scalar plaintext×ct products, A ct×ct products; rank factor  r(A+B) scalar plaintext×ct and r ct×ct, excluding unchanged two KProducts. Balanced A=B=√P improves scalar count only if r<√P/2, and ct×ct count only if r<√P. Generic random LUT matrix has full rank=min(A,B) with high probability => rank method doubles plaintext products and doesn't save ct×ct. SOURCE itself benchmarks random/unstructured LUTs, so our method cannot be presented as broadly faster than original.

Reproducible exact toy local /tmp/boot_b040_lowrank.py SHA256 cf759de5bf2936ebc414da53684dfaf28ccb3016c9d1d38a3b7ed1470aa50799: P256, basep4, nd4 digit groups balanced A=B16, SymPy exact integer/rational rank decomposition; three LUT matrices:
 (1) Y_ij=(i²+7)+(3j²+11) rank2 => PT products256->64, CtCt16->2;
 (2) Y_ij=(-1)^i*g_j where g_j random integer [-100,100], rank1 => PT256->32,CtCt16->1;
 (3) iid integer random Y∈[-100,100]^(16×16) full rank16 => PT256->512 (worse), CtCt16->16.
For each sampled LUT verify exact SymPy U V^T = Y; for 200 independent noisy/real selector vectors L,R verify floating bilinear outputs original/factor agree to1e-7; 600/600 PASS. Random Y best rank2 SVD has max entry approximation error122.9365 against entry range [-100,100], not valid as exact LUT computation in typical noise budget. This is one sampled random instance; don't claim a general numerical lower bound.

Novelty failure: low-rank matrix contraction is basic linear algebra and available to any matrix-based cryptosystem. Many simple rank1/2 LUT examples are themselves cheap direct arithmetic circuits, no distinctive FHE bootstrapping contribution shown. More recent Dumezy–Suvanto ePrint2026/1200 "Character Block Encodings for Discrete CKKS" achieves arbitrary LUT as one-level affine plaintext map by CHANGING ciphertext representation, released authors' GitHub jdumezy/ckks-block-encoding; it is important competing prior art for structured discrete LUTs, albeit larger slot space/representation costs. ePrint2026/1023 sparse CoeffToSlot and 2026/1026 sparse Hermite are newer related prior art, but research MCP PDF acquisition FAILED with eprint403 and no mirror. Do NOT guess their details; authorized PDFs may be needed if B041 requires them. No author CMT source code independently confirmed, no CKKS secure parameter/noise/latency/DFR benchmark.
Conclusion FAIL generic LUT optimization, PASS low-rank conditional cost upper model; no publication-grade new bootstrapping method.
Finding: findings/boot-B040-cmt-lowrank-lut-contraction-source-cost-gate.md
Next B041 (not started): One cheap DECISIVE test whether a genuinely hard discontinuous LUT yields stable small CMT flatten rank and a cost/noise advantage compared to 2026/1200 character-block method or small direct FBT; if this is merely obvious separability, archive promptly and proceed to another whole-algorithm research target. New idea must alter actual core algorithm, not merely reuse matrix rank. BOOT-only. STATE_UPDATE YES.