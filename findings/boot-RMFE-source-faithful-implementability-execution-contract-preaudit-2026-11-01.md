# BOOT RMFE Source-Faithful Implementability / Execution-Contract Pre-Audit

Date: 2026-11-01
Session: 密码学 17.0
Logical Research Turn: 14/25
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Pending native task boundary

Authorized native task:

\`BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01\`

remains UNKNOWN / BACKGROUND.

This turn does not:
- inspect or assume its result;
- modify its source/workdir/binary;
- resubmit it;
- start another heavy native task.

## Read-before-write authority

Current durable authority at turn start:

\`BBBINGW/memory main@010a1d9e68dd9c26c64715c67425ff823739be78\`.

Relevant durable prerequisites:
- Turn 4 paired same-machine native-gate contract;
- exact recrypt-key handle / linear-form gate;
- rawModSwitch carry/fusion gates;
- exact scaling boundary;
- BSGS+10 keyset contract.

## Primary hypothesis

The current candidate can be implemented source-faithfully from HElib/Aung state without:
- inventing a surrogate ciphertext;
- regenerating a fresh boot-key encryption;
- reading the secret key during evaluation;
- reconstructing hidden branch semantics approximately.

Falsifier:
the required exact intermediate state is inaccessible except through cryptographically different substitutes or secret-key-only operations.

A secondary implementation question is whether this can be done as an **unmodified external application using only existing public HElib APIs**.

## Pinned source

HElib base revision:

\`homenc/HElib@acdb264e1a991eaee35fd8b3c31bebe9528c49a1\`.

Relevant declarations/source:
- \`include/helib/Ctxt.h:1254\`: public \`reLinearize(long keyIdx)\`;
- \`include/helib/Ctxt.h:1327-1335\`: public \`rawModSwitch(...)\`;
- \`include/helib/keys.h:67-70\`: private \`recryptKeyID\`, private \`recryptEkey\`;
- \`include/helib/keys.h:230-233\`: public \`PubKey::reCrypt/thinReCrypt\`;
- \`include/helib/keys.h:235\`: \`SecKey\` is friend of \`PubKey\`;
- \`include/helib/keys.h:411-418\`: \`SecKey::genRecryptData()\` returns the recryption-key ID and \`getRecryptKey()\` returns the secret recryption key;
- \`include/helib/recryption.h:36-65\`: public \`RecryptData\` fields including \(e,e'\), \`p2dConv\`, maps, and plaintext-space data;
- \`src/recryption.cpp:69-136\`: file-static \`newMakeDivisible\`;
- \`src/recryption.cpp:1035-1099\`: stock thin rawModSwitch / divisibility / \`recryptEkey\` reconstruction.

Aung ePrint 2025/350 references pinned HElib commit \`acdb264\` but the inspected ePrint text contains no source-code/artifact repository link. Targeted GitHub search in this turn did not identify an obvious public implementation repository. This is absence-of-discovery, not proof that no artifact exists.

## 1. Branch raw state is publicly obtainable without patching Ctxt internals

The candidate requires, for each split branch:

\[
\text{S2C}
\to
\text{reLinearize}(R)
\to
\text{rawModSwitch}
\to
(z_{i,0},z_{i,1}).
\]

HElib exposes:

\[
\texttt{Ctxt::reLinearize(long)}
\]

and

\[
\texttt{Ctxt::rawModSwitch(vector<ZZX>&, long)}
\]

as public methods.

Therefore an application can obtain the exact two raw integer-polynomial channels without:
- reading \`Ctxt::parts\`;
- accessing secret-key polynomials;
- modifying rawModSwitch;
- approximating the branch representative decisions.

The stock thin path itself asserts exactly two raw parts.

Thus the nonlinear branch boundary needed by the candidate is an actual accessible state.

## 2. recryptKeyID is not a cryptographic hidden-state blocker

\`PubKey::recryptKeyID\` is private.

However:
- \`SecKey::genRecryptData()\` publicly returns that ID at key-generation time;
- the ID is only an index identifying the bootstrapping secret-key handle;
- it is not secret key material.

A benchmark setup that generates the keys can record the returned integer and use it for the branch

\[
\texttt{reLinearize(recryptKeyID)}
\]

calls.

For a clean evaluator-only API after deserialization, an internal/public getter would be preferable, but no cryptographic surrogate is required.

Therefore:

\[
\boxed{
\texttt{recryptKeyID private visibility is an API issue, not a semantic blocker.}
}
\]

## 3. Exact carry/divisibility processing does not require hidden secret state

The current candidate can materialize all branch raw \`ZZX\` outputs and compute the public carry from those realized integers.

It therefore does **not** require access to the internal per-branch pre-output rounding variables \(x_i,\delta_i,t_i\).

For odd \(p=5\), the exact aggregate divisibility map is determined by:
- public \(p,e,e'\);
- \(q=p^e+1\);
- public raw integer polynomials;
- the public powerful-basis converter.

The needed \`RecryptData\` members \(e,e'\) and \`p2dConv\` are public.

However, HElib's exact helper

\[
\texttt{newMakeDivisible}
\]

is a file-static function in \`recryption.cpp\`, so an external wrapper cannot call that exact implementation by name.

Two source-faithful options exist:

### Preferred option
Implement the candidate aggregate preprocessing inside \`recryption.cpp\` / a \`PubKey\` member and reuse the exact static helper.

### Acceptable but more fragile option
Copy the exact \`newMakeDivisible\` logic into candidate code using the same public \`RecryptData\`, powerful-basis conversions, balanced residues, and \(p=5\) semantics.

This is not a hidden-state problem.

For reproducibility, the first option is preferable.

## 4. Exact common reconstruction is the one genuine public-API obstruction

Stock HElib reconstructs:

\[
\texttt{ctxt = recryptEkey;}
\]
\[
\texttt{ctxt.multByConstant(zzParts[1]);}
\]
\[
\texttt{ctxt.addConstant(zzParts[0]);}
\]

inside the \`PubKey\` member implementation.

But in the pinned header:

\[
\texttt{recryptEkey}
\]

is a **private \`PubKey\` member**, with no public getter found in the pinned interface.

Therefore an unmodified external application cannot perform the exact one-copy reconstruction using the existing boot-key ciphertext.

This is decisive:

\[
\boxed{
\text{UNMODIFIED PUBLIC-API-ONLY CANDIDATE IMPLEMENTATION = FAIL}.
}
\]

Using any of the following would violate the Turn-4 scientific contract:
- freshly encrypting the recryption secret into a new ciphertext;
- using a dummy one-part ciphertext;
- reconstructing from a separately generated surrogate;
- using the secret key to synthesize an equivalent runtime state.

Those change the exact noise/randomness/runtime semantics.

## 5. Minimal exact patch is straightforward and evaluator-only

The obstruction above does **not** require a new cryptographic construction.

A minimal HElib-internal candidate method can run as a \`PubKey\` member (or modify/factor the existing thin-recryption preprocessing) and therefore legally access the existing private:

- \`recryptKeyID\`;
- \`recryptEkey\`.

It can then perform exactly:

\[
\texttt{ctxt = recryptEkey;}
\]
\[
\texttt{ctxt.multByConstant(B);}
\]
\[
\texttt{ctxt.addConstant(A);}
\]

with the same boot-key ciphertext used by stock HElib.

No secret-key polynomial is needed at evaluation time.

This patch may also reuse the file-static \`newMakeDivisible\` directly if placed in \`recryption.cpp\`.

Thus:

\[
\boxed{
\text{SOURCE-FAITHFUL INTERNAL IMPLEMENTATION = PASS}.
}
\]

The minimal implementation change is an API/control-flow exposure, not a semantic substitute.

## 6. No Ctxt private-part mutation is required

After exact reconstruction, all current recovery operations are available through ordinary ciphertext APIs:

- \`frobeniusAutomorph\`;
- \`smartAutomorph\` / key switching;
- \`multByConstant\`;
- ciphertext addition/copy;
- existing DigitExtract logic.

The candidate need not directly construct arbitrary \`CtxtPart\` objects or forge \`SKHandle\` metadata.

This is important because manually assembling private ciphertext parts would create a large execution-contract risk.

The exact reconstruction can preserve stock metadata by copying the real \`recryptEkey\` object and using the same public operations as stock thin recryption.

## 7. BSGS+10 generation is a setup-side patch, not runtime hidden state

The ten direct RM10 matrices are generated using ordinary HElib:

\[
\texttt{GenKeySWmatrix(1,u,0,0)}
\]

via \`addTheseMatrices\` / equivalent setup code.

This requires \`SecKey\` during key generation, exactly as all evaluation-key generation does.

Runtime evaluation then uses only the resulting public/evaluation key.

This does not violate evaluator-only semantics.

The paired contract still requires the **same BSGS+10 keyset** for:
- thin;
- stock Corr./TnM;
- candidate.

## 8. Consequence for the pending native artifact

A candidate result should **not** be rejected merely because the binary is based on a patched HElib tree.

A patch is actually necessary for a clean exact implementation unless the local Aung fork already exposes equivalent access.

The correct audit question is:

> Does the patch only expose/reuse the exact stock public-key preprocessing state, or does it alter cryptographic semantics?

### Allowed implementation patterns

- add a \`PubKey\` method/getter that exposes the existing \`recryptEkey\`;
- factor stock thin preprocessing into a reusable internal helper;
- add an aggregate-post-raw method inside \`recryption.cpp\`;
- reuse exact stock \`newMakeDivisible\`;
- preserve stock \`rawModSwitch\` unchanged;
- preserve the exact same generated \`recryptEkey\` and evaluation-key set;
- compile thin and stock comparator workflows from the same patched binary.

### Execution-contract failures

Return

\[
\texttt{FAIL_EXECUTION_CONTRACT}
\]

if the artifact instead:
- generates a fresh replacement for \`recryptEkey\`;
- decrypts/re-encrypts intermediate state;
- uses \`SecKey::getRecryptKey()\` during timed/evaluator execution to synthesize candidate state;
- substitutes a fresh-thin or dummy ciphertext;
- skips branchwise rawModSwitch;
- modifies rawModSwitch rounding semantics;
- uses different evaluation-key samples for candidate and comparators;
- benchmarks comparators from a materially different binary/configuration;
- manually forges Ctxt metadata rather than reusing the real boot-key ciphertext.

## 9. Reproducibility requirement created by this audit

Because exact candidate implementation requires an internal HElib patch, reporting only

\`HElib acdb264\`

is no longer sufficient provenance.

The eventual native artifact must identify:

1. upstream base:
   \[
   \texttt{acdb264e1a991eaee35fd8b3c31bebe9528c49a1};
   \]
2. candidate patch commit/diff hash;
3. exact files/functions changed;
4. confirmation that stock \`rawModSwitch\`, key generation, and comparator algorithm bodies are unchanged except for shared instrumentation/hooks;
5. same final binary or same patched source tree for all three paired workflows.

If this provenance is missing, the benchmark may still be suggestive but is not sufficient for a scientific PASS.

## 10. Aung artifact boundary

The inspected ePrint:
- states that the implementation uses HElib commit \`acdb264\`;
- describes the algorithms and measurements;
- does not expose an implementation/source repository in the extracted text.

Targeted GitHub search did not find a clear public source repository for the paper.

Therefore this turn cannot verify whether Aung's own private/local implementation already contains an equivalent internal hook.

The pending local task may have such source; its result must report that provenance rather than assuming public reproducibility.

## Verdict

\`\`\`text
RESULT:
  PASS_SOURCE_FAITHFUL_INTERNAL_IMPLEMENTABILITY
  FAIL_UNMODIFIED_PUBLIC_API_ONLY_IMPLEMENTABILITY

BRANCH_RELINEARIZE:
  PUBLIC API

BRANCH_RAWMODSWITCH:
  PUBLIC API

RAW_TWO_CHANNEL_STATE:
  DIRECTLY ACCESSIBLE / NO PRIVATE Ctxt PARTS NEEDED

RECRYPTDATA_E_EPRIME_P2DCONV:
  PUBLIC

NEWMakedivisible:
  FILE-STATIC
  INTERNAL REUSE OR EXACT COPY REQUIRED

RECRYPTKEY_ID:
  PRIVATE IN PubKey
  BUT RETURNED BY genRecryptData AT KEYGEN

RECRYPTEKEY:
  PRIVATE IN PubKey
  NO PUBLIC GETTER FOUND
  MINIMAL INTERNAL HOOK REQUIRED

SECRET_KEY_NEEDED_AT EVALUATION:
  NO

FRESH_SURROGATE_RECRYPTEKEY:
  FORBIDDEN

DUMMY/FRESH-THIN SURROGATE:
  FORBIDDEN

DIRECT CtxtPart/SKHandle FORGING:
  NOT REQUIRED / SHOULD NOT BE USED

MINIMAL_HELIB_PATCH:
  REQUIRED UNLESS LOCAL FORK ALREADY EXPOSES EQUIVALENT HOOK

PATCH_SEMANTICS:
  CONTROL-FLOW/API EXPOSURE ONLY
  MUST REUSE EXACT EXISTING recryptEkey

PAIRED_COMPARATOR_BINARY:
  SAME PATCHED SOURCE/BINARY REQUIRED

AUNG_PUBLIC_SOURCE_ARTIFACT:
  NOT IDENTIFIED IN THIS AUDIT

PENDING_NATIVE_TASK:
  BOOT-RMFE-CURRENT-PAIRED-THROUGHPUT-NATIVE-20261101-R4-01
  UNKNOWN / DO NOT TOUCH

CANDIDATE:
  IMPLEMENTABLE
  EXECUTION-PROVENANCE AUDIT REQUIRED

RESEARCH_FRONTIER_EXHAUSTED:
  false
\`\`\`

## Scientific disposition

There is no hidden-state impossibility blocking the current candidate.

But there is a concrete reproducibility fact that must not be blurred:

> the exact one-reconstruction candidate needs access to the real HElib \`recryptEkey\`, which stock public application APIs do not expose.

The scientifically clean implementation is therefore a small HElib-internal evaluator-side patch that reuses the exact existing boot-key ciphertext and stock preprocessing helpers.

When the pending native result arrives, the first audit must verify this patch boundary before interpreting latency/capacity numbers.
