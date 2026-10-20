# BOOT-B084 — Joint 2+2 selector-key bridge versus existing multi-bit PBS

- Date: 2026-10-20
- Research track: BOOT only; SHIP remains paused
- Previous: BOOT-B083, offline dynamic-group compression fails a restricted rank gate
- **STATUS:** `PASS_MK_GGSW_2PLUS2_ALGEBRA / FAIL_NOISE_GATE_TOY / FAIL_STANDALONE_NOVELTY / FAIL_NATIVE_DAI_INTERFACE_VALIDATION`
- **NEXT:** B085 (not started): pivot from grouped-key unrolling to B072's nontrivial *secure, low-noise fused external-product* interface; begin with a single exact mechanism and cheap security/noise falsifier. Abort if it amounts to reusing secret-dependent public masks or republishing a standard GGSW/GSW multiplication.

## 1. One primary hypothesis

A fixed 2+2 group of binary selector bits can be represented with only nine extra offline mixed-secret keys, permitting **one** joint online NTRU-to-MK-RLWE conversion rather than the **two** source Dai HProd conversions, *while improving both online cost and noise* and being meaningfully different from already-known multi-bit PBS.

We tested its strongest easily type-correct instantiation: convert to a unified MK-GGSW selector under the **collective MK-RLWE key**, then use one MK-GGSW external product. This makes the new key format explicit rather than silently feeding GLWE into Dai's vector-NTRU HProd.

## 2. Original source and prior-art evidence

- [FACT] Dai, Xiang, Deng, Zhang, *Accelerating MKFHE bootstrapping via parallel-friendly NTRU-based blind rotation*, *Cybersecurity* 9:136 (2026), https://doi.org/10.1186/s42400-026-00563-w . 'External product for hybrid ciphertext' explicitly consists of a vector NTRU `ct_i` operation on **every** component of an MK-RLWE ciphertext, followed by `HProd` using per-party UniEnc. Thus plain MK-GGSW external product is not a drop-in implementation of their source interface. Source security section explicitly uses NTRU, RLWE and circularity assumptions.
- [FACT] TFHE-rs **actual published Rust implementation** [source at docs.rs](https://docs.rs/tfhe/latest/src/tfhe/core_crypto/algorithms/lwe_multi_bit_bootstrap_key_generation.rs.html) `encrypt_lwe_multi_bit_ggsw_group`, approximately lines 13-78: grouping-factor-g uses **2^g GGSWs, one per possible bit combination**, with one-hot products; lines 35-38 assert count = `1 << input_key_elements.len()`. Code line 504 onward (`combine_key_bits`) builds products with complemented bits. [Zama parallel PBS docs](https://docs.zama.org/tfhe-rs/configuration/parallelized-pbs) states larger keys enable fewer sequential group operations. Thus generic joint 4-bit selector unrolling is clearly known in the single-key setting. We do NOT claim this library is an MK-NTRU implementation.
- [FACT] FINALLY, ePrint https://eprint.iacr.org/2024/1505, Sec4.4, preprocesses fixed product-of-secrets key-switching data, NOT Dai's online mask-dependent group rotations. Established in B083.

## 3. Boolean algebra and exact prior-art equivalence

Let `s=(s0,s1,s2,s3)∈{0,1}^4`, public `a=(a0,a1,a2,a3)`, ring `R_q=Z_q[X]/(X^N+1)` and `alpha_i=X^(a_i)-1`. Then

```
X^(sum_i a_i*s_i) = prod_i (1+alpha_i*s_i)
                  = 1 + sum_(empty != S subset [4]) (prod_(i in S) alpha_i) (prod_(i in S) s_i).
```

Local subsets on first two bits: 3; local subsets on last two bits: 3; mixed subsets `(2^2−1)^2=9`; union 15. But the alternative **one-hot basis** `delta_v(s)=prod_(i:v_i=1)s_i * prod_(i:v_i=0)(1−s_i)` for 16 bitstrings v satisfies

```
X^(sum_i a_i*s_i) = sum_(v in {0,1}^4) X^(sum_i a_i*v_i)*delta_v(s).
```

The relations `prod_(i in S) s_i = sum_(v: v contains S) delta_v(s)` and inclusion-exclusion give an invertible change of basis over **any commutative coefficient ring**, no `1/2` requirement. Hence 15 nonempty subset keys + public constant and 16 one-hot keys span exactly the same function space. This proves there is no standalone new selector primitive in the subset-basis formulation. It does NOT prove ciphertext distributions or noise are equal under the change of basis.

[TEST] `verify_b084_priorart.py`: for q∈{257,65536}, all 16 secret assignments and all 81 public mask vectors a∈{0,1,2}^4, **1296/1296** exact polynomial equality each modulus between target monomial, 15-subset expansion and 16-onehot expansion. For each q also 256/256 Boolean basis reconstruction checks. Both odd and torus modular rings PASSED. These are transparent plaintext algebra tests, not security estimates.

## 4. Full-mask toy MK-GGSW correctness

[TEST] `verify_b084.py`, seed 840084, N8, q=2^24, B256,d3 exact gadget (B^d=q), k=2 with independently sampled ternary polynomial output keys z_1,z_2. A MK-RLWE ciphertext is (b,a_1,a_2), phase b−a_1z_1−a_2z_2. Each GGSW of a secret subset value is constructed as fresh uniformly-masked MK-RLWE encryptions of zero for each of `(k+1)*d=9` component/digit rows, adding `B^j * subset_value` to the row's *selected ciphertext component*. After decryption, this row contains `B^j*value` times the corresponding linear coefficient in the MK-RLWE decryption functional plus independent error. This is a dealer-level toy generation; it does NOT establish noninteractive MK key-generation availability or security.

For a public input mask, synthesize GGSW of the two separate 2-bit group monomials with 3 subset tables each; or synthesize one joint 4-bit monomial selector with all 15 subset tables. Apply 2 external products to independently random masked initial MK-RLWE ciphertext (separate) or 1 external product (joint); both should decrypt to `X^(sum a_i s_i)*message` plus the exactly predicted gadget error.

96/96 trials for each path passed **exact coefficient-wise noise recurrences** with independent full masks. Joint-vs-two-stage output noise, with shared initial sample and subset keys (different circuit):

| Metric | 2 group operations | 1 joint operation |
|---|---:|---:|
| RMS error median | 3130.96 | 7196.98 |
| Paired ratio median joint/two | — | **2.274x** |
| Joint beats two | — | **4/96** |
| Largest absolute error observed | 14082 | 58368 |

Not actual DFR: q=2^24,N8,k2 insecure; subGaussian or Gaussian noise modeling not done. Algebraic observations don't establish a source-native Dai MKFHE implementation.

## 5. Same-toy-operation frontier

With k2,d3 each MK-GGSW holds `(k+1)^2*d=27` ciphertext-component polynomials and one MK external product uses `27` ring polynomial multiplies (one for each gadget source row × output component).

| Toy quantity | Independent 2+2 groups | Joint 4-bit group |
|---|---:|---:|
| Subset-GGSW key entries | 6 | **15** |
| GGSW extprod calls | 2 | 1 |
| Extprod ring polynomial multiplies | 54 | 27 |
| Public polynomial multiplications to form input-dependent GGSW selector | 162 | **405** |

The joint construction saves 27 extprod ring multiplications but adds **243 input-dependent public polynomial multiplications**, and increases persistent subset GGSW material 2.5x compared to six local subset encryptions. These operations have different constant factors: public factors are sparse sums of monomials while extprod factors can be dense gadget polys, so one cannot assert joint is slower **in milliseconds** without kernel benchmarks. It is NOT a drop-in reduction of source Dai's `kl` NTRU-ExtProd+UniEnc HProd count: it changes representation, key transcript and security assumptions.

## 6. Security and novelty gates

- The table publishes encryptions of **products of input secret key bits** under a collective MK-RLWE evaluation secret (and its associated zero encryptions). Security under this enlarged transcript, including KDM/circular/related-key exposure and **noninteractive per-party generation** under exactly Dai's setup, remains UNPROVED. A hypothetical public MK encryption procedure would require a full specification and transcript indistinguishability proof, not mere dealer generation.
- A source NTRU GIP output is a vector NTRU ciphertext under `f_i`, whereas one MK-GGSW extprod expects a selector under **the multi-key RLWE key**. Saying 'one GGSW extprod instead of two Dai HProd' is a type error unless the novel conversion is separately defined and costed. B084 has tested a different, properly typed toy.
- TFHE-rs one-hot group BSK is direct prior art for function space and key-count structure; the two representations differ only by invertible Boolean basis. Nothing in B084 establishes an MK-specific novel technique, lower noise, a smaller key or a faster online implementation.
- The two-stage *toy* is not Dai source baseline. Its 2 operations should never be presented as measured source HProd counts or security-equivalent benchmark.

## 7. Decision

**STATUS `PASS_TOY_MK_GGSW / FAIL_NOISE_GATE / FAIL_STANDALONE_PRIORART / UNCLEAR_SOURCE_TYPED_SECURE_CONVERSION`.**

The narrow '9 cross subset keys saves one HProd with less noise and new primitive' claim is **NOT established and should be killed as a publication candidate**. The broad possibility of fundamentally redesigning NTRU→MK-RLWE conversion remains open, but repeating multi-bit group unrolling will not answer it.

**NEXT_TEST B085 NOT STARTED:** pivot to B072's secure fused external-product issue and inspect exactly **one** possible way to decouple the secret-dependent error-cancellation information from public mask correlations. Start with mathematical transcript indistinguishability / noiseless correctness gate, then noise and source security. Reject if no independence of published masks or if 'noise-free' samples constrain a secret-dependent kernel. Or, if a much stronger independent primitive is found through literature, document its true interface before moving tracks; no SHIP changes.

**STATE_UPDATE NO:** prior large `findings/boot-STATE.md` was listed but could not be safely read by connected Notes action. Only new append-only BOOT finding; other tracks untouched.