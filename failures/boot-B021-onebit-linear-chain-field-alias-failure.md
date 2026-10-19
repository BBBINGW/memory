# BOOT-B021 failure archive: one parity bit insufficient for fused q64 two-addition proof

TRACK_ID: BOOT
ITERATION: B021
DATE: 2026-10-19
STATUS: FAIL_B018_ONE_BIT_EXTENSION / FAIL_HASTEBOOTS_RELATIVE_COST_CLAIM

The B018 Goldilocks + one-parity local gadget lemma is true only with its specific tight error bound (<2p). Extending it naively to a q=2^64 two-addition chain is unsound.

Let p=q−2^32+1 and x,a,b,y canonical q-words, aggregate carry k∈{0,1,2}, e=x+a+b−y−kq. Correct computation requires integer e=0. A proof of e=0(modp) and e=0(mod2) fails: choose x=a=p, b=y=k=0. Then e=2p≠0 but both tests pass, and actual output y=2p modq ≠0. This is not a mixed-witness attack; all values are canonical and consistent.

Exact integer repair: e=0(modp), e=0(mod4), SAME canonically committed integer values/ranges. Since |e|<3q<4p and p odd, e must equal0. General m linear additions require 2^t p>(m+1)q and e mod2^t=0, with t logarithmic in m. Witnesses for low bits/quotient must be soundly bound, not automatically free.

Exhaustive q16,p13,m2 test: 196608 bounded tuples; 4096 actual integer-valid witnesses; 11036 extra field-only false; 3336 extra field+parity false; zero extra field+mod4 false. Real q64 random honest 200000/200000 passes; q64 forged e2p rejected by mod4.

Critical baseline correction: HasteBoots (f7ed/HasteBoots, vfhe/src/bfhe/parameters.rs) runs ciphertext modulus GOLDILOCKS p, not source TFHE q64. Its packed accumulator trace (trace/src/acc_trace.rs) already shares rows through indexed lookup and permutation proof (snarks/src/fhe_op/acc_iteration.rs) with batch sumcheck in snarks/src/fhe_op/blind_rotation.rs. Some linear intermediate fields explicitly can be omitted. Thus there is no source ground for claiming eliminated q64 carry/range overhead relative to native HasteBoots. The elementary CRT/checksum lemma also lacks publishable novelty by itself; complete adaptation to q64 would need full verification protocol, privacy/security/DFR, and matched benchmark.

Technical proof and source references: findings/boot-B021-linear-region-lowbit-integer-certificate.md.

DECISION: Archive the ONE-BIT aggregated certificate and its supposed HasteBoots speedup. Do not archive the mathematically correct B018 one-bit SPECIFIC gadget lemma or B021 two-bit generalization as false. Stop parametric minor repairs without a new substantive bottleneck.

NEXT_TEST B022: Pivot away from q64-vs-Goldilocks arithmetic. Seek an unaddressed specific source-grounded BOOT dataflow/control/memory/security bottleneck after BatchBoot 2026 and identify one smallest original test; other FHE/cryptography work may inspire a structural repair. Remain strictly BOOT-owned.