# BOOT-B020 — Goldilocks field + parity torus representation: unique encoding, no carry-free additive closure

TRACK_ID: BOOT
ITERATION: B020
DATE: 2026-10-19
STATUS: PASS_UNIQUE_ENCODING / FAIL_CARRY_FREE_ADDITION / PASS_EXACT_CORRECTION / NO_PROVED_PROOF_COST_ADVANTAGE
STATE_UPDATE: YES

## Primary hypothesis
For q=2^64 and p=q−2^32+1, represent a canonical torus integer x∈[0,q) by E(x)=(z=x mod p,b=x mod2). Hypothesis: this compressed field+bit representation can be updated through a concrete source-compatible q-torus addition cheaply using native F_p field addition and Boolean parity, without proving a 64-bit overflow/carry or repeatedly reconstructing integer limbs. This is B019's one necessary structural bottleneck; do not treat mere injectivity as computational closure.

## Read-before-write provenance and relevant prior art
[FACT] BOOT B018, B019 already established the conditional one-parity integer-link lemma for approximate TFHE gadget and an exact mixed-witness forgery; files findings/boot-B018-goldilocks-parity-approx-gadget-integer-link.md and findings/boot-B019-lookup-parity-shared-witness-gate.md. Last BOOT iteration B019; THIS is B020.
[FACT] Guimarães–Pereira 2025/686, Table 3 p23, true q64 torus and approximate one-level gadget; HasteBoots USENIX Security 2026 official artifact f7ed/HasteBoots uses Goldilocks proof field and exact decomposition. Do not assume source code supports this proposed representation.
[PRIOR ART] Tremblay Thibault–Walter, CCS 2025 DOI 10.1145/3719027.3765097 and https://www.zama.org/post/verifiable-fhe-bootstrapping-using-snarks : their verifiable TFHE changes ciphertext modulus to the proof system's native prime field, rather than cheaply proving the source q64 torus unchanged; this is an independent architectural alternative.
[PRIOR ART] Mark Pedron, Zellic, "Formal Verification of a Plonky2 Gate", dated 2026-06-15, https://www.zellic.io/blog/formal-verification-plonky-gate/ : Section "Why U32 Addition Needs a Dedicated Gate" and exported U32AddManyGate soundness example derive Goldilocks native-field arithmetic plus integer limb range/carry checks. In particular, it has a soundness and completeness proof over canonical integers, not just mod-p equality. This is highly relevant precedent for carry enforcement; does not constitute novelty for BOOT.
[VERSION/SCOPE] Original research notes GitHub_Notes read_repo_file returned bare {} in this session; relied on latest B019 STATE already in conversation and file list/sha, and used GitHub Notes connected write/append tools for BOOT-only. No verifiable FHE circuit built, no native runtime/security benchmark. Web results are citations to public current sources, not validated whole-protocol implementations.

## Exact two-lift representation theorem (PASS)
Let q=2^64, D=2^32−1, p=q−D (Goldilocks odd prime).
For canonical x∈[0,q), define E(x)=(z=x mod p, b=x mod2).
For canonical field element 0<=z<p, candidate integer lifts are x=z and, ONLY when z<D, x=z+p. Since p is odd, these candidates have opposite parity. Hence (z,b) uniquely identifies x, with explicit decode:
  h=(b XOR (z mod2)) ∈{0,1},
  x=z+h*p,
  VALID iff h=0 or z<D.
Converse: every valid tuple is an E(x), and all x are encoded uniquely.
[OBSERVATION] Decoding/relation certification needs access to canonical integer parity of z, NOT natively available as an algebraic F_p operation; upper-lift h=1 requires proving z<D (a 32-bit interval), not merely a Boolean h. These are part of the proof-cost ledger.

## Decisive counterexample to carry-free addition
Proposed native coordinatewise operation:
   N(E(x1),E(x2))= (z1+z2 modp, b1 XOR b2).
Take x1=x2=q/2=2^63. Real q-torus sum is 0, E(0)=(0,0).
But native pair is (q modp=D,0). Since D is odd and D is NOT less than D, neither canonical lift z=D (odd) nor z+p is legal with even parity. So native result is INVALID, a zero-noise full-q counterexample.
WORSE: a native result can also be VALID BUT WRONG. In scaled q=256,p=251,D=5 with x1=247,x2=255, actual torus sum is246 and true E(246)=(246,0). Input residues are z1=247,z2=4; native field sum 0 modp, parity=0, giving (0,0), a valid encoding of integer 0 rather than246. Hence merely proving all states E-valid is insufficient to certify each transition.

## Restricted general algebraic obstruction (PASS)
Assume an injective group homomorphism phi:(Z/qZ,+) -> (F_p,+)×(F_2,+), with coordinatewise additive update. Let phi(1)=(a,b). Then q*phi(1)=(q a modp,0)=0 since q is even. As gcd(p,q)=1, a=0; image of generator has order at most2, so phi cannot be injective for q>2. Thus NO such group-homomorphic, carry-free, coordinatewise field+one-bit addition encoding exists, regardless of which injection phi was chosen. Does NOT rule out changed ciphertext type, nonlinear update with comparison, large extension ring, full limbs, or approximate/partial domains.

## Correct arithmetic bridge and its required cost
Define exact torus overflow/carry k=floor((x1+x2)/q)∈{0,1}. Then
  x_out = x1+x2−k q ∈[0,q),
  z_out=(z1+z2−k D) modp,
  b_out=b1 XOR b2 (since q even).
These are identities. The correction coefficient D=q−p is only 32 bits, but k is a function of the ORIGINAL 64-bit canonical x1,x2. An unbound Boolean claimed carry k and output E-validity do NOT suffice for soundness, as the q256 example with k=0 passes the field equation, parity and valid output but is wrong when the genuine carry is 1. Need prove correct integer carry, e.g. x1+x2=x_out+k q in Z with sufficient bounds and common commitment, or an equivalent sound limb comparator/lookup. A single mod-p relation is not a proof of integer equality.
[GROUP OBSERVATION] Because (F_p,+)×F_2 cannot embed the 2^64 cyclic additive group, a nontrivial carry/correction or changed operation semantics is unavoidable in THIS class; this is classical elementary group theory, NOT a novel lower bound worthy of publication by itself.

## Cheap independent verification
[EXHAUSTIVE SMALL-Q] q=256,p=251, D=5, all x∈[0,256) have unique valid (z,b), tested 256/256.
Enumerated ALL (x1,x2)∈[0,256)^2: exactly 65,536 pairs. Native z-sum+b-XOR yielded:
  correct 32,896;
  INVALID output (z,b) 32,595;
  valid output encoding WRONG torus result 45.
The genuinely carried formula with k=floor((x1+x2)/q) matched exact E((x1+x2) modq) on 65,536/65,536. Valid-but-wrong example x1=247,x2=255 documented above.
[FULL REAL-Q] q=2^64,p=q−2^32+1. With deterministic Python Random(20261019), tested 100,000 uniform random input pairs and all 15×15=225 boundary pairs from {0,1,2,2^32−2,2^32−1,2^32,p−2,p−1,p,p+1,q/2−1,q/2,q/2+1,q−2,q−1}, 100,225/100,225 PASS for unique decoding and corrected exact addition; native carry-free full-width counterexample x1=x2=q/2 PASS as counterexample.
[REFERENCE CODE]
  def enc(x): return (x%p,x&1)
  def decode(z,b):
     h=(z&1)^b
     return z+h*p if h==0 or z<q-p else None
  def add_pair(x,y):
     k=(x+y)//q
     (z1,b1),(z2,b2)=enc(x),enc(y)
     return ((z1+z2−k*(q-p))%p,b1^b2)
  assert add_pair(x,y)==enc((x+y)%q)
All tests use exact arbitrary-precision Python integers; not native TFHE, SNARK, proof-soundness benchmark, cryptographic parameter check or noise/DFR certification.

## Repair search: can the small q−p gap make carry cheap?
[DERIVATION] High integer lift x=z+p is needed only when z<D, a narrow 32-bit prefix region. For *uniform* q64 integer words Pr[x>=p]=D/q≈2^−32. For 2048 or8192 independent uniform coefficients probability at least one upper-lift roughly 2^−21 or2^−19, respectively — nowhere near a typical 128-bit failure target. These are ideal uniform random masks only; intermediate MPmul ciphertext distribution may be different. Neglecting the upper branch as "rare" is not an acceptable exact-verification shortcut or FHE correctness proof.
[DERIVATION] If BOTH incoming integer lifts are known to be the low representatives x_i=z_i (<p), let s=z1+z2, Goldilocks reduction carry j=floor(s/p)∈{0,1}, u=s−j p∈[0,p). Then genuine torus carry is k=j*[u>=D]. This exploits the SMALL D threshold on a narrow exceptional interval after field reduction. However verifying the field carry j and the comparison u>=D with sound canonical limbs/commitments is itself NOT free; and upper-lift operands need additional branches. No proof-time or memory advantage demonstrated. This suggests a possible research exploration only if the proof system ALREADY supplies a certified field carry and low-prefix range check.
[PRIOR ART/COST] Zellic's Plonky2 2026 U32AddManyGate analysis independently demonstrates precisely why native-field arithmetic for bounded integers needs integer carry+limb range gates. Zama CCS25 sidesteps much of this incompatibility by altering TFHE's ciphertext modulus to the native prime. A cheap generic q64->Goldilocks no-carry representation would need an additional innovation beyond the classical pseudo-Mersenne reduction.
[SECURITY/DFR] No scheme changed or secret distribution estimated, and no new publishable gadget or speedup established. A local algebraic obstruction is not an attack on HasteBoots or Zama; both account for arithmetic in their chosen contexts.

## Decision
STATUS: PASS_UNIQUE_ENCODING / FAIL_NATIVE_ADDITIVE_CLOSURE / PASS_BOUND_CARRY_REPAIR / NO_MEASURED_NET_GAIN.
RESULT: (z,b) is an injective 64-bit torus encoding, but cannot natively support q-torus additions by coordinatewise F_p+XOR. Need true 64-bit carry and parity/exact-lift binding. Source already uses certified limb carry/changes modulus, so not a new competitive verifiable TFHE optimization. Do not promote B018/B019 to a new protocol just because their local lemma is true.
NECESSARY_CONSTRAINTS: exact q64 torus intermediate semantics and arithmetic across rounds, true overflow k, bounds for every canonical lift and output, shared committed witness and Fiat–Shamir transcript, error/DFR and total proof costs.
REPAIR_ATTEMPT: precise k D field correction, two-lift decoding and conditioned narrow comparison under known low lifts; no certified inexpensive full-trace solution.
NOVELTY_GATE: LOW for coordinatewise compression itself; pseudo-Mersenne field carry gates well-known. Potential full verifiable TFHE system not established.
NEXT_TEST B021: pivot AWAY from blind q64/Goldilocks compression and toward a NEW problem-first structural question rather than more low-level patches. A focused initial hypothesis: can a source-verified batched FHE/PBS verification transcript use *one committed canonical torus lift reused across multiple adjacent linear operations* so that range/carry lookup count scales with values at nonlinear boundaries rather than every native addition? First read actual HasteBoots and CCS25 transcript/trace structure, identify explicit sharing invariant/one-mixed-witness counterexample, and compare true proof cost against existing batching; if no real common-boundary reuse, archive quickly. Alternative novel BOOT subtopic may be chosen by PI after source check. One hypothesis and minimal test only.
STATE_UPDATE: YES; only BOOT.
