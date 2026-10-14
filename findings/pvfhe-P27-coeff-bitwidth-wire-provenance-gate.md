# PVFHE-P27 — Coeff bitwidth and helper-wire source provenance gate

2026-10-15 Asia/Tokyo. **P27 COMPLETE; P28 NOT STARTED.** **STATUS:** PASS independently corroborated original source text and precise source-Q coverage counts; FAIL original text/code uniquely determines compiler Coeff arity and Coeff/KeySwitch/XPow bit-wire sharing; **MISSING CRITICAL SOURCE / HUMAN_REVIEW / PARK** global R1CS-to-SNARG exploitability. No original-paper cryptographic attack claimed.

## Read before write
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, global STATE.md SHA 3b83237bc5aba4a77479b09dc1f3ac8bccaebc7c (parallel V42 NOT EDITED), P26 findings/pvfhe-P26-full-gate-dag-wire-merge-gate.md SHA 9a52b76db2bc06b8bad9984fc600e413e933e172 and P25 SHA 27bd63328f3ae749e3afbd0d7c78b82da0a5e354. P27 destination absent beforehand. MISSING_SOURCES.md checked SHA dd57c4e17ea4764b1e6cfed16850360b53ceaac9; no PVFHE-1764 entry at read time.

## ONE falsifiable hypothesis / decisive source search
**HYPOTHESIS P27:** Accessible original paper/source compiler uniquely identifies Coeff bit arity (53 vs54) and which Coeff/KeySwitch/XPow auxiliary bit wires are identical, settling P26's competing full-gate witness cases.
**FALSIFIER:** Cross-check original bit count equations and compiler wire rule with two independently available indexed paper texts, then find actual author compiler or unambiguous source-level wire mapping. If formula statements conflict and needed code/render is inaccessible, do NOT assume a compiler policy: mark full-scheme exploit SOURCE_BLOCKED.

## Original source facts
Huang, Li, Mao, Zhang, Fully Homomorphic Encryption with Efficient Public Verification, ePrint2024/1764, https://eprint.iacr.org/2024/1764. Research MCP 29pp original mirror PDF SHA256 7f42f4e9cf8218894226903a0c5ab3434e35812276b641acd01f8280ab183089 (VERSION_UNVERIFIED) and independently IACR publicly indexed 29pp PDF text https://eprint.iacr.org/2024/1764.pdf both have:
- Physical p15 Lemma4.5: BitDecomp(y;x0,...,x_ell) indexes 0 through ell INCLUSIVE; N_BitDecomp=3ell+4, so ell=53 means 54 bits and 163 rows.
- Physical p16 Lemma4.11 statement: N_Coeff=N*N_BitDecomp+2N, invoking named full-width gadget.
- Physical p17 Lemma4.11 PROOF: BitDecomp(yi; xi,0,...,xi,ell-1) indexes 0 through ell−1, i.e. only 53 bits. Inconsistent with source gadget name/cost.
- Physical p27 AppendixC.3: Merge variables representing the same circuit value; no explicit auxiliary-bit identity equivalence relation across the Coeff, KeySwitch and XPow gadgets; no integer-range predicate for canonical decomposition.
- Physical p26 AppendixB: Q=2^53+5,N=2048,n=q=1024.
Official IACR landing shows 2024-10-29 submitted and 2024-10-30 approved, with only a PDF link; version-history click cache miss. Web screenshot PDF pp14–16,26 CACHE MISS; direct alternate GitHub mirror container download DNS unavailable. Targeted web and GitHub repo/source searches for author implementation and paper found no functioning compiler. This search is bounded; not a claim code does not exist anywhere. No author contact.

## ONE minimal exact source-Q consistency test [ACTUALLY EXECUTED]
Set Q=9007199254740997, ell=53 and illustrative N=2048.

Literal 53-bit Coeff: max unsigned scalar 2^53−1, hence FIVE legitimate canonical residue values 2^53,...,2^53+4 are not representable. A scalar zero has only all-zero bit representation. IF its 53 low helper bits are also the low 53 KeySwitch helper bits, P25's alias {0,2,53} is excluded; no source proof such sharing occurs.

Named 54-bit Coeff: source zero modulo Q has two scalar bit words, integer 0 and integer Q=2^0+2^2+2^53. Even full bit sharing between Coeff and KeySwitch cannot by itself force a canonical integer decomposition. Other specifically linked gadget wires, including XPow, COULD block the global P25 graft; source does not specify their precise equivalence.

Hypothetical source formula counts at N=2048: 54-bit N_BitDecomp=163 → N_Coeff=337920; 53-bit resized N_BitDecomp=160 →331776; difference 6144 per Coeff or 12288 for two. These are conditional arithmetic counts, not observed complete compiler wire counts. P17 separately warns of N vs q/2 count convention ambiguity.

Reproducible ACTUALLY RUN independent arithmetic consistency script:
- /mnt/data/pvfhe_p27_source_contract_gate.py SHA256 b864fd5eea3661649575a700e2f7223385696fff987597f03df9ba462fce9c91
- /mnt/data/pvfhe_p27_source_contract_results.json SHA256 34899cdfe4342f917020adb7ef09a26be0b1970043831a40ce0533a65094e0ad
- /mnt/data/PVFHE_P27_Coeff_Bitwidth_Source_Provenance_Gate.md SHA256 7fdd364b5a7a0ceba8ca7367a4e00ee214610ee22b40672eabe16b8b7eaf9591.
Script verifies arithmetic ONLY; not full Ring-R1CS, PCS or SNARG. Paper-source text checked separately.

## Research decision
**STATUS:** PASS text inconsistency + bit coverage/cost; FAIL unique source artifact arity/wire decision; **UNCLEAR/HUMAN_REVIEW / MISSING CRITICAL SOURCE** full FHE.EvalGate/SNARG and newest rendered edition.
**RESULT:** A source-description dilemma is documented: literal 53-bit Coeff lacks whole Z_Q scalar coverage; named 54-bit Coeff is noncanonical. This is not proof that no corrected compiler can work or that a complete accepting SNARG counterfeit exists. The primary blocker is actual author source compiler/SSA wire-sharing specification.
**NEXT_ACTION:** PARK dependent full-gate exploit until an original author/compiler artifact or authoritative repaired-source variant clarifies bit arity and auxiliary sharing. If PI considers worthwhile, request the original full FHE.EvalGate→Ring-R1CS compiler/supplement plus authenticated PDF; no unsolicited author contact. Avoid further KeySwitch toys and do not reopen parked P05–P22 PCS/FS. PI may select genuinely independent new FHE hypothesis.
**STATE_UPDATE:** YES standalone P27 plus MISSING_SOURCES.md registry ONLY; NO global STATE.md, parallel vFHE/SHIP or prior P01–P26 edits.