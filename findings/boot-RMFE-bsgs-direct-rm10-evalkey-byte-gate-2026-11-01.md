# BOOT RMFE BSGS+10 Direct-RM10 Evaluation-Key Byte Gate

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 4/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

Read-before-write authority:
`BBBINGW/memory main@df3dd029825d2193132db15301f062cfe04743a4`.

Durable prerequisites:
- Turn 3 established exact physical-KS counts:
  FULL 70->14, BSGS 100->24, MIN 905->1044;
- adding ten direct RM10 target matrices makes candidate RM10+joint recovery exactly 14 physical KS;
- BSGS Frobenius direct-target count changes 180->190;
- exact added key bytes were unresolved.

One hypothesis only:

> In the pinned HElib representation, does adding the ten direct RM10 matrices to a BSGS Frobenius keyset incur at most a small, target-independent evaluation-key byte overhead, or can matrix size vary materially with the automorphism target and destroy the +10/180 matrix-count intuition?

Falsifier:
show that `GenKeySWmatrix` chooses target-dependent digit count, prime set, stored DCRT dimensions, plaintext space, or serialized payload length large enough that ten RM10 matrices can cost substantially more than ten ordinary BSGS Frobenius matrices.

No native execution, key generation, benchmark, parameter sweep, or R4 rerun occurred.

## Source provenance

Pinned HElib:
`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.

Relevant source:
- `src/keys.cpp:1152-1238` — `SecKey::GenKeySWmatrix`;
- `include/helib/keySwitching.h:53-100` — matrix representation;
- `src/keySwitching.cpp:196-218` — binary serialization;
- `src/DoubleCRT.cpp:1530-1540` — binary DCRT serialization;
- `src/binio.cpp:75-122,180-190` — fixed 64-bit integer / vec-long encoding and variable-length ZZ seed;
- `src/Ctxt.cpp:41-54` — fixed three-long `SKHandle`;
- `src/NumbTh.cpp:343-429` and `src/PAlgebra.cpp:443-512` — ordinary generators span `Z_m^*/<p>`;
- Aung et al. ePrint 2025/350, physical p23 — m=32768, bits=400; the paper does not expose HElib digit decomposition or exact prime counts.

The ePrint mirror is VERSION_UNVERIFIED, SHA256
`922c860a838fd8c9a8a5853489ac8ac7706fc3332e2083075540ad5f422bde82`.

## 1. Target-independent stored matrix geometry

For every call

`GenKeySWmatrix(1, fromXPower, keyID, keyID)`

in one fixed context, HElib does the following independently of `fromXPower`:

1. sets
   [
   n = 	exttt{context.getDigits().size()};
   ]
2. allocates exactly n stored `DoubleCRT` objects in `ksMatrix.b`;
3. every stored DCRT uses exactly
   [
   	exttt{ctxtPrimes} cup 	exttt{specialPrimes};
   ]
4. each DCRT row has exactly (phi(m)) long entries;
5. for bootstrappable BGV and omitted explicit p, every matrix receives the same bootstrapping plaintext-space policy;
6. only the secret-key automorphism `fromKey.automorph(fromXPower)` changes with target.

The pseudorandom bottom row `a` is NOT stored. HElib stores only the top-row vector `b` and a 256-bit PRG seed.

Therefore the dominant stored DCRT payload of every same-context Frobenius automorphism matrix has exactly the same geometry and byte length.

There is no target-dependent decomposition-width or prime-set blowup.

## 2. Binary payload formula

Let:
- (D = |	exttt{context.getDigits()}|);
- (L = |	exttt{ctxtPrimes}cup	exttt{specialPrimes}|);
- (phi=phi(m)=16384).

`DoubleCRT::writeTo` writes the same IndexSet and, for every used prime, one `vec_long` of length (phi). `write_ntl_vec_long` stores an 8-byte header plus (phi) 64-bit entries.

Ignoring the common IndexSet encoding for one moment, every stored DCRT contains at least

[
L(8+8phi)
]

bytes of row data, and all matrices contain exactly D such DCRTs.

More explicitly, using HElib's own binary-layout accounting, one DCRT has fixed context-dependent size

[
S_{m DCRT}
=
8 + L(16+8phi)
]

bytes under this binary format.

A `KeySwitch` serializes:
- two 4-byte eye catchers;
- `SKHandle`: three 64-bit longs = 24 bytes;
- `toKeyID`: 8 bytes;
- `ptxtSpace`: 8 bytes;
- vector-`b` length: 8 bytes;
- D copies of the identical-size DCRT payload;
- PRG seed: 8-byte byte-count plus 1..32 seed bytes for a successfully serializable 256-bit `ZZ`;
- `noiseBound`: fixed 16-byte xdouble.

Hence each same-context Frobenius matrix has

[
oxed{
S_{m KS}=80+D S_{m DCRT}+s
}
]

with only

[
1le sle32
]

bytes of target-independent-random seed-length variation.

Thus two matrices can differ in binary size by at most 31 bytes; all cryptographic DCRT storage is exactly equal-sized.

## 3. The ten RM10 matrices are genuinely new under standard BSGS

For m=32768,p=5:

[
phi(m)=16384,qquad operatorname{ord}_m(5)=8192,
]

so the SIMD quotient

[
Z_m^*/langle5angle
]

has order 2.

HElib `findGenerators` chooses ordinary dimensions in this quotient. Therefore the sole nontrivial ordinary-dimension generator lies outside the Frobenius subgroup (langle5angle), and its order-2 direct 1D matrix cannot equal any Frobenius target (5^e).

Other stock matrices also cannot deduplicate the ten targets:
- power/relinearization matrices have `fromSPower>1`;
- recryption-key switching has different source/target key IDs.

The ten RM10 targets from Turn 3 all lie in (langle5angle) and none belongs to the BSGS direct baby/giant index set.

Therefore, for the standard BSGS Frobenius configuration:

[
oxed{	ext{exactly 10 new KeySwitch objects are added}.}
]

The existing BSGS Frobenius set has exactly:
- 90 babies j=1..90;
- 90 giants j=91,182,...,8190;

for 180 distinct direct Frobenius matrices.

## 4. Exact DCRT-payload overhead

Because all 190 Frobenius matrices have identical stored DCRT geometry,

[
rac{Delta 	ext{Frobenius DCRT payload}}
     {	ext{baseline BSGS Frobenius DCRT payload}}
=
rac{10}{180}
=
oxed{5.555555ldots%}.
]

This ratio is exact for the dominant stored DCRT payload.

It is independent of:
- the unknown digit count D;
- the unknown number of ciphertext/special primes L;
- actual random matrix contents;
- RM10 target exponent.

## 5. Conservative whole-PubKey binary-size upper bound

The only per-matrix binary-size variability is at most 31 PRG-seed bytes.

Even under the impossible smallest geometry D=L=1, one DCRT already contains at least

[
8+16+8cdot16384=131096
]

bytes.

Thus one serializable matrix is at least 131177 bytes and at most the same fixed payload plus 31 extra seed bytes.

Using an adversarial comparison in which all 10 added seeds are maximum-length and all 180 baseline BSGS Frobenius seeds are minimum-length gives

[
rac{10(131208)}{180(131177)}
=
0.0555686845ldots
]

Therefore, without knowing D or L,

[
oxed{
Delta |	ext{serialized PubKey}|
<
5.557%
}
]

relative to a baseline public key that already contains the 180 BSGS Frobenius matrices.

This is conservative because the actual baseline PubKey also contains:
- ordinary 1D matrices;
- relinearization matrices;
- recryption-key material;
- public encryption key;
- context and fixed maps.

Those only enlarge the denominator.

So the actual whole-PubKey percentage increase is strictly smaller than this 5.557% bound.

## 6. What remains unknown

Aung et al. publish `bits=400` and maximum ciphertext bit-width 538--541, but not the exact HElib digit decomposition, ciphertext-prime count, special-prime count, serialized evaluation-key bytes, or RSS.

Therefore this static gate does NOT establish:
- absolute extra MiB;
- RSS increase;
- cache/memory-bandwidth effect;
- key-generation time;
- Aung's exact unpublished key configuration.

Those remain native measurements.

## Verdict

```text
RESULT:
  PASS_STATIC_BSGS_DIRECT_RM10_KEY_BYTE_OVERHEAD_SMALL

DIRECT_RM10_MATRICES_ADDED:
  EXACTLY 10

BASELINE_BSGS_DIRECT_FROBENIUS_MATRICES:
  EXACTLY 180

TARGET_DEPENDENT_DCRT_SIZE_VARIATION:
  NONE

EXACT_FROBENIUS_DCRT_PAYLOAD_INCREASE:
  10/180 = 5.555556%

CONSERVATIVE_WHOLE_SERIALIZED_PUBKEY_INCREASE:
  < 5.557%

ABSOLUTE_EXTRA_MIB:
  UNRESOLVED

RSS_OVERHEAD:
  UNRESOLVED

KEY_GENERATION_TIME:
  UNRESOLVED

AUNG_EXACT_KEYSET:
  UNRESOLVED

CANDIDATE:
  SURVIVES / BSGS+10 KEY-SIZE RISK STATICALLY BOUNDED

NATIVE_RECOVERY_BENCHMARK:
  STILL HIGH VALUE

WHOLE_PIPELINE_CAPACITY:
  UNRESOLVED

PUBLISHABLE_NOVELTY:
  NOT ESTABLISHED

RESEARCH_FRONTIER_EXHAUSTED:
  false
```

## Scientific disposition

The Turn-3 low-regret BSGS+10 augmentation is no longer merely a matrix-count heuristic.

Its dominant Frobenius-key storage cost is exactly +5.56%, and its total serialized public-key overhead is statically bounded below +5.557%, independent of the unpublished HElib digit/prime decomposition.

This removes a potential catastrophic key-size blocker for the next bounded recovery benchmark, but does not replace native measurement of absolute bytes/RSS.

The next latency experiment should therefore compare stock BSGS against BSGS+10 with:
- exact public/evaluation-key bytes;
- RSS;
- direct-hop audit;
- one reconstruction + RM10 + chained joint-recovery latency;
- same source-faithful post-raw input state.
