# BOOT-B143 — Compact carry-state transplant into ePrint 2026/1869

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Sources:
  - supplied ePrint 2026/1869, High-Precision Homomorphic ALU over Arbitrary Moduli with O(1) Bootstrapping
  - supplied ePrint 2026/1840, Efficient Homomorphic Arithmetic Logical Units with O(1) Bootstrapping
- Status: COMPLETE
- Decision: PASS_LOCAL_ALGEBRA / FAIL_WHOLE_SYSTEM_HEADROOM / PARK
- CODEX_REQUIRED: NO

## Target

2026/1869's power-of-two A2B specialization uses radix B=32. The second functional bootstrap outputs:
- binary carry-transition indicators for both possible incoming carries;
- two candidate bit functions for each of s=5 output bits.

The authors then compose these finite-state maps over ell=ceil(n/5) positions using an indicator-matrix prefix circuit.

For |C|=2, s=5 and H=ceil(log2 ell), their stated multiplication count specializes to

2(s+1)(H-1)+s.

At n=256, ell=52 and H=6, this is 65 ciphertext-ciphertext multiplications after the second FBS, at multiplicative depth H=6.

## Compact carry state from 2026/1840

For binary monotone carry maps there are only three possible transition behaviors:
- kill: 0 -> 0, 1 -> 0;
- propagate: 0 -> 0, 1 -> 1;
- generate: 0 -> 1, 1 -> 1.

2026/1840 encodes these three behaviors into one complex carry-state ciphertext u and gives public linear maps pi(u), chi(u) such that

f_u(c)=chi(u)+pi(u)c,

and block composition can be done as

u_{a:k}=u_{b:k}+pi(u_{b:k})(u_{a:b}-u_{b:k}).

Because pi is linear in u and conjugate(u), one prefix-composition layer needs one ciphertext-ciphertext multiplication for all packed positions.

This state encoding applies directly to the binary-carry B=32 specialization of 2026/1869.

## Hybrid A: compact state + 1840-style bit correction

Let the second FBS output:
- one compact carry-state ciphertext;
- the s bits of a_j mod B.

After H compact-state prefix levels, recover incoming carries linearly and correct each radix digit by subtracting the incoming carry as in 2026/1840.

For s=5:
- carry composition: H=6 CMults;
- borrow/bit correction: s(s-1)/2+s=15 CMults;
- total post-FBS CMults: 21 instead of 65.

But the bit correction adds about ceil(log2 s)+1=4 depth levels after carry recovery. This changes the post-FBS depth from about 6 to about 10.

Decision: strong operation-count reduction, poor depth tradeoff.

## Hybrid B: compact state + dual candidate bits

Keep 2026/1869's candidate-bit interface:
for each bit k, the second FBS outputs b_k(0) and b_k(1).

Use compact carry states only for the prefix. After H levels, recover each incoming carry c_j linearly and select

b_k = b_k(0)+c_j (b_k(1)-b_k(0)).

All s bit selections occur in parallel in one additional multiplication level.

For n=256, s=5:
- compact carry prefix: 6 CMults;
- final bit selection: 5 CMults;
- total: 11 CMults instead of 65;
- depth: H+1=7 instead of H=6;
- second-FBS output width: 1+2s=11 functions instead of 12.

Algebraically this is correct for the binary monotone carry case.

A same-depth variant can propagate compact affine bit transducers during the prefix, but then it requires roughly O(s) products per level and loses most of the operation-count advantage. The cheap 11-CMult form inherently waits for the final carry and therefore adds one dependent level.

## Whole-system value gate

The directly comparable 2026/1840 implementation provides a stage breakdown at N=2^16.

For 256-bit, base-2 A2B:
- RefreshI: 17.36 s
- Stage 1 FBS: 50.34 s
- Stage 2 FBS: 32.96 s
- Carry recovery: 1.80 s
- Bit correction: 1.56 s
- Total: 104.02 s

Thus the two FBS stages plus RefreshI account for 100.66/104.02 = 96.77% of latency.
Carry recovery plus bit correction account for only 3.36/104.02 = 3.23%.

The 1869 implementation runs on different older CPU hardware and does not publish the same stage breakdown, so the 1840 profile is diagnostic, not a matched Amdahl measurement. Still, both constructions have the same qualitative shape: two expensive CKKS functional bootstraps followed by logarithmic leveled carry work.

Even deleting all post-FBS carry/bit work would therefore have only low-single-digit headroom in the measured 1840 system. Hybrid B also adds one 43-bit-scale level in the 1869 parameterization, so the larger modulus chain can offset part of the local multiplication savings.

## The actual dominant open problem

The dominant cost is the existence of **two sequential functional bootstraps**:
1. first FBS computes periodic radix reduction / remainders;
2. linear operations recover quotients and cancel shared overflow;
3. second FBS evaluates local carry/bit functions.

A naive one-FBS fusion would need the second local function to depend directly on data from neighboring pre-reduction values. Packing a pair into one univariate LUT expands the effective finite input domain and loses the small periodic LUT advantage; a bivariate/paired FBS is a different construction.

This is exactly why ePrint 2026/2368 is now critical: its public abstract claims parallel digit decomposition using a single bootstrapping with O(log B) lookup depth. Until its full source is audited, a one-FBS fusion claim here would have an obvious likely prior-art collision.

## Minor source inconsistency

2026/1869 Section 5.5 states total B=32 depth
19+ceil(log2 ell).

For n=32,64,128,256 with ell=ceil(n/5), this evaluates to 22,23,24,25.

Section 6.3 instead says the implemented depths are 23,24,25,26.

This is a one-level textual/accounting discrepancy. It may reflect an implementation-only/output level not included in the analytical formula, so it is not treated as a correctness flaw without code/source confirmation.

## B143 decision

- Compact-state transplant: PASS algebraically.
- Best simple hybrid: 65 -> 11 post-FBS CMults at n=256, but +1 multiplicative level.
- Whole-system headroom: LOW from the only available measured stage breakdown.
- Novelty: weak/moderate because it is an explicit combination of two concurrent/public constructions.
- Native/Codex: NO.
- Decision: PARK.

The higher-value unresolved target remains reducing two FBS stages to one, but that direction is SOURCE_GATED on ePrint 2026/2368.

## Next

Continue fresh BOOT scouting among already supplied full sources while keeping 2026/2368 as P0 missing source.
