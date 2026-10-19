# BOOT B021 failure archive — parity-only boundary aggregation and assumed HasteBoots savings

TRACK_ID: BOOT
ITERATION: B021
DATE: 2026-10-19
STATUS: FAIL_ONE_BIT_SOUNDNESS / NO_DIRECT_CURRENT_HASTEBOOTS_BENEFIT
SCOPE: Only the proposal that two q64-torus linear operations can be fused into one field relation with a ONE-bit CRT checksum and thereby immediately reduce HasteBoots proof costs. Not a rejection of every lazy-reduction technique.

## Minimal falsifier and repair
With q=256,p=251, x=a=b=250,z=248,K=0 all in canonical ranges, e=x+a+b−z−Kq=502=2p. Field identity e=0 modp and parity e=0 mod2 pass but z is wrong: true (x+a+b) modq=238. A q64 counterpart exists by taking x=a=b=ceil(2p/3), z=3x−2p,K=0, p=Goldilocks. Thus one parity bit inherited from B018's tighter gadget interval does NOT prove a two-addition aggregated integer identity.

Repair valid only under simultaneous canonical range/input binding: -3q<e<3q<4p; if e=0 modp and e=0 mod4 then e must be 4p multiple and hence exactly zero. Exact sum-multiplicity counts for q256 triple input / one ternary K: field-only 51,334,388 accepted with 34,557,172 wrong; field+parity 23,050,072 with 6,272,856 wrong; field+mod4 16,777,216 with zero wrong. Full q64 honest 100000/100000 reference arithmetic PASS. This is an elementary coprime CRT argument, not a SNARK or performance benchmark.

## Why no demonstrated contribution
In the source f7ed/HasteBoots, vfhe/src/bfhe/parameters.rs uses native Goldilocks as the ciphertext ring modulus, and trace/src/acc_trace.rs lines ~225–269 already packs ONLY input_acc and monomial_times_acc into committed oracles and derives output_acc, external_product_input and linear permutation traces. Hence this source does not currently pay the hypothetical q64 canonical carry cost at every field-linear step, and sharing derived linear intermediates is ALREADY practiced. Lazy reduction and keeping unreduced intermediate limb expressions are preexisting ideas in arkworks-rs/nonnative and gnark nonnative (source README/docs). No new key security, soundness, noise/DFR or measured proof efficiency was established.

## Next
Complete evidence and limits: findings/boot-B021-boundary-linear-lazy-carry-mod4-gate.md.
NEXT_TEST B022: test the exact duplicated commitment flagged BY AUTHORS in f7ed/HasteBoots batch_blind_rotation.rs around 210–215,455–465 against DecompositionSnarks::prove_as_subprotocol around 140–150; seek valid same-witness canonical PCS oracle/layout mapping to save duplicate commit/open. First check actual trace ordering/index MLE and Fiat–Shamir order; don't overclaim until matched PCS costs/security.
Only BOOT-owned files.