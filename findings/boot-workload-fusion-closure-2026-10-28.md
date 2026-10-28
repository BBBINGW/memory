# BOOT — Workload-specific CKKS bootstrap fusion closure

Date: 2026-10-28
TRACK_ID: BOOT
MODE: PAPER_LEVEL_ONLY
CODEX: NOT_USED
NATIVE: NOT_RUN

## Authoritative BOOT state

LATEST_COMPLETED: B162_AUDIT
NEXT_NATIVE_GATE: B163_CORRECTED_B160_NOSCALE_SELECTOR_GATE
B163_STATUS: PENDING_CODEX_QUOTA
CODEX_AVAILABLE: NO
DO_NOT_AUTO_RUN_CODEX: YES

B158_ALGEBRA: PASS
B158_CTCT_MULT_COUNT: OPTIMAL
B158_NOVELTY: PROMISING_NOT_ESTABLISHED
B158_NATIVE_FEASIBILITY: UNRESOLVED
B163: NOT_RUN

## Question

Can a publishable BOOT contribution come from fusing user computation into CKKS bootstrapping rather than evaluating it before/after refresh?

At the broad level, this direction is now highly occupied.

## Prior-art map

### RBOOT — nonlinear activation inside EvalMod

RBOOT: Accelerating Homomorphic Neural Network Inference by Fusing ReLU within Bootstrapping
(USENIX Security 2026; ePrint 2025/1534).

Its central idea is that CKKS EvalMod is itself nonlinear/trigonometric, so ReLU and related nonlinear functions can be co-designed with the modular-reduction approximation instead of evaluated separately.

USENIX reports about 2.77x end-to-end speedup and 81% lower memory relative to its polynomial-approximation baselines.

Sources:
https://www.usenix.org/conference/usenixsecurity26/technical-sessions
https://eprint.iacr.org/2025/1534

Therefore:
    NONLINEAR_ACTIVATION_PLUS_BOOTSTRAP = DIRECT PRIOR ART.

### Bootstrapping is All You Need — linear layers inside S2C

Pan Xiao, Rending Ouyang, Heng Zhang, Jiawen Zhang, Jian Liu,
"Bootstrapping is All You Need: Secure Transformer Inference via Improved CKKS Functional Bootstrapping",
ePrint 2026/1255.

The public abstract explicitly:
- fuses as many operations as possible into each bootstrap;
- uses trigonometric minimax functional bootstrapping for nonlinear layers;
- incorporates linear layers into SlotToCoefficient, eliminating their separate evaluation.

It reports 1.9x runtime speedup and 3x communication reduction versus its stated state of the art.

Primary landing:
https://eprint.iacr.org/2026/1255

Therefore:
    GENERIC_LINEAR_LAYER_PLUS_S2C_FUSION = DIRECT PRIOR ART.

### BootNet — convolution + ReLU + refresh in one bootstrap

Zhaomin Yang, Chao Niu, Cheng Hong, Tao Wei,
"BootNet: Homomorphic CNN Inference with Convolution and ReLU Fused in Bootstrapping",
ePrint 2026/1279.

The public abstract states that every CNN layer can combine:
    convolution + ReLU + noise refresh
in one bootstrapping invocation.

It further fuses:
- NeuJeans-style masking with RBOOT's arcsin stage;
- shortcut/split-merge schedules;
- EvalRound+ adaptations;
and reports 67--73% lower end-to-end latency and 76--90% lower storage versus Orion in its evaluation.

Primary landing:
https://eprint.iacr.org/2026/1279

Therefore:
    LINEAR_PLUS_NONLINEAR_PLUS_REFRESH_WHOLE_LAYER_FUSION = DIRECT PRIOR ART.

## Structural interpretation

The two obvious fusion degrees of freedom are already explicit prior art:

1. Linear map composition:
   Since CtS/S2C are homomorphic linear transformations, a workload linear map can often be algebraically composed into their matrices/diagonals.

2. Nonlinear map composition:
   Functional bootstrapping can replace the standard modular-reduction approximation by a periodic/interpolating approximation of the desired nonlinear target.

A generic paper claiming only
    "fuse operation f into bootstrap"
is no longer a cryptographic contribution unless it identifies a new structural class with a theorem/cost bound not subsumed by these mechanisms.

## Decision

GENERIC_USER_LINEAR_LAYER_FUSION:
    PRIOR ART.

GENERIC_ACTIVATION_FUSION:
    PRIOR ART.

CNN_CONVOLUTION_PLUS_ACTIVATION_PLUS_REFRESH:
    PRIOR ART.

TRANSFORMER_LINEAR_PLUS_NONLINEAR_BOOTSTRAP_CO-DESIGN:
    PRIOR ART / ACTIVE.

WORKLOAD_SPECIFIC_FUSION_AS_BOOT_MAINLINE:
    PARK.

CCF_A_B_VALUE:
    FAIL for generic fusion.

CODEX/NATIVE:
    NOT REQUIRED.

## What could still survive

A future fusion result would need a structural theorem rather than an application substitution, e.g.:
- a lower/upper bound characterizing exactly which operators can be absorbed without increasing multiplicative depth or key material;
- a new representation that removes an existing conversion stage;
- a cross-scheme bootstrap whose conversion + refresh beats native refresh for a provable parameter region.

The next scout therefore moves to cross-scheme bootstrapping rather than another workload-specific fused neural-network operator.

B163 remains the highest native gate once Codex quota returns.
