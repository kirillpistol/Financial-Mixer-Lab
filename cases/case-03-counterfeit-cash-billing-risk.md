# CASE 003 — Alleged counterfeit-cash acceptance and subscription-payment laundering risk

**Classification:** Historical case narrative supplied by the narrator; defensive research only. Specific actors and financial records are not independently established.  
**Safety boundary:** Fictional data, simulated events, no real bank, ATM, payment, messaging, printing, shipping, or P2P integration. This is not a laundering or counterfeiting playbook.

## Executive summary

The case narrative places the production of counterfeit US-dollar banknotes in **China** and their movement across borders via third parties. It places the cash deposit activity at **ATMs in the United States**, followed by subscription charges and subsequent service payouts. **Only part of the intended cash volume was accepted; the deposited amount is deliberately unspecified because the processed amount was below plan.** This is a reconstruction of the narrator's account, not an independently adjudicated finding about a specific manufacturer, courier, bank, or individual.

The description also mentions possible postal or diplomatic involvement, without evidence identifying particular persons or channels. The US bank is anonymized as **Bank N**. The reported financial loss has not been quantified or verified. Do not equate counterfeit face value, deposits, successful subscription charges, merchant settlements, and realized bank loss.

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
6. An alleged loss is never computed as accepted cash or any planned or face-value amount without documented evidence.

## Detection and QA evaluation

Test anomaly alerts on fictional labeled incidents, including legitimate lookalikes. Track precision, recall, false-positive rate, detection latency, audit-trail completeness and exception-resolution quality. Use defensive test cases to assess both unauthorized billing and banknote-authenticity failures.

## Evidence to request (redacted and non-operational)

Approximate historical period; public source for the alleged claim; whether Bank N is a pseudonym; verified figures for presented vs accepted notes and any realized loss; public regulatory or court records if available. Do not collect personal account numbers, bank access details, shipping routes, reproduction specifications, or operational laundering steps.

## Status

- **Documented:** narrator allegations and defensive monitoring questions.
- **Not verified:** all underlying historical claims, including Bank N losses.
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

## Supplement B — Reported prevalidation and multi-merchant charge pattern

**Historical narrator account; not independently verified.** The narrator describes a pre-existing collection of phone numbers allegedly screened by a third-party checker and associated with small initial subscription charges reported as **RUB 1**. The account claims that further, substantially larger amounts — described as **USD 300 or USD 1,500** — were sought through as many as **10 subscription services**. A one-day interval is mentioned, but the precise chronology, payment authorizations and any completed settlement are unverified. These figures are anecdotal, not evidence of debited balances or bank losses.

This account is preserved only as a **defensive risk hypothesis**, not a usable payment, subscription or account-setup workflow. It does not establish whether any given service stored valid recurring-payment consent, whether the small charge was an authorization or a captured payment, whether larger charges were approved, or whether EMV 3-D Secure was technically circumvented.

### Bank and acquirer investigation checklist

- Examine validity and scope of initial customer consent and subsequent merchant-initiated payment mandates.
- Distinguish verification authorizations, captured charges, attempted recurring payments and successful settlement.
- Look for abnormal cross-merchant concentration of disputes or complaints, using lawful data and appropriate privacy protections.
- Review merchant underwriting and recurring-billing disclosures against documented contractual terms.
- Reconcile claimed attempted amounts against actual ledger postings and any documented financial losses.

**Research controls:** Synthetic, fictional event logs only. No real-number databases, checker integrations, small-charge testing, merchant setup, SMS delivery, subscription triggering or payment execution.

## Supplement C — Clarified alleged sequence and provenance

**Narrator clarification (unverified):** The alleged incident is described as counterfeit US-dollar notes being accepted by a cash-deposit ATM, followed by subscription payments through third-party services, and then onward disbursements presented to recipients as ordinary service-generated payments. The narrator characterized the proceeds as “almost clean.” This phrase describes **apparent payment provenance**, not lawful origin or actual legal status.

**Accounting and legal distinction:** A payment appearing in a merchant or subscription service statement does not cure counterfeit origin, validate a fraudulent mandate, or extinguish potential recovery claims. Actual cash acceptance, ledger credit, merchant charge settlement, payout, and ultimate loss are distinct events. None is independently verified in this case.

**Defender traceability requirements:** Preserve the link between cash-authenticity incident records, ATM reconciliation, credited account entries, disputed subscription authorizations, merchant/acquirer settlement, and payout beneficiary. Investigators should establish evidentiary continuity and assess who controlled each stage; do not infer identity or criminal intent merely from temporal coincidence.

This supplement supplies no practical workflow for injecting counterfeit notes, triggering charges or withdrawing proceeds.

## Supplement D — Preparatory infrastructure and cross-system forensic model

**Scope:** Technical risk research, not operational instructions. The following details are taken from the narrator's account. They are not proof that particular vendors, card issuers, telecom providers or software developers were involved.

### 0. Preparatory identity and payment infrastructure

The narrator describes a previously assembled dataset of telephone numbers with prior subscription and billing associations (described as a "number dump"). The narrative also references acquired or reissued payment cards, third-party-controlled numbers, and accounts with existing subscription records. The term "warmed" indicates a claimed prior activity history; it does not establish legitimate cardholder authorization.

A separate claim concerns compromised subscription-service databases and retained payment credentials. For defensible investigation, distinguish **records of a card token**, merchant vault references, actual cardholder data, and proof of consent; the existence of a record in a system does not authenticate its owner.

The narrator refers to card-data rewriting with an embosser. An embosser is associated with physical card personalization; assertions that it can rewrite payment authorization or chip credentials cannot be accepted without technical evidence. This report does not provide personalization, encoding, cloning, or tampering steps.

**Investigative controls:** token lifecycle and issuer reissue records, reported compromise dates, PCI DSS incident evidence, cardholder consent audit, third-party identity verification, phone-number ownership change history under lawful process, and merchant onboarding records.

### 1. Cash acceptor and ATM controls

The scenario places counterfeit production in China and cash-in at US ATMs via third parties. The diagnostic question is whether an exception in authenticity screening and cash-credit reconciliation was resolved or left open.

**Forensic artifacts:** ATM event journal, note-acceptance inspection findings, service technician incident records, cassette balancing, credited account journal, exception escalation and supervisory disposition. Do not treat an ATM credit as independent proof of genuine banknotes.

### 2. Subscription consent and billing compromise

The narrative describes pre-existing subscriptions, apparently successful charges, recurring billing and potential service compromise. The relevant question is which entity authorized which transaction and whether an authenticated consent record exists.

**Forensic artifacts:** customer mandate text and version; customer-initiated versus merchant-initiated classification; token provenance; acquiring merchant and settlement identifiers; refund/chargeback status; application security and breach audit logs. An SMS-bombing allegation warrants notification-volume review; it does not establish that 3-D Secure was bypassed.

### 3. Merchant payouts and beneficiary attribution

A merchant-facing receipt or payout may appear to be normal service revenue while the source is disputed. This is an **appearance of ordinary settlement**, not legal cleansing.

**Forensic artifacts:** processor settlement reports, beneficiary ownership investigations under legal authority, merchant registration and beneficial-owner verification, refunds, dispute reversals, and accounting adjustments. Flag unverifiable documentation rather than assuming it leaves no trace.

### 4. Developer and operator attribution

The narrator mentions the developers of subscription applications, an alleged SMS-bombing tool, and parties handling payment infrastructure. Attribution must distinguish developer, service operator, data broker, merchant owner, and beneficiary. Shared infrastructure or source-code similarity alone is not proof of common control.

**Forensic artifacts:** signed application releases, code provenance where lawfully obtained, vendor contracts, security alerts, incident reports, access logs, merchant onboarding and legal records. No intrusion or de-anonymization techniques are specified.

### 5. Silent fraud: detection without a complaint

A lack of customer complaints is a **missing input**, not an exonerating event. In a defensive model, review unresolved cash exceptions, invalid consent, unverified merchant ownership and payout discrepancies independently of complaints.

### QA acceptance criteria

1. Preserve event/source references for every alert; missing sources may not be silently upgraded to verified.
2. Separate an authorization request from captured funds, cleared settlement, payout and proven loss.
3. Do not equate card reissue, card token storage, physical card personalization or a phone-number association with consent.
4. Include benign examples and false-positive review; report case-level precision, recall and false-positive rate.
5. Keep the entire pipeline offline with fictional records. No cards, phone numbers, payment credentials, banks, ATMs, subscription services or SMS systems are connected.
