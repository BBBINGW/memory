# Iteration 81 — Native-field Pedersen/IPA replacement: 49-bit subgroup-order bottleneck

Date: 2026-10-12
Active target: Cascudo et al., *Verifiable Computation for Approximate Homomorphic Encryption Schemes*, CRYPTO 2025, ePrint 2025/286, sound CRT digit lookup repair.
Scope: PI's "好的，请继续" after I80 HUMAN_REVIEW permits exploration of replacement/co-design of commitment interface within existing vFHE repair target. No research direction change and **NO author contact, Gmail draft, or public disclosure**.

## Source provenance
[FACT] Primary paper ePrint 2025/286, cached Research MCP 52-page mirror SHA256 `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, VERSION_UNVERIFIED. §5 physical pp25–26 / Appendix F.1–F.2 pp50–51: original PCS is a per-F_(p_k^d) code/Merkle Brakedown commitment, with F_{p^4} for 49-bit CRT base primes explicitly stated on p26; §6 p27 benchmarks 49-bit RNS primes. The original Brakedown PCS does **NOT** assume discrete-log hardness in order-p_k groups.
[FACT] Ganesh, Nair, Sharma, *Dual Polynomial Commitment Schemes and Applications to Commit-and-Prove SNARKs* CCS 2024 ePrint 2024/943 §5, Appendix E: its Dory/Pedersen/AFG route assumes a cryptographic bilinear group over a scalar prime field, not an automatically compatible F_(p_k^d) of 49-bit characteristic. I80 established non-drop-in nature.
[BACKGROUND] Standard Pedersen commitment binding depends on DLP in the commitment group; generic DLP methods (e.g., BSGS or Pollard rho in suitable prime-order groups) require O(sqrt(r)) group operations for group order r. This is a textbook security consideration, not a new algorithm or novelty claim.

## ONE primary hypothesis and minimal decisive test
[HYPOTHESIS — FAIL] Replace vFHE Brakedown with a *standard cyclic prime-order Pedersen/IPA-style group commitment* whose homomorphic message map directly preserves the additive law of the native F_(p_k^d) (no non-native modular arithmetic), while retaining computational binding at ~128-bit security for original 49-bit p_k.
[FALSIFIER] A nontrivial native additive homomorphism into a cryptographically large group of coprime prime order cannot exist; choosing the required p_k-order group gives only ~24.5-bit generic discrete-log work factor for a 49-bit p_k.
[CHEAPEST TEST] Check additive group exponents and group-order compatibility, compute generic DLP work factor, demonstrate binding failure mechanism in a 101-order subgroup using an exact BSGS recovery and double Pedersen opening. No implementation of FHE or full PCS.

## Exact argument
Let F=F_(p^d), char(F)=p, and G be a cyclic group of prime order r. For a nontrivial *additive homomorphism* φ:(F,+)→G, every x∈F satisfies p x=0, whence φ(x)^p=1. If r≠p, the only element whose p-th power is one is 1_G; φ is trivial. Hence nontrivial scalar-additive group compatibility requires r=p. This is an argument about standard cyclic prime-order homomorphic Pedersen/IPA architectures, **NOT** a blanket impossibility theorem for PCSs, hash commitments, general CP-SNARKs, higher-order groups, or non-native circuits. It also does not assert a single cyclic order-p group can faithfully represent all d extension-field coordinates.
If r=p≈2^49, the DLP of two standard public Pedersen generators has generic work O(sqrt(p))≈2^24.5≈23.7 million group operations, dramatically below ~2^128. Knowing h=g^a allows arbitrary two openings of C=g^x h^s:
  choose x'≠x and s'=s+(x−x') a^(−1) mod p, then C=g^(x') h^(s').
For strong generic ~128-bit DLP security in a conventional prime-order group one ordinarily targets r of size ≥2^256. Since r ≠ p for native 49-bit p, this removes the direct homomorphic field interface and forces encoding/limb/range handling or another architecture. For fields of extension degree d=4, a group of order p does not by itself provide an F_(p^4)-module action; more structure/coordinates would be required even before security.
Note group-security work factor is not the same as whole vFHE proof security. vFHE's original field-size soundness arguments use |F_(p^d)| and coding, not DLP in p-order groups.

## Reproducible toy binding collision
Exact subgroup order p=101 of (Z/607Z)^*, cofactor 6. Set g=2^6 mod607=64, h=g^13 mod607=26. Compute log_g(h)=13 by baby-step/giant-step. Let C=g^7 h^19 mod607=512. Set alternative opening (x',s')=(33,17), and verify g^33 h^17 mod607=512, x'≠7. No cryptographic security is expected at p=101; this is merely a numerical demonstration of the algebraic DLP-to-commitment-equivocation mechanism.
Executed exact stdlib Python helper: `/mnt/data/iteration81_native_field_group_commitment_test.py`; SHA256 `1d2582a32146f0958cf9caead77f67f50e2ea39005e01842ae8b5bc14ae01f26`; all assertions PASS.

## Consequence
[NEGATIVE] Direct replacement of componentwise code/Merkle PCS by *standard native-additive, prime-order Pedersen/IPA* under 49-bit CRT primes is not a 128-bit binding-sound shortcut. It does not solve hidden external integer ↔ field-PCS linkage.
[OPEN] Other commitments (Merkle/hash based, encoding with large-order groups and proven non-native modular arithmetic, specialized cross-characteristic proof systems) are not ruled out. No efficiency or impossibility result for those architectures; no new complete repair, no cryptographic attack on actual system, and no novelty claim.
Avoid I63–I68 previous CRT-local/algebraic/coding variants and I77–80 simple commitments, batched postchallenge CRT and ready-made DualPCS.

## End of Iteration 81
STATUS: **FAIL** — scoped native-additive prime-order Pedersen/IPA replacement at 49-bit p cannot provide ~128-bit DLP binding security.
RESULT: prime-order group-char mismatch or insecure p-order DLP; 101-order toy BSGS creates two verified openings to identical commitment.
NEXT_ACTION: Open ePrint 2025/286 Appendix F.2 pp50–51 and test ONE proposed ZK masking of the Brakedown evaluation response `v'=q1 U_f` using `w=v'+z` and a separately committed codeword for z: determine whether original verification checks can authenticate the masked response **and bind a hidden unmasked aggregate** without non-native PCS verifier. First write exact acceptance equations; falsify with independent mask equivocation or missing external-u link before any protocol implementation. No encoder variants.
STATE_UPDATE: YES — architecture eligibility now explicitly excludes prime-order native Pedersen/IPA for 49-bit p at 128-bit binding.
