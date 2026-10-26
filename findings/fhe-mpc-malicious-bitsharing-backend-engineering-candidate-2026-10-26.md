# FHE×MPC — Engineering Candidate: Native-Modulus Malicious Random-Bit Backend for CKKS Smudging

2026-10-26 | **PARKED_ENG_CANDIDATE** | preserved by PI request. **Not a new cryptographic scheme, verified speedup or an active research line.** Related source gate: `findings/fhe-mpc-malicious-random-bit-backend-novelty-gate-2026-10-26.md`.

## Candidate
For Hwang et al. ASIACRYPT 2026, `papers/supplied/2025-395.pdf`, physical pp15–17 Fig8–11 and §4.3, replace or benchmark the discrete-CKKS **BinBoot+Clean** method for producing additive random-bit shares used to sample **fresh** prescribed E-smudging noise in `R_{q_out}`. Candidate *engineering backends* include malicious MASCOT/SPDZ2k random-bit/edaBit/daBit pipelines, offline OT extension and PCG-based preprocessing. Competing protocol **must** reproduce Hwang's ideal per-output law (conditioned on any permissible corrupt subset) and account for internal randomness, public transcripts, masks and selective aborts. Merely generating random bits under an unrelated field/ring is not a drop-in replacement. No proof of realizing malicious UC `FMGHE` follows from this change.

## Source baseline and reported costs
- Hwang et al., **On the (In)security of Approximate Computation Protocols from CKKS**, author paper ePrint 2025/395, PI-supplied `papers/supplied/2025-395.pdf`, blob `84710edb51998a1c9d50a8c306ec1970d8d389f5`. Physical p16: `k≈log E + lambda` shared bits per coefficient; p17 Fig11: `BinBoot(sum ciphertext)`, `Clean`, distributed decrypt & PRF pairwise zero-share mask. Author benchmark on Xeon Platinum 8268 single thread: 2^16 bit shares/33.96s; 2^18/135.84s. **Only BinBoot+Clean was implemented in reported MPC measurement**. Do not call it total application runtime.
- Existing random-bit techniques: Escudero et al. CRYPTO 2020 `ePrint 2020/338` edaBits; BarnOwl `ePrint 2022/800` (different 3PC honest-majority corruption model); MP-SPDZ `https://github.com/data61/MP-SPDZ` MASCOT (prime field), SPDZ2k (2^k ring), daBits and bits-from-squares. These are prior art; ordinary substitution is engineering, not a new primitive.
- Cao et al. 2025/1845, PI-supplied `papers/supplied/2025-1845.pdf` supplies a more stringent UC MGHE/OtF-MPC setting (IND-CPApD, SIM-PDEC, Rob, plus IND-CIRC depending on corruptions) that cannot be assumed from Hwang's semi-honest hybrid theorem.

## Decisive correctness/security trap

Bit b=1 shared over Z8 as (6,3): 6+3=1 (mod8). Reducing each share to Z5 yields (1,3), sum=4 ≠1 (mod5). Therefore conversion to `R_{q_out}` must use native target arithmetic or proven carry-aware share conversion. For RNS/CRT representations, generated bit shares across primes must reconstruct *the same underlying bit* (not unrelated per-prime bits). Reusing total noise e across outputs is disallowed for independent fresh-error ideal functionalities. Maliciously biased bit generation, malformed shares, abort and public commitments must be verified.

## Future optional Codex benchmark — PENDING / NOT AUTHORIZED

Only execute after PI explicitly requests and a formal interface & matching security model are fixed. A proper comparison pins ring N, q_out and RNS factors, n,t, E, lambda, bits/output, number of outputs, corruption threshold, CPU/network/hardware. Compare end-to-end under full **offline + online** counts:
1. Original source-equivalent BinBoot+Clean plus distributed decrypt, PRF masking, key setup.
2. Candidate MPC bit generator: OT/PCG/VSS/MAC preprocessing, native target modulus or share-conversion/carries, online n-party communication, malicious checks, correct embedding into R_qout.
3. Assess reproducible correctness for all bits, uniformity/conditional views, whole-output E-smudging distribution, round count, bytes, full latency/throughput, RAM, setup/key material, behavior under malicious bias/abort and failure.
4. If one candidate has measurable gain at *matched threat assumptions*, retain as engineering work; cryptographic novelty needs an independently specified new invariant.
No benchmarks have run, no performance claim and no approval to start Codex/GPU/server. Prior-art note `findings/fhe-mpc-malicious-random-bit-backend-novelty-gate-2026-10-26.md` gives full source caveats.

`STATUS: PARKED_ENG_CANDIDATE`
`EVIDENCE: SOURCE_VERIFIED_AUTHOR_TEXT + COUNTEREXAMPLE_DERIVED; NATIVE_NOT_RUN`
`NOVELTY: FAIL_GENERIC_BIT_BACKEND; ENGINEERING_VALUE_POSSIBLE`
`NEXT_TEST: ONLY_IF_PI_REOPENS`
`STATE_UPDATE: THIS_NOTE_ONLY; NO_OTHER_TRACK_STATE_CHANGE`
