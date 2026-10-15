# CGS-38 — Direct public-PMF MPC lookup is not a hidden-covariance two-round ThFHE sampler

**2026-10-15. Active CGS, following CGS-37.** One primary hypothesis; one decisive public-first-table/protocol-interface test.

**PRIMARY HYPOTHESIS H-CGS38 [FAIL direct port]:** The existing Franzese et al. (CCS2025/ePrint2025/1025) Algorithm4 dice-ensemble approximation and Figure4 Pi_noise protocol can directly replace Okada–Takagi ePrint2025/409 per-session correlated Shamir Gaussian pads, while (1) keeping the target covariance hidden, (2) preserving any T-out-of-N Shamir replies, (3) using only original two online rounds and (4) saving O(LDec) session storage.

## Original full sources [FACT]

**Okada–Takagi, Low Communication Threshold FHE from Standard (Module-)LWE**, ASIACRYPT2025, https://eprint.iacr.org/2025/409; original full 40-page Research MCP mirror SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, version unverified. Algorithm6 physical p26 needs scalar pad D_Z,sigma0 sqrt(Bpub²−||s||²). Algorithm7 physical p29 needs n-dimensional integer Gaussian with width matrix sigma0 sqrt(Bpub²I−Sigma_s) and secretly shared pads per sid, where Sigma_s=sum_i Gram(s_i). Algorithm5 p23 exposes processed ciphertext plus all active PartDec replies, while the Server remains untrusted/noncolluding. Intended online interface is Server broadcast, then parties' one-response broadcasts, any T out of N.

**Franzese, Fang, Garg, Jha, Papernot, Wang, Dziedzic**, Secure Noise Sampling for Differentially Private Collaborative Learning, CCS2025, https://eprint.iacr.org/2025/1025; original full 38-page Research MCP PDF SHA256 ea7f3a14ddbff6214bad0a1550b2d42e2a81b9a4d01051e41841d6b0ac575d4f, VERSION_UNVERIFIED. Algorithm1 p7 constructs one n-faced die with floor(n*f(x)) entries of face value x. **Algorithm4 p12 takes the target PMF f as INPUT**, its first die d1=1DA(f,2*|supp(f)|), with Theorem2 p11 L1 approximation error <2^(-ell) after ell dice. Corollary1 p13 covers one fixed public f; Theorem3 p14 explicitly treats a CONSTANT count of noise oracle calls (not automatically arbitrary polynomial LDec). **Figure4 p17 Pi_noise INPUT explicitly says ALL parties HOLD PUBLIC entries of T0,...,T_(ell−1)**. Per lookup layer Step1d every party sends encrypted partial dot product to P1, P1 sums and sends the combined ciphertext to every party. Figure2 p15 FABB Random/B2E/E2A functionality and Figure3 p15 BGV-THE one-hot circuit add interaction. Final Figure4 Step2 calls E2A and outputs ADDITIVE MPC shares, not original arbitrary T-out-of-N Shamir shares. Table2 p21 gives **actual** per-sample protocol benchmark for 16 parties/size 2^16: about 11.18 MB communication at ell64 and 22.22 MB at ell128, in THEIR setting, not a CGS ThFHE implementation. Independent CCS2025 confirmation on CISPA public publication page. Remote web screenshot attempts for ePrint PDF were blocked (IACR HTTP403 / GitHub mirror cache miss), so exact page/protocol claims come from full Research MCP extracted original PDF, not unverified secondary source.

## ONE decisive exact first-public-die test [DERIVED AND EXECUTED]

Use the SCALAR source Algorithm6 to keep Gaussian distribution EXACT rather than pretending an MLWE correlated vector has independent univariate marginals. Four iid-binary secret coordinates admit s0=(1,0,0,0), with ||s0||²=1, and s1=(1,1,1,1), with ||s1||²=4. Choose illustrative Bpub=5 and sigma0=16 (NOT a complete security-validated FHE parameter set). The two REQUIRED scalar Gaussian widths are w0=16 sqrt24 and w1=16 sqrt21.

Truncate the source-style discrete Gaussian into support S=[−392,392], |S|=785, and NORMALIZE exactly in that support so f_m(x)=exp(−pi*x²/(256*(25−m)))/Z_m. **Original Algorithm4 first die has 2*|S|=1570 public faces.** Consequently:

- m=1: the number of 0-valued entries in the first public die is floor(1570 f_1(0)) = **20**.
- m=4: the number of 0-valued entries is floor(1570 f_4(0)) = **21**.

Thus publishing the actual Algorithm4 secret-dependent first table deterministically identifies which of these TWO promised key-dependent scalar target PMFs is used BEFORE any private lookup. **This demonstrates auxiliary norm-class leakage under the proposed modification, not any ciphertext-security attack on the unchanged source.** Scalar known-norm LWE security may be reduced to standard LWE by separate prior art, but a ring-wide secret-conditioned covariance public table is not within the original ordinary-MLWE assumption.

The two finite target PMFs have high-precision **TV = 0.032299091363487953357775233497473768688373...**. Triangle inequality implies any single secret-independent public target PMF H has worst-case TV at least **0.01614954568174397667888761674873688...** from one of these two specific targets. Original unbounded lattice-Gaussian mass omitted by truncation is conservatively <3.73e−34 and <4.36e−39, respectively. This is a FIXED-size toy and NOT a general asymptotic bound for arbitrary full protocol parameterization.

Reproducer: /mnt/data/cgs38_public_table_leak_and_rounds_gate.py SHA256 **d8fce27462913956485de1ac3459683491733414eb519112007473b9c145fb63**. Exact output /mnt/data/cgs38_public_table_leak_and_rounds_results.json SHA256 **0305754a4d4ce801ccec2a3591552595bac7da84f7a0ec3c32dea184f97652e4**. mpmath 85 digits, integer floor, exact finite-support normalization, no Monte Carlo, no FHE library or lattice estimator.

## Other necessary interfaces read from SAME original Pi_noise [SOURCE FACT]

1. **Additional online dependent messages:** Figure4 runs party-to-P1 encrypted partial sends followed by P1-to-parties aggregate broadcast EACH of ell chained table stages. Source protocol as written entails at least 2*ell sequential directed send/broadcast **legs**; ell=128 means 256 such legs, not counting FABB calls. This is NOT a round lower bound for newly redesigned MPC protocols and NOT a runtime benchmark. Online source ThFHE has only two broadcasts total in its Server/PartDec design.
2. **Wrong share access structure:** Pi_noise returns additive shares among all engaged parties after E2A, not Shamir shares allowing any arbitrary T active set and dropout. Its input assumes all parties participate, plus a coordinator P1.
3. **Wrong native target complexity:** Source Algorithm7 requires a non-diagonal correlated n-dimensional integer-lattice Gaussian. Independent scalar DP-Gaussian table lookups generally give only a product/diagonal distribution. Direct generic lookup for the full n-dimensional Gaussian would have potentially exponential finite support. This was not cost-instantiated here.

A new method could use PRIVATE table creation and private FHE lookup, robust threshold resharing, online MPC and/or extra trusted setup. This is genuinely different from unmodified 2025/1025 and requires a new security proof and cost model; not proven impossible.

## End of iteration

**ITERATION:** CGS-38.
**STATUS:** **FAIL** direct public-table MPC sampler for hidden covariance/two-round Shamir; **PASS** original full protocol-interface inspection and exact first-public-die witness; **HUMAN_REVIEW** parent source original O(LDec) problem OPEN. This is NOT a claim that either source is insecure or that public norm disclosure necessarily destroys scalar-LWE security.
**RESULT:** First die alone reveals chosen secret-conditioned scalar Gaussian (20 vs21 zeros); as-written private MPC lookup presumes PUBLIC tables, extra interaction per table, additive shares. Correcting it requires additional machinery not provided by the paper.
**NEXT_TEST CGS-39 (PI next “继续”):** Pick one CONCRETE relaxed-constraint design (e.g. allow additional MPC online messages or fixed new secret-table preprocessing), specify EXACT hidden-PMF handling and source threat model, and falsify its cheapest security/round/storage claim. If preserving all initial constraints, recommend explicit PI HUMAN_REVIEW/pivot instead of accumulating more generic MPC no-go comments.
**STATE_UPDATE:** YES own finding + append CGS full history + latest root override, no other topic edits.
