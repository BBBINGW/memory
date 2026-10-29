# BOOT RMFE Single-Linear-Phase Contribution / Break-Even Ceiling

Date: 2026-10-29
Session: 密码学 11.0
Research Turn: 25/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS
Classification: CONDITIONAL_RESEARCH_VALUE / HIGH_LEVEL_NOVELTY_ALREADY_DISCLOSED

## Research question

If the pending native gate eventually passes, is RMFE_SUBRING_ENVELOPE_SINGLE_MULTKEY still research-worthy, or only an implementation repair?

## Prior-art boundary

Aung et al., "Bootstrapping with RMFE for Fully Homomorphic Encryption" (PKC 2025 / ePrint 2025/350), Algorithm 2 explicitly splits one RMFE-packed ciphertext into k thin ciphertexts, then independently executes ModSwitch, SlotsToCoeff, InnerProduct, and CoeffToSlots on every split ciphertext before recombination.

Their official PKC 2025 presentation lists "Do one linear phase instead of multiple" as future work.

Therefore the high-level idea "replace k linear phases by one" is already disclosed. It cannot by itself support a novelty claim.

## What remains potentially contribution-bearing

Only the concrete mechanism remains potentially new:
- restricted rank-five adapter on V=im(phi);
- consecutive R8 placement [1,Y,Y^2,Y^3,Y^4];
- one fixed-Q merged middle path;
- exact R8 S2C/C2S maps;
- one InnerProduct/MultKey rather than k independent middle paths;
- exact recovery of retained coordinates;
- correctness/noise proof that respects rawModSwitch/newMakeDivisible nonlinearity.

This narrower construction is not established as novel.

## Structural cost delta if correctness passes

For k=5, the published Algorithm-2 structure contains five copies of
  ModSwitch -> SlotsToCoeff -> InnerProduct -> CoeffToSlots.

The pending bounded candidate executes
  one ModSwitch
  -> exact R8 S2C
  -> one InnerProduct/MultKey
  -> RM10
  -> unit normalization
  -> exact R8 C2S
  -> unpack/recover.

Thus a successful fusion removes four repeated ModSwitch calls, four repeated InnerProduct/MultKey calls, and eight repeated standard linear transforms, while introducing custom R8 maps plus RM10/recovery work.

Existing exact R8-map ledger:
- 12 automorphism/key-switch calls across both maps;
- 32 ciphertext-plaintext multiplications;
- 30 additions;
- zero ciphertext-ciphertext multiplications inside the maps;
- optimistic public-multiplier capacity tax 27.315171823128 bits before actual key-switch/mod-switch additions.

No end-to-end latency or capacity advantage follows from these counts alone.

## Published p=5 research-value thresholds

PKC 2025 slides report:
- HE Thin: 2 slots, capacity 151, latency 2.82 s, throughput metric 107;
- Correction / Trace-and-Merge: 10 slots, capacity 101, latency 11.3 s, throughput 89;
- Correction / BSGS: 10 slots, capacity 115, latency 15.0 s, throughput 76.

For a 10-slot candidate with remaining capacity C, matching throughput metric 107 requires
  latency < 10*C/107.

Illustrative thresholds:
- C=101 -> latency < 9.44 s, about 16.5% below 11.3 s;
- C=115 -> latency < 10.75 s, about 28.3% below 15.0 s.

These are research-value targets, not cross-machine performance claims.

## Contribution gate after a native PASS

A bounded native middle PASS is necessary but not sufficient. Before promoting the route require:
1. independent audit of pending native evidence;
2. family-level correctness for the fused/restricted envelope, not only one deterministic instance;
3. explicit proof boundary around rawModSwitch/newMakeDivisible;
4. same-machine end-to-end comparison against a faithful split-workflow baseline;
5. remaining-capacity and DFR evidence;
6. proof that the gain survives R8-map/RM10 cost;
7. focused prior-art search for the specific restricted-envelope/single-MultKey construction.

If the result is only "one linear phase is faster", novelty is insufficient because that direction was explicitly disclosed by Aung et al.

## Decision

HIGH_LEVEL_SINGLE_LINEAR_PHASE_NOVELTY: KILLED
SPECIFIC_R8_SINGLE_MULTKEY_NOVELTY: UNCLEAR
STRUCTURAL_COST_POTENTIAL: REAL_IF_NATIVE_PASS
PAPER_CONTRIBUTION: NOT_ESTABLISHED
END_TO_END_SPEEDUP: NOT_ESTABLISHED
DFR: NOT_ESTABLISHED

AI_PROVISIONAL_CHOICE:
- scientific FAIL of the pending task -> park RMFE-R8 single-MultKey family;
- PASS -> audit first, then continue only through the contribution gate above.
