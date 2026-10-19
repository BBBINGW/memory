# BOOT P4 — 2025/696 incomplete INTT direct port to 2025/686 MPmul

TRACK_ID: BOOT
ITERATION: B009
STATUS: FAIL_DIRECT_PORT (not a general impossibility theorem)
DATE: 2026-10-19

Hypothesis killed: replace a homomorphic two-part INTT in Guimarães–Pereira 2025/686 with Paiva et al. 2025/696's free incomplete-NTT technique, without changing algorithmic/key representation and while preserving sparse-secret speedup.

Decisive source facts:
- 2025/686 Algorithm 1 MPmul and Algorithms 2,6 use nested secret-controlled monomial rotations using external products and automorphism. There is no homomorphic two-part inverse NTT on which the 2025/696 optimization acts. The sparse Hamming weight h enters the cost as O(h n log B).
- 2025/696 Algorithm 3 modifies *GPvL23* homomorphic polynomial multiplication and assumes a dense array of N transform-coordinate exponent encryptions Zi, using two rounds of homomorphic dot product. Incomplete NTT embeds block base multiplication in MA so overhead is free relative to already-present two-part INTT—not free for unrelated architectures.
- In F_41[Y]/(Y^8+1), ℓ=1 incomplete NTT maps any single monomial Y^j to four nonzero CRT degree-2 blocks, disproving naive preservation of coefficient secret sparsity. Verified 512 modular ring multiplications and eight monomial cases. This does not exclude a new compressed transform-key derivation.
- 2025/686 concrete q=2^64 cannot directly support the negacyclic CRT roots/inverses used by an odd-prime incomplete NTT over the same modulus. Auxiliary CRT primes would be a different and additional algorithm.
- Source versions are identity-checked but VERSION_UNVERIFIED; no actual runtime, DFR or security measurements. 2025/696's 2.12x comparison was against GPvL23, not 2025/686.

Result: archive only the drop-in reuse idea, not all potential hybrid algorithms. Full derivation in findings/boot-B009-sparse-mpmul-incomplete-ntt-interface.md. Revisit only after a specific transform-key bridge with bounded key size, arithmetic count, noise, and security is constructed.

NEXT_ACTION: B010 test per-output noise asymmetry under 2025/686 MPmul bit-selector reuse + 2025/1892 heterogeneous gadget; one mathematically minimal falsifier, prior art check first.
