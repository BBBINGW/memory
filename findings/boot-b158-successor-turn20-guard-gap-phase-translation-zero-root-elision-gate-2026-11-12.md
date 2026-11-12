# BOOT / B158_OVERALL — Successor Research Turn 20/25
Date: 2026-11-12 (Asia/Singapore)
TRACK_ID=BOOT
ACTIVE_SUBLINE=B158_OVERALL
Phase: PROBLEM_SELECTION
Candidate: boot-b158-guard-gap-phase-translation-zero-root-elision-v1
Final status: PARKED — PASS_CONDITIONAL_PHASE_ALGEBRA / FAIL_STANDALONE_PAPER_VALUE / UNKNOWN_FULL_SOURCE_DFR
Native/Codex: NOT RUN

## Durable read-before-write / candidate differentiation
Controller entry ACTIVE=UNKNOWN and BACKUPS none. Fetched and independently verified:
- predecessor findings/boot-b158-successor-turn19-fully-unmerged-branch-rail-frontier-cost-gate-2026-11-12.md blob 4086669bc11af1d921808ee18afb99c2f65c2171 (PARKED).
- findings/boot-B175-source-level-si-error-bounds-2026-10-29.md blob c75aa60e080b28b688de7ee8859c5df4d1951c02 (B175 terminal SI dominant tensor/reference noise).
- findings/boot-B176-order8-three-bit-packed-cmux-2026-10-29.md blob 6159bc9c07e4ecc44a3783f7051e24939075396e (standard CMux/selector conversion parked; FREE zero selector, root bits and conversion were granted even in that value ceiling).
- findings/boot-b158-successor-turn9-message-plateau-interpolation-leading-degree-gate-2026-11-12.md blob 013eb14b560360a7ffcb8869226535655cc9cafe (S63 legal phase domain was explicitly CONDITIONAL, not source-authenticated).
- findings/boot-B174-audit-si-grouped-marginal-and-pointwise-gate-2026-10-28.md blob ffffc7e6a9c56ff0e4208a5c5ff5fe2cb786cf29, exact fixed 9-bit BFV/BGV setting N32768, T65537, H8192, 8 PS blocks, LWE dimension2048, 128m+e examples.
Distinctness: This is NOT the closed Turn10 compensated affine recentering of the terminal SI (where tensor error invariance killed value), Turn3 full polynomial direct-LT, Turn9 plateau interpolation, or archived B176 STANDARD order-8 CMux itself. It is a new mathematical *input-domain offset / LUT-variable conjugation* to remove the exceptional zero root of order-8 selector. It does NOT claim to have resurrected B176's complete conversion/key-cost advantage.

## Mandatory pre-registration of one decisive test
QUESTION: If the B175 legal phase domain is exactly or contained in S63={128m+e mod65537 | 0<=m<512, -63<=e<=63}, does a single public delta=64 translate all legal x away from zero, permitting a 3-layer rather than 4-layer order-8 packed selection while preserving arbitrary f(m), including original x=0, using offline recompilation F_delta(Z)=F(Z-64)?
CURRENT_BELIEF: Algebraically YES for S63. But the source legal phase domain is not authenticated, cross-domain input addition and whole-output DFR are unverified, and standard 3-bit RLWE->RGSW selection is still costly/non-novel. The saved B176 whole-cost gate already gives the originally 4-layer CMux FREE selector bits and zero flag, making small gains unlikely to support an original paper without new conversion.
CHEAPEST_DECISIVE_TEST: Exactly enumerate S63, its complement, the shifted zero exclusion and eight-power roots in F65537; prove function translation and assess the most favorable 4->3 external-product count, charging the missing 3-bit selector conversion and public LUT preprocessing. No native.
IF_PASS: If source formal input domain confirms the zero-free guard gap, and a complete typed three-layer selector/input conversion with positive whole cost and novel functionality exists, retain ACTIVE for matched source/DFR/security checks.
IF_FAIL: If legal domain includes x=-64, or the 3-layer proposal reduces no material all-in cost/novelty after selector conversion, PARK as a standalone paper candidate.
IF_UNCLEAR: Preserve the exact CONDITIONAL algebra and the missing source/DFR and conversion costs as UNKNOWN; PARK unless a new independently specified conversion mechanism satisfies the three killer gates.
WHICH_PAPER_GATE_CHANGES: full legal-input and root-zero semantics (1); input offset and GGSW selector source contract (2); saved zero-flag CMux gadget/selector cost, noise, keys and offline LUT recompilation (3).
WHY_THIS_RESULT_CHANGES_THE_NEXT_DECISION: If zero-root could be eliminated while retaining the same function, an entire packed CMux layer and RGSW zero-selector might be removed. Without complete source domain and conversion value, there is no reason to launch native or reopen archived CMux.

## Exact algebraic gate, no source-domain overclaim
Let p=65537, message m∈{0,..,511}, and conditional error e∈[-63,63], phase x=128m+e (mod p). The 512 intervals of length127 do not overlap mod p; hence |S63|=512*127=65024, and complement size513. In particular x=-64 mod p=65473 is NOT in S63. Choose delta=64. Then for every x∈S63,
    x' = x+64 != 0 mod p.
Since F_p^* has order p-1=65536 and 8*H=8*8192=65536,
    y'=(x')^8192,   (y')^8=(x')^65536=1.
Thus for these legal values y' lies in the eight-element group mu8 ⊂ F_p^*. This removes the algebraic root-zero special case, which ordinarily exists at original x=0 (m=0,e=0).

Independent read-only pure-JS enumeration verified:
 legal S63 size65024; complement513; (-64 mod65537) NOT legal; all 65024 shifted x' nonzero; each shifted (x')^65536=1; mu8 roots exactly {1,16,256,4096,61441,65281,65521,65536}.
This is not a native encrypted test and does not validate source-defined FULL phase support/DFR. If source permits e=-64 or a broader domain including x=-64, the invariant fails.

For arbitrary public polynomial F(X)∈F_p[X] representing the desired source LUT on all legal original x (including x=0), define:
   F_delta(Z)=F(Z-64).
For every original x∈S63,
   F_delta(x')=F(x), including the original x=0 mapped to x'=64.
Thus public offline coefficient re-compilation exactly preserves the plaintext LUT function for the specified conditional domain. The composition has same polynomial degree generally and requires recomputing all public block coefficients; it is NOT a low-degree compression or a reduction of ordinary monomial basis costs. Conjugating the variable by a constant is standard algebra, with an offline cost that must be charged (naive binomial coefficient shift up to O(D²), potentially faster algorithms; no concrete implementation cost measured).

At the encrypted interface, a BGV plaintext Add of +64 can in principle transform a ciphertext encryption of x into encryption of x+64 at compatible scale, without a ct-ct multiply. However the actual author LWE->RLWE Step1 normalization, scale/carry, BGV ciphertext noise, output extraction and complete legal phase domain after conversion were NOT independently verified. One cannot merely edit metadata or assume no extra rounding/carry. No actual source-compatible end-to-end construction was run.

## Bounded value / novelty screen
In archived B176 standard order8 packed CMux, 8 nonzero roots require 3 packed external products for 3 binary root bits, plus 1 final zero-flag CMux for the full domain: 4 packed external products total. It gives a deliberately ORACLE-FREE COST for three RGSW bits, zero RGSW flag, CRT branches and conversion and still fails the whole-value/novelty screen.
Under the CONDITIONAL input translation, the exceptional zero root is removed, so ONLY the 3 nonzero-root packed external products remain and the zero-flag RGSW ciphertext/last CMux may be omitted. In the B176 operation-count abstraction this would change 21 basis ctct + 4 packed external products to 21+3; compared with B175 26 ctct through output, it gives two abstract fewer operations (26 vs 24), but SI ctct and external products are incomparable units. This is at most one packed external product and one zero selector saved RELATIVE to the already optimistic B176 scheme.
For gadget decomposition parameter l, one fewer packed external product saves a layer (optimistically ~2l gadget-row accumulations), and one fewer RGSW selector saves ~2l RLWE rows, without including key switching, selector-bit conversion, CRT/DFT branch construction and offline F_delta coefficient generation. Standard production of THREE encrypted RGSW root-index bits from RLWE y'∈mu8 still requires a genuinely supported secure conversion; none is supplied. No native fixed-Q DFR or meaningful runtime/key/memory advantage is evidenced. Source-independent gain is an algebraic removal of one exceptional branch, not a novel core selector mechanism.
Closest prior art: classic domain-offset/phase guardband programming of lookup tables; B176 standard CMux and scheme-switch cost audit; published TFHE PBS LUT phase/error guardbands and programmable test vectors (e.g. sources https://www.iacr.org/archive/asiacrypt2021/130900334/130900334.pdf and https://eprint.iacr.org/2024/1376.pdf). Prior art does not conclusively prove exact delta64 B175 setting was published; NOVELTY_STATUS=PREFLIGHT not CLEAR or proven COLLISION.
No new independent algorithmic contribution or complete noise certificate has been demonstrated. The saved B176 scheme-switch family remains closed; this conditional public-offset optimization DOES NOT satisfy its necessary novel low-cost conversion and whole-value reopening conditions.
Therefore FAIL_STANDALONE_PAPER_VALUE / PARKED; CONDITIONAL_SEMANTICS_PASS_MATH. No pending native/Codex tasks, no parameter changes.

## Decision / named uncertainty and reopening
GATE1: PASS_MATH conditional on S63 and public LUT-variable translation; full source-authenticated legal-domain/whole-output carry semantics UNKNOWN.
GATE2: Stock arithmetic scalar addition possible in principle, but exact pre-LT offset placement and 3-bit RGSW selector conversion/keys remain UNKNOWN/BLOCKED.
GATE3: One CMux layer and zero selector potentially saved vs already archived standard CMux, but no verified positive all-in value or independently distinct novelty; PAPER_VALUE_FAIL for the standalone offset alone.
STATUS=PARKED; NEW_MECHANISM=NO_CREDIBLE_NEW_MECHANISM as standalone paper mechanism. REOPEN_CONDITION: A source-authenticated legal input/DFR domain excluding -64, complete typed input translation and F_delta polynomial compilation with original full output (including zero original phase), a NEW nonstandard low-cost three-bit selector conversion/key mechanism that demonstrably crosses a meaningful whole-system cost/security/DFR frontier, and independent novelty audit. A phase shift alone does not reopen standard CMux.
ELIMINATED_UNCERTAINTY: Under exact conditional S63, can one public phase translation make all encoded phases nonzero while preserving the original arbitrary polynomial LUT through offline variable translation? YES; can this standalone step establish a publishable fixed-Q B158 replacement? NO, source domain/conversion/DFR and actual value remain missing.
DECISION_CHANGED=true: newly screened candidate PARKED, standard zero-flag cost distinguished but not resurrected. research_frontier_exhausted=false.
