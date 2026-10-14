# SHIP I223 — Reuse one HMux prepared group across a microbatch of bootstrap requests

Date 2026-10-14 Asia/Tokyo. Independent SHIP I223. Read START_RESEARCH_SESSION.md, RESEARCH_PHILOSOPHY.md, AGENT.md, global STATE.md (vFHE V17 READ ONLY), independent findings/ship-memory-STATE.md (still I221), and I222 source finding. Audited independent third-party Poulpy at commit 250d4392656cd313f92ca66d96d8865702d39ddf, NOT original author HEaaN. Do not edit global STATE or upstream code.

## One primary hypothesis and one decisive test

H223: For B real SHIP bootstraps that share EXACTLY the same dense secret and evaluation keyset, interchange the outer request loop with source's slot/group loops so each original HMux group is read/prepared ONCE and used over B request-local accumulators before release, without changing per-request operation order or introducing new FHE multiplications.

Test: Inspect real source loops and key use (keyset.rs ShipKeySet::prepare; bootstrap.rs ship_bootstrap_roots; mux.rs ship_mux_rotate), then compute key-read amortization versus required resident per-request ciphertext leaves. Falsify if prepared key needed beyond group or requests share secret-dependent intermediates that cannot be kept independent.

## Exact pinned source observations [FACT]

- keyset.rs blob 8be6ab92846168330100efeabe9fa19dbd9720e4: original ShipKeySet::prepare eagerly prepares all 480 rank2 HMux keys; GLWE switching key can be prepared individually.

- bootstrap.rs blob edbec7d8ad60493d53aa5c11c842da1f30cff542 lines 151–220: creates trivial leaf0 then loops support slot, within slot half, then mux digit group, invoking ship_mux_rotate for one request-local masked accumulator; pushes finished leaf and later builds product tree using tensor key. No dependency between distinct ciphertext requests in this source schedule.

- mux.rs: ship_mux_rotate receives immutable prepared group and mutable request-local ct; computes VMPs and returns ct, preserving no pointer to group. Rotation plans likewise public and can be derived from raw-key gal_el metadata. Current concrete API needs refactor for groupwise prepared groups.

- I222 source-compatible baseline for IFMA N16384,h32,theta4,window256,radix52,k468,group sizes [4,4,4,3]: original HMux raw 480*45MiB=21.09375GiB; prepared 480*90MiB=42.1875GiB; other prepared keys 2.34765625GiB; disk-backed current group raw180MiB + prepared360MiB gives 2.875GiB named resident keys, EXCLUDING all live ciphertexts/scratch.

## Conditional loop interchange [DERIVATION]

For each batch of B inputs under SAME key bundle, create separate sparse bottom inputs and per-request pi encodings. For slot i: create B request-local masked acc. For mux group j: read one raw group, prepare 3 or 4 original keys, call existing ship_mux_rotate sequentially B times using same immutable prepared keys and separate acc, discard prepared group. After groups, save B leaves for slot i; after all 32 slots build B separate product trees. Each request sees identical order of operations and inputs as its original single bootstrap. Requires batching latency/queueing and enough per-request input/encoding/acc storage. Not compiled; source-shaped schedule only.

One batch must scan raw keys just once: 21.09375GiB key bytes, requiring 480 raw->prepared conversions total per B requests, compared to B*480 if each request runs separate streamed bootstrap. The actual 480*B HMux VMP applications persist. Amortized raw reads/request 21.09375/B GiB. Assumes cold disk and no cross-batch caching; effective disk reads may differ with OS cache.

## One source-shaped named payload bound [DERIVATION]

At k468, rank1 GLWE with N16384, radix52 has 2 polynomials * 9 limbs * N * 8 bytes=2,359,296 bytes=2.25MiB per ciphertext. For real SHIP each input creates 33 leaves; a conservative raw leaf ciphertext payload account is 33*2.25MiB=74.25MiB/request. This ignores smaller ciphertexts after product-tree level reduction and excludes separate current accumulators.

Key payload 2.875GiB plus resident leaf payload (NOT total peak RAM):

- B1: 2.947509765625GiB; raw read amort 21.09375GiB/request

- B8: 3.455078125GiB; raw read amort 2.63671875GiB/request

- B32: 5.1953125GiB; raw read amort 0.6591796875GiB/request

- B64: 7.515625GiB; raw read amort 0.32958984375GiB/request

- B128: 12.15625GiB; raw read amort 0.164794921875GiB/request.

Not accounted: B pending accumulators (up to 2.25MiB each if separate), B coefficient encoding bundles and q52 inputs, FFT/NTT scratch, runtime tensor product intermediates, threaded scratch, allocator overhead, host/device copies, compression and serialisation, I/O queue depth. Hence neither 2.875GiB nor table rows are asserted measured RSS or safe peak bounds. Complex SHIP also has two halves and would require explicit two-half scheduling.

## End

STATUS: PASS source-schedule feasibility for same-key real-CKKS bootstrap microbatch, named payload arithmetic and per-request read amortisation; UNCLEAR code integration, performance, RSS, true security, novelty. Reuse of immutable eval keys across ciphertexts is conventional and is NOT an algorithmic/key-size FHE advance.

RESULT: Group-major schedule can read/prepare 480 original HMux keys ONCE per batch B and execute B*480 unchanged VMPs. B32 payload keys+leaves 5.195GiB, disk raw read/request 0.659GiB, excluding substantial unknown buffers. No new CT×CT and no changed eval-key distribution; prior security concerns remain.

NEXT_ACTION: Real pinned IFMA Rust end-to-end microbatch benchmark (B1,8,32) against eager execution on same keyset: per-query correctness, key preparation time, disk I/O, peak RSS, throughput and latency under stated storage cache. If compiler/runner unavailable, PARK as ordinary systems candidate; do not claim publishable novelty or 128-bit security.

STATE_UPDATE: YES independent SHIP checkpoint only; global vFHE state untouched.