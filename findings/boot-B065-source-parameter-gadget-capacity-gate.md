# BOOT-B065 — Exact gadget-capacity gate for Dai et al. 2026 published parameters
DATE: 2026-10-20
TRACK_ID: BOOT. SHIP PAUSED.
STATUS: FAIL_PUBLISHED_TABLE_EXACT_GADGET_CAPACITY / BLOCKED_MATCHED_SECURITY_H2_CROSSOVER / HUMAN_REVIEW_REAL_IMPLEMENTATION.

## Primary hypothesis
Dai et al.'s public Table 4 100-bit and 128-bit parameter rows instantiate their own stated exact centered digit decomposition h_B: Z_Q→D_B^d with D_B=(-B/2,B/2]∩Z and a=Σ h_B(a)_i B^i mod Q for every a. This capacity check must pass before transferring B064 toy partial-merge h=2 noise crossover into a source-backed security-matched parameter set.

## Verified source
[FACT] Dai, Xiang, Deng, Zhang, "Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation," Cybersecurity 9:136 (2026), https://link.springer.com/content/pdf/10.1186/s42400-026-00563-w.pdf, physical PDF p5 Gadget decomposition/Theorem1, physical p13 Table4 and Table5, p14 Table6, pp7-9 Lemmas2–4, p12 PBR noise, appendix.
[FACT] Table4: 100-bit N=2048,Q=2^32,B=2^4,d=4,f ternary,σ_g=0.25,n=560,q=2^11; 128-bit N=2048,Q=2^32,B=2^3,d=5,f Gaussian,σ_g=1.1,n=572,q=2^11. Different LWE KSK decomposition B_ks=2^7,d_ks=2 covers q=2^11 and is not implicated.
[FACT] Table6 parallelism P=k*l*d: k2,l8 P64 for 100-bit and k2,l4 P40 for 128-bit. These independently use the same d4/5 values, so cannot assume without proof that Table4 contains only an isolated typography error.
[FACT] Table5 multiplication count 2knd²+(3k²+5k)ld.

## Decisive algebraic falsifier
D_B has exactly B integer values. Only B^d different digit vectors exist; hence h cannot be surjective onto Z_Q unless B^d≥Q. For table values:
100-bit: B^d=16^4=2^16 <2^32; exact coverage for uniform residue at most 2^-16; minimum standard exact d is 8.
128-bit: B^d=8^5=2^15 <2^32; coverage at most 2^-17; minimum exact d is 11.
With digits (-B/2,B/2], actual reconstructed integer sums range [-30583,34952] (B16,d4) and [-14043,18724] (B8,d5). In particular input a=B^d (65536,32768 respectively) is unreachable modulo 2^32. Even the primitive identity ExtProd(a,G(1))=a cannot hold for such a with the stated restricted gadget vector G(1)=(1,B,...,B^(d-1)).
An approximate decomposition with global coefficientwise error epsilon may cover at most (2epsilon+1)*B^d residues: covering Q requires epsilon≥32767.5 (100bit), ≥65535.5 (128bit). For the specifically published CENTERED digits, a=Q/2 has best possible circular error ≥2147448696 and ≥2147464924, respectively. A scaled high-bit gadget, altered internal modulus, or unrestricted coefficient distributions could escape this no-go but is NOT the same published decomposition and needs new rounding-error proofs.

## Independent reproducible verification
[TEST] Exact Python exhaustive enumeration of all 65536 allowed 100-bit digit tuples and 32768 128-bit tuples; exactly B^d distinct residues, concrete a=B^d outside image in both. Script b065_gadget_capacity_audit.py SHA256 cc9cbd17fbd8f8d51e8a765e17910e8c1300989382721d3e27cb0759bf694e40, JSON SHA256 3c17898ce40f7fab37c4887a27872eef0a943f10d646f2a86637e150028c12db; full local BOOT_B065_handoff.zip.

## Consequences and limits
Conditional hypothetical repair of STANDARD exact gadget at Q2^32 requires d 4->8 (100bit), d 5->11 (128bit). If retain source Table5 symbolic architecture, k2,n560,l8 predicted polynomial multiplication units 36544->144768 (~3.96x), and k2,n572,l4 57640->277816 (~4.82x); this is NOT observed latency or proof that the published implementation is faulty. Author OpenFHE experiment source not located; source might use differently scaled/approximate h or modulus. Thus this is an INTERNAL DOCUMENT PARAMETER CONSISTENCY proof, NOT cryptanalytic insecurity, NOT confirmed implementation error, NOT DFR result.
Published Table4 does not supply a consistent exact gadget regime for B064's full-size group-coalescing h2. Further the gamma, Var(e_d), Var(e_pk), real NTRU R*R noise and correlation model are not instantiated sufficiently to certify a secure crossover. Artificial B064 sigma_uec ×400 toy crossover cannot be promoted to real 128-bit performance.
[SECURITY] No 128-bit attack and no claim that the authors' runtime measurements themselves are fabricated; requires implementation-level verification of actual decomposition before any stronger claim.

## End of iteration
STATUS FAIL_PUBLISHED_TABLE_EXACT_GADGET_CAPACITY / BLOCKED_MATCHED_SECURITY_H2_CROSSOVER.
RESULT Mathematical contradiction under expressly specified exact centered gadget, independently checked in both security-table rows. This is a potentially meaningful reproducibility/correctness issue but NOT a new publishable Bootstrapping primitive.
NEXT_TEST B066 (NOT STARTED): identify authoritative author implementation or clarification; test one replacement gadget (full-length d or scaled approximation) for correctness, noise and computational cost; only then reevaluate h2 under security-matched parameters. If no available source, archive B063/B064 and pivot toward new primitive. Ask PI to supply code if necessary.
STATE_UPDATE NO: existing findings/boot-STATE.md read_repo_file returns {}, preserve it rather than overwriting (187967 bytes). Append only BOOT B065 finding. SHIP unchanged.
