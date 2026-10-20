# BOOT-B067 — Dyadic monomial-power LUT decoding: exact span vs torus-scale failure

Date 2026-10-20 | TRACK_ID BOOT | SHIP PAUSED
STATUS: PASS_EXACT_DYADIC_LUT_SPAN / FAIL_NATIVE_TORUS_RAW_SQUARING / UNCLEAR_SCALE_PRESERVING_FHE_AND_NOVELTY

## Primary hypothesis
One standard blind rotation of a public constant polynomial yields an RLWE/GLWE encryption of the phase monomial X^t. Could a chain of log2(N) encrypted ciphertext squares produce X^(2^j t) and enable an arbitrary full-domain LUT f:Z_(2N)->Z_q using ONLY public polynomials and sample extraction, replacing a second blind rotation? Require proof of representability and the most elementary ciphertext type/scale feasibility before expensive noise/security studies. A mathematical solution to LUT representation alone is NOT a new FHE algorithm.

## Primary literature and provenance
[FACT] Hwang, Lee, Min, Song, "Efficient Full Domain Functional Bootstrapping from Recursive LUT Decomposition", SAC2025 pre-proceedings, https://sacworkshop.org/SAC25/preproceedings/sac2025-2-paper18.pdf , physical pp2-3, explicitly gives the **same dyadic recursive decomposition** into negacyclic and lower-domain components. This part is NOT new. Its algorithm evaluates them with separate PBS instances. Original PDF inspected visually on physical p3.
[FACT] TFHE universal monomial blind rotation (monomial lift) and reusing its output are known, including https://patents.justia.com/patent/20260291734 and https://www.zama.org/post/tfhe-deep-dive-part-4 . Do not claim novelty for monomial lift.
[FACT] Wang et al., Full domain functional bootstrapping using the prime cyclotomic ring, Theoretical Computer Science 2025, https://doi.org/10.1016/j.tcs.2025.115392 , supports full-domain LUT with a single blind rotation using a different ring; strong competitor. Search for the precise monomial-power construction remains incomplete.
[FACT] Torus plaintext coefficient scaling and Q=2^w negacyclic rings are the actual constraints; GF_257 toy is NOT this ciphertext type.

## Algebraic observation (q odd; 2 invertible)
Let N=2^m, R_q=Z_q[X]/(X^N+1). Let r0=f have period 2N. At dyadic level j let p_j=N/2^j, r_j periodic 2p_j; set
  a_j(i) = (r_j(i)-r_j(i+p_j))/2
  r_(j+1)(i) = (r_j(i)+r_j(i+p_j))/2  for 0<=i<p_j.
Extend a_j anti-periodically with half-period p_j. The process ends at constant c=r_(m+1). Define public polynomial V_j coefficient 0 =a_j(0), coefficient N-2^j i = -a_j(i), 1<=i<p_j, remaining coefficients zero. Then for every t in Z_(2N)
  f(t) = c + sum_(j=0)^m Coeff_0( V_j X^(2^j t) mod (X^N+1)).
Function-subspace dimensions N+N/2+...+1+1=2N. The decomposition follows known Hwang et al. math; potential novel tradeoff would be using encrypted monomial **powers** to compute all layers instead of multiple independent bootstraps. Repeated squaring is not claimed to be cryptographically viable.

## Exact test 1: functional span
[TEST] Python b067_power_monomial_full_domain.py SHA256 1a49184524d0c867b7966bc277037e11c372d98319fbf469892b2201ca88cfbd.
For q=257, N in {4,8,16,32}: 300 random arbitrary LUTs for each N, exact constant-coefficient extraction for all phase values 2N, totals 36000/36000 PASS. Basis matrix ranks 8/8,16/16,32/32,64/64 over F_257 PASS. No encryption, noise or runtime benchmark.

## Exact test 2: even-modulus obstruction and scaled lifts
[DERIVATION] If q=2^w and all public LUT decoding operations are Z_q-linear on monomials X^(2^j t), the output mod2 is invariant under t->t+N, because -1=1 mod2. An arbitrary impulse f(0)=1,f(N)=0 cannot be represented. The odd-q dyadic recursion involves division by 2, invalid as a general Z_(2^w) operation. For integer-lifted LUT values divisible by Delta=2N, each halving step is integral, and a full reconstruction **of this restricted scaled LUT** succeeds modulo Q. At Q=65536, N=4,8,16,32 and Delta=2N, 300 random small integer-valued scaled LUTs per N: 36000/36000 phase checks PASS. Representability consumes up to log2(2N) bits of output-scale headroom and demands consistent integer lifts.

## Critical exact test 3: scaled torus ciphertext multiplication destroys phase
[DERIVATION] Standard TFHE blind rotation encrypts Delta X^t, typically Delta=2^(w-b) mod Q=2^w for b-bit plaintext. Ordinary ciphertext-ciphertext multiplication without scale restoration yields Delta² X^(2t). If b<=w/2, Delta²=0 modQ. The plaintext signal becomes identically zero immediately. Relinearization does not restore a zero plaintext.
[TEST] Exhaustive modular monomial square arithmetic over ALL 2N phases for (w,b,N)=(16,4,8),(32,8,16),(64,8,1024),(64,16,1024),(64,32,1024): 6192/6192 squares produce zero plaintext coefficient. This falsifies direct native-torus **raw** square implementation, not all scale-preserving schemes.
An alternative would need an explicitly constructed BFV/BGV/CKKS-like scale-preserving multiplication, modulus ladder/rescale and relinearization; no such concrete circuit, parameter proof or benchmark is available this round. Also the first-order relative noise term of j repeated squarings grows by 2^j (N at j=log2N), ignoring evaluation-key and rescale error; for N1024 the last level amplifies initial relative noise by 1024. All realistic DFR bounds remain unknown.

## Conditional cost and novelty
At N1024 the conceptual candidate needs 1 TFHE blind rotation + 10 GENERAL RLWE ct-ct squarings (depth10), 11 public polynomial multiplies/extractions, evaluation keys and scale handling. This may be substantially slower/larger than two TFHE blind rotations, and must beat Wang et al.'s one-BR prime-cyclotomic approach. No native encrypted test, no security parameter match, no performance claim and no proven new primitive.

## Decision
PASS pure algebra / FAIL direct torus-scale realization / UNCLEAR alternate scale-preserving FHE.
Do not promote dyadic LUT decomposition as novel; it is already published. This is a new **candidate composition question** and early scale-type falsifier only.
NEXT_TEST B068 (not started): one smallest attempt to define a genuinely scale-preserving square that maps Enc(Delta X^t) to Enc(Delta X^(2t)) under supported ciphertext representation, then compare a 10-square chain, noise/modulus ladder, key size and real runtime against an additional PBS and a prime-cyclotomic FDFB. Archive quickly if no credible cost edge.
STATE_UPDATE=NO: current Research GitHub Notes read_repo_file for findings/boot-STATE.md returns {}; do not overwrite existing large BOOT state. Only append new B067 finding. SHIP unchanged.
LOCAL: BOOT_B067_handoff.zip includes full report, exact Python and JSON, SHA256 JSON eb0555f9bff3f89490d083e819839966a573db0371a1586dc9c303f1ecdf98a6.