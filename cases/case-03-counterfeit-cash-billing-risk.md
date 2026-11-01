# CASE 003 — Alleged counterfeit-cash acceptance and subscription-payment laundering risk

**Classification:** Unverified user-reported historical scenario. Defensive research only.  
**Safety boundary:** Fictional data, simulated events, no real bank, ATM, payment, messaging, printing, shipping, or P2P integration. This is not a laundering or counterfeiting playbook.

## Executive summary

The narrator describes a purported operation involving high-precision counterfeit US-dollar banknotes with an alleged face value of **USD 6 million**, claimed international circulation and purported use of postal or diplomatic channels. The narrative further alleges that an unidentified **US bank (“Bank N”) accepted only part of the presented cash and incurred substantial losses**. A subsequent claimed stage associates account-linked phone numbers with automated recurring billing through applications supporting payment processing and P2P transfers.

**All of these assertions remain unverified.** No country, manufacturer, bank, diplomat, transaction, loss, account, or criminal conduct has been independently established. No implication that diplomats or a real identifiable bank were actually involved should be drawn from this narrative.

Importantly, USD 6 million is a **claimed nominal face value**, not a confirmed amount deposited, credited, laundered or lost.

## Critical uncertainty: alleged Bank N loss

The narrative does not establish:
- the amount of cash presented, accepted, detected or rejected;
- whether the bank credited any funds before an authenticity finding;
- whether purported losses represent credit reversal, unrecovered settlement exposure, fraud reimbursement, operational costs or another category;
- the timing, source, and independent documentation of the asserted loss.

**Accounting distinction:** Claimed face value != accepted cash != credited balance != realized loss. A bank's receipt of suspicious notes does not, by itself, establish the size or existence of a realized financial loss.

## Defender-facing risk boundaries

| Area | What investigators / monitoring teams should assess |
|---|---|
| Cash acceptance | Authenticity-testing controls, unresolved machine exceptions, incident reporting and reconciliation |
| Deposit accounting | Crediting and reversals, proof of loss, audit events and unresolved provenance |
| Recurring payments | Genuine payer authorization, merchant identity, repeated charges, disputes and refunds |
| Platform / P2P flows | Economic substance, beneficial ownership, abnormal concentration and traceable settlement |
| Alleged international movement | Independently verified evidence and applicable jurisdictional authority |

## Synthetic research model

A closed-loop local test may use imaginary accounts and synthetic balances to represent **control outcomes**, not executable laundering stages.

Example simulation records:
- `cash_control_review`: synthetic incident ID, result, hypothetical declared amount, supporting evidence flag.
- `credit_review`: simulated ledger ID, original source tag, reconciliation status, decision.
- `billing_consent_review`: consent validity, mandate status, dispute indicator.
- `merchant_risk_review`: onboarding completeness, charge dispute ratio and source-of-funds traceability.
- `case_alert`: rule ID, severity, evidence references and reviewer decision.

Invariants:
1. No real-world currency, bank accounts, identities or instruments.
2. No issuance of actual counterfeit cash or detailed manufacturing/transport/placement workflows.
3. Cash-origin risk tags survive all simulated accounting transitions.
4. Billing authorization is explicitly reviewed; a phone-number association alone is not proof of consent.
5. Every simulation state transition produces an immutable audit entry.
6. An alleged loss is never computed as accepted cash or the nominal USD 6 million without documented evidence.

## Detection and QA evaluation

Test anomaly alerts on fictional labeled incidents, including legitimate lookalikes. Track precision, recall, false-positive rate, detection latency, audit-trail completeness and exception-resolution quality. Use defensive test cases to assess both unauthorized billing and banknote-authenticity failures.

## Evidence to request (redacted and non-operational)

Approximate historical period; public source for the alleged claim; whether Bank N is a pseudonym; verified figures for presented vs accepted notes and any realized loss; public regulatory or court records if available. Do not collect personal account numbers, bank access details, shipping routes, reproduction specifications, or operational laundering steps.

## Status

- **Documented:** narrator allegations and defensive monitoring questions.
- **Not verified:** all underlying historical claims, including the USD 6 million figure and Bank N losses.
- **Not implemented:** case-specific synthetic replay and detection tests.

## Supplement A — Alleged SMS flooding around pre-existing recurring billing

**Narrator clarification; not independently verified:** In the reported scenario, an SMS flooding tool (colloquially called a "bomber") allegedly saturates a phone number with unrelated messages. The narrator describes subscriptions as already associated with an account before a subsequent suspicious payment episode, with an asserted temporal link to either cash acceptance at a terminal or a retail refund. These are **allegations about a proposed sequence, not a demonstrated attack chain**.

**Important technical distinction:** An SMS flood cannot itself disable EMV 3-D Secure or prove that any authentication requirement was bypassed. Recurring merchant-initiated transactions can be handled differently from initial customer-initiated payments, subject to network rules, mandate validity, issuer/acquirer controls, and applicable regulation. Whether authorization was invalid, consent forged, or processing misclassified cannot be determined without trustworthy transaction records.

### Defender research questions

- Were recurring payment mandates genuinely consented to, correctly enrolled and traceably linked to the payer?
- Did the bank, acquirer and merchant apply the right authentication, exception and recurring-transaction classification controls?
- Was there an unusual increase in notification traffic or customer support contacts around disputed payments, and could that have impaired detection?
- Were cash-credit or refund ledger events followed by disputes or anomalous merchant billing, without assuming that temporal sequence proves causation?
- Did a purported refund actually finalize, or was it pending, reversed or rejected?

### Closed-loop defensive tests

Generate only fictional `funding_or_refund_review`, `mandate_audit`, `billing_authorization_audit`, `notification_volume_anomaly`, and `dispute_review` records. Evaluate an alert that **correlates**, rather than executes, suspicious authorization, notification volume and disputed transaction events. Include legitimate billing and notification-burst counterexamples. Never send SMS, generate accounts, obtain cards, connect payment gateways, or automate real charges.

### Verification gaps

No timestamps, disputed transaction records, consent proof, issuer logs, 3DS result codes, bank statements, refund state or measured notification volumes have been supplied. The claimed SMS flooding and authentication bypass must remain unverified.
