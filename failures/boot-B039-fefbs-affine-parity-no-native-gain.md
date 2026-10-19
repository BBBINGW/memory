# BOOT-B039 failure archive — Affine-odd symmetry is already implicit in Sigmoid FEFBS, and GeLU's affine part cannot be removed across unknown HalfBTS lift

TRACK_ID BOOT
ITERATION B039
DATE 2026-10-20
STATUS FAIL_NEW_SOURCE_ONLINE_EVALPOLY_SAVING / FAIL_FREE_GELU_AFFINE_EXTRACTION / PASS_REFLECTION_SYMMETRY
STATE_UPDATE YES
SHIP PAUSED_BY_PI; no cross-track changes.

Original work: Bian et al. EUROCRYPT26 ePrint2026/367 "High-Precision Functional Bootstrapping for CKKS from Fourier Extension"; 43pp title-verified full research-MCP PDF sha256 ee2384e0a8148a0678b3fdb0e0d14eb5f988f19750a94081a378e8fb82966e7a VERSION_UNVERIFIED; physical p23 Alg2/Eq43–45 positive-power complex Fourier EvalSeries, p24 claims generic input occupancy rho>N/4 leads to TExp+2TFourier while odd/even Fourier target enables TExp+TFourier. Original AUTHORS code https://github.com/FYHSSGSS/FEFBS:
  * coeffs/sigmoidcoeff.txt blob 27dd4722b6c830a8b44ba1c1b6611a8b66d9c688 degree34 constant0.25, max abs positive harmonic cosine coeff2.7118e-15, L1 sum cosine1.28321e-14, L2 cos3.92285e-15, L2 sin0.305115.
  * coeffs/gelucoeff.txt blob e644434987b05bd6c5d04f26a44067592dffe419 degree44 has cosine L2 1.604 and sine L2 2.713; expcoeff.txt blob 5a6b7ced3eaaaff2d0470a934cb3134bff1e5764 similar mixed.
  * src/pke/lib/scheme/ckksrns/ckksrns-fhe.cpp blob e76f897827ee49f9092ecebafe6f5fe611abd6e8 EvalFEFuncBootstrap lines1147–1153 ALREADY calls cc->EvalPoly(ctxtExp,coefficients) exactly ONCE for both generic and symmetric target, then Conjugate and adds output +2a0; it does not branch into two EvalPoly calls. Source high-occupancy cost gain from mathematical parity therefore does not imply any fewer actual native polynomial evaluations without changing internal packing/layout and benchmarking.
  * author sigmoid_test.cpp blob23c0b35708b68ff60338b2a298e883436386f632 target original f=1/(1+exp(-x)) interval[-8,8], n34, nslots32768; gelu_test.cpp blob e568345ba106a849a16fab0e43b2216257c9738b uses x/2*(1+tanh(sqrt(2/pi)*(x+.044715x^3))) interval[-8,8].
  * original numeric Hermite coefficient generation in fourier_calculator.py blob 9ddf9dbe0a9ae055423fcff398356991de624178 pre-scales target by 1/2; sigmoid constant0.25.
No native compile/runtimes or complete CKKS noise/2^-128 DFR tests.

Positive lemma: On symmetric [-T/4,T/4], if f(-x)+f(x)=2c, subtract c to obtain odd g. The unique Hermite polynomial bridging endpoint derivatives at T/4 and3T/4 obeys H(T-x)=-H(x) by reflection plus matching derivatives, so periodic extension of g is odd and ALL positive cosine Fourier coeffs mathematically vanish. Sigmoid is c=.5. Source literal coefficients confirm cosine L2/sine L2 ~1.2857e-14; zeroing their numerical residual changes source 2Re Fourier output by <=2 sum|a_k|=2.5664e-14 (~45.15bits), but cannot reduce polynomial degree or ciphertext multiplications. Exact SymPy toy k=1,2,3,4 unique Hermite bridges with g(x)=x on [-1/4,1/4] give P(x)+P(1-x)=0 exactly 4/4; for k2 P(x)=(2x-1)(8x²-8x+1). Script /tmp/boot_b039_symmetry.py SHA256 98f602e85d1dd587223a9494448fe03f1a0a322817aa8cd69901f4a5275939b3.

Naive broader repair COUNTEREXAMPLE: Original author's tanh-GeLU satisfies GeLU(-x)=GeLU(x)-x, so GeLU(x)-x/2 is even, but x/2 is NONPERIODIC. The HalfBTS stage outputs y=σ(m)+I with unknown integer I; exp(2πi y) and periodic Fourier approximation cannot distinguish y and y+1, while x/2 differs .5. Taking x=.2 and I=0/1 yields exact .5 false offset if simply evaluating even periodic part + y/2. Need an extra carry/modular correction or full separate bootstrapping, not free parity exploitation. Authors' original direct Fourier eval is not incorrect.
Original paper already documents even/odd cases, and source sigmoid polynomial is already pure sine; generic affine odd constant handling is elementary. No paper-ready nontrivial new Bootstrapping algorithm, runtime speedup or changed evaluation key format. Archive after B039, do not overexplore activation symmetry.

FINDING findings/boot-B039-fefbs-affine-odd-fourier-symmetry-source-cost-gate.md
NEXT_TEST B040 (not initiated): one potentially more substantial source-co-design hypothesis: optimally allocate numerical precision/depth across online fixed TrigTransform exp approximation (EvalChebyshevSeries + double angle r) and per-function EvalSeries polynomial using sensitivity bound sum k|ck|. Need test actual kernel multiplication/depth savings, full Fourier+CKKS error and prior art; do NOT claim novel if source's existing env overrides/parameter tuning already cover. Only BOOT, SHIP remains paused. STATE_UPDATE YES.