# BOOT-B041 failure archive — SPRU pair-onehot precomputation does not yield an inexpensive online-depth improvement

TRACK_ID BOOT
ITERATION B041
DATE 2026-10-20
STATUS FAIL_DIRECT_PAIR_TABLE_MEMORY / FAIL_LINEAR_DERIVATION_FROM_ORIGINAL_BSK / PASS_LOCAL_DEPTH_IDENTITY
STATE_UPDATE YES. SHIP PAUSED_BY_PI, no SHIP writes.

Source: Coron–Köstler Low-Latency Bootstrapping for CKKS using Roots of Unity ePrint2025/651 (2026 arxiv2607.27401), title-verified 42-physical-page GitHub ePrint mirror SHA256 2882eebc04de278055f413fc639534717539efe110baf66832e1c648751d01d6, VERSION_UNVERIFIED, p13–14 §4 product-of-phase factors, p19–22 §5 sparse h-onehot blocks, p23–24 Table2 h64 ring N32768. Original authors' OpenFHE C++ at github coron/spru_boot master tree ad00b57ad15e5a32d227e36c713253c5667cfe3e, src/single_slot.cpp blob38d9fda8023ca0a06c5f4c9632802c83e4762c22: exactly 2 packed CKKS BSK ciphertexts represent hB=N onehot secret positions; public phase multiplied, then rotations sum within B and ciphertext products over h blocks depth log2h.

Primary hypothesis: pair neighboring onehot block keys offline by encrypting P_(i,j)=s_i*t_j so evaluator can select public combined phase exp(2pi i(c_i+d_j)/q) by ciphertext-plaintext linear lookup; reduces online product tree log2h→log2(h/2), one level. Algebra identity true. Fixed-seed q64 roots complex tests B4/h2, B8/h4, B16/h4, B16/h8 1500 each: 6000/6000 PASS, error <=5.66e-16. Not actual encrypted computation.

Decisive dimension/memory obstruction for proposed direct linear lookup: each pair onehot key has B² independent indicator coordinates, there are h/2 pairs and each CKKS ciphertext packs max N/2 slots. Therefore ceil((h/2)*B²/(N/2))=B BSK ciphertexts vs original2. Original publication N32768,h64,B512 ->32*512²=8,388,608 encrypted indicators ->at least512 packed BSK ciphertexts, up from2 (×256 BSK ciphertext OBJECT count), before key-generation, rotations, trace, key switching, errors and serialization. Rank independence of public monomial phase features u_i v_j on independent roots: B2 q4 full256 assignments rank4, B3 q2 64 rank9, B4 q2 256 rank16, Gram residual <1e-16. Not a universal impossibility for alternative nonlinear or compressed constructions, only direct tensor table.

Linear derivation obstruction: a separate onehot pair indicator f(i,j)=1_{i=i0,j=j0} has nonzero mixed rectangle cross difference1 across four valid secret choices, whereas any affine combination of original separately encrypted s_i,t_j has zero mixed difference. Therefore any public homomorphic LINEAR operator on existing two original BSK cannot produce all pair secret bits. One needs online secret-dependent ciphertext multiplication (consumes intended depth saving) or new encryption of quadratic secret monomials under CKKS key, requiring new degree2 KDM/circular-security plus joint noise analysis, not implied by original simple linear-secret BSK proof.

No actual runtime/DFR/security or new protocol demonstrated. Simple precomputed tensorization exchanges one online multiplication depth for 256x BSK key-object growth at original parameters, strongly noncompetitive and standard prior-art-adjacent. Source scheme's separability is efficient: the pair public phase table is rank-one u⊗v; forcing all B² secret pair positions into linear key table throws away that low-rank compression. Full finding findings/boot-B041-spru-pair-onehot-depth-memory-kdm-gate.md.

Handoff integrity: found TWO preexisting B040 findings (CMT lowrank and Whitebox SignBoot) with distinct failure archives; B041 is next free numeric index. Preserve both B040 files; read_repo_file returns {}, so do not claim read content. This is B041 archival, not redoing B040.
NEXT B042 (NOT STARTED): source-first BOOT audit of a different recent algorithm (e.g. CCS2026 Decoupled TFHE-type Functional Bootstrapping or sparse NTRU), verify full text and original code and choose one falsifiable new whole-algorithm bottleneck. Do not revive SPRU pair table without a genuinely NEW secure compressed bilinear primitive. No SHIP resumption.
STATE_UPDATE YES, BOOT only.
