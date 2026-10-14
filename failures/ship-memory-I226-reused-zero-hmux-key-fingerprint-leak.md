# SHIP I226 — Identical reuse of zero HMux evaluation keys leaks one-hot support digits



Date: 2026-10-14 Asia/Tokyo. Independent SHIP subtarget HMux evaluation-key memory. Source evidence: third-party Poulpy, NOT authors' HEaaN, pinned `poulpy-fhe/poulpy@250d4392656cd313f92ca66d96d8865702d39ddf`. Read-before-write: START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, current concurrent global STATE.md vFHE V19 (READ ONLY), findings/ship-memory-STATE.md I225 SHA f889e6a42781d5f364f792d78a2a598ea7415c71, findings/OPEN_RESEARCH_BRANCHES.md and I204/I205/I208/I209/I210 archives. The idea below is a **new hypothetical compression candidate**; NOT behavior in original Poulpy or a SHIP-paper bug.



## ONE primary falsifiable hypothesis / one cheap decisive test



**H226:** For each fixed public (mux digit stage, choice d), reuse **one byte-identical valid GGLWE ciphertext of the zero rank2 input secret** for ALL support slots with beta=0, but retain independent freshly randomized GGLWE encryption for each slot where beta=1. Because all messages remain encrypted, the public key bundle's ciphertext equality pattern does not disclose useful information about the hidden one-hot beta choices or sparse bottom secret.



**Falsifier:** Give adversary access only to the public serialized/NTT-prepared keys and their public stage/choice labels. Compare exact bytes per fixed (stage,d) across the 32 slots. Use the source's one-hot digit constraints, recover repeated zero-key equality classes, and calculate a universal upper bound on remaining signed windowed sparse secret candidates (no secret decryption required). An upper bound <=2^100 for h32 falsifies 'no useful disclosure' relative to original log2 support 320.09.



## Exact source facts



- `poulpy-ckks/src/layouts/ship/keyset.rs` blob `8be6ab92846168330100efeabe9fa19dbd9720e4`, `hmux_rot_key_encrypt_sk` creates input secret `(beta*s,beta)` under output secret `t_g=sigma_(g^-1)(s)` with g determined by PUBLIC rotation `d*weight`, independent of support slot. `generate` uses `digit=(u/weight)%b` and `beta=(d==digit)`, i.e. **exactly one beta=1 per stage and support slot**. Original source ALWAYS calls randomized encrypt-sk separately for each candidate/key, even when beta=0; **no byte-identical reuse is in original source**. The only candidate being refuted is hypothetical reuse.

- `poulpy-ckks/src/layouts/ship/secret.rs`: support j_i=(i*N/h + delta_i) mod N, -w<=delta_i<=w, independent sign ±; offset u_i=(j_i-i*N/h+w) mod N lies [0,2w].

- `poulpy-ckks/src/layouts/ship/plan.rs`: theta4, window256 => u_i in [0,512] and q_i=floor(u_i/4) in [0,128]; mixed-radix stages [4,4,4,3] encode q. For each fixed q, at most FOUR possible u, and sign independently ±.

- Baseline I203 480 HMux rank2 GGLWE keys. Hypothetical identical-zero-sharing retains 32*4=128 independently encrypted nonzero β=1 keys plus 15 shared zero templates (4+4+4+3)=**143 keys**, a **70.2083% object-count reduction** and (conditional IFMA same-shape) prepared HMux 42.1875GiB → 143*90MiB=12.568359375GiB; complete non-HMux prepared payload 2.34765625GiB, so all-named prepared 44.53515625→14.916015625GiB. THESE ARE TEMPTING BUT INSECURE RESOURCE COUNTS, NOT A SAFE OPTIMIZATION.



## Public-fingerprint leakage proof [DERIVATION]



Assume original β=1 ciphertexts in each slot are fresh and their serialized bytes distinct from the fixed β=0 template and one another (overwhelmingly likely for properly randomized large ciphertexts). For every fixed (stage,d), any ciphertext occurring at least twice must be its repeatedly reused **zero template**. Call those positions CERTIFIED ZERO. Under h=32 one-hot choices for stage base b∈{3,4}, at most one candidate d can have its zero-template appear 0 or 1 times: if two candidates each have ≤1 zero, they would each have ≥31 ones, totaling ≥62 selected ones across only 32 support slots, contradiction. Therefore *at most one candidate d has zero assignments not detectable via equality*. For the other choices zero positions are certified. Consequently each slot is either (a) uniquely decoded as its only noncertified candidate or (b) has at most two uncertified candidates. Case (b) happens for at most **ONE support slot per digit stage**: a candidate with a single zero and 31 ones is potentially ambiguous with that slot's actually selected other choice. Thus **at most 2 globally consistent digit-assignment patterns per stage**, and over four stages at most 2^4=16 full high-digit patterns, using ONLY public byte identity + one-hot structure. The bound holds in worst-case 31:1 skew even though full digit recovery is typical; do NOT falsely assert all bits always fully recovered.



Given any full high-digit assignment q_i, each u_i∈{4q_i,4q_i+1,4q_i+2,4q_i+3}∩[0,512] has ≤4 possibilities. Each chosen sparse support location gives 2 independent sign possibilities. Hence legal signed sparse secret candidate count at most (4*2)^32 * 2^4 = **2^100** (further duplicate-support restrictions only reduce it). The I217 original support set had log2 size ~320.09. This candidate-list collapse is **severe information leakage**, not an observed practical 100-bit security break; demonstrating an actual algorithm recovering the sparse key under realistic observability/noise and matching IND-CPA model needs additional work. In I219 PK-enabled interface, public dense encryption plus D2S can generate known-message sparse ciphertexts, potentially aiding verification; not modeled or benchmarked here.



## Executed reproducible test



Deterministic source-shaped Python test: 50,000 independent h32 random offset vectors in [0,512], mixed radix [4,4,4,3], one shared ZERO token per stage/d and distinct ONE tokens per slot. For every group, mark repeated token as zero; assert at most one ambiguous support slot with at most two candidates; assert total product patterns <=16. **PASS 50,000/50,000**, no violation. Also explicit adversarial patterns per group: all select0, balanced, 30:1:1, **31:1**: the latter leaves **one ambiguous slot** exactly, refuting an overclaim of guaranteed complete digit recovery. No actual GLWE encryption/NTT/Rust execution.



Artifacts created in local container and hashes:

- `/mnt/data/ship_i226_reused_zero_key_fingerprint_gate.py` SHA256 `fc3d6988b3fe047b574dacceae55e5199dad29b0f7888c702ed5315e1e13c8dc`

- `/mnt/data/ship_i226_reused_zero_key_fingerprint_results.json` SHA256 `10cd3250816af42ed2ddeed8955cc70114a18ba854db99d5c565d21e50c2c900`



## End of iteration



**STATUS: FAIL H226** confidentiality of beta under *byte-identical zero GGLWE key reuse*. **PASS exact source one-hot/offset audit and rigorous candidate-space bound (conditional on hypothetical scheme)**. **Not an attack on source original SHIP/Poulpy**, which uses separate randomized encryption per key, and not a security-bit calculation for an actual modified deployment. No real performance/correctness/security parameter evidence; NOVELTY NOT VERIFIED.

**RESULT:** The apparently cheap alternative to I207 would cut original 480 HMux keys to 143 but publicly reveal enough one-hot digits that the h32 windowed sparse bottom secret has at most 2^100 candidates, rather than ~2^320. The zero selector's encryption does not prevent fingerprint leakage if ciphertext randomness is reused. Do NOT recommend this dedup compression for confidential SHIP support.

**NEXT_ACTION:** Archive this precise unsafe dedup repair as negative and do not attempt variants differing only in hash labels, memory copies or seeded deterministic public zero re-encryption. Any secure key material dedup needs *fresh indistinguishable ciphertext distribution per beta* or a credible new nontrivial mechanism avoiding equality side channels, and must address I205's necessary hidden-bit×ciphertext bilinearity, I210 joint key security, and I216 security-matched parameters. PI HUMAN_REVIEW before another major SHIP hypothesis; if no such mechanism is identified, PARK/redirect to independent promising line by PI decision. Do not modify global STATE.

**STATE_UPDATE: YES** independent SHIP archive + checkpoint only.