# Business Requirements Document

## Future Festival, Pop-up and Field-Sales Stock and Payment Capability

**Version:** 0.1  
**Status:** Draft for stakeholder validation  
**Source:** Requirements discovery meeting transcript  
**Prepared by:** Business Analysis  
**Date:** 25 November 2026

> **Important:** This document records business needs from the discovery meeting. It does not select a technology solution. Terms, dates, roles and financial treatments that were unclear in the transcript are marked for validation.

## 1. Executive summary

The current Evolve-based operating model is expected to be decommissioned during 2027. A replacement capability is therefore required to support festivals, pop-ups, field teams, HORECA and related channels.

The capability must manage stock ordering, receipt, custody, pricing, discounting, sales, payments, returns, reconciliation and reporting. It must support business-to-consumer (B2C), business-to-business (B2B) and hybrid journeys.

The immediate objective is to agree channel-specific processes and requirements before assessing whether One-to-One, another platform, an integration or a combination of solutions is appropriate.

The source material demonstrates a clear operational need but does not yet provide confirmed volumes, performance targets, financial rules or a confirmed retirement date. These are decision items, not assumptions to be treated as fact.

## 2. Background and context

The current process involves Evolve, One-to-One, NRL, D365, agencies, agency warehouses, field representatives, retailers and Finance. Stock is ordered, delivered, counted, moved through warehouse and van states, priced, sold and reconciled.

The future model may change stock ownership and financial treatment. The discussion indicated that stock may remain BAT-owned when transferred to an agency, rather than being purchased by NRL. This must be confirmed with Finance and Treasury.

The transcript also identifies a future SAP environment. SAP integration requirements must therefore be considered, but detailed design belongs with Finance and the SAP team.

## 3. Purpose and objectives

### Purpose

To define the business capabilities required to continue festival, pop-up and field-sales activity after the current Evolve-based process is retired.

### Objectives

1. Maintain operational continuity after Evolve retirement.
2. Provide a simple, portable sales process for field users.
3. Track stock ownership, custody and movement accurately.
4. Support approved pricing and discount codes.
5. Support B2B, B2C and hybrid commercial journeys.
6. Reconcile stock, payments and financial postings.
7. Support operation in poor or intermittent connectivity.
8. Provide reliable operational and financial reporting.
9. Reduce manual work, duplicate entry and avoidable errors.
10. Produce an agreed requirements baseline before solution selection.

## 4. Scope

### In scope

- Stock ordering, approval, receipt and discrepancy recording
- Stock counting and custody tracking
- Warehouse, cage, van, issued, sold and returned stock states
- Unit-level product handling
- Product catalogue, prices and approved discounts
- Portable sales and card-machine payments
- B2B, B2C and hybrid sales journeys
- Failed and declined payments
- End-of-shift reconciliation
- Missing, damaged and disputed stock
- Returns and transfers
- Finance and Treasury reconciliation
- Operational, commercial and financial reporting
- Offline or low-connectivity operation
- User access, roles and audit trails
- Required enterprise and reporting integrations

### Out of scope

- Selecting One-to-One as the final solution
- Selecting a replacement platform
- Detailed technical architecture or database design
- Detailed SAP or D365 design
- Final commercial terms
- Final legal treatment of every sales model
- Code-level specifications
- Detailed retailer implementation
- Setting retailer resale prices

## 5. Stakeholders and governance

| Stakeholder | Interest or responsibility |
|---|---|
| BAT channel teams | Define operational journeys and business needs |
| Field representatives | Receive, move and sell stock |
| Supervisors or managers | Oversee activity and reconciliation |
| Agencies | Receive, store, issue and return stock |
| Retailers, clubs, pubs and bars | May receive stock, sell product or retain revenue |
| Finance | Define accounting, reconciliation and controls |
| Treasury | Define payment settlement and money flows |
| SAP team | Define future enterprise-system integration |
| Global platform team | Assess One-to-One capability and constraints |
| Trade Systems | Support price and discount-code processes |
| Stock auditors | Validate stock movements and discrepancies |

A formal RACI matrix must be agreed during requirements validation. Owners must not be inferred from the transcript.

## 6. Current-state assessment

The transcript indicates that:

- Stock is currently ordered through NRL and delivered to an agency or agency warehouse.
- Stock is counted and accepted, with discrepancies recorded.
- Stock may move from a warehouse cage into a sellable van state.
- Products may need to be broken down from bundles into individual units.
- Prices and approved discount codes are configured before sale.
- Field users sell using portable payment devices.
- The current product interface is difficult to use and may lack product images.
- Authentication can require access to shared or operational email accounts.
- Poor connectivity may affect activity at festivals and temporary venues.
- Stock is counted at multiple points, including at the end of a shift.
- Unused stock must be returned and reconciled.
- Financial visibility of stock costs, deliveries, sales and budget impact is insufficiently defined.

## 7. Future-state vision

An authorised user should be able to request or receive approved stock, confirm quantities, track custody, apply approved prices and discounts, complete sales, operate during connectivity interruptions, reconcile stock and payments, record exceptions, return unused stock and produce the required reports.

The future state must support different channel journeys rather than force all activity into a single commercial or operational model.

## 8. Channel journeys requiring validation

### Festivals and events

Likely characteristics include direct consumer sales, temporary locations, portable devices, high transaction volumes, connectivity challenges, end-of-event reconciliation and stock returns.

### Pop-ups

Likely characteristics include temporary activations, portable operation, stock movement to and from the activation, product reporting and payment processing.

### Fly teams

Likely characteristics include mobile teams, tactical venues, pubs, clubs, bars and B2C or hybrid sales. Temporary venues may not be set up as customers in the existing system.

### HORECA

Likely characteristics include sales or transfers to venues, retailer revenue retention and a B2B transaction model.

### Retail One-to-One

Likely characteristics include retailer or venue receipt of product, possible revenue retention, discount-based treatment and separate reporting or financial treatment.

The final scope and priority of each journey must be confirmed.

## 9. Business requirements

### Stock and inventory

| ID | Requirement | Priority |
|---|---|---|
| REQ-B-001 | The business shall be able to request stock for an approved activation or channel. | Must |
| REQ-B-002 | The process shall record stock ownership and custody at each stage. | Must |
| REQ-B-003 | The process shall support delivery to an agency or agency warehouse. | Must |
| REQ-B-004 | An authorised user shall confirm quantities received. | Must |
| REQ-B-005 | The process shall record dispatched-versus-received discrepancies. | Must |
| REQ-B-006 | The process shall support warehouse, cage, van, issued, sold, returned and unavailable states. | Must |
| REQ-B-007 | The process shall support unit-level tracking where products arrive in bundles or cases. | Must |
| REQ-B-008 | The process shall support transfers between warehouses, agencies, vans, field users and venues. | Must |
| REQ-B-009 | The process shall retain an auditable history of stock movements. | Must |
| REQ-B-010 | The process shall support stock returns after an activation or shift. | Must |
| REQ-B-011 | The process shall support end-of-shift stock counts. | Must |
| REQ-B-012 | The process shall record approved reasons for discrepancies, including damage, theft, failed payment and data-entry error. | Must |

### Products, pricing and discounts

| ID | Requirement | Priority |
|---|---|---|
| REQ-B-013 | The solution shall display the approved product catalogue for the relevant user or channel. | Must |
| REQ-B-014 | The product catalogue should display product images where available. | Should |
| REQ-B-015 | The solution shall support approved prices by product, market, channel or activation. | Must |
| REQ-B-016 | The solution shall support approved discount codes. | Must |
| REQ-B-017 | The solution shall prevent unauthorised price or discount changes. | Must |
| REQ-B-018 | The solution shall record the price, discount and final transaction value. | Must |
| REQ-B-019 | The solution shall distinguish acquisition or trial stock from standard sellable stock where the commercial treatment differs. | Must |

### Sales and payments

| ID | Requirement | Priority |
|---|---|---|
| REQ-B-020 | An authorised field user shall be able to record a sale using a portable device. | Must |
| REQ-B-021 | The solution shall support contactless or card-machine payment where required. | Must |
| REQ-B-022 | The solution shall distinguish successful, declined, failed and pending payments. | Must |
| REQ-B-023 | The solution shall prevent a failed payment from being treated as a successful sale unless an authorised exception is recorded. | Must |
| REQ-B-024 | Each transaction shall record product, quantity, price, discount, payment status, user, date, time and activation. | Must |
| REQ-B-025 | The solution shall support B2C sales. | Must |
| REQ-B-026 | The solution shall support B2B stock transfers or sales. | Must |
| REQ-B-027 | The solution shall support hybrid journeys where BAT, an agency or a retailer processes payment. | Must |
| REQ-B-028 | The solution shall support approved retailer or venue revenue-retention models. | Should |
| REQ-B-029 | The solution shall record the party responsible for collecting payment. | Must |

### Reconciliation and finance

| ID | Requirement | Priority |
|---|---|---|
| REQ-B-030 | The solution shall reconcile stock issued, sold, returned and remaining. | Must |
| REQ-B-031 | The solution shall reconcile recorded sales with successful payments. | Must |
| REQ-B-032 | The solution shall identify cases where a customer was charged but the product was not issued. | Must |
| REQ-B-033 | The process shall support investigation, write-off or resolution of failed, missing and disputed transactions. | Must |
| REQ-B-034 | Finance shall receive the data required to reconcile stock and cash. | Must |
| REQ-B-035 | The solution should report stock cost, delivery cost, sales value and budget impact where available. | Should |
| REQ-B-036 | The solution shall support different financial treatments for B2B, B2C and hybrid transactions. | Must |
| REQ-B-037 | The solution shall support the agreed SAP integration or reconciliation model. | Must |

### Reporting and connectivity

| ID | Requirement | Priority |
|---|---|---|
| REQ-B-038 | The solution shall report products, quantities, variants and channels. | Must |
| REQ-B-039 | The solution shall report stock movements and discrepancies. | Must |
| REQ-B-040 | The solution shall report payment success, failure and decline rates. | Must |
| REQ-B-041 | Reports shall support activation, venue, user and date views. | Must |
| REQ-B-042 | Relevant sales and activity data shall be available to the approved reporting or consumer-data platform. | Must |
| REQ-B-043 | The solution shall provide auditable exports for Finance and operational users. | Must |
| REQ-B-044 | The solution shall support operation in poor or intermittent connectivity. | Must |
| REQ-B-045 | The solution shall retain locally captured transactions until synchronisation is possible. | Must |
| REQ-B-046 | The solution shall prevent duplicate transactions during synchronisation. | Must |
| REQ-B-047 | The user interface shall support rapid use by field staff. | Must |
| REQ-B-048 | The user interface shall minimise scrolling and manual entry. | Should |

### Governance and control

| ID | Requirement | Priority |
|---|---|---|
| REQ-B-049 | Access shall be role-based. | Must |
| REQ-B-050 | The solution shall distinguish field users, supervisors, agencies, Finance users, stock auditors and administrators. | Must |
| REQ-B-051 | The solution shall retain an audit trail of stock, pricing, payment and reconciliation activity. | Must |
| REQ-B-052 | The process shall support approval of stock, prices, discount codes and write-offs. | Must |
| REQ-B-053 | The solution shall report exceptions requiring investigation. | Must |

## 10. Non-functional requirements to define

The following require confirmation before solution selection:

- Transaction response time
- Offline transaction capacity and duration
- Synchronisation time
- Expected users, retailers, transactions and stock transfers
- Availability during events
- Supported devices and operating systems
- Authentication and access model
- Data encryption and retention
- Audit-log retention
- Recovery Point Objective and Recovery Time Objective
- Support hours and escalation model

## 11. Acceptance criteria

The capability will be acceptable when:

1. Each agreed channel journey has been documented and approved.
2. Stock ownership and custody are visible at every process stage.
3. Users can receive, count, issue, sell and return stock.
4. Approved prices and discounts are applied correctly.
5. Successful and failed payments are distinguishable.
6. Stock and payment reconciliations can be completed.
7. Discrepancies can be recorded, investigated and resolved.
8. The process works in an agreed offline or low-connectivity scenario.
9. Duplicate transactions are prevented during synchronisation.
10. Finance confirms that the data supports the agreed accounting model.
11. SAP and other integration boundaries are agreed.
12. Representative users can complete sales without excessive scrolling or manual entry.
13. Required operational and financial reports can be produced.
14. Festival, pop-up, HORECA and hybrid scenarios have been tested.
15. Business owners sign off the requirements and acceptance evidence.

## 12. Assumptions and evidence gaps

### Assumptions

- Evolve will no longer support the required process after the confirmed retirement date.
- BAT may retain ownership of stock transferred to an agency.
- Some stock will be intended for trial or acquisition rather than normal sale.
- Different channels will require different financial and payment treatments.
- Connectivity cannot be assumed at temporary venues.
- One-to-One may not be suitable as a point-of-sale and inventory platform without change.

### Evidence gaps

- Confirmed Evolve retirement date
- Channel volumes and transaction forecasts
- Field-user and retailer numbers
- Stock-transfer frequency
- Offline duration and capacity
- Finance and SAP integration rules
- Approved pricing and discount rules
- Stock ownership and category rules
- Required KPIs and reports
- Data retention and audit requirements
- Confirmed role names and responsibilities

## 13. Risks and dependencies

| ID | Risk or dependency | Impact | Required response |
|---|---|---|---|
| R-001 | Requirements are not approved before Evolve retirement. | High | Confirm the retirement date and requirements timetable. |
| R-002 | B2B and B2C journeys are treated as one process. | High | Map each channel separately. |
| R-003 | Stock ownership and financial treatment remain unclear. | High | Hold a Finance and Treasury design workshop. |
| R-004 | Offline operation creates duplicates or data loss. | High | Define synchronisation and reconciliation controls. |
| R-005 | The selected platform cannot support both POS and consumer-data needs. | High | Assess capabilities against the approved requirements. |
| R-006 | Temporary venues cannot be set up quickly enough. | Medium | Define a lightweight venue and retailer process. |
| R-007 | SAP requirements are identified too late. | High | Involve SAP and Finance during validation. |

## 14. Decisions required

1. What is the confirmed Evolve decommissioning date?
2. Which channels are included in the first release?
3. Which journeys are B2B, B2C or hybrid?
4. Who owns stock at each stage?
5. Who collects payment and who retains revenue?
6. What is the approved treatment of trial and acquisition stock?
7. Should temporary venues be set up as formal customers?
8. What data must flow to SAP?
9. What data must flow to One-to-One or another reporting platform?
10. What offline operating model is required?
11. Who owns pricing, discount codes, reconciliation and write-offs?
12. Which capabilities must be available for the first activation?

## 15. Recommended next steps

1. Confirm the retirement date and critical delivery deadline.
2. Create channel-specific swimlane maps for festivals, pop-ups, Fly teams, HORECA and Retail One-to-One.
3. Validate the maps with field teams, Finance, Treasury, SAP and the Global platform team.
4. Collect operating volumes and transaction forecasts.
5. Define stock categories, ownership states and financial treatments.
6. Define B2B, B2C and hybrid payment journeys.
7. Agree offline, synchronisation and reconciliation requirements.
8. Prioritise the requirements using MoSCoW.
9. Assess One-to-One, a separate platform and an integrated solution.
10. Obtain stakeholder sign-off before solution selection.

## 16. Critical appraisal

### Strengths

- The discussion identified the main operational processes.
- Stakeholders recognised that channels require different journeys.
- Stock, payment, finance, reporting and connectivity were treated as linked concerns.
- The group agreed to remain solution-agnostic during discovery.
- The need for one signed-off requirements document was clear.

### Weaknesses

- Several terms and roles are unclear because of transcript quality.
- Stock ownership and financial treatment are unresolved.
- Volumes and performance expectations are absent.
- The exact technology boundary is not defined.
- The retirement date appears inconsistent.
- Requirements were discussed at different levels of detail and require validation.

### Recommendation

Proceed with a short requirements-definition phase using channel-specific process maps and a POPIT assessment covering People, Organisation, Process, Information and Technology.

Do not select or configure a platform until the B2B, B2C and hybrid journeys, stock ownership, payment responsibility and Finance/SAP requirements have been agreed.

## Appendix A: glossary and transcription notes

| Term | Interpretation or issue |
|---|---|
| Evolve | Current stock or sales platform referenced in the meeting. |
| One-to-One | Existing or proposed global platform. Suitability is not yet confirmed. |
| NRL | Current stock-supply or ordering party. Exact future role requires confirmation. |
| Cage | Warehouse stock state referenced by participants. |
| Van | Sellable or field-issued stock state referenced by participants. |
| B2B | Business-to-business transaction. |
| B2C | Business-to-consumer transaction. |
| SAP | Future enterprise platform referenced in the meeting. |
| D365 | Existing enterprise platform referenced in the meeting. |
| BA, VA, EA, WBA | Role abbreviations used in the transcript. Exact definitions require confirmation. |

The transcript contains speech-to-text errors and ambiguous product, system and role names. These must be validated with the meeting participants before requirements are approved.
