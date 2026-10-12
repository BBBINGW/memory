# Iteration 98 — PaCo encoded_eta scale is correct; no hidden deterministic factor in boot_to_nonboot

Date: 2026-10-12. Paper: Coron–Seuré, *PaCo: Bootstrapping for CKKS via Partial CoeffToSlot*, ASIACRYPT 2025, ePrint 2025/886.
STATUS: **FAIL** hypothesis that an unaccounted fixed scale in author implementation falsifies ideal small-angle output model. **PASS** source-line algebraic normalization and two-channel high-precision toy verification. **UNCLEAR** source actual integer output equals a single round(g(m)), because CKKS has many intermediate encodings, rescalings, switching noise, and no single final rounding. **HUMAN_REVIEW** whether to leave this low-novelty precision audit and select a new technical hole or authorize one independent actual noise measurement. No paper flaw, security attack or novel method.

## Read before write / pinned source
Read AGENT.md, RESEARCH_PHILOSOPHY.md, current STATE.md (I97→I98), I97 finding and used connected GitHub read tools.
[FACT] Main author public repo `se-tim/PaCo-Implementation` fixed git commit `84a91afbd8558eb15facc66609cc1d0098e0da87`, file `paco_package/ckks_x.py` SHA ea8073682c82dadcc892ab48b29e8d8bc4ccc237, lines 153–170, 270–300, 183–197.
[FACT] Pinned Git submodule `se-tim/CKKS-in-SageMath` at `2d7eab254f5be4daed5e2099be5d348abbe3ae07`, file `ckks_package/ckks.py` SHA d93f13fe7a49382b75feb0e375dd3810b26cb732, lines396–457, 694–733, 931–943, 1319–1352, 1505–1553.
[FACT] Original ePrint 2025/886 §5.3 eq(10) pp19–20, Algorithm4 p24 lines13–16, Appendix C physical p35 ideal coefficient extraction. Latest official PDF version UNVERIFIED; mirror SHA256 ee427d006097fabdbd30a0a4dc36ed09df5ffea68df30a0511cc154b303a936a.

## One precise hypothesis / cheap falsifier
HYPOTHESIS: author code's final η encoding / product operation / conversion has an extra constant factor or division which invalidates I97 model ideal coefficient round[g(m)], perhaps accounting for 1.74-bit shortfall.
FALSIFIER: static source produces the unique coefficient `g(m)=q/(2π)sin(2πm/q)` in continuous ideal arithmetic with no hidden scalar, and a minimal independently calculated complex-number identity matches both real/imag channels.

## Exact source facts
- `ckks_x.py` lines153–170 defines `eta = -q0*1j/(4*delta*pi) * [(i<C/2) + 1j*(i>=C/2)]`, then `encoded_eta = encode(eta,is_boot=True)`. Preceded by `encoded_mu` a mask.
- `seq_PaCo` lines283–300 obtains ideal circle aggregate via 4 public coefficient encodings * 4 secret bsk, trace, partial CtS, `conj_rotate(C)`, `encoded_mu`, product, trace, then `ct = ct - ct.conjugate()` (line293), `ct = encoded_eta @ ct` (line294), `trace(C,C//2)` (line295), grouped SlotToCoeff (296–298) and `boot_to_nonboot()` (line299).
- Core `encode(z,is_boot=True)` lines396–457 uses integer polynomial encoding multiplied by **delta**, with coefficientwise rounding. `@ = multiply then rescale` lines931–943, `rescale()` lines694–716 divides by delta and rounds polynomial coefficients at EACH multiplication step. Grouped BSGS matrix transformations also rescale.
- Core `boot_to_nonboot` lines720–733 uses `l=floor(self.l * log(delta,p)+1)`, `q=self.moduli[l]` then `return CKKS(self.b % q,self.a % q,is_boot=False)`. NO additional scale multiplication/division and NO final `round(g)` call at this conversion.
- Source precision function at core lines1505–1553 compares initial decrypted plaintext polynomial with output decrypted plaintext polynomial, with coefficientwise mean of `log2(|pt|+1) - log2(|error|+1)`. Initial ciphertext includes Gaussian encryption noise; I97 ideal distribution refers to generated messages.

## Algebraic normalisation [DERIVED]
Let `z=ψ(m)=exp(2πim/q)`, `z - conj(z)=2i sin(2πm/q)`, and `η_real=-iq/(4Δπ)`. Then:
`Δ*η_real*(z-conj(z)) = Δ*(-iq/(4Δπ))*2i*sin(2πm/q) = (q/(2π))*sin(2πm/q) = g(m)`.
Imaginary-half packing uses `η_imag=iη_real`, hence `Δ*η_imag*(z-conj(z))=i*g(m)`. Source's decomposed SlotToCoeff inputs are correctly scaled by `1/Δ` and source final conversion contributes NO extra factor.
This is a high-level algebraic identity under the already established PaCo ring-coefficient representation, NOT a proof of exact encrypted implementation output.
- `g(m)` is real generally NONINTEGRAL, and source does not implement a final `round(g(m))` operation; final ciphertext coefficients are integers because encodings/key switching/rescales have rounded throughout. The I97 single-final-round ideal model is a reasonable zeroth-order control, but not an exact zero-encryption-noise implementation even if encryption noise is switched off.
- Core `boot_to_nonboot` modulo reduction can alter centered representatives if actual output exceeds its new modulus range; we do not assert no-wrap for all intermediate ciphertexts or that operations are noiseless.

## Minimal independent calculation (NO CKKS)
Local deterministic `/mnt/data/iteration98_paco_scaling_identity_check.py`, sha256 32b66ca6dc45c639ce07fb958cd69cde80831d116cd2955cd49ba385fbe66f1e, JSON `/mnt/data/iteration98_paco_scaling_identity_check_results.json` sha256 b7443d096a4c61fd85410be7e8945a9c486d967a0a811bbaba7e4ca424a404bf. Used 85 decimal mpmath digits for PaCo I (q=2^29,p=2^22,Δ=2^32), PaCo II (q=2^44,p=2^32,Δ=2^48), m∈{0,1,⌊p/3⌋,p-1,p,−p}. All 12 real and imaginary channel assertions within 1e−65 PASS. At m=p, g_I=4192619.79043951155920196 (m=4194304), g_II=4294965611.587713726708074 (m=4294967296). Not full Sage CKKS execution nor empirical error attribution.

## Scientific conclusion / next action
[FAIL] The specific proposed extra-deterministic-scale cause of I97 reported 12/22 versus ideal model 13.736/23.736 is ruled out at algebraic and fixed-source level.
[OPEN] Relative to actual author's mean-of-logs statistic, ~1.74-bit numerical discrepancy cannot be assigned solely to key switching, rescale, and encoding, because original publication reports integer bits and no controlled noise decomposition has been run. No evidence of an author correctness defect or new technique.
[RECOMMENDATION] Stop endless elementary sine/scale model variations: no verified novel contribution in I95–98. Ask PI to choose between (A) one **specific** experimental isolated-bias versus operational-noise comparison in pinned Sage implementation (needs environment and benchmark design) or (B) park PaCo precision micro-audit and choose a different FHE gap. Do not auto-pivot, and never contact authors without instruction.
End:
STATUS: FAIL (extra scale), PASS (source normalization), UNCLEAR (actual final integer effect), HUMAN_REVIEW (future direction).
RESULT: Circle sine coefficient scale is exactly g(m), no extra boot_to_nonboot divisor; the sole final-round toy model is conditional, with interleaved integer rounding in actual CKKS.
NEXT_ACTION: PI decide A narrow Sage isolate-vs-real error experiment or B archive low-novelty PaCo sine/precision micro-audit and choose another paper/hole; do not automatically launch I99.
STATE_UPDATE: YES — corrected and source pinned final scaling/precision ambiguity.
