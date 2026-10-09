# Archived: GL generic BigSwitch structure

Status: ARCHIVED / NEGATIVE
Archived: 2026-10-09
Paper: Craig Gentry and Yongwoo Lee, "Fully Homomorphic Encryption for Matrix Arithmetic", IACR ePrint 2025/1935.
Source: Section 3.2 (Switchbig/Switchsmall); Theorem 3.6 and Corollary 3.9 (coefficient-matrix representation); Sections 3.4-3.5 (d3 = au ⊛ av and relinearization).
Evidence copy: MCP cached 2025/1935 via GitHub mirror, SHA-256 985173da6bc45f1c89c86769d5b6b16bfcdd98bf07e91476cd424778b8d9ec84, VERSION_UNVERIFIED.

## Primary hypothesis [NEGATIVE]
For generic independent GL encryptions, the trace product d3 = au ⊛ av always has sufficiently restricted rank, norm, or gadget-digit distribution that its BigSwitch can exploit this structure for a general performance/noise improvement.

## Decisive falsification [DERIVED]
By the coefficient-matrix form in Corollary 3.9, D3 = Au (Bv')^T over the relevant coefficient ring, with Bv' obtained from av by a bijective coefficient permutation/automorphism. For independently uniform encryption components au,av, Au and Bv' are independent uniform matrices. Conditioned on Au being invertible, multiplication by Au is a bijection; consequently D3 is *exactly uniform* over the whole matrix space. In particular generic low rank/sparse/low-gadget-digit structure cannot be guaranteed.

A deterministic full-rank example is Au = I and Bv' = I, giving D3 = I. Thus universal low-rank claims are false even without a probabilistic argument.

## Scope / limitations
- This negates a *generic ciphertext-distribution structural advantage*, not every algorithm that exploits factorization or changes evaluation keys.
- Conditional uniformity is not independence from Au/av.
- Does not cover correlated ciphertext inputs (self-multiplication), structured intermediates, or special restricted plaintext/ciphertext classes.
- Earlier BigSwitch noise investigations identified an n-dependent gadget convolution cost under stated idealized assumptions, but did not demonstrate a new security or correctness flaw, nor quantify actual DESILO parameters.
- The ePrint source version is not verified against the formal publication.

## Decision [HUMAN]
Human research lead instructed archive. Do not continue this branch without a genuinely different, falsifiable construction or new evidence.

NEXT: Focus on MRFHE (ePrint 2026/853) batch-bootstrapping EvalMod: test whether nonlinear EvalMod P can be evaluated over an extension ring directly without cross-component interference and without costly projection.
