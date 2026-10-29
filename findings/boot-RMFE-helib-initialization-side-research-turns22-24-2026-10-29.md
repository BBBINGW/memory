# BOOT RMFE / HElib Initialization Side Research — Turns 22–24

Date: 2026-10-29
Session: 密码学 11.0
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Turn 22 — TraceMap reuse / parallelism gate

Pinned compatible HElib lineage: acdb264e1a991eaee35fd8b3c31bebe9528c49a1.

ThinStep1Matrix constructs 2*d-1 TraceMap values, a d x d trace Gram matrix, and its inverse. For PA_zz_p over p^r, the exact trace-dual power basis can instead be built from u=G'(alpha)^(-1), with beta_(d-1)=u and beta_i=alpha*beta_(i+1)+a_(i+1)u. This deletes all 2*d-1 TraceMap calls and the d x d trace-matrix inversion.

CPU TraceMap parallelism is fallback-only. GPU-port priority is killed because the targeted work can be deleted algorithmically.

## Turn 23 — exact ring correctness gate

PASS_EXACT_RING_CORRECTNESS.

- 90/90 exact small prime-power quotient tests matched the dense trace-Gram inverse.
- 22/22 HElib-style cyclotomic/Hensel tests matched Frobenius TraceMap semantics and multiplication trace.
- HElib InvModpr supplies the prime-power-safe inverse primitive.

Boundary:
- exact trace-subpath replacement: supported;
- setup/runtime speedup: not established;
- RMFE native correctness, DFR, security, memory advantage, and paper contribution: not established;
- cryptographic novelty of the trace-dual identity: not supported;
- engineering value: retained.

## Turn 24 — serialization/cache scope and second bottleneck

Context serialization does not persist ThinEvalMap / ThinStep1Matrix / A_deflated. HElib build_cache upgrades zzX constants to DoubleCRT but is not a persistent cross-process cache.

For m=32768,p=5:
- ord_m(p)=8192;
- phi(m)=16384;
- sz=2.

If deg(G)=512, the pre-deflation dense matrix is 1024 x 1024. NTL ppInvert already uses internal thread-pool parallelism.

Best persistence boundary: the final public algebraic map or pre-upgrade zzX constants. A_deflated has sz^2*d=2048 mod-625 coefficients in this geometry.

The dense A1 is the transpose of a multipoint-evaluation matrix; structured interpolation reproduced its inverse in 13/13 exact small cyclotomic/Hensel tests. Direct use for the current custom degree-512 construction remains UNCLEAR until exact G / point / embedding lineage is matched.

These findings are independent of the pending R21 native gate and do not rescue RMFE on a scientific native FAIL.

GPU_PORT_PRIORITY: KILLED_FOR_CURRENT_RESEARCH
CPU_TRACEMAP_PARALLELISM: FALLBACK_ONLY
ENGINEERING_VALUE: RETAIN
CRYPTOGRAPHIC_NOVELTY: NOT_SUPPORTED
