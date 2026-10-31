# BOOT Orchestrator self-healing reconciliation — 2026-10-31

## Incident

The `密码学 15.0` logical session diverged at database Turn 21 while the legacy ChatGPT conversation contained complete, durably persisted scientific bodies for Turns 22 and 23. Both historical bodies lacked a valid control envelope, and repeated control-only generation attempts ended in ChatGPT `Unknown error` / `无法加载此回复`. A replacement ordinary Chat also failed to generate the historical control envelopes.

## Verified recovery

- Legacy conversation evidence was preserved and frozen; no completed scientific body or native experiment was regenerated.
- Turn 22 (`assistant@2345e905`) and Turn 23 (`assistant@569fd44b`) were reconciled exactly once from their original bodies and durable persistence evidence.
- Deterministic control reconstruction was limited to complete, tool-complete, durably persisted bodies with no hard-stop, `WAIT_PI`, `STOP`, or `EXECUTE` marker, under continuous-autonomous policy with no pending PI decision.
- Database progress advanced contiguously from 21/25 to 23/25.
- The same active physical conversation `6ae55e69-e060-83ec-ac7e-6467a0f24feb` received the substantive Turn 24 prompt with idempotency key `continue:ac423144-d459-486f-aca9-738a4f452637:24`.

## Root causes and permanent guards

1. Historical reconciliation depended exclusively on new control generation. It now has a bounded, evidence-gated deterministic recovery path after the generative repair budget is exhausted.
2. Restart recovery treated an in-flight status as proof that a prompt had been sent. It now checks durable `pending_research_prompt`; a missing prompt is self-healed by an idempotent send for the same next logical turn.
3. Exactly-once reconciliation now updates `body_complete`, `control_valid`, durable persistence, and counted state together.
4. A reasoning-only UI readback such as `思考强度 Extra High` no longer causes a false model mismatch when the ordinary-Chat creation certificate proves GPT-5.6 Sol. Explicit conflicting model evidence still blocks.
5. `surface=unknown` remains revalidation state, never positive Work evidence.

## Validation

- TypeScript typecheck passed.
- Full regression suite passed: 89/89.
- Production build passed.
- Bridge 0.2.0 returned GET_HISTORY and a verified Turn 24 SEND_MESSAGE receipt.
- Research policy remained ordinary Chat / GPT-5.6 Sol / Extra High with zero API billing.

