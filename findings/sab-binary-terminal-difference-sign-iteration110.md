# I110 — Printed sparse SAB terminal-difference sign audit

Date 2026-10-12. PRIMARY: Antonio Guimarães and Hilder V. L. Pereira, Fast amortized bootstrapping with small keys and polynomial noise overhead, CCS2025, IACR ePrint 2025/686, https://eprint.iacr.org/2025/686 . Research MCP full 34-physical-page PDF, mirror SHA256 84b694a59fe50dc0062ff9f24bd26f1a9cdc335b5ef9becae36aad83362cd335, revision 29f9da07b541e562a94af168cef80c29a8b3fb2d, official VERSION_UNVERIFIED. Printed formula extraction may lose mathematical symbols: repeated at physical pp12 and21 and consistent with displayed Eq(3) p13; direct rendered-PDF visual confirmation unavailable, so a sign transcription error cannot be categorically excluded.

STATUS: PASS mathematical counterexample to the literal extracted printed definition + Algorithm2/Eq(3); UNKNOWN actual implementation correctness; NOT a cryptographic attack or novel FHE improvement.

## One technical hypothesis and minimal falsifier
[FACT] Section4 physical p12 before Algorithm2 defines a binary sparse secret s(Y)=sum_i Y^(j_i), strictly ordered j_0<...<j_(h-1), and its diff(s) by d0=-j0, d_i=j_(i-1)-j_i for 1<=i<h, and final d_h=-j_(h-1). Eq(3) physical p13 writes the Horner evaluation with multiplication by each Y^(d_i), subtracting a at the first h stages, claiming to equal r(Y)=b(Y)-a(Y)s(Y) in R_Y=Z[Y]/(Y^n+1). Lemma4.1 physical p14 asserts Algorithm2 outputs encryptions of the coefficients of r, with independent LUT test vectors. Paper §6.1 physical p21 REPEATS final negative d[h].
HYPOTHESIS: the literal displayed d values + Horner recurrence compute r for all noiseless polynomial messages.
FALSIFIER: find a,b,s under simple negacyclic ring whose output differs from b-as even granting an exact ideal monomial-multiplication subroutine.

## Symbolic contradiction [DERIVATION]
Sum of literal shifts telescopes to -2 j_last:
 d0 + sum_(i=1)^(h-1)(j_(i-1)-j_i) + d_h = -2*j_last.
Expanding the Horner recurrence gives out=(b-a*s) Y^(-2 j_last) in the negacyclic quotient. This is not generally b-as. Change ONLY the last shift to d_h=+j_last and the same Horner recurrence becomes EXACTLY b-as for all h, a, b, and ordered j positions. Interpretation of negative exponents uses Y^(2n)=1.

## One exact toy [TEST]
n8; h1, s(Y)=Y; a(Y)=1; plaintext m(Y)=1; b(Y)=Y+1; encryption error zero. The literal source d=(-1,-1) yields
 (b*Y^-1-a)*Y^-1 = (1+Y^-1-1)*Y^-1=Y^-2=-Y^6, not m(Y)=1, constant coefficient 0 instead of 1.
Using d=(-1,+1) gives (b*Y^-1-a)*Y=1. Additional h1 and h2 examples and 35 deterministic n8/h1 test vectors confirm exact derived wrong shifted output and corrected recovery. The actual MPmul binary API needs an unsigned encoding of negative exponents; even granting ideal signed monomial shift this contradiction holds.

## Pinned author C code [FACT & LIMIT]
Public author GitHub repository https://github.com/antoniocgj/Fast-Amortized-Bootstrapping pinned commit 8938ab5bd42a80c93ed5ee4caef36efbb01bf7ef (2026-08-17; includes unrelated rejection-sampling fix). File src/sparse_amortized_bootstrap.c blob SHA b86d4d7f8f578665196a94dd6a2c9ca155f8bde7: keygen lines146–185 starts previous=in_N, traverses secret positions DESCENDING, stores positive differences previous-current, and a final positive previous; sparse_mul lines283–301 applies each RGSW_monomial_mul; setup test vector lines330–355 uses a potentially shifted LUT phase convention. The C scheduling differs from the printed increasing-position d definition, so there is NO demonstrated corresponding Go/C code bug, ciphertext failure, practical exploit, or failure of authors' benchmarks. Source Theorem/Lemma scope refers to its printed algorithm, but C might realize an equivalent corrected algorithm with a global sign/phase adjustment.

## Scope and next cheapest test
[RESULT] A likely local printed sign error, not a nontrivial new primitive. Neither the complete source PDF sign fidelity (visual page unavailable) nor the actual C end-to-end behavior is fully certified, so do NOT claim the paper theorem is fundamentally broken.
[NEXT_TEST I111] Check ONE exact code-inspired descending-key schedule and its global sign/offset relative to the test vector, on n8 h1; determine if actual C code sidesteps the printed terminal sign. If yes, archive as low-value paper notation inconsistency and pivot; do not proceed to broad benchmark or contact the authors.

Reproducer /mnt/data/iteration110_sparse_SAB_terminal_shift.py SHA256 67d39a2376a0201ae29d2ea530da9b1a5c43bd9c856851cbbe90419716f12a6c; JSON /mnt/data/iteration110_sparse_SAB_terminal_shift_results.json SHA256 76ebba87b023bb3922a0623dfeee33090a0cbb81f1306697fce8ed70f2699dfa. Tested exact negacyclic integers; no encryption execution.
END OF ITERATION: STATUS PASS printed-algebra falsifier; IMPLEMENTATION UNCLEAR; NOVELTY LOW. NEXT_TEST I111 one code schedule sign check. STATE_UPDATE YES. No outreach/public disclosure.
