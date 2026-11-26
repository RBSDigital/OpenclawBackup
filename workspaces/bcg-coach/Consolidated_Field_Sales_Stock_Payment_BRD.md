**BUSINESS REQUIREMENTS DOCUMENT**

Field Sales, Stock Management and Financial Reconciliation

Replacement capability for festivals, pop-ups, Retail One-to-One and
other field activations

| **Field** | **Detail** |
|----|----|
| Version | 1.0 consolidated draft |
| Status | Draft for stakeholder validation |
| Prepared by | Business Analysis, consolidated from two supplied BRD artefacts |
| Date | 25 November 2026 |
| Source | Two supplied BRD artefacts and the meeting transcript recorded 25 November 2026 |
| Approval status | Not approved. Operating model, scope, requirements and solution remain subject to validation. |

| **Purpose: establish a solution-neutral baseline of the business need before assessing whether One-to-One, a global platform, an off-the-shelf product or another capability is the best fit.** |
|----|

Evidence note: statements are derived from the supplied draft and
transcript. Conflicts, unclear terminology and unsupported technical
detail are retained as open points rather than converted into facts.

# Document Control

| **Version** | **Date** | **Change** | **Status** |
|----|----|----|----|
| 0.1 | 25 November 2026 | Initial transcript-based draft | Draft |
| 0.2 | 25 November 2026 | Consolidated current state, requirements, risks and open issues | Draft |
| 0.3 | 25 November 2026 | Structured management-ready BRD baseline with prioritised requirements and decision agenda | Draft for validation |
| 1.0 | 25 November 2026 | Consolidated the two supplied BRDs; added traceability, benefits, acceptance conditions and source-quality controls | Consolidated draft |

## Review and Approval

| **Role** | **Named owner** | **Required contribution** |
|----|----|----|
| Business sponsor / owner | TBC | Approve scope, priorities, operating model and final BRD |
| Field Operations / Channel leads | TBC | Validate channel journeys, volumes, user roles and operational needs |
| Finance and Treasury | TBC | Approve stock ownership, funds flow, revenue treatment, reconciliation and write-offs |
| Global Platform / One-to-One | TBC | Assess platform fit and governance |
| Technology / Architecture | TBC | Assess options, integrations, security, support and transition |
| ERP / SAP team | TBC | Confirm D365-to-SAP impacts and interfaces |
| Agencies / field users | TBC | Validate hand-offs, usability, access and offline working |

# Contents

1\. Executive Summary

2\. Background and Business Need

3\. Objectives and Success Measures

4\. Scope

5\. Stakeholders and Governance

6\. Current-State Assessment

7\. Target Business Capability

8\. Business Requirements

9\. Non-Functional Requirements

10\. Data, Reporting and Integration

11\. Business Rules and Decisions

12\. Risks, Assumptions and Dependencies

13\. Transition and Acceptance

14\. Recommended Next Steps

1\. Appendix A. Glossary

# 1. Executive Summary

| **The immediate business need is to maintain agreed field-activation activity when Evolve is decommissioned, while improving stock accountability, field usability and financial reconciliation.** |
|----|

The current process spans stock ordering and receipt, custody transfers,
product preparation, sales or sampling, portable payment, end-of-shift
counts, returns and Finance reconciliation. The meeting indicates that
these activities are fragmented across Evolve, One-to-One, payment
devices, agencies and manual controls. Transactions recorded in
One-to-One do not currently deplete Evolve inventory, and several
operating-model choices remain unresolved.

No replacement solution has been selected. The BRD therefore remains
solution-neutral. Candidate options include extending One-to-One, using
a future Evolve or global capability, procuring an off-the-shelf
point-of-sale and stock product, or implementing a separate capability
with integrations.

## Decisions required first

- Confirm the exact Evolve decommissioning date. The transcript
  references both 7 July, with no confirmed year, and June 2027, with a
  mid-June readiness need.

- Confirm which channels and journeys are in scope: festivals, pop-ups,
  Retail One-to-One, Flight Teams, Recorders and other activation
  models.

- Approve stock ownership, custody, sales, payment, venue revenue and
  retailer-balancing models for each channel.

- Confirm the relationship between NRL, AT stock, Evolve, One-to-One,
  E265, D365, SAP and Tetris/BAT Club.

- Assign accountable business, Finance, Treasury, platform and
  technology decision-makers.

## Recommended approach

1\. Validate channel process maps and business rules.

2\. Baseline the requirements and measurable non-functional needs.

3\. Assess solution options against the approved requirements and
transition date.

4\. Pilot the approved end-to-end journeys with field, agency and
Finance users before cutover.

# 2. Background and Business Need

Evolve is used for stock and sales-related activity supporting festivals
and pop-ups. The discussion also covers future use across Retail
One-to-One and field activation channels. The existing capability is
expected to be retired, creating a continuity risk unless a replacement
process or capability is ready.

## Reported current-state flow

1\. Stock is ordered through NRL and delivered to an agency or agency
warehouse.

2\. The agency counts the delivery, accepts it and records
discrepancies.

3\. Stock is held in a “cage” state and moved to a “van” or sellable
state.

4\. Products are broken down into saleable units; prices and approved
discount codes are configured.

5\. Field users select products and take portable card payments where
relevant.

6\. Stock is counted at shift end, variances are explained and unused
stock is returned.

7\. Finance reconciles stock, payments and exceptions, with E265
referenced but not defined.

## Drivers for change

- Evolve decommissioning and the need to protect operational continuity.

- Potential move from NRL-purchased stock to internally owned AT stock.

- Potential D365-to-SAP transition and associated financial/integration
  changes.

- Disconnected stock depletion and consumer-interaction processes.

- Poor product-selection usability, including long lists and no product
  images.

- Email-based MFA and agency proxy-account workarounds.

- Poor or absent connectivity at festivals and field locations.

- Limited visibility of product cost, delivery charges and
  activation-budget impact.

# 3. Objectives and Success Measures

| **ID** | **Objective** | **Draft success indicator** |
|----|----|----|
| OBJ-01 | Maintain approved activations after Evolve retirement | Approved journeys operate without reliance on Evolve after cutover. |
| OBJ-02 | Provide end-to-end stock accountability | Stock can be traced through receipt, custody, activity, count and return. |
| OBJ-03 | Support approved sales, payment and reconciliation models | Stock, transaction and payment outcomes reconcile under Finance-approved rules. |
| OBJ-04 | Improve field usability | Representative users can identify products and complete transactions on supported devices. |
| OBJ-05 | Improve management information | Approved sales, stock, exception and cost reporting is available to authorised users. |
| OBJ-06 | Support poor-connectivity operations where required | Approved offline scenarios preserve complete, non-duplicated records. |
| OBJ-07 | Provide accountable access | Users access the capability through an approved identity model without unapproved proxy accounts. |

No numerical KPI baseline or target was approved. Proposed figures in
the source, including 99.9% availability, 72-hour offline working and
60-second synchronisation, require validation before inclusion in a
baseline.

# 4. Scope

## In scope, subject to validation

- Festival, pop-up, Retail One-to-One and other approved field
  activation journeys.

- Stock allocation/order, delivery, receipt, count, preparation, custody
  transfer, sale or sampling, return and reconciliation.

- Product and saleable-unit definitions, prices and approved discounts.

- Portable field sales or activity recording, including product imagery
  where appropriate.

- Payment recording where BAT or its field team collects payment.

- Approved B2B, B2C and hybrid journeys.

- Stock, sales, payment, exception and activation-cost reporting.

- Solution assessment and transition away from Evolve.

## Not yet agreed or excluded from this baseline

- Selection or procurement of a specific replacement solution.

- Detailed architecture, API design, database choice or SAP core
  configuration.

- Modification of third-party retailer payment terminals.

- A definitive venue-retained revenue or retailer-pricing model.

- Complex consumer CRM functionality outside confirmed One-to-One or
  Tetris boundaries.

- Unapproved service levels, technical thresholds or global rollout
  commitments.

# 5. Stakeholders and Governance

| **Stakeholder group** | **Primary interest / decision** |
|----|----|
| Business sponsor / channel owner | Scope, continuity, commercial model and priority |
| Field teams, supervisors and agencies | Usable stock, sales, count, return and access processes |
| Finance and Treasury | Ownership, funds flow, reconciliation, write-off and reporting controls |
| Trade Systems / product and pricing owners | Product, price, discount and approval rules |
| Global Platform / One-to-One | Platform scope, governance and re-use decision |
| Technology / Architecture / Security | Solution, integration, identity, security, resilience and support |
| SAP / ERP programme | Target financial and stock interfaces |
| Retailers and venues | Commercial roles, revenue and operational hand-offs |

| **Governance gap: no approved sponsor, product owner, RACI, decision forum or escalation route was established in the meeting.** |
|----|

# 6. Current-State Assessment

| **Area** | **Current position** | **Business impact** |
|----|----|----|
| Stock ledger | Stock and consumer-interaction activity are not consistently connected. | Manual reconciliation and risk of inaccurate availability. |
| Custody | Multiple counts and hand-offs across warehouse, cage, van and field user. | Disputes, shrinkage and unclear accountability. |
| Product setup | Units must be broken down and Evolve is described as ounce-oriented. | Configuration complexity and count errors. |
| Field interface | Long scrolling product list with no images. | Slow selection and risk of choosing the wrong product. |
| Payments | Portable Bluetooth card machines are used; funds-flow models vary. | Payment and stock outcomes may not reconcile consistently. |
| Identity | Email MFA creates reported proxy-account workarounds. | Security, audit and operational friction. |
| Connectivity | Festivals may have poor or no signal. | Transactions or stock movements may be interrupted. |
| Reporting | Cost and product-level visibility is limited or manually obtained. | Slower decisions and weak budget transparency. |

# 7. Target Business Capability

The target capability should support the approved operating models while
remaining clear about where financial ownership transfers and where BAT
accountability ends.

- Create or receive an approved stock allocation for an activation.

- Record delivery, receipt, accepted quantity and discrepancy.

- Represent approved stock states and custody holders.

- Maintain products, saleable units, prices, images and approved
  discounts.

- Record sales or sampling and apply the corresponding stock movement.

- Record payment status and references where payment is in scope.

- Support closing counts, return hand-offs and discrepancy reasons.

- Reconcile stock, activity, payment and financial outcomes.

- Provide channel, product, stock, exception and cost reporting.

- Support approved offline behaviour and controlled synchronisation.

- Attribute controlled actions to an identified user or role.

# 8. Business Requirements

| **ID** | **Area** | **Requirement** | **Priority** | **Key dependency** |
|----|----|----|----|----|
| BR-001 | Business | Support each activation journey approved for continuation after Evolve retirement. | Must | Scope and retirement date |
| BR-002 | Stock | Record stock ordered, allocated or transferred to an activation and reconcile it to receipt. | Must | Stock sourcing and ownership |
| BR-003 | Stock | Record received quantities, acceptance and discrepancies against expected quantities. | Must | Receiving roles and source data |
| BR-004 | Stock | Represent approved warehouse, transit, van, field-user and retailer custody states. | Must | Future stock-state model |
| BR-005 | Product | Support approved received units, saleable units and conversion rules. | Must | Product master data |
| BR-006 | Pricing | Apply approved product prices with effective dates and authority. | Must | Pricing owner and rules |
| BR-007 | Pricing | Support approved discount codes and retain evidence of their application. | Should | Discount policy |
| BR-008 | Usability | Enable field users to identify products quickly; assess search, categories and product images. | Should | Image assets and UX design |
| BR-009 | Transaction | Record each approved sale or sampling activity and its stock effect. | Must | Channel definitions |
| BR-010 | Payment | Where the field team collects payment, record the approved method, status and reference. | Must if applicable | Payment provider and funds flow |
| BR-011 | Count | Record end-of-shift or activation counts, variances and required explanations. | Must | Variance rules |
| BR-012 | Return | Record return dispatch, receipt, quantities and discrepancies. | Must | Return locations and roles |
| BR-013 | Reconciliation | Support investigation and disposition of missing stock, failed payments and other exceptions. | Must | Finance rules and authority |
| BR-014 | Channel | Support venue-retained revenue only where that scenario is explicitly approved. | Conditional | Commercial and Finance decisions |
| BR-015 | Reporting | Provide approved product-level sales and activity reporting, including relevant product attributes. | Should | Report definitions |
| BR-016 | Audit | Attribute controlled stock, price, discount, transaction and reconciliation actions to a user or role. | Should | Identity and audit model |
| BR-017 | Transition | Provide an approved transition and readiness assessment before Evolve is decommissioned. | Must | Confirmed dates and solution |
| BR-018 | Product | Distinguish confirmed non-commercial nano cans from commercial stock and enforce usage rules. | Conditional | Product and policy validation |
| BR-019 | Retail | Support retailer balancing at 100% discount only if Finance and the business approve the model. | Conditional | Commercial model |
| BR-020 | Offline | If offline working is required, retain records for later synchronisation and prevent duplicates. | Conditional | Device, network and payment capability |
| BR-021 | Security | Use an approved identity model and avoid unapproved shared or proxy accounts. | Should | Security and agency model |
| BR-022 | Cost reporting | Provide approved stock cost, delivery overhead and activation-budget information. | Should | ERP and Finance data |

# 9. Non-Functional Requirements

| **ID** | **Area** | **Requirement to baseline** |
|----|----|----|
| NFR-01 | Performance | Agree response-time expectations for product selection, checkout, counts and synchronisation. |
| NFR-02 | Capacity | Confirm users, SKUs, daily transactions, custody transfers and offline queue volumes by channel. |
| NFR-03 | Availability | Define service hours, event/weekend support and permitted downtime. |
| NFR-04 | Offline resilience | Define which actions must work offline, for how long, and how conflicts and payments are handled. |
| NFR-05 | Security | Define named-user access, role-based permissions, shared-device controls, encryption and audit evidence. |
| NFR-06 | Privacy | Confirm whether personal data is required by journey and define lawful basis, consent, minimisation and retention. |
| NFR-07 | Reliability | Define retry, duplicate prevention, recovery and reconciliation for network, application and payment failures. |
| NFR-08 | Usability and accessibility | Validate field use in low-light, mobile and high-throughput conditions and agree accessibility needs. |
| NFR-09 | Compatibility | Confirm supported tablets, phones, operating systems, browsers, card readers and connectivity hardware. |
| NFR-10 | Supportability | Define service ownership, monitoring, alerting, diagnostics, support hours and operational runbooks. |

# 10. Data, Reporting and Integration

## Core data entities

| **Entity** | **Minimum candidate content** |
|----|----|
| Product / SKU | Identifier, name, category, flavour/attribute, image, received unit, saleable unit, commercial classification |
| Stock balance | Product, quantity, unit, state, location, custody holder and ownership where required |
| Stock movement | Source, destination, quantity, time, sender, receiver, movement type, status and discrepancy |
| Activation | Identifier, channel, location, date, assigned users and assigned stock |
| Price / discount | Product, value, eligibility, effective period, approval and audit evidence |
| Sale / sampling | Product, quantity, channel, user, activation, price, discount, outcome and stock effect |
| Payment | Amount, currency, method, status, reference, settlement and exception |
| Count / return | Expected quantity, actual quantity, variance, reason, dispatch, receipt and approval |
| Reconciliation exception | Type, evidence, investigation, decision, write-off or recovery and approver |
| Activation cost | Product cost, delivery charge, cost centre and activation allocation |

## Candidate reports

- Activation product sales and product-attribute analysis.

- Stock movement, custody, closing balance and discrepancy.

- Payment outcome and Finance reconciliation.

- Activation budget, product cost and delivery overhead.

- Retailer balancing, if approved.

- Multi-channel sales, sampling and acquisition summary, subject to
  privacy scope.

## Candidate integrations requiring validation

| **Integration** | **Purpose** | **Status** |
|----|----|----|
| Evolve to transition capability | Migration or continuity of product, stock, price or transaction information | Future role unknown |
| Field POS to payment service | Submit or record payment and status | Provider and technical capability unconfirmed |
| Future capability to SAP / Finance | Post or reconcile stock, sales, payment and cost information | D365-to-SAP scope unconfirmed |
| Product / pricing source to field capability | Supply approved product, price and discount data | Master-data owner unconfirmed |
| Future capability to One-to-One / Tetris | Supply consumer interaction or engagement data where required | Scope, consent and platform ownership unconfirmed |

# 11. Business Rules and Decisions

| **Decision** | **Question to resolve** | **Required owner** |
|----|----|----|
| D-01 Channel scope | Which festivals, pop-ups, Retail One-to-One, Flight Team, Recorder and hybrid journeys must be supported? | Business owner |
| D-02 Payment and revenue | Who takes payment and who retains or receives revenue in each journey? | Business, Finance and Treasury |
| D-03 Stock ownership | Who owns stock at each stage and when does financial ownership transfer? | Business and Finance |
| D-04 Retailer balancing | Is the 100% discount / £0 balancing model approved and for which products? | Commercial and Finance |
| D-05 Venue-retained revenue | Is this model included, excluded or deferred? | Business and Finance |
| D-06 Product rules | What are the definitions and permitted uses of commercial stock, WSS/WSO stock and nano cans? | Product / policy owner |
| D-07 Pricing and exceptions | Who approves prices, discounts, variances and write-offs? | Trade Systems and Finance |
| D-08 Offline scope | Which transactions and stock actions must remain available without connectivity? | Business and Technology |
| D-09 Platform option | Should One-to-One be extended, or should another solution be selected? | Sponsor, Global Platform and Technology |
| D-10 Transition date | What are the exact Evolve retirement and readiness dates? | Evolve / business owner |

# 12. Risks, Assumptions and Dependencies

| **ID** | **Risk** | **Impact** | **Response** |
|----|----|----|----|
| R-01 | Replacement is not ready before Evolve retirement. | High | Confirm dates, prioritise minimum journeys and define contingency. |
| R-02 | Stock ownership or funds flow remains unresolved. | High | Obtain Finance and Treasury approval before design. |
| R-03 | Custody hand-offs lack clear accountability. | High | Define send/receive evidence, roles, counts and variance treatment. |
| R-04 | One-to-One cannot be extended or is not suitable. | High | Maintain solution-neutral requirements and assess alternative products. |
| R-05 | Poor connectivity causes lost or duplicate activity. | High | Baseline offline rules and test synchronisation and recovery. |
| R-06 | ERP assumptions are incorrect or interfaces are unavailable. | High | Confirm SAP programme scope, data ownership and timing. |
| R-07 | Ambiguous product and role terminology drives incorrect design. | Medium | Validate glossary, role model and representative products. |
| R-08 | Authentication workarounds continue. | Medium-high | Agree agency identity and shared-device controls with Security. |

## Key assumptions

- At least some activation activity must continue after Evolve is
  retired.

- Stock must be traceable across approved custody points.

- Multiple B2B, B2C and hybrid journeys may be required, but none is
  treated as approved solely because it was discussed.

- AT stock may replace NRL purchasing, subject to confirmation.

- Offline capability may be necessary at festivals, subject to detailed
  validation.

## Critical dependencies

- Confirmed decommissioning and readiness dates.

- Approved operating and financial models by channel.

- Finance and Treasury decisions on payments, settlement and
  reconciliation.

- Confirmed SAP, One-to-One, E265, Tetris and master-data boundaries.

- Agency, venue and retailer responsibilities.

- Validated volumes, devices, network conditions and support model.

# 13. Transition and Acceptance

No delivery plan is approved. The following gates should be completed
before implementation commitments are made.

1\. Approve scope, channel journeys, business rules and governance.

2\. Confirm Evolve retirement, readiness and contingency dates.

3\. Assess solution options against the requirements and transition
constraint.

4\. Complete detailed design for data, integration, identity, payment,
audit and support.

5\. Pilot with representative field, agency and Finance users under
online and poor-connectivity conditions.

6\. Complete business, Finance, security, operational and technical
acceptance.

7\. Execute an approved cutover, rollback and decommissioning plan.

## Draft acceptance principles

- All approved Must requirements pass end-to-end business acceptance.

- Stock, sales and payment outcomes reconcile for each approved
  scenario.

- Critical defects are resolved or formally accepted by an authorised
  owner.

- Finance and Treasury approve financial outcomes and controls.

- Operational support, training, monitoring and incident routes are
  ready.

- Named go-live and residual-risk authorities approve deployment.

# 14. Recommended Next Steps

| **Priority** | **Action** | **Output** |
|----|----|----|
| 1 | Confirm Evolve retirement date, year, scope and mid-June readiness definition. | Written date and readiness decision |
| 2 | Map and validate Retail One-to-One, Festivals, Flight Teams and Recorders separately. | Approved channel process maps |
| 3 | Run a Finance and Treasury decision workshop on ownership, payment, revenue, retailer balancing and write-offs. | Approved financial operating model |
| 4 | Confirm system landscape and programme dependencies across Evolve, One-to-One, NRL, AT stock, E265, D365, SAP and Tetris. | Validated system and integration context |
| 5 | Collect volumes: users, retailers, activations, SKUs, transactions, transfers, returns and peak/offline periods. | Capacity and NFR baseline |
| 6 | Assign sponsor, product owner, process owners, requirement owners and approvers. | Governance and RACI |
| 7 | Baseline the BRD, then run a structured option assessment. | Signed requirements baseline and recommendation |

| **The BRD should not be signed off until the conflicting retirement dates and the channel-specific stock, payment and revenue models have been resolved.** |
|----|

## 15. Benefits and measures

The supplied artefacts support expected benefits, but do not provide a quantified baseline. Benefits must therefore be validated rather than presented as achieved.

| Benefit ID | Expected benefit | Proposed measure | Evidence status |
|---|---|---|---|
| BEN-001 | Reduced risk of stock loss and unexplained variance | Stock variance by activation and channel | Baseline required |
| BEN-002 | Faster and more reliable field sales | Transaction completion time and failure rate | Baseline required |
| BEN-003 | Better financial visibility | Time to reconcile stock, payments and costs | Baseline required |
| BEN-004 | Reduced manual work and duplicate entry | Manual steps and re-keying per activation | Baseline required |
| BEN-005 | Improved user experience | User completion rate and field-user feedback | Baseline required |
| BEN-006 | Greater continuity during poor connectivity | Successful offline transactions and synchronisation exceptions | Baseline required |

Each benefit requires an owner, baseline, target, measurement frequency and review date before it can be treated as a committed outcome.

## 16. Acceptance and traceability

The following traceability rules apply to the consolidated requirements:

- Every approved requirement must trace to an objective, process, decision or stakeholder need.
- Every Must requirement must have at least one acceptance scenario.
- Every requirement involving Finance, payment, stock ownership or SAP must be approved by the relevant owner before solution selection.
- Every non-functional requirement must have a measurable threshold or an explicit validation action.
- Every implemented requirement must trace forward to design, configuration and test evidence.

### Representative acceptance scenarios

**AC-001: Stock receipt**

- Given an approved stock dispatch exists,
- when the agency receives the stock,
- then the authorised user can confirm quantities, record discrepancies and identify the receiver.

**AC-002: Sale and payment**

- Given a product is available for sale,
- when an authorised user records a sale and payment,
- then the transaction records the product, quantity, price, discount, payment status, user, activation and time.

**AC-003: Failed payment**

- Given a payment fails or is declined,
- when the transaction is closed,
- then the system does not treat the item as a successful sale unless an approved exception is recorded.

**AC-004: End-of-shift reconciliation**

- Given stock has been issued for an activation,
- when the shift closes,
- then issued, sold, returned and remaining quantities reconcile, or each variance has an approved reason and status.

**AC-005: Offline operation**

- Given the device has no network connection,
- when an approved offline action is completed,
- then the record is retained locally and synchronises once connectivity returns without creating a duplicate.

## 17. Consolidation review

The two supplied artefacts were assessed as follows:

### Strengths of the first BRD

- Clear business purpose and scope.
- Strong high-level requirements catalogue.
- Useful acceptance criteria and explicit evidence gaps.
- Clear recommendation to remain solution-neutral.

### Strengths of the second BRD

- Stronger document control and approval structure.
- More complete current-state assessment.
- Better treatment of channel variation, system dependencies and decision points.
- More mature data, integration, transition and non-functional sections.
- Better distinction between confirmed information and proposed thresholds.

### Consolidation changes

- Retained the second BRD's stronger operating-model, data, integration and transition structure.
- Retained the first BRD's explicit business capabilities around stock, payment, returns, failed transactions, reporting and audit.
- Removed repeated requirements and combined overlapping statements.
- Replaced unsupported claims with validation actions or evidence gaps.
- Added benefits measures, acceptance scenarios and traceability controls.
- Preserved unresolved dates, role names, product terms and financial decisions as open points.
- Set the status to a consolidated draft rather than an approved baseline.

### Remaining quality limitations

- The source transcript contains speech-to-text errors and ambiguous system and role names.
- The BRD is not ready for final approval until the decision agenda is resolved.
- No quantified volume, performance, cost or benefits baseline was supplied.
- Detailed process maps and a formal RACI remain outstanding.

# Appendix A. Glossary

| **Term** | **Working meaning** | **Validation status** |
|----|----|----|
| AT stock | Internal stock model or source expected to replace external/NRL purchasing | Meaning and timing to confirm |
| BA / VA / PA / EA | Field-role labels used inconsistently in the transcript | Role mapping to confirm |
| Cage / van | Current stock states; “van” is described as sellable stock | Future definitions to confirm |
| E265 | System or process referenced for financial reconciliation | Exact role unknown |
| Evolve | Current stock and sales-related capability | Scope and retirement date to confirm |
| Nano cans | Reported 10-pouch non-commercial cans for acquisition or sampling | Product status and rules to confirm |
| NRL | Current stock-purchasing or supply party/process | Expansion and future role unknown |
| One-to-One | Consumer-interaction application and candidate platform option | Current and future scope to confirm |
| Tetris / BAT Club | Consumer-engagement platform referenced in the discussion | Integration need to confirm |
| WSS / WSO / CD | Terms appearing in the transcript | Definitions may be mistranscribed; validate |

# Appendix B. Source and Evidence Caveats

- Source material comprises the supplied draft BRD and meeting
  transcript recorded on 25 November 2026.

- No approved process maps, financial model, policy set, system
  architecture, data dictionary, volume model or service-level agreement
  was supplied.

- Statements attributed to unnamed speakers must be validated with
  identified stakeholders.

- Proposed technical figures and detailed workflows are not treated as
  commitments unless separately approved.
