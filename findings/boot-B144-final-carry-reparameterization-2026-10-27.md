# BOOT-B144 — Final-carry reparameterization for kappa=0 arbitrary-modulus A2D

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Primary source: supplied ePrint 2026/1869
- Supporting prior-art screen: ePrint 2026/2368 abstract-level only
- Status: COMPLETE
- Decision: PASS_ALGEBRA / HIGH-POTENTIAL / NEEDS IMPLEMENTATION-LEVEL COST VALIDATION
- CODEX_REQUIRED: NOT YET

## Target

Section 5.2 / Appendix C.1 of 2026/1869 converts an arithmetic polynomial to radix digits by:
1. first FBS: radix remainders and quotients;
2. forming a_j;
3. second multi-value FBS for every public candidate lambda in
   Lambda={-K_I,...,floor((M-1)/b^d)+K_I};
4. logarithmic carry composition for each lambda;
5. checking candidates and selecting the smallest valid lambda.

For kappa=floor(m/b^d)=0 (equivalently M <= b^d for every represented m), the paper itself gives
q_{ell-1}=c_ell-I'_{d-1}
and lambda=I'_{d-1}.
Therefore

    lambda = c_ell - q_{ell-1}.

The original algorithm still parameterizes the whole second FBS and carry circuit by the much larger static set Lambda.

## Reparameterization

Let g be a public candidate for the FINAL carry c_ell, and let q=q_{ell-1}, which is already encrypted after the first FBS.

For a candidate g define the encrypted value

    lambda_g = g - q.

The original local carry map is

    f_{j,lambda}(c) = ceil((c - a_j - lambda*alpha_j)/B_j).

Substituting lambda_g gives

    f_{j,g}(c)
      = ceil((c - a_j - alpha_j(g-q))/B_j)
      = ceil((c - (a_j-alpha_j q) - alpha_j g)/B_j).

Hence broadcast q to the radix slots and form, using linear operations only,

    a_tilde_j = a_j - alpha_j q.

The second FBS can now be indexed by g in the small final-carry set G rather than by lambda in Lambda. For each g it evaluates the carry-transition functions on a_tilde_j and one validity bit

    1[-K_I <= g-q <= K_I]

at the final slot.

After composing the carries for candidate g, accept g iff:
1. the computed final carry equals g (fixed-point/self-consistency), and
2. g-q is inside the allowed overflow bound.

Select the smallest valid g.

## Correctness equivalence

For kappa=0, there is a bijection between valid original lambda candidates and valid new g candidates:

- Original -> new:
  if lambda is valid and its carry path ends at g=c_ell, the original candidate check requires
  lambda=c_ell-q=g-q. Therefore the same path is exactly the path evaluated by candidate g and is self-consistent.

- New -> original:
  if candidate g is self-consistent and lambda_g=g-q lies in [-K_I,K_I], then lambda_g satisfies the original final check and has exactly the same carry path.

Because q is common to all candidates, lambda_g is strictly increasing with g. Therefore selecting the smallest valid lambda is exactly equivalent to selecting the smallest valid g. The original uniqueness/correctness argument then applies unchanged.

A 10,000-case randomized synthetic test over small radix systems compared the complete valid-candidate sets of the two formulations and obtained 10,000/10,000 exact matches.

## P-384 concrete count at b=2, B=32

From 2026/1869:
- d=384;
- p384 < 2^384, so kappa=0;
- OverflowRefresh gives K_I=17;
- ell=ceil(384/5)=77;
- last radix width h=4, so B_last=16;
- defining polynomial
  F384=X^384-X^128-X^96+X^32-X^2+3.

For the block coefficients
alpha_j=sum_{r=0}^{s-1} 2^r f_{5j+r},
only four nonzero values occur:

    (j,alpha_j)=(0,-1),(6,4),(19,-2),(25,-8).

The general carry bound in Appendix C gives the global carry set
C={-5,...,5}, |C|=11.
At the final block alpha_76=0 and B_last=16, so any valid final carry lies in

    G={-2,-1,0,1,2}, |G|=5.

Original candidate set:
    Lambda={-17,...,17}, |Lambda|=35.

### Second-FBS output width

Appendix C.2 states that for kappa=0 the original second FBS returns

    |Lambda| (|C|^2 + |C|)

ciphertexts (carry indicators plus candidate checks).

P-384:
    35*(121+11)=4620 outputs.

Reparameterized form:
- |G||C|^2 transition outputs;
- one overflow-range check per g.

    5*121+5=610 outputs.

Reduction:
    4620 -> 610 = 7.57x fewer output functions/ciphertexts.

### Carry-composition multiplications

Appendix C.2 uses |Lambda||C|^3 CMults per carry-composition level.
For ell=77, H=ceil(log2 77)=7:

Original:
    7*35*11^3 = 326,095 CMults.

Reparameterized:
    7*5*11^3 = 46,585 CMults.

Reduction:
    exactly 7x.

This excludes smaller candidate-selection savings, so it is a conservative structural comparison.

## Relation to 2026/2368

The public abstract of 2026/2368 already kills the generic novelty claim
"one bootstrap extracts all radix digits in parallel using carry look-ahead."
B144 is different: it targets the global lambda-candidate explosion specific to the arbitrary-modulus polynomial conversion of 2026/1869. The reparameterization uses the final quotient relation of that construction and does not follow from the abstracted scalar digit-decomposition claim.

Full 2026/2368 remains source-gated and must be audited before any publication-level novelty claim.

## Limits

- The clean reduction above requires kappa=0, i.e. M <= b^d.
- It therefore applies directly to all P-384 defining-polynomial choices in 2026/1869 and to the Curve25519 choices b=4,8,16, but NOT to their b=2, d=254 Curve25519 representation where kappa in {0,1}.
- No matched runtime is available because 2026/1869 benchmarks only the Boolean-output specialization, not this general P-384 A2D path.
- The second FBS may still be expensive at 610 outputs; B144 does not yet establish a practical runtime win.

## Next falsification

Exploit the highly nonuniform per-block carry ranges and sparse alpha_j of P-384:
- 72 ordinary nonfinal blocks have carry range {-1,0,1};
- only four alpha-exception blocks expand the range;
- the final block has {-2,-1,0,1,2}.

Test whether the global |C|=11 indicator-matrix composition can be replaced by variable-size/segmented carry maps without changing depth. This is potentially multiplicative with B144 and may be necessary to make the general P-384 conversion practical.
