# NMI Miura M020 Card Reader Assessment

## UK 1:1 representative readiness and procurement decision paper

**Prepared:** 11 September 2026  
**Scope:** Miura M020 hardware, NMI enablement, operating model and readiness for approximately 50 UK representatives  
**Decision required:** Confirm whether the M020 is a viable interim or target card-present payment solution, and what must be proven before procurement and deployment.

## 1. Executive conclusion

**Recommendation:** Proceed to a controlled technical and commercial proof of concept for the Miura M020, but do not commit the full estate until NMI, Lloyds Cardnet and the implementation team confirm processor certification, merchant onboarding, integration ownership and field connectivity.

The M020 is a credible candidate for the stated use case because it is a compact, UK-supported payment terminal with EMV chip, contactless/NFC and magstripe interfaces, a keypad, display, battery and USB connectivity. NMI’s current guidance supports Wi-Fi configuration, manual or API device registration and card-present integration through the Customer Present Cloud API. The manufacturer material also positions the device for mobile, table-side and tablet-integrated payment scenarios.

The principal decision risk is **not whether the device can read cards**. It is whether the complete service works with the proposed acquirer and estate model. NMI’s published device/processor matrix must be reconciled with the meeting statement that NFC/Tap to Mobile is not supported by Lloyds Cardnet. The public NMI matrix reviewed for this assessment does not provide sufficient evidence that Miura M020 plus Lloyds Cardnet is a supported, certified route. This must be confirmed in writing before purchase.

The M020 should therefore be treated as **conditionally suitable**, subject to five gates:

1. Written confirmation of M020 certification and transaction support for the selected acquirer, including contactless and chip-and-PIN.
2. A working end-to-end integration with the 121 application, including amount hand-off, result return, retries, voids, refunds and reconciliation.
3. A tested operating model for roughly 50 devices and representatives, including pairing, replacement, charging, support and device inventory.
4. Confirmed merchant, MID, AML, credit-check and settlement dependencies, including the meeting assumption of 10–15 working days for new MIDs.
5. A field pilot that demonstrates successful transactions across representative connectivity conditions before the 1 November 2026 target date.

## 2. Situation, sponsor and decision

### Situation

The meeting summary describes an urgent requirement for payment capability for UK 1:1 representatives in advance of the UK Vapes Bill date cited in the meeting: **1 November 2026**. The current discussion has identified a gap between the preferred NMI NFC/Tap to Mobile approach and Lloyds Cardnet support. The fallback under consideration is the NMI Miura M020, potentially paired with tablets or other host devices.

### Sponsor and stakeholders

- **Business sponsor:** UK 1:1 representative operation and WE IDT.
- **Technology and integration:** 121 product/application team and Sean Armstrong’s integration workstream.
- **Payments:** NMI, Lloyds Cardnet and any alternative acquirer.
- **Enterprise architecture:** decision on the target payment pattern and control points.
- **Procurement and finance:** approximately 50 devices, accessories, spares and commercial terms.
- **Representatives and customers:** usability, trust, accessibility and transaction success in the field.

### Decision to be made

Should the organisation adopt the Miura M020 as the interim or target card-present device for UK 1:1 representatives, and under which acquirer, integration and operating-model conditions?

## 3. Method and evidence discipline

Applying the **Business Analysis Process Model**, this paper investigates the product and context, considers stakeholder needs, analyses the current-to-required gap, evaluates options and defines acceptance requirements.

Applying **POPIT** (People, Organisation, Process, Information and Technology) ensures that the assessment does not treat the reader as an isolated hardware purchase.

Evidence is classified as follows:

- **Primary product evidence:** NMI support and developer documentation; Miura manufacturer product material and operational guide.
- **Implementation evidence:** NMI integration documentation and an independent POS integration guide used only to illuminate possible connection patterns.
- **Meeting input:** the supplied meeting summary, including the regulatory date, Cardnet limitation, MID lead time and estate size. These are treated as requirements or assumptions, not independently validated legal or commercial facts.
- **Inference:** conclusions drawn from the evidence and clearly marked where confirmation is still required.

## 4. Product overview

### 4.1 What the M020 is

The Miura M020 is a compact payment terminal intended for countertop, table-side and mobile point-of-sale use. NMI describes its UK M02X offer as accepting EMV payments and lists the M020 as UK-supported. The M020 hardware includes:

- chip card reader;
- contactless/NFC indicators and contactless interface;
- magnetic-stripe reader;
- colour TFT display;
- physical keypad with enter, clear, cancel and function controls;
- USB connector and charging contacts;
- battery-powered operation;
- Bluetooth and Wi-Fi functions.

Miura’s product material also describes USB 2.0 OTG communication, rear M-Link contacts for charging and peripherals, signature-capable capacitive touch, major contactless scheme support and a Revive recovery feature. The exact production configuration, software version, scheme certifications and available accessories must be confirmed against the proposed supply package.

### 4.2 What is included and what is not

NMI’s current quick-start guide lists the base bundle as one M020 reader and a USB-A to micro-USB charging cable. It does not, by itself, establish that the bundle includes:

- a tablet or phone;
- a charging cradle or multi-charger;
- a protective case;
- a managed SIM or mobile data service;
- a receipt printer;
- an acquirer merchant account or MID;
- the 121 application integration;
- field support or replacement stock.

These must be specified in the procurement bill of materials and service contract.

## 5. User-guide analysis

### 5.1 Setup and registration

The NMI quick-start sequence is:

1. Charge and power on the terminal using the red cancel/power control.
2. Open the device menu with the yellow left-arrow control.
3. Configure Wi-Fi by selecting a network and entering its password. Hidden SSIDs are supported only on later MPI releases, according to the guide.
4. Register the device either manually through the NMI Merchant Portal or through the Customer Present Cloud API.

This implies a two-layer onboarding process: physical device setup and logical registration to a merchant account. For 50 devices, manual registration may be possible for a pilot but is a weak scale process unless the implementation team defines naming, serial-number capture, ownership and exception handling.

### 5.2 Pairing and host-device operation

The M020 can operate with a smart device through Bluetooth or Wi-Fi, subject to the integration pattern and software used. A representative third-party POS guide demonstrates the practical implications: Bluetooth commonly creates a one-reader-per-host pairing model, while Wi-Fi can allow several host devices to reach a reader on the same network, although not necessarily concurrently.

This is an important design choice:

- **Bluetooth:** simpler for a representative, clearer device ownership and less network configuration; more sensitive to pairing errors, range and device replacement.
- **Wi-Fi:** potentially more flexible in a controlled environment; dependent on network access, IP discovery, security configuration and stable connectivity.
- **USB:** potentially useful for fixed or tightly controlled tablet configurations; verify operating-system and application support before treating it as a field option.

The product team must specify one supported pattern for the pilot rather than allowing representatives to choose ad hoc.

### 5.3 Payment interaction

The M020’s physical controls and display support customer-facing payment interaction. The operational guide describes separate flows for PIN entry and contactless payment. It warns that the compact design may make contactless cards near the magstripe slot detectable, so contactless should be enabled only when the customer has confirmed that method. This is a relevant training and user-experience consideration.

The 121 application should send a transaction amount and a unique transaction reference to the payment layer. The result should return a controlled status such as approved, declined, cancelled, timed out, reversed or unknown. The system must prevent a representative from retrying an unknown transaction without first checking the gateway status.

### 5.4 Updates, recovery and troubleshooting

The M020 operational guide describes:

- software updates transferred over Bluetooth or Wi-Fi;
- a Revive pin-hole reset for an unresponsive terminal;
- normal reboot, system restore and total factory reset options;
- diagnostic export and hardware functional testing;
- a filtering process covering visual inspection, charging, startup, diagnostics and functional tests.

The guide explicitly notes that an apparent terminal failure may originate in the smart device or application. This supports a tiered support model:

1. representative checks power, battery, pairing and application state;
2. central support checks device registration, transaction status and connectivity;
3. payments/integration support checks gateway, acquirer and MID status;
4. hardware supplier handles tamper state, persistent hardware failure and return-to-repair.

A total factory reset is not a casual first-line action because it requires re-pairing and reconfiguration. The runbook should require central support authorisation and record the device serial number before reset.

## 6. Diagrams and system interpretation

### 6.1 Logical transaction flow

![M020 logical transaction flow.](/tmp/m020_transaction_flow.png)

This is a target logical model, not a confirmed production architecture. The acquirer, API route, certification scope and whether the 121 application talks directly to NMI or through a connector must be confirmed.

### 6.2 Device and estate model

![M020 field estate model.](/tmp/m020_estate_model.png)

The one-reader-per-representative model is operationally simple but may require spare readers, secure storage, charging discipline and a controlled device swap process.

### 6.3 Failure-handling sequence

![Unknown-outcome control to prevent duplicate charges.](/tmp/m020_failure_handling.png)

The most important control is preventing duplicate charges when connectivity fails after the card has been authorised.

## 7. Representative use cases

| Use case | Required behaviour | Evidence or test needed |
|---|---|---|
| 1:1 sale with chip and PIN | Representative enters or confirms amount in 121; customer inserts card and enters PIN; approved result is recorded | End-to-end certified test with Cardnet or selected acquirer |
| 1:1 sale with contactless card or wallet | Customer taps the M020; customer-facing prompts are clear; result returns to 121 | Test physical card and supported wallets; verify limits and fallback to PIN |
| Declined transaction | Decline is shown without exposing sensitive data; representative can offer an approved alternative payment route | Test issuer decline, offline/online response and customer messaging |
| Connectivity interruption before authorisation | Transaction fails safely and can be retried without duplicate charge | Test Wi-Fi loss, Bluetooth loss and host application timeout |
| Connectivity interruption after authorisation | 121 checks status before retrying | Simulate unknown outcome and gateway status lookup |
| Refund or void | Authorised roles can initiate the correct follow-up transaction and retain the original reference | Confirm API and operational permissions; test partial/full refund rules |
| Device replacement | New M020 is registered, paired and assigned without losing auditability | Test swap with inventory, registration and support runbook |
| Lost or stolen device | Device is disabled or deregistered; merchant risk is contained | Confirm NMI controls, acquirer procedure and incident response |
| Battery failure | Representative uses spare/charging process; transaction is not abandoned ambiguously | Measure field battery performance and define charging standard |
| End-of-day reconciliation | All approved, declined, reversed and refunded transactions reconcile to the merchant reporting view | Compare 121, NMI and acquirer reports |

## 8. POPIT assessment

| Dimension | Required target state | Main gap or risk | Action |
|---|---|---|---|
| People | Representatives can take payments and handle common exceptions | Pairing, PIN prompts, contactless behaviour and unknown outcomes may be unfamiliar | Create short training, simulation and escalation script |
| Organisation | Clear ownership across WE IDT, payments, procurement, NMI, Cardnet and Sean’s integration workstream | Device, MID and integration decisions may be split across teams | Name one accountable product owner and one payments owner |
| Process | Repeatable order, register, pair, transact, reconcile, replace and retire lifecycle | 50 devices magnify manual setup and support variation | Define a standard operating procedure and device register |
| Information | Reliable transaction references, serial numbers, MIDs, status and audit trail | Device and payment identifiers may be confused or incomplete | Define data model and reconciliation controls |
| Technology | Certified M020 plus supported host, network and 121 integration | Cardnet compatibility and exact API route are not evidenced publicly | Obtain written certification and complete pilot tests |

## 9. Options appraisal

| Option | Description | Benefits | Drawbacks | Assessment |
|---|---|---|---|---|
| 1. Do nothing / retain current fallback informally | Continue without a controlled device decision | No immediate procurement effort | Does not address readiness, creates operational and compliance exposure | Reject |
| 2. Minimum viable M020 pilot | Procure a small controlled batch, confirm acquirer path, integrate and test with representative scenarios | Fast learning, limits sunk cost, exposes field issues | Temporary dual running and pilot effort | **Recommended next step** |
| 3. Full M020 estate | Procure and deploy approximately 50 M020s after technical sign-off | Consistent device estate and rapid scale | Risk of locking in an unsupported processor path or poor support model | Conditional only |
| 4. Alternative terminal/acquirer | Select a Verifone or other certified route, potentially with stronger mobile connectivity or estate management | May resolve Cardnet/NFC constraint and improve field resilience | New commercial, integration and procurement work; possible longer lead time | Maintain as parallel contingency |
| 5. Tap to Mobile / NFC route | Use software-based contactless acceptance or dedicated NFC host where supported | Lower hardware burden and potentially faster deployment | Not equivalent to full card-present capability; processor/device support is decisive | Do not assume viable until Cardnet certification is confirmed |

### Recommendation and conditions

Back **Option 2**, with a time-boxed proof of concept and Option 4 retained as a contingency. Move to Option 3 only if the five decision gates in Section 1 pass. Change the recommendation towards an alternative terminal if Cardnet cannot certify the M020 route, if the 121 integration requires excessive custom work, or if field connectivity and support performance are unacceptable.

## 10. Procurement and implementation readiness

### 10.1 Minimum bill of materials for a 50-representative deployment

The procurement request should price and specify:

- 50 M020 terminals, plus an agreed spare ratio;
- charging cables and, if needed, cradles or multi-chargers;
- protective cases and secure storage;
- host tablets or phones, if not already available and supported;
- connectivity, including Wi-Fi or managed mobile data where required;
- merchant accounts, MIDs and acquirer fees;
- NMI licensing, device registration and support;
- 121 integration, testing and monitoring;
- training, field support, replacement and return logistics.

### 10.2 Critical dependencies

- Confirm whether a new MID is required per market, legal entity, representative or merchant structure.
- Validate the meeting estimate of 10–15 working days against current AML, credit-check and underwriting requirements.
- Confirm whether one MID can support the operating model and reporting requirements.
- Decide who owns customer receipts, refunds, chargebacks and settlement queries.
- Establish whether representatives use corporate tablets, BYOD devices or dedicated host devices.
- Confirm whether the M020 operates through NMI Customer Present Cloud, an SDK, a virtual terminal or another connector.
- Confirm processor/acquirer certification for every payment method required.

### 10.3 Indicative delivery sequence

1. **Day 0–2:** confirm sponsor, decision owner, processor route, MID model and integration architecture.
2. **Day 1–5:** obtain commercial quotes, certification evidence, security requirements and pilot devices.
3. **Day 3–10:** configure NMI, register devices, build or configure the 121 connector and produce the runbook.
4. **Day 8–12:** execute functional, security, exception and reconciliation tests.
5. **Day 10–15:** run a representative pilot and make the go/no-go decision for the wider estate.

This sequence is illustrative. It does not replace the meeting’s 10–15 working-day MID assumption or a formal project plan.

## 11. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation / owner to assign |
|---|---:|---:|---|
| M020 is not certified for Lloyds Cardnet in the required NMI path | High until confirmed | High | Written NMI/Cardnet confirmation before purchase |
| 121 integration cannot distinguish unknown, declined and approved outcomes | Medium | High | Define status model and automated status lookup |
| MID onboarding exceeds the assumed 10–15 working days | Medium | High | Start underwriting immediately; obtain dependency dates |
| Bluetooth pairing or host-device inconsistency causes field failures | Medium | Medium | Standardise host hardware and run pairing test at dispatch |
| Battery or charging discipline reduces availability | Medium | Medium | Measure battery life; issue charging standard and spares |
| Device loss, tamper or replacement is not controlled | Medium | High | Maintain serial register, disable procedure and spare pool |
| Representatives retry transactions after unknown outcomes | Medium | High | Training, UI controls and gateway status check |
| Contactless capability exists in hardware but not in the selected processing route | High | High | Separate hardware capability from processor certification |

## 12. Acceptance criteria for go/no-go

The M020 route should not be approved for full deployment until all criteria are met:

- [ ] NMI and the selected acquirer confirm in writing that M020 is certified for the required UK transaction types.
- [ ] Lloyds Cardnet position is explicitly recorded for M020 chip, contactless and any NFC/Tap to Mobile alternative.
- [ ] 121 can initiate a transaction, pass a unique reference, receive a final status and prevent unsafe retries.
- [ ] Approved, declined, cancelled, timed-out, reversed, voided and refunded journeys are tested.
- [ ] Device registration, pairing, replacement, lost-device and factory-reset procedures are documented.
- [ ] Merchant, MID, AML, credit-check and settlement responsibilities are agreed.
- [ ] Serial number, device ID, merchant ID and transaction reference data are reconciled end to end.
- [ ] Representative training and support escalation are tested with users.
- [ ] Field pilot results meet agreed transaction-success, support and availability thresholds.
- [ ] Security, PCI/P2PE scope and data-handling responsibilities are confirmed by the payments and security owners.

## 13. Evidence gaps requiring explicit validation

The public sources reviewed do not establish the following points for this specific programme:

- Lloyds Cardnet certification or commercial availability of the M020 through the NMI route.
- The exact NMI product/API selected for the 121 integration.
- Whether the required transaction types and refunds are supported in the chosen flow.
- Current purchase price, lead time, warranty, repair SLA and stock availability.
- Battery endurance in the intended representative workflow.
- Mobile-data or Wi-Fi operating model outside controlled premises.
- Exact UK Vapes Bill obligations and how they apply to this operating model.
- Whether 50 representatives require 50 MIDs, one MID, or another merchant structure.

These are decision-critical gaps, not minor documentation details.

## 14. Peer-review conclusion

The report was reviewed against the requested scope and the BCG-plus consulting quality gate.

- **Decision framed:** yes, the device and operating-model decision is explicit.
- **Evidence distinguished from inference:** yes, meeting assumptions and public documentation are separated.
- **User guides analysed:** yes, setup, registration, pairing, transaction, updates, recovery and testing are covered.
- **Diagrams included:** yes, transaction flow, estate model and failure-handling sequence are included.
- **Use cases included:** yes, core sale, exception, support, replacement and reconciliation journeys are covered.
- **Whole-system view:** yes, POPIT, procurement, MIDs, support and adoption are included.
- **Options:** yes, baseline, minimum, full, alternative and Tap to Mobile options are assessed.
- **Recommendation:** yes, a conditional pilot recommendation and change conditions are stated.
- **Formatting and consistency:** headings, tables, terminology and acceptance criteria were checked for alignment and internal consistency.

## 15. Sources

1. NMI, [Miura M02X Quick Start Guide](https://support.nmi.com/hc/en-gb/articles/13556811794577-Miura-M02X-Quick-Start-Guide), accessed 11 September 2026.
2. NMI, [Payment processors and devices](https://www.nmi.com/payment-processors-devices/), accessed 11 September 2026.
3. NMI, [Customer Present Cloud API](https://docs.nmi.com/docs/device-api-cloud), accessed 11 September 2026.
4. NMI, [Standalone device inputs](https://docs.nmi.com/docs/standalone-device-inputs), accessed 11 September 2026.
5. NMI, [Obtaining payment device information](https://support.nmi.com/hc/en-gb/articles/15397546851857-Obtaining-Payment-Device-Information), accessed 11 September 2026.
6. Miura Systems, [Miura product guide](https://miurasystems.com/hubfs/MiuraUI2018/Downloads/J1724_Miura_product_guide_v6.2.pdf?t=1515784564485), accessed 11 September 2026.
7. Miura Systems, [M020 Operational Guide](https://fccid.io/2AO4FM020-1/User-Manual/User-Manual-3901319.pdf), accessed 11 September 2026.
8. Mews, [Connecting a Miura M020 to a mobile device](https://help.mews.com/articles/en_US/Knowledge/connecting-a-card-reader-miura-m020-to-a-mobile-device), accessed 11 September 2026. Used as implementation evidence for connection patterns, not as manufacturer certification.

**Important:** Product capability, processor support, legal applicability and deployment dates must be confirmed with the relevant commercial, legal, security and payments owners before procurement.
