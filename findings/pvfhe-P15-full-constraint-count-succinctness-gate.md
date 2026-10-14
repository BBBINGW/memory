# PVFHE-P15 — Source-sized constraint budget versus duplicated witness / matrix preprocessing

**2026-10-15 Asia/Tokyo. P15 COMPLETED, P16 NOT STARTED.**
**STATUS:** PASS source-compatible sparse Ring-R1CS correction and conditional asymptotic bounds; FAIL inferring total preprocessor/prover overhead from sparse row increase; UNCLEAR actual whole-gate compiler, concrete matrix padding/PCS implementation and classical ROM/QROM security. No claimed original-paper attack or measured runtime.

## Read before write and original source

Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, separate global STATE.md SHA 87346c423fb22f4941029a242797357a5c37179e (parallel independent vFHE V32), P14 findings/pvfhe-P14-augmented-matrix-lde-arity-gate.md SHA fc0613aa8a890dbd39b904207172f73d92b7374b, P13 SHA 7286590014e7480cb8a0559cd36e1084aecc8de1 and P03 SHA e0d6bd682b1dea5f1a9b15a5276a2220bf57261b. P15 target did not exist. No prior files or concurrent states edited.

Primary Huang–Li–Mao–Zhang, Fully Homomorphic Encryption with Efficient Public Verification, ePrint 2024/1764. Original full Research MCP mirror 29 physical pp PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089, VERSION_UNVERIFIED. Read pp15–17 source gadget formulae, pp21–22 Theorem5.7, p26 AppendixB, p27 AppendixC.3 and pp28–29 AppendixD. Public web PDF located; screenshot attempts failed cache miss. Respect physical formula extraction warnings. §4.1 says simplified N=q/2, yet AppendixB uses actual N=2048 and q=n=1024 (four times q/2), so P15 counts actual AppendixB N, not 512.

## ONE hypothesis / ONE source-counted falsifier

**[HYPOTHESIS P15]** P13/P14’s repaired scalar/canonical BitDecomp constraints can be compiled across ALL BitDecomp uses with source Lemma4.4 <=2 nonzeros in each A/B/C row, O(old m) new rows/wires, preserving published Theorem5.7 asymptotic verifier/proof complexity. Moreover, the small row increase alone might imply a comparably small total prover/preprocessing cost.

**[FALSIFIER]** Explicit source-gadget operation ledger for real AppendixB parameters, at most TWO per-matrix row sparse canonical comparator plus Y=M*W, source-Q boundary test, then independently audit source AppendixD public-matrix commitment m^2 size under equal-width Y duplication, and any power-of-two padding cliffs. If m can double even when row growth is small, reject the concrete-cost inference.

## Source-derived complete BitDecomp-site count [FACT/DERIVATION]

At Q=2^53+5, ell=53, ellprime=43 for source near-power-two modulus switch, N=2048, n=q=1024:
  NBitDecomp=3ell+4=163.
  NIndex=4.
  NXPow=NBitDecomp+5(ell+1)+1=434.
  NRounding=NBitDecomp+3(ell-ellprime+1)=196.
  NCoeff=N*NBitDecomp+2N=337920.

Per single EvalGate, source AppendixC.3 gives KeySwitch N=2048 BD uses; XPow twice per n=1024 accumulator updates =2048 uses; n+1=1025 roundings =1025 uses; two Coeff extractions, each N=2048 BDs =4096 uses. Total K=9217 BD instances. This counts all four source paths, avoiding omission of coefficient-extraction scalarity; some may later be proven public/anchored and optimized away.

Source NONRING row ledger with 53 KeySwitch Index digits:
  KeySwitch BitDecomp 333824
  KeySwitch Index 434176
  XPow 888832
  Rounding 200900
  Coeff 675840
  TOTAL R0=2533572.
If every key switching index uses 54 digits rather than source notation N*logQ interpreted as ell=53, R0=2541764; 8192-row ambiguity noted. Excludes other original FHE ring operation constraints and unknown actual padding/witness count.

## Corrected exact source-sparse rank-one comparator [DERIVED + TESTED]

Earlier general R1CS 4-row comparator uses one 3-term linear expression and does NOT retain the source's <=2 nonzero entries PER MATRIX PER ROW. For maximal source alignment use FIVE R1CS comparator rows plus ONE Y-copy link. Original BitDecomp computes prefix ring-valued sums acc52=sum_{j<=52}2^j*x_j and acc2=sum_{j<=2}2^j*x_j. Set h=x53, and fresh helpers k,u,b:

  1. h*(acc52-acc2)=0
  2. (1-x0)*x1=k
  3. (x0+k)*1=u
  4. h*x2=b
  5. b*u=0
  6. Y_i*1=M_i*y_i    (public fixed M_i in {0,1})

Append a single zero anchor row. Each row's A/B/C contains at most two source variables. For 0/1 digits this is equivalent to bit integer sum S<Q=2^53+5; in the actual reducible ring the check is factorwise and does NOT independently enforce scalar bitness. P04/P12's separate sigma-invariance condition on reconstructed values is ESSENTIAL. A 53-bit-only decomposition already has S<Q, so this six-row allowance is conservative.

New rows <=6*K+1=**55,303**, or **2.1828%** of R0=2,533,572 (2.1758% for 54 Index digits). New auxiliary/compressed-Y witness positions <=4*K+1=**36,869** before alignment/padding. Source exact arithmetic script validates the six rank-one rows and <=2 terms per matrix per row for 20 original-Q boundary/mask cases; invalid integer encodings S=Q, Q+1 and 2^54−1 are rejected.

## Decisive honest accounting of source public-matrix preprocessing [DERIVED]

Theorem5.7 source already states preprocessing and prover O((n_sparse + m^2)*poly(lambda)), verifier O(log(m)*poly(lambda)), proof O(log(m)^2*poly(lambda)); m=full padded square Ring-R1CS dimension, NOT LWE n=1024. Additional source-compatible row/wire counts are O(old m), so m_new=Theta(old m): ASYMPTOTIC succinctness and quadratic prover/preprocessing remain, conditioned on unfinished PCS/FS security.

But P13/P14's convenient same-size masked subvector builds old full vector (private W length L, public P length L, m_old=2L) into new private W_aug=W||Y with Y padded to L and padded public P_aug=P||0^L: m_new=4L=**2*m_old** BEFORE any new auxiliary variables. A dense public A/B/C matrix LDE has nominal m_new^2 = **4*m_old^2** coordinates. If the new canonical auxiliaries exceed remaining W padding and force a private L->2L pad, then m_new may reach **4*m_old** and nominal dense interpolation size **16*m_old^2**. These are conditional dimension/symbolic array-size effects, **NOT measured wall-clock or unavoidable lower bounds**; source notes sparse-matrix linear-time preprocessing is a future open problem. Public CA/CB/CC require fresh commitments to updated A/B/C; P14 SHA hashes are only fingerprints, not real PCS commitments.

An independent hypothetical raw-row cliff 4,180,000->4,235,303 crosses the 2^22 padded dimension to 2^23; NOT claimed to be the actual source complete circuit row count. Conversely 2,533,572->2,588,875 original nonring rows alone stay in 2^22. Full ring constraints, public input, extra wire count and actual AppendixD compiler remain unmeasured, so no actual padded m reported.

**Consequence:** small R1CS row delta DOES NOT mean small overall prover runtime; under P13/P14's concrete alignment strategy matrix interpolation domain can increase by factor4 even though row budget is ~2.18%. This changes the candidate optimization target.

## Executed evidence and hard limitations

Actually ran source-derived script at /mnt/data/pvfhe_p15_source_constraint_cost_gate.py SHA256 **553fe7ea201c8adb93ddce408d449af771822561a137c91f8ef28bb0d14d34de**.
JSON /mnt/data/pvfhe_p15_source_constraint_cost_results.json SHA256 **7b0858db1de74f0be1b7514d7a4108d2da68a4e5fa74ac5331fb2657e68d490f**.
Detailed local Markdown /mnt/data/PVFHE_P15_Full_Constraint_Count_Succinctness_Gate.md SHA256 **b596d4f4f845b50b4d9bad247186f5a022536c872ef0c615316354aaa1526cae**.
No compiled real FHE.EvalGate, complete lattice PCS, SIS estimator, full sum-check transcript, prover timings, or adaptive classical ROM/QROM extraction. This is a rigorous source-formula cost ledger plus exact synthetic boundary check, not a production benchmark.

## End of iteration

**STATUS:** PASS strict source-sparse canonical/link row design, static gadget count and asymptotic succinctness; FAIL identifying row count with actual matrix-preprocessing/prover cost; UNCLEAR real padding, speed, proof security and novelty.

**RESULT:** At source AppendixB parameters the scheme's per-gate nonring ledger has 9217 BitDecomp instances; conservative repaired rows +55303 (~2.18%). However P13/P14's equal-width duplicated private branch forces doubling of full m under assumed padding, giving a 4x nominal dense matrix encoding-size factor and possible further cliff, motivating layout optimization rather than more toy arithmetic.

**NEXT_ACTION P16 only upon PI continuation:** ONE compact selected-Y witness packing experiment: retain only actually selected original-private BitDecomp y values, bind them with sparse rows to noncontiguous original witness indices, verify one PCS private selection and R1CS/public A/B/C index encoding, quantify padded width versus equal-width duplication. If no material gain, PARK concrete-efficiency claim and require human review. Actual PCS/FS/QROM security remains separate OPEN.

**STATE_UPDATE:** YES this standalone P15 file ONLY; no global STATE.md, parallel SHIP/vFHE or prior P01–P14 edits.
