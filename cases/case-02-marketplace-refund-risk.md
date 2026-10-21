# CASE 02 — Marketplace cashback/refund abuse (risk research)

**Project:** Mixer by PISTOL / Financial-Mixer-Lab  
**Status:** Case registered; no execution tooling.  
**Date:** 2026-10-21  
**Scope:** Financial-risk analysis and detection, not an operational playbook.

## User-supplied case description (unverified)

A proposed AliExpress storefront selling small electronics, with a network of accounts and repeated disputed/refunded marketplace purchases, intended to generate bank loyalty rewards while recovering purchase funds. The description also references payment obfuscation and payment-authentication bypass; these elements are **excluded from implementation**.

### Hypotheses / inputs to validate

| Input | User-supplied value | Interpretation |
|---|---:|---|
| Initial capital | RUB 20,000 | Stated seed capital; does not establish liquidity for larger orders |
| Typical transaction / refund amount | RUB 40,000–60,000 | Stated target range; no evidence or bank record |
| Primary bonus accounts | 5 | Separate ownership/authorization must be respected |
| Other marketplace accounts | ~100 | Treated as a fraud-risk signal, not a scaling target |
| Cashback rate | 5%–10% | Not verified for actual MCC, category or merchant |
| Frozen funds/accounts assumption | 2%–2.5% | User estimate; denominator and observation period unknown |
| Promotional redemption assumption | 1 bonus = RUB 1.81 on Nov 13–15, 2026 | Not verified; redemption value is not the same as cash value |

## Critical financial distinctions

1. Gross transaction volume is not revenue or profit.
2. A refund reverses a legitimate sale and can trigger reward clawback even after credits post.
3. A bonus is not cash; redeemability, settlement delay and program restrictions are essential.
4. The 2%–2.5% freezing estimate is not a measured probability and cannot be used as a validated input.
5. Marketplace, acquiring and bank fees, tax, disputes, locked balances and inventories require separate accounting.
6. With RUB 20,000 initial cash, transactions in the RUB 40,000–60,000 range require a real source of financing; the discrepancy is an unresolved assumption.

## Risk and integrity checks

- Confirm genuine goods, shipment evidence, beneficial ownership and independently acting customers.
- Separate valid refunds from induced or fabricated disputes.
- Identify repeated closed-loop cash movements and coordinated account behavior without specifying evasion tactics.
- Check platform refund rules, bank rewards reversal policy, merchant acquiring agreement, applicable law.
- Model both downside (funds frozen, chargebacks, fines, fees) and the legitimate-commerce baseline.

## Next research tasks

- Obtain authoritative terms for the relevant reward program, marketplace and acquirer.
- Record lawful transaction traces using anonymized, consented data.
- Calculate conservative profitability only on completed, non-refunded genuine sales.
- Build a read-only anomaly/risk dashboard and a scenario comparison: legitimate sales vs disputed/returned sales.

## Boundary

This case must not implement fabricated storefront transactions, account farms, refund manipulation, funds laundering, 3-D Secure circumvention, or techniques for avoiding fraud detection.
