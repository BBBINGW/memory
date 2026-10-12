# Iteration 90 — Published Medium-circuit parameters do not kill the bounded-public-A no-wrap route

Date: 2026-10-12. Active target: vFHE ePrint 2025/286 CRT digit range-check repair.
STATUS: **PASS, qualified** for sufficient no-wrap bound at a source-reported real workload; **UNCLEAR** exact per-oracle digit packing and full cost/privacy/security. No novel method, SNARK forgery, author contact or public disclosure.

## One hypothesis, cheapest decisive check
I89 proposed that the real-world vFHE range-check configuration may be unable to satisfy the stronger condition T=m(beta-1)<p_min after accounting for the FULL batched digit oracle, thereby killing I88/I89 before expensive analysis. Falsify using ONE actual source configuration, not a toy per-digit slice.
Read repo AGENT.md, STATE.md, and I89 finding. Read original ePrint 2025/286 52pp mirror via Research MCP, SHA256 29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19, VERSION_UNVERIFIED vs official current binary. Source anchors physical §4.3 pp20–24 digit decomposition and beta, Table 2 p27, §6.3 p29, §6 pp27–29 HE primes and performance. Author-maintained reference code repository is https://github.com/vfhe/proof-friendly-CKKS (PoC benchmarks; not a full SNARK repair).

## Published numeric parameters [FACT]
Section 6.3 p29, cited 'Medium circuit' application, explicitly prints (W,D,L,N,c)=(1,1,3,8192,5), extension d=4, and a '20-bit' lookup-table configuration; §6 p27 uses 49-bit RNS primes. Paper says Πrange maximum input size is 286720 Rq0 elements for this case. Table 2 p27 gives max size
  M_reported=N*c*(W*(D+1)*(L-D/2)+2*D*W)
            =8192*5*(1*2*(3-0.5)+2)=286720.
[INTERPRETATION] A table with at most 2^20 digit entries implies beta≤2^20. The text says 'lookup table to 20-bit', but does NOT explicitly give beta=2^20 nor complete digit lengths for *every* range proof. We use beta≤2^20 as the natural bound, not a verified exact digit-base/packing statement. Real 49-bit primes p_i have 2^48≤p_i<2^49, so p_min≥2^48. The floor of 20-bit table cardinality may be smaller; using 2^20 is safely conservative under the above interpretation.

## One conservative full-batch computation [DERIVED]
To avoid silently using a single hand-picked coefficient (or inventing author padding), upper-bound one digit-oracle input length by the source-reported Πrange max 286720. Use a mathematical next-power-of-two envelope M_pad=2^ceil(log2(286720))=524288=2^19; this is NOT a claim about the implementation's actual MLE layout.
 T_reported=286720*(2^20−1)=300647424000.
 T_pad=524288*(2^20−1)=549755289600<2^39.
 2^48=281474976710656. Therefore T_pad<2^48≤p_min.
 Conservative margin is 2^48/T_pad=512.0004882817. Thus the I88 sufficient condition T<p_min SURVIVES this published Medium-circuit size even using a pessimistic padded length. For a padded M=2^19 and 49-bit p_i, even power-of-two beta=2^29 would satisfy T<p_min. beta=2^30 does not have a guaranteed pass based solely on the bit-length lower bound.
This is a parameter *feasibility* check. It does NOT certify correct circuit/oracle wiring, the original paper's CRT digit bounds, 128-bit knowledge soundness, optimal runtime, or privacy.

## IMPORTANT unresolved formal/experimental mismatch
§4.3 pp20–21 presents c=2^gamma and beta=B^(1/c), using binary gamma-bit digit index. Section 6.3 p29 nevertheless reports c=5. The exact padding/generalization to c=5, the meaning of '20-bit lookup table' as per-oracle beta, and the difference between Table2 maximum input size and actual size of the one same-h digit oracle are NOT specified sufficiently in the examined text. DO NOT claim that c=5 literally obeys c=2^gamma or that authors actually pad to 2^19, and do not call this a soundness flaw without inspecting code or appendices. The conservative numeric test is robust for any beta≤2^20 and any single h digit array length≤286720, including padded to 524288.
[PRIOR-ART/SOURCE LIMIT] The reference code is a PoC library for CKKS and sumcheck/encoding benchmarks, not a confirmed complete deployed SNARK. The original ePrint official latest PDF hash remains VERSION_UNVERIFIED.

## Reproducible exact script
/mnt/data/iteration90_vfhe_no_wrap_parameter_audit.py SHA256 f49e51d2a9854cae2e58b32e6fd1fb54fd069a800148a756a4c216e071a01f5a
/mnt/data/iteration90_vfhe_no_wrap_parameter_audit_results.json SHA256 166527a9d3a2055068a05f718011f1e7f3ddd3cc20b2902491c3283410cd1904
Integer assertions PASS. No FHE implementation, PIOP transcript or cryptographic security experiment.

## End of Iteration 90
STATUS: **PASS (qualified)** published medium-circuit no-wrap feasibility assuming 20-bit lookup means beta≤2^20; actual c=5 digit packing and exact per-oracle beta UNVERIFIED.
RESULT: Source M286720, conservative envelope 524288, beta≤2^20 ⇒ T≤549755289600 versus p_min≥281474976710656; >512× gap. The stronger I88 no-wrap assumption is not automatically a nonstarter at one published workload, yet does not follow from the general original theorem.
NEXT_ACTION (I91): One cost falsification: for the same medium-circuit case, compare minimum number of ADDITIONAL original-h PCS evaluations and sumcheck rounds needed for 128-bit outer-product masks (309 repetitions) or full Bernoulli masks (128 repetitions) against baseline Πrange 25D original oracle queries, using source §4.3 p24, §5/App F, and I87 exact probability. Check whether any reuse/batching changes naive counts. Do not build complete repair, invent timings, or contact authors.
STATE_UPDATE: YES — materially verified a published parameter regime where the no-wrap branch survives; next bottleneck is overhead not arithmetic feasibility.
