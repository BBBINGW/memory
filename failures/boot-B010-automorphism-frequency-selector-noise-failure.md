# BOOT B010 failure archive — Automorphism fraction is not MPmul selector-noise frequency

TRACK_ID: BOOT
ITERATION: B010
DATE: 2026-10-19
STATUS: FAIL — NAIVE BIT-WEIGHTED HETEROGENEOUS GADGET
HYPOTHESIS: Assign per-bit i a GSW key-error weight 2^i/n because only 2^i outputs require automorphism in MPmul; then optimize gadget precision (B_i,d_i,delta_i) via 2025/1892.

COUNTEREXAMPLE / SOURCE:
- 2025/686 Algorithm 1 p.12: in every bit stage i, all n outputs perform one external product with the SAME GSW selector key C_i; only the first 2^i outputs require Galois automorphism. The 2^i/n fraction measures automorphism count, not selector-key usage.
- Exact n=8,N=16 negacyclic monomial test provides stage-specific inputs u_j=(n/2^i-2)/2 - floor(j/2^i), so the selector difference at every coordinate is X^{u_j}(X-1) and has squared coefficient norm 2. In an idealized shared i.i.d Gaussian GSW-error polynomial model, every coordinate in every bit stage has the SAME variance 2 sigma_i², regardless of 1,2,4 automorphisms.
- Output errors share the GSW key errors, so may be strongly correlated. In the idealized example bit stages i=0,1,2 produce normalized output covariance ranks 8,4,2; treating n output uses as n independent GSW encryption errors is invalid.
- 2025/1892 Theorems 3.1–3.2 concern per-key gadget choices in the CGGI blind rotation and do not establish 2^i/n scaling for shared-key multi-output MPmul.
- This is NOT a correctness flaw in either published work, an attack, or an impossibility result for all heterogeneous gadgets.

DECISION: Archive the 2^i/n weighting hypothesis. The reuse/covariance structure may be researched if a robust source-faithful joint DFR bound across multiple outputs can be established; this is an independent and nontrivial problem. Do not optimize parameters on unsupported noise weights.

PROVENANCE: findings/boot-B010-mpmul-selector-reuse-noise-asymmetry.md. 2025/686 mirror PDF SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335; 2025/1892 mirror PDF SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018; both VERSION_UNVERIFIED.

NEXT_TEST: B011 two-output covariance-based joint DFR potential and worst-case input counterexample. Only BOOT-owned files.
