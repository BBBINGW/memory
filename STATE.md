# Research State — 2026-10-12

ACTIVE: **Nested-RNS large-integer FHE — source-grounded correctness and composition audit**.
Paper: Dan Boneh and Jaehyung Kim, *Homomorphic Encryption for Large Integers from Nested Residue Number Systems*, IACR ePrint **2025/346**, https://eprint.iacr.org/2025/346.
Primary full text acquired with research MCP: **31 physical pages**; GitHub ePrint mirror PDF SHA256 `7a26e911b00368dace336f4324e8e3f036927a57683cf5fbea1e26ee19777ef5`, source revision `edfb5603b09e7608360f41b276e1389857051f5b`, `VERSION_UNVERIFIED` against latest official binary. Source §2 p7 centered Z_t representatives, §3.2 pp13–14 IEcd and Inner/Outer Rotation definitions, §3.3 pp14–17 Theorem2/Algorithm3, §4 pp19–22 nested RNS.

LAST COMPLETED ITERATION: **99 (2026-10-12)**.

## PROTOCOL AND PI BOUNDARIES
Read AGENT.md and RESEARCH_PHILOSOPHY.md each session: smallest falsifiable claim → cheapest decisive test, **one primary hypothesis and one minimal test per iteration**, [FACT]/[DERIVATION]/[SPECULATION] and physical source location, read-before-write, separate archive/STATE commits + reread, end iteration STATUS/RESULT/NEXT_ACTION/STATE_UPDATE.
Human PI sets research direction, judges contribution/novelty, strategic pivots, external communication. **NO AUTHOR CONTACT/EMAIL/OUTREACH OR PUBLIC DISCLOSURE** unless PI explicitly authorizes.

## CURRENT FINDING — I99
[FACT] §3.2 pp13–14 puts different CRT moduli p_i in separate CKKS slot blocks: IEcd=Ecd∘ι∘iCRT and InLeftRotβ is a CKKS ciphertext-slot rotation across the p_i blocks. §3.3 p16 uses inner rotations as ingredients of **weighted homomorphic base conversion**, then Modp.
[HYPOTHESIS FAIL / DERIVATION PASS] Treating inner rotation as a plaintext **unital ring automorphism** of Z_P for arbitrary CRT messages, or as a freely composable integer-ring rotation, FAILS. Let P=5·7=35, E(x)=(center(x mod5),center(x mod7)); swap the two blocks then reinterpret under original p0=5,p1=7 and apply CRT, yielding T. E(3)=(-2,3); T(3)=33; T(6)=29 != 2T(3)=31 (mod35). Also T(9)=27 != T(3)^2=4 (mod35). Exhaustively all 35² inputs: 522 additive failures, 532 multiplicative failures. A unital ring endomorphism of Z_35 fixes 1, hence all elements, so cross-prime T cannot be ring automorphism.
[CRITICAL SCOPE] **Not** an attack or correctness flaw of Boneh–Kim, who use ciphertext rotations on integer representatives inside explicit Algorithm3 conversions; no source claim it is an automorphism of abstract Z_P. This kills ONE naive cross-prime rotation/drop-in linear-transform optimization, not the underlying published scheme or all optimizations. Elementary insight; NOVELTY NOT VERIFIED.
Archive `findings/nested-rns-inner-rotation-cross-modulus-algebra-obstruction-iteration99.md`. Exact script `/mnt/data/iteration99_nested_rns_inner_rotation_counterexample.py` SHA256 `9d7f2dcb3858d9bb514de35e19b3ab216ca6180fd2969d1d98c13db4de4abb85`; JSON results SHA256 `07b09a1c096148a071d03271db09030d2a7a96084692b9c44fc100a2d63007f3`. Artifacts are ephemeral, repo finding contains formulas/reproducibility.

## NEXT_ACTION — ONE MINIMAL TEST (I100)
Read ePrint **2025/346 physical pp14–17**, especially §3.3 Theorem2 and Algorithm3 lines1–14. Test ONE precise candidate: whether the source's per-prime weighting in Algorithm3 is NECESSARY for CRT base conversion under inner slot rotations. Use **one exact p0=5,p1=7,P=35, target coprime r=3**, a centered input x (small enough for theorem assumptions), compute y_i=[[x]pi·(P/pi)^{-1}]pi and v=round(sum yi/pi), then verify Algorithm3's rotated weighted sum recovers x (mod r), while removing per-prime cross-modulus weights breaks for some small valid x. Stop if authors already explicitly justify the required weights (then archive as known boundary, not novel), do not run CKKS/Sage or develop full new scheme. Note Theorem3 precision requires |x| << min P/pi and is asymptotic; choose tiny x satisfying obvious size separation where possible or label toy as pure algebra, NOT practical parameter validation. One hypothesis/test only.

## PARKED / ARCHIVED HISTORY
- PARKED: **PaCo sine/scale precision micro-audit** I95–98, PI implicitly chose option B by '好的，请继续'. Details `findings/paco-precision-microaudit-parked-iteration99.md`. Full previous-state snapshot `logs/paco-state-pre-nested-rns-handoff-iteration99.md`. Former source PaCo ePrint 2025/886 and all I95–98 findings retained. No found paper flaw, no novel improvement.
- PARKED: **RIG-HE**. Full state `logs/rig-state-2026-10-12-pre-vfhe-handoff.md`.
- ARCHIVED: **GL generic BigSwitch** `failures/gl-generic-bigswitch-structure.md`.
- ARCHIVED ONLY direct **vFHE bounded-public-A + native Brakedown repair** I88–94 (high cost and incomplete proof), `failures/vfhe-bounded-public-A-direct-brakedown-repair-archived-iteration95.md`. Original **vFHE CRT componentwise range lookup correctness/soundness audit** ePrint 2025/286 survives as important conditional ideal-IOP finding; NOT a validated compiled SNARK forgery. Full previous-state snapshot `logs/vfhe-state-2026-10-12-pre-paco-handoff.md`. Do not delete all prior findings.
- Other 2026 candidate PDFs 2026/975 and 2026/956 retrieval blocked, and new candidate 2024/115 and 2025/022 not verified: **do not use abstracts as technical proofs**.

STATUS: **ACTIVE nested-RNS FHE; I99 conditional algebra/composition obstruction proved; I100 direct CRT base-conversion minimal test NEXT**. Paper originality/implementation security not established. No outreach or public release.