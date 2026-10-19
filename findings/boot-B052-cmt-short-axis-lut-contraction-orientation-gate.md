# BOOT B052 — CMT-FBT shorter-axis final matrix contraction

TRACK_ID: BOOT
ITERATION: B052
DATE: 2026-10-20
STATUS: PASS_EXACT_CMT_CONTRACTION / PASS_SOURCE_OPERATION_COUNT / UNCLEAR_NATIVE_CKKS_DFR_AND_RUNTIME / FAIL_STANDALONE_NOVELTY
STATE_UPDATE: pending connector confirmation; SHIP paused.

## Source and prior work
Dumezy, Alexandru, Polyakov, Clet, Chakraborty, Boudguiga, "Evaluating Larger Lookup Tables using CKKS", TCHES 2026(1), pp559–591, DOI 10.46586/tches.v2026.i1.559-591, ePrint 2025/1301. Full title-verified research-MCP mirrored PDF, sha256 048ba3ae4fe97eae0417138b816572b1c79b503727db54ce76576a4d38190b19, physical35 pages, VERSION_UNVERIFIED. Source p13 Algorithm2 FDD explicitly supports a short final digit; p15–16 Algorithm3 KProduct forms pairwise Kronecker products, counts pair-size products, depth ceil(log(number digits)); p19 Algorithm6 CMT splits digits into first ceil(nd/2) LSD vectors, remaining MSD vectors, does a plaintext LUT dot per LSD row and one ciphertext multiply PER LSD row; p20 Algorithm7 FDD and CMT; pp25–27 performance, e.g. original 20bit LUT p16 experiments. The original paper offers OpenFHE code UPON REQUEST (p1 footnote), and source implementation was NOT obtained or natively run. Cannot claim production OpenFHE includes or lacks this optimization. Same CMT low-rank branch B040 and other BOOT artifacts are archived; do not repeat them.
B051 was completed in separate local Library handoff, not in GitHub Notes: finite-difference A2B quotient alias FAIL, 30720/31744 source-shaped overflow tests wrong, next B052 named this paper; B051 not claimed GitHub synced. GitHub Notes list already has B050, and B040/B041 have duplicates: never overwrite any existing numbered artifacts.

## One falsifiable claim and exact construction
CMT Algorithm6 evaluates U^T Y V where U is first/low-digit Kronecker onehot vector (length A), V second/high-digit Kronecker vector (length B), Y is plaintext LUT matrix with correct indexing Y[i,j]=f(i+A*j). Existing Algorithm6 outer loop over i in A constructs U_i*(sum_j Y[i,j] V_j), requiring A FINAL ciphertext-ciphertext multiplies. For unbalanced A>B, transpose the PUBLIC LUT and instead evaluate sum_j V_j*(sum_i Y[i,j] U_i), requiring B FINAL ciphertext-ciphertext multiplies. Exact commutative ring equality for ALL U,V,Y (including noisy approximate-indicator input symbols), no new secret/evaluation key, no change to digit extraction FDD or KProduct subtrees. This algebraic reassociation does NOT imply ciphertext bitwise equality under CKKS relinearization/rescaling or unchanged actual DFR.
Let p_i=2^w for i<nd, p_last=2^(k−(nd−1)w), k=log2 LUT size, nd=ceil(k/w). A=product first ceil(nd/2) p_i; B=product rest. Kronecker cost KU and KV is counted source-Algorithm3-style, iteratively multiplying adjacent vector pair lengths and carrying any odd tail. Original entire CMT ciphertext multiplication count KU+KV+A; revised KU+KV+min(A,B). Both have EXACTLY P=A*B public scalar MulInt terms, and the same ideal max multiplicative depth max(ceil(log ndU),ceil(log ndV))+1. This is an algorithmic operation count, NOT a full FBT speedup.

## Verified deterministic exact tests
Python exact integer/polynomial-function model with local Random(20261020) and (404052):
- Random unstructured integer LUT with outputs in [-100,100], legal onehot U,V for 8 (k,w) configurations (10,4),(13,4),(14,4),(16,4),(18,4),(20,4),(18,5),(20,5); 39,400 selected plaintext x, source/revised contraction equals original LUT f(x) for all cases, with full x enumeration when k<=14 and seeded draws otherwise.
- Additional direct nested contraction for (k,w)=(10,4),(12,4),(13,4): 1024/1024 PASS.
- 600/600 exact tests for ARBITRARY perturbed integer vectors U,V (entries -2..2) and random integer Y on (A,B)=(16,4),(64,8),(256,4), verifying BOTH contraction parenthesizations return EXACT SAME integer, including errors in input indicator vectors. Not an encrypted noise test.

## Exact source Algorithm3+Algorithm6 count table
bits,w; A,B; original total CMT CTCT; revised total; saved fraction
13,4;256,32;544;320;41.18%
14,4;256,64;576;384;33.33%
16,4;256,256;768;768;0%
18,4;4096,64;8512;4480;47.37%
20,4;4096,256;8704;4864;44.12%
18,5;1024,256;2304;1536;33.33%
20,5;1024,1024;3072;3072;0%
At 20bit w4 final products decrease 4096→256 (93.75% last stage), but 1,048,576 MulInt, FDD repeated MVB, Gid cleaning, CKKS level management and memory costs do not decrease by this algebra alone. Cannot claim 44.12% latency/RSS/DFR.
Caveat: source paper's output depth analysis assumes certain balanced cases; orienting final contraction does not increase abstract depth. However the two input tensor groups may have DIFFERENT RNS level and noise from KProduct, and transposition changes WHERE plaintext scalar multiply and CKKS rescale/relin/key-switch error occurs; actual secure parameters, native benchmark and DFR must be re-evaluated.

## Novelty and scientific decision
Pure public matrix-transpose contraction choice and choosing shorter loop is elementary matrix-algebra/compilation. Paper itself explicitly optimizes number of CTCT and minimized Kronecker split, so source code might already reorder contraction even if literal Algorithm6 loops LSD. Thus the current result is a source-derived possible implementation improvement, NOT a novel FHE primitive, not yet a full publishable BOOT result. Cannot make a vulnerability, correctness-bug or source implementation claim.
STATUS PASS_EXACT_ALGEBRA/PASS_ABSTRACT_SAVED_PRODUCTS/FAIL_PUBLICATION_NOVELTY/UNCLEAR_NATIVE_NET_GAIN.
NEXT_TEST B053: Do not spend multiple rounds tuning transpose. Seek a substantially new BOOT core primitive/dataflow beyond prior archived low-rank CMT (B040), cleaning (B045/B046), LUT synthesis (B047), or this ordinary reassociation, or if original author's source becomes available do a single native benchmark and noise check before archiving. One hypothesis per round; SHIP PAUSED_BY_PI. B053 NOT STARTED.

## Independent enumeration-count correction (2026-10-20)
The verified onehot LUT test counts listed in the table above sum to **50,600**, not the 39,400 stated in the earlier narrative: 1,024 + 8,192 + 16,384 + 5×5,000 = 50,600. All 50,600 recorded comparisons were exact matches. This numerical correction does not affect any per-configuration operation count, mathematical theorem, or scientific status; it supersedes only the mistaken total.
