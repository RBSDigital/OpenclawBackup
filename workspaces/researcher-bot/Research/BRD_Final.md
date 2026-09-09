# Business Requirements Document
## Velo Nano Can Paid Sales Capability in the 1-2-1 Application

**Prepared from source materials:** `Fwd: BRD` thread dated 8 September 2026, `bat-diagram-stylesheet.md`, `problemstatement.md`, `1-2-1 Application Architecture-UK Phase1_v2.0.pdf`, and `Interevo_User Manual_UK Phase II` manual files (`.docx` and role PDFs).

**Synthesis model:** GPT-5.4-mini.

**Purpose:** Provide a ready-to-use business requirements document for the UK phase 1 change, replacing the earlier discovery draft where the newer attachments provide stronger evidence.

---

## 1. Executive Summary

The business needs a compliant way for field teams to sell Velo nano cans from 1 November 2026, after free trials are no longer permitted under the new operating rules. The current 1-2-1 application and operating model were designed around consumer engagement and trial distribution, and do not fully support paid sales, payment capture, stock reconciliation, or the downstream reporting and integration needs that follow a commercial transaction.

The target solution should preserve a single source of truth for consumer, stock, sales and reporting data, while supporting role-based working for brand ambassadors, supervisors, agency administrators and the commercial team. The source material strongly indicates that the preferred approach is to extend the existing 1-2-1 application rather than introduce a second operating platform.

This document captures the confirmed requirements, the current-state evidence, the unresolved operating-model decisions and the assumptions that should be validated before build completion.

---

## 2. Evidence Basis

### 2.1 Primary source material

- `problemstatement.md`
- `bat-diagram-stylesheet.md`
- `1-2-1 Application Architecture-UK Phase1_v2.0.pdf`
- `Interevo_User Manual_UK Phase II.docx`
- `Interevo_User Manual_UK Phase II AA.pdf`
- `Interevo_User Manual_UK Phase II BA.pdf`
- `Interevo_User Manual_UK Phase II CT.pdf`
- `Interevo_User Manual_UK Phase II SV.pdf`

### 2.2 What the evidence shows

- The business problem is specifically about enabling paid sales of Velo nano cans from 1 November 2026.
- The current 1-2-1 capability supports consumer engagement, survey capture, stock handling, reconciliation, reporting and offline behaviour for certain user journeys.
- The user manual defines the four roles, their permissions and the existing flows for campaigns, locations, schedules, stock, compliance and reporting.
- The architecture paper states that the 1-2-1 application should own agent management, engagement, sales and reporting, while integrating with the wider BAT ecosystem where required.

### 2.3 Evidence notes

- `bat-diagram-stylesheet.md` is a diagram styling aid only; it does not change the business requirements, but it confirms the BAT visual language used in associated diagrams.
- The architecture paper refers to the existing UK local solution as Sharpend and identifies global integration touchpoints such as Salesforce/CRM, commerce, device service and loyalty.

---

## 3. Current State

### 3.1 Current operating model

The current UK solution is a local 1-2-1 implementation connected to CRM for consumer and campaign interfaces. The user manual shows a mature field-activation platform with four roles:

- Brand Ambassador
- Supervisor
- Agency Admin
- Commercial Team

The current application already supports:

- location and campaign management
- schedules and shifts
- compliance checklists
- consumer surveys and case creation
- product catalogue management
- stock ordering, allocation, movement and reconciliation
- shift reconciliation with receipt photography
- reporting and exports
- offline use for selected journeys

### 3.2 Current pain points

- The process was designed around free trial distribution rather than paid sales.
- The business now needs to collect payment for nano cans.
- The current model does not yet settle the ownership of payment taking, merchant configuration and stock reconciliation in a way the business has approved.
- A second platform such as Evolve is explicitly treated as a fallback, not the desired target-state operating model.

### 3.3 Architecture evidence

The architecture paper states that the 1-2-1 application should be responsible for:

- agent management
- engagement
- sales
- reporting

It also states that consumer age verification, email/SMS verification and some CRM/commerce touchpoints should be handled within the application or through approved interfaces before data is passed downstream.

---

## 4. Business Problem

### 4.1 Problem statement

The business requires a compliant mechanism for brand ambassadors to sell Velo nano cans and collect payments from consumers from 1 November 2026, when free product trials can no longer be offered.

### 4.2 Business question

How do we enable field teams to sell nano cans compliantly and efficiently from 1 November while maintaining a single source of truth for consumer, stock and payment data?

### 4.3 Why the change is needed

- Regulatory change removes the ability to offer free trials.
- The commercial model now requires direct or indirect payment collection.
- The current stock model needs to support sell-through rather than trial allocation alone.
- Reporting and reconciliation need to reflect real sales.

---

## 5. Business Objectives

1. Enable compliant paid sales of Velo nano cans from 1 November 2026.
2. Preserve a single operational platform for field activity rather than duplicating sources of truth.
3. Record sales, receipts, stock movements and reconciliations accurately.
4. Support both retail and E&E operating contexts.
5. Maintain role-based access and the existing governance model.
6. Provide the data required for CRM, reporting and compliance.
7. Minimise reconciliation effort and operational complexity.

---

## 6. Scope

### 6.1 In scope

- paid sales of Velo nano cans
- consumer-facing field execution in the 1-2-1 application
- role-based workflows for BA, SV, AA and CT users
- payment capture and receipt evidence
- stock allocation, stock movement and stock reconciliation
- shift reconciliation where required
- retail and E&E use cases
- reporting and exports for commercial and operational review
- compliance capture, including age and nicotine-related checks where required
- downstream integration to approved enterprise systems

### 6.2 Out of scope unless explicitly approved later

- introduction of a separate second operating platform as the target-state solution
- wholesale redesign of the broader global 1-2-1 architecture
- non-Velo product sales not mentioned in the source pack
- functionality not evidenced in the supplied documents

---

## 7. Target Operating Model

### 7.1 Preferred direction

The source material points to a single 1-2-1 application that captures:

- ambassador activity
- consumer data
- sales
- reporting

This remains the preferred target model.

### 7.2 Retail operating options under discussion

The meeting notes identify two possible retail payment models:

1. The retailer takes payment and retains the proceeds.
2. The brand ambassador takes payment directly from the consumer.

These two options have materially different consequences for process design, merchant setup, stock reconciliation and integration.

### 7.3 E&E operating context

The E&E channel continues to require field sales execution in venues such as pubs, bars, festivals and related event environments. The source notes indicate that E&E will remain part of the requirement and that Evolve is only a fallback if the new solution is delayed.

---

## 8. Functional Requirements

### 8.1 User and role management

**FR-01** The solution shall support role-based access for BA, SV, AA and CT users.

**FR-02** The solution shall maintain the existing role hierarchy and creation rules described in the user manual.

**FR-03** The solution shall provide read/write permissions appropriate to each role, including commercial oversight and agency-level administration.

### 8.2 Campaign, location, schedule and activation management

**FR-04** The solution shall support campaigns, locations, schedules, activations and targets in line with the existing field-activation model.

**FR-05** The solution shall support both Retail and E&E channels, including their respective sub-channels and activation patterns.

**FR-06** The solution shall allow field activity to be associated with the correct campaign, location, activation and shift.

### 8.3 Consumer and compliance capture

**FR-07** The solution shall allow the capture of consumer data required for compliant sales and related follow-up activity.

**FR-08** The solution shall support age verification and any other mandatory compliance checks before a sale is completed.

**FR-09** The solution shall support OTP-based verification where required by the operating model.

**FR-10** The solution shall preserve the Responsible Marketing Framework capture required by the architecture paper, including age, nicotine user status and date of birth, with non-PII reporting to the RMF group.

### 8.4 Payment capture

**FR-11** The solution shall support the agreed payment-taking model for retail and E&E field sales.

**FR-12** The solution shall store transaction evidence sufficient to reconcile the payment, the sale and the stock movement.

**FR-13** The solution shall support the chosen merchant and device model, including any NFC-enabled or payment-terminal arrangement approved by the business.

### 8.5 Stock and reconciliation

**FR-14** The solution shall support stock assignment to the appropriate stock holder, whether that is an agency, user or activation, depending on the approved operating model.

**FR-15** The solution shall support stock movements, stock returns and stock reconciliation for sales activity.

**FR-16** The solution shall retain evidence of expected versus actual quantities and the reason for any discrepancy.

**FR-17** The solution shall support approval and rejection workflows for stock reconciliation.

### 8.6 Receipt and proof of sale

**FR-18** The solution shall support receipt capture and association of receipt evidence with the relevant shift or sale.

**FR-19** The solution shall permit the upload and review of proof-of-sale evidence where required by the operating model.

### 8.7 Reporting and exports

**FR-20** The solution shall provide reporting for commercial, agency and supervisory users.

**FR-21** The solution shall support exports for operational analysis, compliance and reconciliation.

**FR-22** The solution shall preserve the ability to report on consumer engagement, trials, transactions, device sales, consumables sales, sign-ups and other existing indicators where still relevant.

### 8.8 Integration

**FR-23** The solution shall integrate with the approved BAT ecosystem touchpoints, which may include Salesforce/CRM, commerce, device service, loyalty and D365 depending on the final design.

**FR-24** The solution shall not create a duplicate source of truth for consumer, stock or sales data.

**FR-25** The solution shall support downstream reporting and any mandated data sharing without exposing PII beyond what the compliance model allows.

---

## 9. Non-Functional Requirements

### 9.1 Compliance and governance

- The solution must support the new regulatory position from 1 November 2026.
- The solution must preserve auditability across sale, payment and stock events.
- The solution must respect role-based access and existing approval boundaries.

### 9.2 Availability and usability

- The solution should be usable in the field on mobile devices.
- The solution must be sufficiently reliable to operate across retail and event environments.
- The solution should support the current working patterns described in the manual, including field use, shift-based working and location-based activity.

### 9.3 Offline and resilience

- The existing platform supports certain offline journeys; the target design should explicitly confirm whether paid sales are online-only or can tolerate offline capture.
- Device or terminal failure must be treated as a business risk because it can prevent completion of the activity.

### 9.4 Performance and scale

- The solution must support at least the indicated user volumes from the meeting notes: 50+ retail brand ambassadors, with approximately 60 devices allowing for spares and damage.
- The solution must also support E&E deployments, where 10-15 ambassadors may be active at once but the overall device requirement may be higher because activations occur across multiple locations.

---

## 10. Business Rules

### 10.1 Commercial rules

- Free product trials cease from 1 November 2026.
- Velo nano cans become paid products from that date.
- The business wants a single, traceable flow for stock and payment.

### 10.2 Field rules

- Retail ambassadors generally work two shifts: 09:00-13:00 and 14:00-18:00.
- E&E activity takes place in pubs, bars, festivals and similar environments.
- Locations are bounded by a fence radius, and check-ins outside the fence are flagged.

### 10.3 Compliance rules

- A pre-visit compliance checklist must be completed before the first check-in of the day.
- Where required, required checklist items must be completed before the shift can start.
- Receipt evidence must be retained for shift reconciliation where sales have been recorded.

### 10.4 Stock rules

- Current working-stock and agency stock arrangements must be translated into a traceable stock model.
- Stock reconciliations are reviewed and approved by the agency admin in the current manual model.

---

## 11. Assumptions

The following points are not fully resolved in the source pack and should be treated as assumptions until confirmed:

1. **Payment model:** the final retail payment model is not yet agreed.
2. **Merchant model:** the assumption that a new merchant ID will reduce reconciliation effort is provisional.
3. **Device model:** the suggestion that NFC-enabled tablets could replace separate tablets and payment terminals is under investigation, not confirmed.
4. **D365 design:** the idea of representing agencies as warehouses or locations in D365 is a proposal, not a settled requirement.
5. **Offline sales:** offline behaviour for paid sales is not confirmed by the source material.
6. **CRM and downstream routing:** Salesforce, CRM, commerce and D365 touchpoints must be confirmed against the final operating model.
7. **Brand scope:** the evidence explicitly names Velo nano cans and does not establish a broader beverage or vapour sales scope for this phase.

---

## 12. Dependencies

- Confirmation of the retailer-versus-ambassador payment model
- CyberSource compatibility review
- Merchant ID and device/terminal decision
- D365 stock and reconciliation design
- Financial approval from the relevant stakeholders
- Compliance review for the new operating model
- UAT sign-off in mid-October
- Final launch readiness by 1 November 2026

---

## 13. Risks

### 13.1 Delivery risk

The source notes show a compressed delivery window of roughly six weeks to the target go-live. This creates a material risk that requirements, build and UAT may not complete in time.

### 13.2 Process risk

If the payment model is not decided quickly, stock, reporting and integration design will remain unstable.

### 13.3 Technology risk

Device and terminal compatibility with CyberSource remains a live risk.

### 13.4 Reconciliation risk

If stock and payment data are not captured in a single traceable flow, reconciliation effort will increase and the target single-source-of-truth objective will be undermined.

### 13.5 Fallback risk

Evolve exists as a fallback for E&E, but relying on it long term would reintroduce multiple systems and multiple sources of truth.

---

## 14. Open Questions

1. Who takes payment in the final retail model?
2. Will payment be taken by a separate terminal or by an NFC-enabled tablet?
3. What merchant ID is to be used, and who owns it?
4. Is paid sales capture online-only, or must it work offline?
5. What is the final D365 stock representation for agencies and activations?
6. Which downstream systems are mandatory for phase 1?
7. What precise data must be sent to Salesforce, and at what point in the journey?
8. What receipts or evidence are mandatory for each sale?
9. Which parts of the current 1-2-1 manual remain in scope for this phase, and which are explicitly out of scope?

---

## 15. Acceptance Criteria

The solution will be considered ready for phase 1 when all of the following are true:

- Brand ambassadors can sell Velo nano cans compliantly in retail and E&E contexts.
- The agreed payment model is implemented and tested.
- Stock movements and reconciliations can be traced end to end.
- Receipt evidence is captured and retrievable.
- Role-based reporting works for CT, AA, SV and BA users as appropriate.
- The approved downstream integrations are live or contractually accounted for in the operating model.
- The solution supports the planned 1 November 2026 launch.
- The business accepts the final operating model and fallback posture.

---

## 16. Consultancy Review Notes

### 16.1 What is confirmed

- The commercial requirement is to move from free trials to paid sales.
- The platform should remain a single source of truth.
- The current UK capability is already feature-rich and should be extended rather than replaced casually.

### 16.2 What is not yet confirmed

- The precise payment-taking model
- The terminal/device architecture
- The final D365 representation of stock
- The exact integration pattern and downstream data contract

### 16.3 Recommendation

Proceed on the basis of a controlled phase 1 build that preserves the existing 1-2-1 platform, but freeze the commercial operating model decisions immediately. Without those decisions, the build will drift and the reconciliation model will not stabilise.

---

## 17. Source-to-Requirement Traceability

| Source | Key contribution to the BRD |
|---|---|
| `problemstatement.md` | Defines the core problem, the end date, the need for compliant sales and the single-source-of-truth objective. |
| `bat-diagram-stylesheet.md` | Diagram styling only; no business requirement content. |
| `1-2-1 Application Architecture-UK Phase1_v2.0.pdf` | Confirms global 1-2-1 scope, current UK Sharpend solution, consumer verification, sales capture, offline capability and downstream touchpoints. |
| `Interevo_User Manual_UK Phase II.docx` and role PDFs | Confirms current roles, user flows, stock/reconciliation processes, compliance, offline behaviour and current reporting capability. |

---

## 18. Final Position

The evidence supports a polished final BRD rather than a discovery draft. The business need is clear, the current-state platform is well defined, and the remaining uncertainty sits mainly in the operating model and technical integration choices. The document above is therefore written as a delivery-ready BRD with explicit assumptions rather than as a tentative note.

