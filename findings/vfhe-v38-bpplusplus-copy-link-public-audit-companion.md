# vFHE V38 COMPANION — BP++ native vector-input copy-wire gate and independent 2024 technical review

**2026-10-15. COMPANION ONLY**, not another V38 and not V39. The authoritative already-completed MAIN V38 is `findings/vfhe-v38-bulletproofspp-vector-input-constraint-dimension-gate.md`; MAIN V39 is NEXT and GLOBAL I192 FROZEN.

## One falsifiable auxiliary subclaim
With a BP++ ePrint 2022/510 prechallenge vector commitment `C_a=Com(a;rho)`, can an external arithmetic circuit simply use another internal candidate digit vector `w_O` to satisfy original vFHE F.2 native weighted integer y/quotient rows without an input-vector link, while still claiming an argument about C_a? **NO**. A source-correct proof must genuinely link witness wires to the SAME precommitted vector under BP++ §5 Eq(29)–(32), by explicit Eq(30) copy/input relations or a sound equivalent.

## Primary sources & version [FACT]
- BP++ Eagen, Kanjalkar, Ruffing, Nick, original ePrint **2022/510**, https://eprint.iacr.org/2022/510. 38pp Research MCP mirror PDF SHA256 `29bb2a877ba96d703f88f65d459a84797f58eaa056a03eceb604488375452603`, **VERSION_UNVERIFIED** vs later EUROCRYPT2024 edition. BP++ original §2.2 physical p8 vector Com(v;s)=v0 G+sH0+<v1:,H8:>, §5.1 physical p15 Eq30 `0=Wl*w+fl*wV+al`, Eq31 `wL∘wR=Wm*w+fm*wV+am`; original p15 explicitly discusses copy constraints for using input entries multiple times. Theorem2 p19 covers BP++ exact source relation, NOT our incorrect omitted-copy version.
- Cascudo et al., original vFHE ePrint **2025/286**, 52pp Research MCP mirror SHA `29b6b2e99308fff0e06ca1950764653faa660a9d40e08a394404947a9e3b1f19`, **VERSION_UNVERIFIED** versus official Feb2026 revised ePrint. §3.1 p10 native RNS fields; §4.3 pp20–23 scalar digit table; Appendix F.1/F.2 pp50–51 PUBLIC y and original Merkle/RS.
- Independent **PRIOR PUBLIC REVIEW**, Cypher Stack, *Bulletproofs++ review* 2024-03-29, https://github.com/cypherstack/bppp-review / https://moneroresearch.info/index.php?action=resource_RESOURCEVIEW_CORE&id=217 , §2.5 notes ambiguities/dimension preconditions in original BP++ §5 Eq30/31: `k Nv=Nl` when fl=1 and `k Nv=Nm` when fm=1; the report does NOT assert exploit, and doesn't establish the latest EUROCRYPT text is wrong. Since our toy k1,Nv=H,Nl=H, it is source-type-valid and does not claim novelty on dimensional observation. (2024 review pre-existed this research.)
- Official vFHE https://eprint.iacr.org/2025/286 landing as checked 2026-10-15 plainly states **“Fixed a flaw in the proof of Theorem 4.8”**, revision dated **2026-02-16**. Since the actual revised 2026 binary SHA is not authenticated (MCP caches 52pp old mirror, and web PDF snapshot is stale), a V17–V21 original-paper soundness flaw remains SOURCE-VERSION-GATED; it may have been addressed by this revision. The official statement does not by itself prove the new theorem correct.

## Exact independent source-shaped test [EXPERIMENT]

N4,d2,ellstar3,H8,beta4,p13=1+4*3,p29=1+4*7, K13=F13[T]/(T²−5), K29=F29[U]/(U²−12), with legal offcube reference query tuples (2+w,3+2w,4+3w). Full finite-extension MLE canonical coefficient rows and exact non-wrap y and integer quotients computed by independent Python, yielding:
```
p13 coefficient rows: (8,4,10,3,2,10,3,0),(4,0,2,6,8,12,9,11)
p29 coefficient rows: (10,16,0,2,10,20,6,24),(26,7,9,15,15,8,5,2)
a_wire=(0,1,2,3,0,1,2,3), beta4-legal
p13 S=(49,85), y=(10,7), k=(3,6)
p29 S=(126,94), y=(10,7), k=(4,3).
```
Source native field tables may honestly equal a_wire. But PRECHALLENGE BP++ vector input committed to `a_pre=(0,0,0,0,0,0,0,0)`. If source Eq(30) ignores wV by choosing fl=0 and circuit range/weighted sum conditions refer solely to auxiliary wires a_wire, their algebraic relations are satisfied by unrelated a_wire and say NOTHING about committed a_pre. With correct input-enabled `fl=1,N_l=k*N_v=8,a_l=0,W_l*w=−a_wire`, the Eq30 residual is `a_pre−a_wire`: exactly **6/8** nonzero, so the invalid mixture is rejected. If a_pre=a_wire, exactly **0/8** residuals nonzero; proper interface satisfies honest check. Illustrative toy commitment scalar order1009 is INSECURE; no actual BP++ prover, F.2 compiled source, FS, real 128bit proof or new published exploit was executed.

**Size scope:** H=2^24, L2,d4 require 8H=134,217,728 canonical coefficient terms by a straight dense approach and ~74-bit bounded integer weighted sums with 26-bit quotient. BP++ needs O(H) independent-generator CRS for H-dimensional committed input, 512MiB points IF fully cached (can be regenerated), but ONE group commitment is transmitted, not 512MiB per-value commitments. Correct range protocols might REUSE copy constraints required for input digit membership; this does NOT establish H *additional* constraints on top of an already properly bound range circuit. Original transcript complete ZK and practical cost remain unverified.

**STATUS:** FAIL OUR no-copy binding shortcut; PASS exact Eq30 source-shape and public prior audit. Main V38 separately also FALSIFIED only-8-row BP++ native quotient shortcut and dummy multiplication gate error, and is authoritative.

**NEXT_ACTION:** MAIN V39: FIRST prioritize official ePrint2025/286 Feb2026 revised theorem 4.8 source/authentication gate, not another speculative million-element patch. If final binary inaccessible, report precise version boundary to PI. GLOBAL I192 FROZEN. No author outreach without PI.

**Files:** report `/mnt/data/VFHE_V38_BPplusplus_Vector_Input_Copy_Link_Gate_2026_10_15.md` SHA256 `107eb444225acc29f2588a162090618a2b07e360effda6a5e66dc7446d845ef1`; script `/mnt/data/vfhe_v38_bpplusplus_vector_input_copy_gate.py` SHA256 `4fcb4847a4236a54a52c4951422be496b0ec52e01b9d3ad07ca6103db7a91ba0`; JSON `/mnt/data/vfhe_v38_bpplusplus_vector_input_copy_results.json` SHA256 `4d0a94a1e751301499522233acf97695d9bc13cfdfa39b19a4502bce3499d52c`.

**STATE_UPDATE:** Companion reference only; main V38 complete/V39 not started; global I192 frozen.
