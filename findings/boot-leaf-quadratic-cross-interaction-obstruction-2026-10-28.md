# BOOT paper-only: quadratic cross-leaf obstruction (2026-10-28)

TRACK_ID: BOOT. Native state unchanged: B162_AUDIT completed; B163 PENDING_CODEX_QUOTA, NOT RUN.

## Source gate
Official ePrint 2026/1779 landing page https://eprint.iacr.org/2026/1779 identifies author source code at https://github.com/Zhaoyang-Liang/bootstrapping-via-ring-switching-without-slot-recovery and says latest of 5 revisions dated 2026-10-26. Full PDF fetching returned 403; public GitHub page access was blocked. No full-text/source-specific claims made.

## Model theorem
Assume two leaves hold independent field elements u,v. The available operations are arbitrary independent leaf-local maps and public linear recombination, but NO joint multiplication/conversion or interaction-capable key. Every output has form A(u)+B(v)+c. Its mixed finite difference Delta_u Delta_v vanishes. For x=alpha*u+beta*v, alpha*beta !=0, over characteristic !=2:
Delta_u Delta_v(x^2)=2*alpha*beta*(u-u')*(v-v'), nonzero for suitable inputs.
Consequently x^2 cannot be implemented by this restricted independent-leaf/additive-recombination interface. This is not an impossibility for general FHE/ring switching.

## Candidate correction and cheapest next gate
The prior polynomial interaction rank d-1 is a separation-rank count, not a ciphertext communication/operation cost bound. A formal uv cross statistic may be ill-typed if u and v live in different ring ciphertext spaces or under different keys.
First obtain source details; identify exact leaf plaintext rings, ciphertext rings, secrets, maps, recovery and output API. Type-check uv multiplication and identify necessary key switch/repacking/ring alignment. Compare its online work, evaluation-key bytes and noise with full recovery; PARK if uv already costs comparable to full recovery. Do not generalize to d>2 without a cheap quadratic gate.

STATUS: MODEL_OBSTRUCTION PASS in restricted model; SCHEME_COMPATIBILITY UNKNOWN; VALUE UNKNOWN; NOVELTY NOT_ESTABLISHED. B163 NOT RUN.
