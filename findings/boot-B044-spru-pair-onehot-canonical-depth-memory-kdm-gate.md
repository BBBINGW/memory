# BOOT B044 — CANONICAL: SPRU pair-onehot depth/memory/KDM gate (renumbered from accidental B041 collision)

TRACK_ID: BOOT
ITERATION: B044
DATE: 2026-10-20
STATUS: PASS_EXACT_ONEHOT_PHASE / FAIL_COMPACT_PRECOMPUTED_PAIR_KEY / FAIL_PUBLIC_LINEAR_REKEY / NO_PAPER_READY_ALGORITHM
STATE_UPDATE: YES
SHIP PAUSED_BY_PI, no SHIP writes.

## Numbering provenance and repair
Read-before-write list of BOOT findings checked on 2026-10-20 proves preexisting B040 twice, B041 leveled-FBS, B042 lazy-trace, and B043 trace-coset output-noise. The SPRU research in this chat was mistakenly first saved as B041, yielding a collision with the PRIOR B041 leveled-FBS result. No older file was modified or deleted. This B044 is the CANONICAL unique-numbered archive of that exact SPRU experiment; prior findings/boot-B041-spru-pair-onehot-depth-memory-kdm-gate.md and failures/boot-B041-spru-pair-selector-quadratic-keyspace-kdm-failure.md are DUPLICATE-INDEX early writes (same evidence, not a separate completed iteration); preserve them for audit and do NOT count them again. Older B040–B043 LFBS/other files remain immutable. Future NEXT B045, not B042. GitHub Notes read_repo_file returned empty object for old STATE; list_repo_files successfully verified paths and SHAs, no prior content fabricated.

## Primary hypothesis and original evidence
Question: Coron–Köstler SPRU ("Low-Latency Bootstrapping for CKKS using Roots of Unity", ePrint2025/651, updated arXiv2607.27401) uses single-slot h-block binary-sparse secret and expensive log2h encrypted product tree. Can pre-encrypted joint onehot selectors for adjacent blocks eliminate one online encrypted multiplication level without unacceptable key-memory/security cost?
Original paper 42 physical pages, title-verified ePrint mirror PDF SHA256 2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6, VERSION_UNVERIFIED: pp13–14 Eq5 group homomorphism and product, pp19–22 multi/block structure, pp23–24 Table2 real params N32768,h64, bootstrap depth7 including plaintext multiplication; product-tree depth6.
AUTHOR code https://github.com/coron/spru_boot master tree SHA ad00b57ad15e5a32d227e36c713253c5667cfe3e; src/single_slot.cpp blob38d9fda8023ca0a06c5f4c9632802c83e4762c22 generates two encrypted packed secret vectors (N/2 slots each), then public-phase plaintext multiplication, blockwise trace and h-factor ciphertext product tree; src/keygen.cpp blob a367acf060fec5f85601d65974a2f1d989320f76 generates onehot blocks.

## Exact construction, test and killer
Let onehot secret choices within two independent blocks of B=N/h options be s_i, t_j, public roots u_i=e^(2pi i c_i/q),v_j=e^(2pi i d_j/q). Candidate offline pair key P_ij=s_i*t_j; publicly weight W_ij=u_i v_j, so Σ_ij P_ij W_ij = (Σ_i s_i u_i)(Σ_j t_j v_j). This is exact and could replace h factors with h/2, reducing ciphertext multiplication tree log2h→log2(h/2) by ONE level if pair keys supplied.
Deterministic exact-coordinate numpy complex roots q64 test: B4/h2, B8/h4, B16/h4, B16/h8, 1500 independent random phase+secret cases each, 6000/6000 PASS, max complex absolute discrepancy5.66e−16. Not a native encrypted CKKS, DFR or security test.
THE DIRECT ONEHOT REPRESENTATION EXPLODES: h/2 pair blocks × B² pair-secret coordinates =hB²/2=NB/2. A CKKS ciphertext has N/2 complex slots. Thus at least B packed ciphertexts to hold DIRECT pair table (vs original TWO). Published N32768,h64 ⇒ B512 ⇒32*512²=8,388,608 selectors /16384 slots =512 encrypted BSK ciphertexts versus2 (256× key-object growth), before additional trace/rotation/Galois keys/noise. This is specifically a direct linear pair lookup slot-capacity bound, not a general impossibility against alternative encrypted compressed bilinear gadgets.
Public phase functions u_i v_j have rank B² as functions of independently varying phase vectors. Full character-domain Gram numerical tests: B2,q4 features4 rank4; B3,q2 features9 rank9; B4,q2 features16 rank16, residual<1e−16. That explains independent pair table coordinates.
Existing BSK encrypts degree1 functions of secret s_i,t_j. A pair indicator s_i*t_j has nonzero 2×2 mixed rectangle difference on legal onehot secret assignments, whereas any public affine/linear operation on separately encrypted onehot vector has zero mixed difference. Hence not derivable for free from TWO source ciphertexts via ciphertext additions, plaintext multiplication, rotations alone: must perform the very ciphertext product we seek to remove, or generate NEW degree2 KDM/circular-secret-dependent encryptions with new security/noise analysis.
This is a classic separable low-rank versus dense tensor tradeoff: original two-vector representation exploits u⊗v factored form, proposed precompute stores whole pair table. One depth level is not credible against 256x key-object count at h64 and extra KDM assumptions. No full native code, security estimator, precision, noise or latency benchmark. Novelty low; NOT a new publishable bootstrapping protocol.

## End
STATUS: FAIL_DIRECT_PRECOMPUTED_KEY_SIZE_AND_KDM / PASS_LOCAL_PHASE_EQUALITY / HUMAN_REVIEW_ONLY_IF_NEW_BILINEAR_COMPRESSION_EXISTS.
RESULT: strong source-aligned cost falsifier; archive SPRU direct pair selector unless independently discovering secure compressed joint-selector primitive that beats B² and new key-security constraints.
NEXT_TEST: B045 (NOT started) use source-first audit of a different 2026 BOOT algorithm, avoid already B040–B043 LFBS mini-branches and generic tensor key tricks, one falsifiable full-scheme idea, verify author code/prior art/noise/security.
STATE_UPDATE YES, only BOOT files.
