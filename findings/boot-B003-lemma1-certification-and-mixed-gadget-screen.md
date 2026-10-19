# BOOT B003 — Actual-Parameter Mixed-Gadget Certification Gate

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATION: B003
STATUS: FAIL_CERTIFICATE / OPTIMIZATION_UNCLEAR

## Primary hypothesis
The source-proved worst-case Lemma 1 noise bound of Lee–Min–Seo–Song ePrint 2023/958, combined with Hong–Lee ePrint 2025/1892's heterogeneous gadget parameter selection, can certify a beneficial mixed-parameter schedule in the 2023/958 real n,N,ell configuration.

## Source provenance
[FACT] 2023/958 original PDF physical pp. 11 (Algorithm 2, Lemma 1), 15–17 (security, performance, Tables 2, 4, 5). Mirror SHA256 0ab8c83d5aebbbf0185e200c7c3aab10150aa4e3bad0470a839246d33954e6de; VERSION_UNVERIFIED.
[FACT] 2025/1892 original PDF physical pp. 11–13 (Theorems 3.1–3.2) and 25–26 (Appendix B, DM/LMKCDEY extension). Mirror SHA256 508a5a0b3914e23e8d71198476a50879c471a6f192e6f65bcd68314b89622018; VERSION_UNVERIFIED. Its Appendix B does not directly establish 2023/958 Algorithm 2's block-binary noise law.
[FACT] The block-key paper implements N=1024, B=2^7, d=3, beta=2^-25, alpha=2^-15, n=630,687,788,885,978 for ell=2,3,4,5,6; k=n/ell. Source Table 2 gives (2d+2)k FFT and (4d+2)nN scalar mult. Source Table 5 reports 7.05,6.49,6.70,6.82,7.12 ms total bootstrapping for the five source configurations, NOT for any new mixed schedule. Upstream public implementation SNUCP/blockkey-tfhe, src/libtfhe/tfhe_gate_bootstrapping.cpp at 633c9ed9adae9b6eab095af7dd9f9757acc59300 contains bk_l=3, bk_Bgbit=7, bk_stdev=2^-25 in its 128-bit preset.

## Minimum falsifier: published uniform baseline already fails this certificate
[FACT] Lemma 1 gives ||e||_infty <= 2k(1+N) epsilon + 4 delta eta_beta n d N, where the unsigned gadget decomposition satisfies epsilon <= B^-d. For a *conservative guaranteed certificate*, setting epsilon=B^-d=2^-21 suffices.
[DERIVATION] For the genuine N=1024, B=2^7, d=3 configurations:

| ell | n | k | 2k(1+N)2^-21 |
|----:|--:|--:|--------------:|
|2|630|315|0.30791759490966797|
|3|687|229|0.22385120391845703|
|4|788|197|0.19257068634033203|
|5|885|177|0.1730203628540039|
|6|978|163|0.15933513641357422|

Each first-term upper bound exceeds 1/8=0.125 before including the nonnegative encryption-error term, so this particular worst-case certificate cannot establish the nominal correctness margin even for the published uniform d=3 baseline. This does NOT imply the actual error exceeds 1/8, and is NOT a correctness attack. A half-ULP epsilon/2 assumption still yields 0.15396 for ell=2.

[ILLUSTRATION ONLY] Taking eta_beta =6 beta (not from source, not a deterministic Gaussian support bound) and delta=128 gives 4*128*6*2^-25*630*3*1024=177.1875 for key error; this shows how loose a naive infinity-norm bound may be but cannot be substituted for a real tail bound.

## Exhaustive two-format artificial proxy test
[DERIVATION] Choose only d in {3,4}, same B=128, with m of k blocks at d=4, remaining k-m at d=3. Ignore all TRGSW key errors, key-switch/mod-switch errors and actual approximate-gadget rounding distribution; constrain only
2(1025)[(k-m)128^-3+m128^-4]<=1/8.
Minimizing FFT count 8k+2m gives:

| ell | k | minimal m | mixed FFT | all-d4 FFT | published all-d3 FFT | mixed vs all-d4 FFT saving | key-length unit saving vs all-d4 |
|---:|---:|---:|---:|---:|---:|---:|---:|
|2|315|189|2898|3150|2520|8.00%|10.00%|
|3|229|102|2036|2290|1832|11.09%|13.86%|
|4|197|70|1716|1970|1576|12.89%|16.12%|
|5|177|50|1516|1770|1416|14.35%|17.94%|
|6|163|36|1376|1630|1304|15.58%|19.48%|

Mixed scalar-multiplication proxy: N*ell*[14(k-m)+18m]. BRK-size units: ell*[3(k-m)+4m].
[CONCLUSION] This is NOT proof of real performance or DFR improvement. The all-d3 paper baseline is cheaper and empirically works. The apparently attractive comparison with an artificially constrained all-d4 parameter set does not beat the published baseline.

## Secondary conditional-Gaussian gate
[DERIVATION under B002 assumptions] For source n=630,N=1024,beta=2^-25,d=3 and unsigned gadget digit bound D=B=128, the predictable-input Gaussian key-error variance upper bound in a *single extracted coefficient* is V<=8 beta^2 n d N D^2 = 0.00022530555725097656 (sigma<=0.01501018). Even ignoring deterministic residual, key switching and modulus switching entirely, the generic sub-Gaussian bound at t=1/8 is 2 exp(-t^2/(2V)) approximately 1.745e-15 (~2^-49), not tight enough to certify a putative 2^-128 DFR. This is merely a loose upper bound, NOT an observed DFR or insecurity evidence. Its applicability assumes independently sampled fresh Gaussian TRGSW errors and predictable bounded digits; full FHE DFR needs separate reasoning.

## Prior art and novelty decision
[FACT] Hong–Lee 2025/1892 already provides per-key heterogeneous choices, knapsack-like optimization and duplicated key choices. A straightforward blockwise restriction is not a demonstrated novel construction. No exact full prior-art absence claim.
[DERIVATION] The failure of a weak proof certificate is not evidence that parameter combinations are bad; likewise a proxy comparison excluding actual key noise is not evidence that they are good.

## NEXT_TEST B004
Investigate the source implementation's actual digit norms and decomposition-rounding residuals, and formulate a baseline-calibrated high-confidence DFR estimate or rigorously justified tail bound *that first admits the published d=3 uniform configuration*. Only then rerun mixed-vs-uniform optimization under equal 128-bit computational security, statistical failure target, real end-to-end runtime/key size; kill this blockwise composition if it offers only convex-combination tuning already in 2025/1892. Do not branch into unrelated FHE research or change other tracks.

END: STATUS FAIL_CERTIFICATE; RESULT source-proven bound too loose for useful comparison; NEXT_TEST B004; STATE_UPDATE YES.
