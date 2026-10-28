# BOOT — RMFE subring-envelope: key/capacity/value gate
Date: 2026-10-28
TRACK_ID: BOOT
CODEX_USED: NO
NATIVE_RUN: NO
Parent: boot-post-B162-rmfe-subring-envelope-single-multkey-candidate-2026-10-28.md

## Candidate fixed point
p=5, m=32768, d=8192, ell=2, w=512, k=5.
Use temporary degree-r subring with r=8, m_r=32, Y=X^1024.

Pipeline:
RMFE projections -> monomial E8 envelope -> ONE ModSwitch -> degree-8 SlotToCoeff -> ONE boot-key inner product -> RM_10 coefficient selection -> degree-8 CoeffToSlots -> unpack 8 coords -> keep first 5 -> existing CtxtsToSlots/correction maps -> existing Algorithm 4.

## Key-set gate
Ma et al. 2024/164 implementation computes RM_k recursively with
    smartAutomorph((m >> (i+1)) + 1), i=0,...,k-1.
Hence RM_10 uses exactly the first ten stages of the ordinary thin RM_13 chain for d=8192.
The coefficient-selection portion therefore requires no new automorphism type beyond that chain.

The input tau_i projections are exactly the existing Method-1 SlotsToCtxts maps from 2025/350, so their Frobenius keys are reused.

Degree-8 full transforms/unpacking may require a few small-extension automorphisms. Exact direct-key delta is not yet proven.

KEY_RM10 = STRICT_SUBSET_OF_THIN_RM13
KEY_INPUT_PROJECTIONS = REUSED
KEY_TOTAL_DELTA = SMALL / UNRESOLVED

## Multiplicative-level gate
Geelen 2024/153 shows that full SlotToCoeff has the form M^{-1} U_ell M; for small extension width, level collapsing can merge the extension-basis maps with U factors. Generic Z_(p^e)-linear maps can be evaluated in one plaintext-multiplication level. Unpacking/repacking and coefficient-selection traces consume no multiplicative levels.

For r=8, ell=2, use one collapsed degree-8 linear map for SlotToCoeff and one for CoeffToSlots.

Critical-path linear levels:
baseline split-thin branch:
    thin SlotToCoeff: 1
    thin CoeffToSlots: 1
candidate:
    degree-8 SlotToCoeff: 1
    degree-8 CoeffToSlots: 1

Therefore candidate linear-transform multiplicative depth does not increase.

LINEAR_LEVEL_DEPTH = PARITY_WITH_BASELINE

## Input-envelope noise bound
Candidate combines existing projections as
    A(c)=sum_{i=0}^4 X^(1024 i) tau_i(c).
The X powers are monomials/coefficient permutations. If projected noise bounds are B_i:
    B_A <= sum_i B_i <= 5 max_i B_i.
Thus the new merge itself costs at most log2(5)=2.322 bits in the deterministic worst-case capacity bound versus the worst projected branch.

## Conservative structural work proxy
Input RMFE projections remain k log2(w)=45 automorphisms.

Baseline five thin MultKey branches have roughly:
    5 * (thin S2C 1 + RM_13 13 + thin C2S 1)
  ~= 75 automorphism-scale linear operations,
plus five ModSwitch/boot-key-inner-product executions.

Candidate middle has:
- two degree-8 full transforms,
- RM_10,
- r-1=7 unpacking automorphisms,
- one ModSwitch/boot-key inner product.

Using generic/BSGS degree-8 maps gives an order of roughly 40-45 automorphism-scale operations in this middle block, versus about 75 plus five inner products in baseline. This is a structural proxy, not a latency prediction.

## Holistic value threshold
Published p=5 correction/TnM:
capacity after=101, latency=11.3 s, throughput=89.08, thin ratio=0.832.
Vanilla thin throughput=107.06.

If final capacity stays 101, candidate beats thin throughput at total latency below:
    101*10/107.06 ~= 9.43 s.

Using unchanged source anchors:
SlotsToCtxts-like projection ~2.284 s,
CtxtsToSlots-style final combine ~0.078 s,
DigitExtract ~4.240 s,
the new single-MultKey middle should be below roughly 2.8 s to cross the published thin-throughput line.

Existing five-branch MultKey block is 4.732 s.
So eventual native value needs about a 40% block reduction if capacity stays near 101.

More generally, if final capacity is C:
    latency < 10*C/107.06 seconds
is the approximate thin-throughput frontier.

## Capacity risk
Candidate has no extra linear levels, but degree-8 maps can have larger plaintext-constant norms/key-switch noise than thin transforms.
Baseline final capacity 101 supports only five remaining multiplications, so large extra loss is unacceptable.

Current:
DEPTH_GATE = PASS
INPUT_MERGE_PENALTY <= 2.322 bits
RM_CHAIN = SHORTER (10 vs 13)
FULL_MAP_NOISE_CONSTANTS = UNRESOLVED
NATIVE_CAPACITY = UNRESOLVED

## Fallback family
A latency-capacity family exists with r in {1,2,4,8}, b=ceil(k/r):
r=1 -> 5 thin MultKeys (baseline)
r=4 -> 2 degree-4 MultKeys
r=8 -> 1 degree-8 MultKey.
Do not expand this family yet; use r=8 as decisive endpoint and only inspect r=4 if r=8 fails capacity with clear latency headroom.

## Decision
RMFE_SUBRING_ENVELOPE_SINGLE_MULTKEY = KEEP_ACTIVE
ALGEBRA/CORRECTNESS = PASS_P5
LINEAR_DEPTH = PASS_NO_INCREASE
KEY_SET = PROMISING_SMALL_DELTA
VALUE_THRESHOLD = PLAUSIBLE
CAPACITY = DECISIVE_UNRESOLVED_GATE
NATIVE = NOT_RUN

BOOT state unchanged:
LATEST_COMPLETED=B162_AUDIT
NEXT_NATIVE=B163_PENDING_CODEX_QUOTA
CODEX_AVAILABLE=NO
B163=NOT_RUN
