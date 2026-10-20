# BOOT-B089 — Two-harmonic cosine: complete cross-leaf nonlinear DAG cost gate
Date 2026-10-20 | TRACK_ID BOOT only | SHIP PAUSED
STATUS PASS_CORRECT_COSINE_IDENTITY / PASS_20BIT_IDEAL_APPROXIMATION / FAIL_MORE_EXPENSIVE_CROSSLEAF_DAG / FAIL_STANDALONE_NOVELTY / NATIVE_NOT_RUN.

## One minimal falsifiable hypothesis
Using B088's confirmed real Liang–Ding ring-switching leaf type and *common small-ring secret*, evaluate a concrete sparse Fourier function f(z)=cos(z) with only TWO harmonics in encrypted small-ring leaves WITHOUT full slot recovery, and show a stricter full-arithmetic advantage over slot recovery + individual function evaluation + source existing fused inverse recovery. Single fixed example, cheapest decisive analytic DAG and error gate, no new rounds of rank toys.

## Verified source, provenance, prior art
[FACT] Zhaoyang Liang and Dan Ding, "Bootstrapping via Ring Switching without Slot Recovery", ePrint2026/1779 https://eprint.iacr.org/2026/1779 official abstract. Real source https://github.com/Zhaoyang-Liang/bootstrapping-via-ring-switching-without-slot-recovery , main.go blob 6d135b72381b5d14d0049caa0f798f487dbfb421, lines887–937 split/merge, 2383–2424 common skLeaf. Vendored Lattigo RingPacking code blob 74b7c25eaf199a501251673c6badce9893d0f17e, lines191–193 documents plaintext ctN(X)=ctEven(Y)+X ctOdd(Y), Y=X². Author Table9 baseline source main.go blob 8806b327e824ea7703511fb2011a856b0b845e1c lines234–245 twiddle alpha_j; lines283–335 slot recovery inverse; lines462–501 test pipeline. Published source scripts/run_fused.sh blob 7bd162ebac8390de95b85f90ec7eb02c7195b9f4 already benchmarks no-recovery, separate-recovery, *fused-inverse*; source final fused inverse should be the performance comparator, NOT naive 3 full plaintext-rescale baseline.
[FACT ABSTRACT ONLY] Cheon–Jang–Kang, "SWIFT: Shallow and SIMD-Aware CKKS Functional Bootstrapping for Low-Latency", ePrint2026/1163 https://eprint.iacr.org/2026/1163: SIMD packing public multiples and exponentials for harmonics, prior-art barrier to generic Fourier strategy. Full technical PDF was not read. Low-rank LUT approach ePrint2026/1264 adds similar novelty barrier. No invented source theorem/page.
[SOURCE LIMITATION] Full verified ePrint1779 and SWIFT PDFs not acquired. Tested author's GitHub code from B088, not original formal full text. No Lattigo benchmarks.

## Exactly typed complex slot identity
Both leaf ciphertexts are encrypted under one skLeaf and encode a,b in R_small. For corresponding original paired top CKKS slots zplus=a+alpha*b, zminus=a-alpha*b, with public |alpha|=1 varying per slot:
  even=(cos(zplus)+cos(zminus))/2 = cos(a)*cos(alpha*b);
  odd=(cos(zplus)-cos(zminus))/(2alpha) = -sin(a)*sin(alpha*b)/alpha.
Computing these via small-ring encrypted cross-leaf multiplication is correctly TYPED and algebraically correct (basic cosine addition formula) but not novel.

## Strict fair toy cost and precision comparison
Fix domain complex |a|<=0.25, |b|<=0.25, |alpha|=1, hence |z±|<=0.5. Fix ideal, plaintext-function error goal <=2^-20=9.536743e-7 in both even and odd outputs. NOT an encryption noise/DFR bound.
(1) SOURCE RECOVERY + f baseline DAG: Forward twiddle t=alpha*b, z±=a±t, evaluate cos6(x)=1−x²/2+x⁴/24−x⁶/720 separately on z±, then inverse recovery. For each branch set y=x² (1 ctct), y² (2), y³=y²*y (3), affine polynomial, total 6 small-ring ctct, depth3, six conventional relins; ctpt twiddle forward and inverse extra; separate recovery source uses 1 forward+2 inverse ctpt/rescales; fused inverse may reduce or fold them (NOT measured). For |z|<=0.5, analytic cos6 tail bound <= 9.715106446478313e-8 <2^-20.
(2) BEST TESTED LEAFWISE DAG: t=alpha*b. For each of a,t compute shared y=x² (1 ctct), y² (2), cos4(x)=1−y/2+y²/24 using no further ctct, sin5(x)=x*(1−y/6+y²/120) using one further ctct (3 per leaf input). Compute even=cos4(a)*cos4(t) (one ctct), odd=-sin5(a)*sin5(t)/alpha (one ctct plus public inverse alpha); total 3+3+2=8 small-ring ctct (2 MORE than recovery baseline), maximum ctct depth4 (one MORE than baseline) and eight conventional relins. Nontrivial pt twiddle also persists. Simple CKKS model counting each ctct/rescale or nontrivial ctpt/rescale as one level: candidate max approximately6 stages versus recovery baseline ~5 separate stages; actual levels and fused schedule NOT measured. This explicit DAG is not guaranteed globally optimal.
(3) Earlier higher-precision variant cos6 and sin7 on each leaf: 10 ctct, depth5; also worse, so don't report it as best candidate.
(4) Error bounds at |a|,|t|<=.25: |cos−cos4|<=r^6/6!/(1−r²/(7*8)); |sin−sin5|<=r^7/7!/(1−r²/(8*9)); using |cos z|<=cosh(.25), |sin z|<=sinh(.25) and product difference, upper bound 7.063770844409805e-7 in even and odd outputs (alpha unit). Both algorithms meet 20-bit *function approximation* bound; CKKS rescale/key/noise errors excluded and could be worse.
Important: The 8 vs6 counts are for explicitly constructed approximants on this domain, NOT a lower bound on all FHE circuits, nor a complete actual FBT native benchmark. Generic FFT/SWIFT sharing not novel; no actual speedup or security result.

## Reproduction
Standalone /mnt/data/boot_B089/verify_b089_cosine_dag.py, seed890226, no external libraries or ciphertexts. Public alpha_j toy sequence of 5^j roots with n16. 1024/1024 exact analytic cos-identity cases PASS, maximum roundoff 4.4414341665e-16.
30,000 random independent complex a,b in DISKS |.|<=.25 each:
  recovery cos6: 30000/30000 meet 2^-20, max error4.72349960932e-8, median9.61596091641e-10;
  candidate cos4/sin5: 30000/30000 meet 2^-20, max6.72476496243e-7, median1.16925596881e-7;
  redundant precise candidate cos6/sin7: 30000/30000 meet, max7.18126176761e-10.
Uniform analytic bounds PASS. No secure encrypted computation; B088 provided separate toy GLWE interface correctness.
ZIP: /mnt/data/BOOT_B089_handoff.zip, SHA256 14824bf0d9aa9ee7cd67f6fb707c3bdbd73f71ce0e5c49748acaa17735f8c0e2 (zip CRC PASS), contains full report (sha256 ac6889df9970af006c90dad07d175491221d530f25a6f5f5f030d690e6abfb51), stdlib Python script (sha256 2327efa76f38af5bc294876dba81d341cc820990572ffa84def9932a9a048529), results json (sha256 29431ee66c76cabd5846b1255a78046c67fff3991629f0c667f0ee546b174aa8), log, README, hash manifest.

## End-of-iteration decision
STATUS FAIL_SELECTED_CROSSLEAF_FOURIER_FULL_DAG_ADVANTAGE / PASS_CORRECTNESS_AND_IDEAL_PRECISION / NO_NEW_PRIMITIVE.
RESULT For this two-harmonic cosine on specified 20bit ideal domain, exact candidate uses MORE ctct/depth/relin than recovered-branch baseline, while recovery inverse is ALREADY fused in published author code. Therefore no justification for a native large-param benchmark of this proposal, and no source-backed publishable improvement.
NEXT_TEST B090 NOT STARTED: archive B087–B089 specific cosine/Fourier crossleaf branch. Search a DIFFERENT bootstrapping primitive in a verified complete full-text original paper; one novel falsifiable technical claim, cheapest test, prove correctness/security/noise/cost before scaling. Don't repeat failed generic Fourier/gadget/CMux variants. Optional independent B065–B066 parameter correctness audit only with real author implementation.
STATE_UPDATE NO: boot-STATE.md listed ~187967 bytes but Notes read returned {}, so preserve. Only append BOOT-B089 finding; SHIP unchanged.
