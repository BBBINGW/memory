# BOOT-B020 archive: carry-free Goldilocks field + one parity bit is not a q64 torus arithmetic interface

TRACK_ID: BOOT
ITERATION: B020
DATE: 2026-10-19
STATUS: FAIL_CARRY_FREE_TORUS_ADDITION / NOT_ALL_COMPACT_REPRESENTATIONS

The encoding E(x)=(x mod p, x mod2), p=2^64−2^32+1 and q=2^64, is injective for canonical x∈[0,q). Decode h=(b XOR (z mod2)), candidate x=z+h p with condition h=0 OR z<q−p. But native field and bit addition (z1+z2 modp, b1 XOR b2) does NOT reproduce addition modq.

Decisive full-q counterexample: x1=x2=q/2, genuine E((x1+x2) modq)=(0,0), while native update produces (q−p,0), INVALID since q−p=2^32−1 is odd and equal to the threshold for upper lift.
More seriously, q256,p251 two-input pair x1=247,x2=255 gives a VALID but WRONG native encoding (0,0) vs true E(246)=(246,0): simply enforcing output validity/parity is not a sound transition relation.

Restricted group obstruction: no injective additive homomorphism Z_(2^64) -> F_p(+)×F_2(+), since q is coprime to p and the image of generator in field must be zero; remaining bit has order at most2. This rules out only coordinatewise carry-free homomorphic embeddings, NOT nonlinear/carry-aware representations or alternative proof systems.

Exact carried formula with k=floor((x1+x2)/q) gives z_out=(z1+z2−k(q−p)) modp and b_out=b1 XOR b2, but correct k must be certified against the SAME canonical integer lifts. Boolean k plus mod-p relation and valid (z,b) endpoints do NOT prove k; pair 247+255 with k=0 is a forged, valid output transition. A canonical z's low bit also requires integer-range/limb proof to distinguish x=z vs z+p.

Independent tests: all q256×q256 =65536 additions: native correct 32896, native invalid32595, native valid but WRONG45. Exact carried formula 65536/65536 PASS. q64 full precision 100000 deterministic random pairs +225 boundary pairs all PASS corrected. Group obstruction symbolic proof. No native FHE/SNARK performance measured.

Conditional repair observation: for known low lifts x_i=z_i, the field reduction carry j=floor((z1+z2)/p), u=z1+z2−jp, gives k=j*[u>=D], D=q−p=2^32−1. However certifying j and comparison still requires sound integer proof; full upper lifts need additional handling. High-lift rate D/q≈2^-32 per uniform coefficient cannot be dropped to meet 128bit robustness; for 2048 independent masks chance >=1 high lift about 2^-21, 8192 about2^-19.

Strong public prior art: Zama CCS25 changes ciphertext modulus to native Goldilocks for verifiable TFHE (https://www.zama.org/post/verifiable-fhe-bootstrapping-using-snarks); Zellic 2026-06 Plonky2 U32AddManyGate formal verification requires true integer carry and limb range gates (https://www.zellic.io/blog/formal-verification-plonky-gate/). No novel paper contribution from this direct compressed encoding alone.

Detailed source, proof, reproducible test and limitations: findings/boot-B020-goldilocks-parity-torus-carry-closure.md.
REPAIR_SEARCH performed; NO proven cheap native closure. Archive this explicit proposal, retain B018 local parity theorem and B019 conditional low-limb sharing as independently correct mathematics.
NEXT_TEST: BOOT-B021 research actual complete HasteBoots/CCS25 proof dataflow and test whether canonical torus lift/carry constraints can be proven only at nonlinear boundaries and reused through adjacent linear operations using a single shared committed witness, with strong same-witness binding. Falsify via one small trace or existing pipeline. No empty repeated parameter tuning.
STATE_UPDATE YES. BOOT-only changes.