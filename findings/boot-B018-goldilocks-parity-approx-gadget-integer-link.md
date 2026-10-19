# BOOT-B018: Goldilocks + 1-bit parity certificate for exact rounded torus gadget

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATION: B018
STATUS: PASS_LOCAL_INTEGER_LINK_LEMMA / PASS_EXHAUSTIVE_TOY / UNCLEAR_NOVELTY_AND_PROOF_COST
STATE_UPDATE: YES

## Primary falsifiable claim
For 2025/686's single-level signed approximate gadget at q=2^64, B=2^23 or 2^22, and Goldilocks proof prime p=q−2^32+1, does a field equality with valid bounded integer witnesses PLUS only x≡r mod2 imply the exact canonical integer gadget relation, despite q>p? If yes, the extra parity condition may avoid an entire second prime-field proof. This is a LOCAL theorem and a proposed repair, not a complete succinct argument, new FHE scheme, security or speed claim.

## Authentic source and prior art
[FACT] Guimarães–Pereira, ePrint 2025/686, PDF Table3 physical p.23, q=2^64, FBS1 N=2048 single-level base B=2^23, FBS2 N=8192 base B=2^22. PDF cached title verified but VERSION_UNVERIFIED, SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335. Authors' code antoniocgj/Fast-Amortized-Bootstrapping/src/mosfhet/src/polynomial.c, routine polynomial_decompose_i (NOT the other trlwe_decompose) rounds centered high bits via 64-bit unsigned offset 2^63+2^(64-b-1); original repository's default branch not immutable-pinned.
[FACT] HasteBoots Liu et al., USENIX Security 2026, official https://www.usenix.org/conference/usenixsecurity26/presentation/liu-fengrun. Public artifact https://github.com/f7ed/HasteBoots README explicitly states their implementation uses EXACT full gadget decomposition, with B=2^5, ell=13 for Zama comparison, not Zama's approximate decomposition. An older ePrint 2025/261 (authors and formulation differ) has an exact gadget/lookup PIOP Section3.3; its research-MCP mirror failed author identity check so NOT claimed to match final USENIX 2026 paper; information from official abstract, artifact README and web old text only.
[FACT] Tremblay Thibault–Walter, CCS 2025, DOI 10.1145/3719027.3765097 already has a TFHE bootstrapping SNARK with approximate gadget-related arithmetic; open TFHEprus repository also advertises an approximate-gadget bounded reconstruction PoC. So generic approximate-gadget verifiability is NOT novel. In-depth priority/novelty still UNVERIFIED.
[SEARCH] Broad source screening included BatchBoot 2026, HasteBoots 2026, 2026 triangle ALU encoding and newer CKKS work. B018 deliberately selected one BOOT-relevant FHE–ZK mathematical problem rather than another pairwise primitive substitution. 2026/1836 and1840 full ePrint PDFs were unavailable in research MCP; no unsupported claims about their contents.

## Exact integer semantics
Let q=2^64, b=22 or23, B=2^b, G=q/B, H=B/2. For any canonical unsigned x∈[0,q), define the AUTHOR-SOURCE rounded balanced digit:
  D_b(x) = ( ((x+q/2+G/2) mod q) >> (64−b) ) − H.
Choose d=D_b(x) in [−H,H), and r the centered lift of x−Gd modulo q in [−G/2,G/2). Then choose w=(x−Gd−r)/q ∈{0,1}. The unique witness satisfies exact integer equation
  x=Gd+r+q w.
At the halfstep tie x=G/2, one gets d=1,r=−G/2,w=0 (matching implementation). At x=q/2, d=−H,r=0,w=1. At x=p, d=0,r=−(2^32−1),w=1.

## Main constructive theorem (independent derivation)
Assume the SAME canonically bounded integer witnesses satisfy
  0<=x<q,
  −B/2<=d<B/2,
  −G/2<=r<G/2,
  w∈{0,1}.
Let e=x−Gd−r−qw. Suppose a proof soundly checks:
  (i) e=0 in Goldilocks F_p,
  (ii) x≡r (mod 2), where this parity relation refers to those SAME canonical integers.

From bounds, |e| < (3q+G)/2 <2p (true at q=2^64,b=22,23,p=q−2^32+1). Goldilocks field equality implies e∈{−p,0,p}. Because q and G are even, parity check implies e is even. Since p is odd, ±p are odd. Thus e=0 over integers.

To prove uniqueness, subtract two bounded exact witness equations: G(d−d')+(r−r')+q(w−w')=0. Since |r−r'|<G and r−r' must be divisible by G, it must be zero. Then d−d'=−B(w−w') with |d−d'|<B, forcing d=d',w=w'. Thus these bounded witnesses define EXACTLY the author's canonical balanced approximate decomposition. Completeness from source's rounding formula and centered residual.

## Field-only counterexample and minimal tests
[COUNTEREXAMPLE] Let x=p (<q), d=0,r=0,w=0. All ranges hold and e=p=0 mod p, but x !=Gd+r+qw. Because x odd and r even, added parity condition rejects this invalid witness. This falsifies any protocol asserting integer equality from only the field check and bound constraints, NOT any published verifiable TFHE proof which may include additional gates.

[EXHAUSTIVE SCALED REFERENCE] With q=256, B=16, G=16, p=251 (odd prime; (3q+G)/2=392<2p=502), exhaustively enumerate all 256*16*16*2=131072 bounded (x,d,r,w) tuples. There is exactly ONE correct witness per x, hence 256 correct. Field congruence ALONE additionally accepts 266 incorrect tuples. Field congruence PLUS parity accepts ZERO incorrect tuples. All 256 canonical witnesses pass. Result PASS.
[FULL-WIDTH REFERENCE] Independently compute source-exact d,r,w with Python big integers on 30,000 uniformly sampled q64 words per b=22 and23, plus seven boundary words (including q/2,p,q−1). All 60,000 sampled witnesses and boundary values satisfied integer equality, field and parity, and ranges. Result PASS.
[REPRO SCRIPT SHAPE] For scaled test:
  for x in range(256):
    for d in range(-8,8):
      for r in range(-8,8):
        for w in (0,1):
          e=x−16*d−r−256*w
          if e%251==0 and (x−r)%2==0: assert e==0
This test checks the entire adversarial bounded witness space, not just randomized honest witnesses.

## VFHE lesson and full-protocol gate
[NECESSARY CONSTRAINTS] (A) Integer bounded canonical x,d,r,w (including correct tie handling), (B) common binding across field equality and parity, (C) parity proof for EXACT SAME r and x, (D) correct accumulator trace/key/NTT/rounding relation, (E) real proof cost, FS soundness, security, full DFR.
[REPAIR] Parity kills precisely the ±p modular aliases left by the tight integer ranges. If bound checks are absent, e can be ±2p and parity alone fails. If r in parity check is a different unbound witness, adversarial mixed-witness forgery succeeds. If x is supplied as only one F_p element without proof of the canonical uint64 lift, the meaning of x's parity is ambiguous. The PIOP must bind witness values to one commitment and enforce x's 64-bit lift, e.g. public canonical word or range-bounded low/high limbs.
[IMPLEMENTATION OBSTACLE] A field equation does NOT enforce parity automatically. Need bound decomposition r=2v+r0 with r0∈{0,1} and appropriate bounded v; verify x's public canonical lowest bit equals r0. One Boolean digit plus associated quotient/range relation may be inexpensive only if the existing range proof on r exposes that low bit. Remainder r is 41 or42 bits and d is 23 or22 bits; the full proof may need as many or MORE range lookup constraints than HasteBoots's many small exact gadget digits. Mathematical one-bit correction is NOT equal to a one-gate complete SNARK.
[NOVELTY] Approximate TFHE SNARK and bounded-carry techniques are prior art (Zama CCS25, TFHEprus); specific parity+Goldilocks alias lemma might be useful but source originality unknown. Do not claim publication or benchmark. Historical preprint and final HasteBoots have different author versions; provenance must remain explicit. Stronger literature/implementation comparison needed.
[RESEARCH_DECISION] Keep the small constructive invariant as a promising but unproven component; do NOT yet select an implementation-heavy path or promise its performance.
NEXT_TEST B019: One primary question: can HasteBoots-like existing range lookup prove the SAME-witness remainder parity at almost zero marginal constraint/opening cost (including canonical x and challenge ordering), compared to exact multi-digit decomposition and CCS25 approximate gadget circuits? Cheap falsifier: one-coefficient explicit witness layout with constraint count and an adversarial two-opening mixed-witness counterexample; stop if range/commitment cost overwhelms savings. Keep BOOT isolation.
END: STATUS PASS_LOCAL_INTEGER_LINK_LEMMA / PASS_EXHAUSTIVE_TOY / UNCLEAR_NOVELTY_AND_PROOF_COST; STATE_UPDATE YES.
