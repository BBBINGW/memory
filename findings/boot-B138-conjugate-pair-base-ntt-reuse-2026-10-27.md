# BOOT-B138 — Conjugate-pair reuse for the remaining base-table NTTs in ePrint 2026/2119

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: ePrint 2026/2119 Section 4-5
- Status: COMPLETE
- Decision: PASS_ALGEBRA / FAIL_WHOLE_SYSTEM_HEADROOM / PARK
- CODEX_REQUIRED: NO
- Novelty: NOT_ESTABLISHED

## Question

After 2026/2119 reduces direct narrow-blind-rotation table transforms from 2gh forward NTTs to 2h base-table NTTs (tail analogously), can the conjugate structure of Eq. (14)/(19)/(20) reduce the remaining pair of base-table NTTs to one?

## Exact algebra

For a head block x, let

z = pi'_{1,x}(a),   pi'_{2,x}(a) = conjugate(z).

The paper forms

tilde_pi_1 = (z - i conjugate(z))/2,
tilde_pi_2 = (conjugate(z) - i z)/2.

Let p be a CKKS plaintext encoding z.

Plaintext complex conjugation is the public ring automorphism C corresponding to X -> X^{-1}; in NTT form it is a fixed public permutation.

For canonical CKKS slots zeta_j = exp(i 5^j pi/N),

zeta_j^(N/2) = exp(i 5^j pi/2) = i

because 5^j = 1 mod 4. Thus J=X^(N/2) represents slotwise multiplication by i exactly. In NTT form J is a fixed public componentwise factor / index relation and requires no forward NTT.

Therefore from one encoded base p we can synthesize coefficient/NTT representatives of both transformed tables:

p1_raw = p - J C(p),
p2_raw = C(p) - J p.

To preserve the paper's target table scale Delta without coefficient-domain modular division by 2, encode the source z at scale Delta/2. Then

p1_raw ~= E_Delta((z-i conjugate(z))/2),
p2_raw ~= E_Delta((conjugate(z)-iz)/2).

This keeps the downstream scale unchanged and costs at most roughly one bit of source-encoding precision versus directly encoding each transformed table at scale Delta. Alternatively, metadata scale-doubling gives the same semantic division by 2 but changes downstream scale bookkeeping.

The same derivation applies to packed tail table pairs tau_{1,q}, tau_{2,q}.

## Operation count

Paper Section 5.2:
- head direct transformed-table path: 2gh forward NTTs;
- paper NTT-permutation fusion: 2h forward NTTs.

This construction:
- head: h forward NTTs plus public NTT permutations/monomial factors/additions;
- tail: ceil(h/B) forward NTTs instead of 2 ceil(h/B).

For repaired LL13 geometry h=31, G=ceil(8192/31)=265, B=floor(4096/[2(G-1)])=7, ceil(h/B)=5:
- paper-style residual base-table transforms: 2*(31+5)=72;
- conjugate reuse: 31+5=36.

So the residual base-table forward-NTT count is halved exactly.

## Correctness / precision caveat

This is public-plaintext preprocessing only:
- no ciphertext key switching;
- no HE multiplicative level;
- no ciphertext noise growth.

The only new approximation issue is the one-bit source encoding scale reduction if the downstream transformed-table scale is kept identical. This is not expected to be a correctness blocker but would need a numerical precision check before any native performance claim.

## Prior-art / novelty gate

No direct paper hit was found for applying this exact one-NTT conjugate-pair synthesis to 2026/2119's narrow transformed tables.

However, every ingredient is standard CKKS algebra:
- conjugation is a Galois automorphism / NTT permutation;
- X^(N/2) represents slotwise multiplication by i;
- real/imag extraction uses these identities routinely.

A public non-author implementation of the narrow 2026/2119-style factor path (virtualsecureplatform/TFHEpp) still constructs the two transformed vectors separately and encodes/NTTs them separately, so the optimization is not already present there. This is implementation evidence only, not publication prior art.

Novelty remains weak because the optimization follows almost immediately from the paper's explicit Eq. (14) conjugacy and Eq. (19) pair formulas.

## Whole-system value gate

The paper already removes almost all original repeated table NTTs:
for LL13, g ~= 265, so 2gh -> 2h removes about 99.6% of the head forward-NTT count before our optimization.

The authors do not publish a GPU stage breakdown, so the exact 8.2 ms benefit cannot be inferred from operation count.

As a diagnostic only, the independent public CPU implementation above reports representative complete-FBS profiles where:
- table NTT ~= 0.64-0.76 s;
- factor stage ~= 6.2-6.9 s;
- full functional evaluation ~= 14-15.6 s;
- matrix work ~= 3.1-3.3 s.

Those artifacts explicitly state they are not hardware/parameter/security-matched paper results. Still, they show the qualitative Amdahl position: even deleting half the table-NTT time would optimistically save only about 2-3% of complete evaluation in that implementation.

Therefore a 2x local NTT reduction is not currently a credible main paper contribution.

## B138 decision

- Algebra/correctness: PASS.
- Residual base-table NTT count: exact 2x reduction.
- New HE depth/security assumption: none.
- Direct prior-art hit: not found.
- Novelty strength: LOW.
- Whole-system headroom: LOW / UNVERIFIED on authors' GPU, diagnostic evidence suggests low-single-digit end-to-end ceiling.
- CODEX/native: NO.
- Decision: PARK as an implementation note, not a primary BOOT research direction.

## Next

Move to the larger FBS cost exposed by Section 7: number of independent blind-rotation frequency roots.

Before proposing a new basis, first audit SWIFT (ePrint 2026/1163) and the paper's GPSP one-extra-level construction to determine whether signed differences, multi-level additive bases, or function-specific sparse bases are already covered.
