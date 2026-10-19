# BOOT B025 failure archive — fixed-rank offline linear compression of block-RGSW key spectra

TRACK_ID: BOOT
ITERATION: B025
DATE: 2026-10-19
STATUS: FAIL_INPUT_INDEPENDENT_LINEAR_SKETCH_RANK_LESS_THAN_BLOCK_SIZE / NOT_A_GENERAL_BOOTSTRAPPING_NO-GO

Baseline Lee et al. 2023/958 Algorithm2 physical pp11,16, Table2: per block K=Σ_(i=1)^ell(X^(a_i)−1)BRK_i, one extprod, online scalar/pointwise work still (4d+2)nN and original authors reported ~45% of blind rotation time in their historical CPU run. One frequency and one key component x_i=NTT(BRK_i)[ζ] produce scalar y=Σ_i(ζ^(a_i)−1)x_i; each a_i is a public modswitch LWE coefficient and can independently equal0 or1. For every j, query a_j=1 and all other a_i=0 selects weight (ζ−1)e_j. Weight span therefore dimension ell for ζ≠1.

Any INPUT-INDEPENDENT field-linear offline key sketch T:F_q^ell→F_q^r, r<ell, has nonzero kernel v. The same sketch of x and x+v cannot answer at least one legal query with v_j≠0. Exact q97, N8, ζ8, ell4 toy query matrix diag(7,7,7,7) has rank4. Explicit r3 sketch T rows (1,0,0,1),(0,1,0,1),(0,0,1,1), kernel (-1,-1,-1,1) has undetectable sketch difference but query a=(1,0,0,0) output difference90 mod97. Thus linear-rank compression of independent standard RGSW Fourier key data cannot save ell dependence without changing representation/key randomness/input-mask space/online reconstruction.
IMPORTANT LIMITATION: This is NOT a universal multiplication lower bound for TFHE: coefficient-domain signed rotations avoid many field multiplications at cost of FFTs (B024); non-linear/seeded preprocessing can compress pseudorandom keys; new FHE ciphertext formats or nonlinear encrypted selection could differ. Restriction is one-frequency field-linear key sketch independent of online mask.

Repair search: across B genuinely distinct PBS inputs with a common legitimate BSK, form W_(b,i)(ζ)=ζ^(a_(b,i))−1 and K_(i,c)(ζ)=BRK_(i,c)(ζ) then selector outputs Y=W*K in tiled GEMM. Exact q97,N8,ell4,m=4d=12 randomized batch tests 2000/2000 matched direct aggregation. At B16 key spectra input 384 elements vs naive off-cache scalar-loop key accesses6144 for frequency-count N8; arithmetic count still6144; ideal 16x KEY-READ reuse is only an assumed slow-memory traffic model, not an empirical PBS speedup. May already be implemented by caches and GPU fused kernels. BatchBoot USENIX2026 and cuFHEpp existing fused kernels are important prior art, novelty/performance UNCLEAR.

Full derivation/test/security/noise/prior-art: findings/boot-B025-block-key-linear-sketch-rank-and-batch-reuse.md.
NEXT B026: audit BatchBoot and cuFHEpp source actual key tiling/reuse; realistic on-chip/cache memory roofline and potential distinctive optimization opportunity. If only commonplace matrix tiling, archive and ask PI for stagnation/pivot after properly judging long-term priority1. BOOT only.