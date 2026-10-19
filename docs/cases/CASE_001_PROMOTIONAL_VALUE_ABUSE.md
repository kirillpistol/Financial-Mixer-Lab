# Case 001 — Bonus-value conversion through coordinated accounts

**Classification:** Historical, user-reported scenario; **not independently verified**.  
**Scope:** Defensive research, fraud analytics, and synthetic replay.  
**Important:** The stated promotion terms, monetary equivalents, technical implementation, and estimated proceeds require independent corroboration before being presented as facts.

## Executive summary

A user-reported historical case describes alleged large-scale abuse of a promotional digital reward in the Russian retail/social-platform ecosystem. The promotion reportedly granted a small non-cash digital entitlement after an account-verification event. A coordinated network of newly established accounts allegedly routed this promotional value through a creator-support feature to a much smaller set of receiving accounts; the accounts allegedly attempted to cash out the resulting balances. The user estimates proceeds at approximately RUB 2 million. These statements are **claims**, not validated findings.

This document deliberately does **not** specify executable registration/verification automation, account suppliers, click sequences, receiver setup, identity misuse, withdrawal mechanics, operational timings, or ways to evade financial monitoring.

## Abstract abuse pattern (defender's view)

1. **Promotion issuance:** A platform issues limited-purpose digital rewards on a qualifying event.
2. **Sybil concentration:** A coordinated population of apparently separate identities attempts to claim rewards at scale.
3. **Value transformation:** Platform-internal entitlements are transferred through a feature that can credit another user or creator.
4. **Beneficiary concentration:** Many reward sources converge on a small receiving cluster.
5. **External settlement exposure:** The system may permit some credited balances to become redeemable externally, revealing a potential mismatch between source restrictions and redemption policy.

> These five steps are a **threat-model abstraction**, not a procedure for conducting the alleged scheme.

## Trust boundaries and control questions

| Boundary | What defenders should verify | Potential control failure |
|---|---|---|
| Eligibility → reward issue | Unique eligible person; frequency; promotion limits | Multiple controlled accounts appear independent |
| Restricted reward → internal transfer | Whether promotional value retains its restrictions | Instrument restrictions lost when converting value types |
| Source account → beneficiary | Common-control relationships and abnormal fan-in | Recipient risk assessed without source provenance |
| Internal credit → payout eligibility | End-to-end provenance and payout rules | Restricted-origin value treated as withdrawable |
| Beneficiary → payment instrument | Legitimate verified ownership | Mismatch between beneficiary and payout identity |

## Detection hypotheses

The following are *candidate features*, not verified signatures of this specific case:

- Unusual ratio of first-time accounts to long-lived accounts participating in one reward campaign.
- Anomalous fan-in: a relatively small group of beneficiaries receives credits from many new sources.
- Strong temporal correlation between reward issuance and subsequent transfer activity.
- Disproportionate redemption attempts involving balances sourced from promotional entitlements.
- Repeated relationships among account clusters, redemption entities and payment instruments, subject to lawful data collection.
- High velocity of automated-looking sessions; account-level signals must not be treated as proof of wrongdoing alone.

Cross-platform analysis should use lawfully obtained, minimized, pseudonymized data and documented legal authority.

## Defensive controls

- Preserve **source-of-funds tags** as value moves across internal ledgers; restricted rewards must not silently become cash-equivalent.
- Enforce promotion eligibility and per-person limits using privacy-preserving anti-abuse controls.
- Assess recipient concentration and graph anomalies as part of fraud detection.
- Recheck redemption eligibility and beneficial ownership before settlement.
- Provide review workflows, explainable alerts and an appeals process to manage false positives.
- Maintain event-level audit trails linking reward issuance, internal credits and settlement decisions.

## Synthetic replay specification

In a **closed local simulation**, model fictional accounts, synthetic non-cash reward units, creator-credit accounts, and a *disabled-by-default* redemption policy. Do not connect to live banks, social platforms, telecom providers, KYC systems or external payment providers.

Suggested event types:

- `reward_issued` — subject ID, reward ID, amount in *virtual reward units*, rule tag.
- `internal_credit` — virtual source, virtual receiver, reward provenance.
- `payout_requested` — request event only; **never actual settlement**.
- `risk_alert` — detection rule, evidence references, severity.
- `review_decision` — approved/denied/escalated in the simulation.

Minimal invariants:

1. **No creation or destruction of value** without a specific issuance/burn event.
2. **Non-cash restriction persists** through all transfers, conversions and accounting views.
3. **Synthetic withdrawals are denied** when funds trace to restricted promotional origin.
4. **Every state transition is auditable**; no direct mutation of reward provenance.
5. **No real identity records, credentials, phone numbers or payment instruments** are used.

## Evaluation plan

Compare baseline and stress-case traffic. Measure case-level recall, precision, false-positive rate, alert latency and share of restricted-origin payout attempts blocked. Test benign analogues (legitimate new-user campaigns and popular creator events) so detection does not punish normal behavior.

## Follow-up evidence requirements

For any later case study, collect a redacted source narrative; approximate period; user-facing campaign policy if publicly available; which value restrictions were contractual vs technical; systems involved at a *category* level; and whether any payout records or external findings corroborate the reported outcome. Do not request or store third-party personal data, actual credentials, usable payout details or actionable evasion sequences.

## Status
**Documented:** defensive hypotheses and synthetic test design.  
**Not built:** case-specific simulator, detectors, external integrations.  
**Not verified:** original event details and reported financial outcome.

## Supplement A — Reported daily account volume (narrator update)

**Reported observation, not independently verified:** Approximately **5,000 new accounts per day** were allegedly obtained through third-party registration services, with automated input and registration processes. This is an account-creation claim, **not** a demonstrated rate of successful reward issuance or payments. No supplier names, operational instructions, or reusable registration methods are retained.

### Quantitative interpretation

- **5,000 accounts/day** = **208.3/hour** = **3.47/minute** = **0.0579/second**, assuming an even 24-hour distribution.
- Real automation can produce much higher **bursts**; peak concurrency and hourly distribution are **unknown**.
- The current load-test tool's **1,000 synthetic accounts per run** is a safety/engineering cap; it does not establish capacity for 5,000 per day.
- For a defensive simulation, split 5,000 **fictional** account events into separately bounded local batches and aggregate metrics. The lab must never register live accounts or connect to external identity, social, telecom, or payment providers.

### Metrics worth collecting in a defender replay

| Metric | Meaning |
|---|---|
| Created account events/day | Reported input volume; compare with accepted and rejected events |
| Eligible reward recipients/day | Actually accepted synthetic reward eligibility checks |
| Reward units issued | Units issued, not a fiat amount |
| Unique senders per receiver | Potential concentration in a synthetic transaction graph |
| Bursty arrival distribution | Contrast average and max minute rates |
| Restricted-origin redemption requests | Attempts to treat non-cash value as withdrawable |
| Alert precision, recall and false-positive rate | Detection effectiveness against a labelled synthetic dataset |

### Unresolved evidence

Whether 5,000 accounts/day was sustained across multiple days; whether these were all registered successfully; how many passed required verification; how many received rewards; time-of-day peak pattern; and whether reported RUB 2 million is gross, net, or approximate.

