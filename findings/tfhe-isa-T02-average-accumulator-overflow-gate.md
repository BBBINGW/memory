# TFHE-ISA T02 — Algorithm 3 Average modulo-256 overflow source audit

2026-10-15 Asia/Tokyo. **T02 COMPLETE, T03 NOT STARTED.**
**STATUS:** PASS a concrete, source-grounded application arithmetic boundary for unrestricted unsigned-byte inputs; **NOVELTY LOW / PARK**. This is NOT a TFHE cryptographic primitive attack, an actual author-implementation exploit, or a new security claim.

## Read before write and provenance
Read START_RESEARCH_SESSION.md SHA 6235e9d376a8b143719a40178132f02a6a41d4f3, RESEARCH_PHILOSOPHY.md SHA 49da3f7fa3e75f502525482ce4a7ab6867, AGENT.md SHA b3e73b2c7f852c05aa674dd97b632e9f99ac5f22, STATE.md SHA 3b83237bc5aba4a77479b09dc1f3ac8bccaebc7c (frozen general I192, independent vFHE V42 SOURCE_BLOCKED), prior T01 failure SHA 812e0c4f494fa33632663ff84cb79f7883523ec8 and OPEN_RESEARCH_BRANCHES.md SHA 28d4811ca5b43830c123d75db98b1eecd2f2a606. Target T02 absent. Do not alter other branches.

Original full source: Trama, Clet, Boudguiga, Sirdey, Ye, Designing a General-Purpose 8-bit (T)FHE Processor Abstraction, TCHES 2025 / ePrint2024/1201, https://eprint.iacr.org/2024/1201. Research MCP 48 physical-page PDF SHA256 ebe98ea393e91f814a2a6098809f2c095de0bf4867c4693b8925df4b8a13ea09, VERSION_UNVERIFIED. Independently IACR landing shows revision 2025-01-10 and publicly indexed 48pp PDF; exact rendered web PDF screenshot pp22/36 failed cache miss/403. Evidence is text corroboration, not authenticated PDF-byte identity.

Source physical p22 §8.1.3 Algorithm 3 Average accepts n encrypted unsigned 8-bit values, declares a 16-bit fixed-point average, accumulates Ca=A[0] then Ca=ADD(Ca,A[i]) for i>=1; DIVi(Ca,n) and DIV_DECi(Ca,n) produce integer and decimal pieces. NO explicit sum bound. Physical p36 Appendix B.2.2: ADD works over Z_256 and explicitly ignores high carry. Section5.3 p15 confirms ADD output mod256. Table6 p25 benchmarks n2,n5,n10; source benchmark data inputs unverified.

## ONE primary hypothesis + decisive falsification
**HYPOTHESIS T02:** Ideal zero-error Algorithm3 correctly computes the true arithmetic mean for EVERY n-element unsigned-byte input array.
**FALSIFIER:** Find two legal equal-length arrays with identical terminal Ca plaintext but distinct target means. Final divisions receive only Ca and public n and cannot recover dropped carry; no FHE noise or security hypothesis is needed.

**Exact witness n=5:** A0=(0,0,0,0,0) gives sum0, Ca0, true mean0. A1=(128,128,0,0,0) gives sum256, accumulator plaintext trace [128,0,0,0,0], Ca0, true mean 256/5=51.2. Both final Ca states encrypt byte0 but their ciphertext samples need NOT be identical. Thus correct source DIVi/DIV_DECi evaluated on the plaintext of Ca cannot return the distinct true averages. n2 array (128,128) similarly has true mean128 but Ca0. Positive control n5 (1,2,3,4,5): sum15, Ca15, correct mean3.

**General exact arithmetic:** For ai in 0..255, S=sum ai and the source pipeline Ca=S mod256. The desired mean S/n differs from ideal suffix input mean (S mod256)/n by 256*floor(S/256)/n. A valid no-wrap precondition is S<=255. To support all n unsigned bytes, accumulating S needs w=ceil(log2(255n+1)) bits; n=5 needs 11 bits. A carry-aware FHE method costs more operations and may alter DFR, not measured. This is standard fixed-width arithmetic, not standalone cryptographic novelty.

## One ACTUALLY EXECUTED exact test
Executable Python model matches modulo256 byte ADD, computes rational means using fractions.Fraction, and checks the n5 collision, n2 collision, no-wrap control. It does not execute real TFHE, author binary, decimal fixed-point DIV_DECi, benchmark timing or any proof system.

Files:
- /mnt/data/tfhe_isa_T02_average_overflow_gate.py SHA256 c807e9709091fec4c2f7b3be818d7c7d3384006697bbb461fe92cbffbdf21dc5
- /mnt/data/tfhe_isa_T02_average_overflow_results.json SHA256 c7647fcf3828e966beed38e7913d14f7321e05c2f2e46d163435646a2ed1b204
- /mnt/data/TFHE_ISA_T02_Average_Accumulator_Overflow_Audit.md SHA256 efa5f87661da4bf2ec87b101873a80ead0781dac4560f49db2d83e793d7c78f4

## Research decision
**STATUS:** PASS source-defined application overflow boundary; **PARK** because trivial fix / LOW NOVELTY and full implementation impact not evaluated.
**RESULT:** Unrestricted input-domain reading of printed Algorithm3 is false without sum(ai)<=255. This is NOT failure of original TFHE instructions, security/IND-CPA, actual measured FHE program, or evidence that authors benchmarked overflowing arrays.
**NEXT_ACTION:** New independent original-full-text FHE algebra/noise/parameter-compatibility problem with genuinely nontrivial potential; do not repeat byte overflow toys, T01 radix/DFR or paused PVFHE/other branch.
**STATE_UPDATE:** YES this standalone T02 finding only; NO global STATE.md, concurrent vFHE/SHIP, old TFHE-ISA-T01, PVFHE or OPEN_RESEARCH_BRANCHES changes.
