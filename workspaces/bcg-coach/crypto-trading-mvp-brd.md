# Business Requirements Document

## Crypto market-data, strategy research and backtesting MVP

**Version:** Final reviewed v1.2, n8n update  
**Date:** 16 October 2026  
**Decision required:** Approve the recommended MVP architecture and implementation boundary.  
**Primary audience:** An LLM or engineering team that will design and build the project.

## Executive recommendation

Build a **manual, research-only Python MVP** that retrieves spot-market data from one execution venue, tests a controlled library of trading strategies with realistic costs, and produces a daily decision report. Use **Kraken Spot as the first venue**, accessed through a small exchange adapter using CCXT for standardised REST access, with the option to call Kraken’s official WebSocket or REST endpoints directly where the unified abstraction loses important detail.

Use:

- `uv` for Python project management, dependency locking and repeatable execution;
- Python 3.12+ subject to package compatibility validation at build time;
- `pandas`/NumPy-compatible structures at the strategy boundary because VectorBT is built around them;
- VectorBT for fast, parameterised research and portfolio simulation;
- Parquet files as the immutable raw and curated data format;
- DuckDB for local analytical queries and report generation;
- Pydantic or equivalent typed configuration and validation;
- pytest for automated tests;
- a command-line workflow first, with notebooks optional for exploration;
- n8n, if adopted, only as an orchestration, notification and run-control layer around the Python CLI; the Python application remains the source of truth and must run without n8n;
- no exchange credentials, order placement or automated trading in the MVP.

This is a recommendation for a research system, not investment advice or a promise of profit. “Maximise returns” should be translated into **maximise out-of-sample net, risk-adjusted performance subject to explicit drawdown, liquidity, turnover and robustness limits**. A strategy that has the highest historical return but fails under costs, alternate periods or out-of-sample data must be rejected.

## 1. Situation, problem and desired outcome

### Situation

The proposed service should support a repeatable morning workflow:

1. Select a desired cryptocurrency or a screened universe.
2. Retrieve current and historical market data.
3. Check data quality and provenance.
4. Apply candidate trading strategies.
5. Backtest each strategy with fees, spread and slippage assumptions.
6. Reject strategies that fail defined gates.
7. Produce a ranked research report and a clear “no actionable result” outcome where no strategy passes.

The longer-term ambition is to automate the process and potentially move performance-critical components to Rust on a VPS. The MVP must therefore create clean interfaces and reproducible artefacts without prematurely building a live trading platform.

### Problem statement

Without a controlled data pipeline and validation framework, apparent strategy returns may be caused by bad timestamps, survivorship bias, look-ahead bias, unrealistic fills, omitted fees, unstable exchange data or overfitting. The primary problem is therefore **not a shortage of strategies; it is the absence of a trustworthy, repeatable research process**.

### Desired outcome

The MVP should allow a technically capable operator to run one documented command each morning and receive:

- the data snapshot used;
- data-quality warnings;
- strategy configurations and assumptions;
- net performance metrics;
- in-sample, validation and out-of-sample results;
- robustness and sensitivity tests;
- a ranked shortlist, if any strategy passes;
- reasons for rejecting other strategies; and
- a reproducible result package that can be rerun later.

## 2. Scope and boundaries

### In scope

- Spot cryptocurrencies and spot trading pairs only.
- One primary exchange in the first implementation.
- Public market-data retrieval without trading credentials.
- Daily or hourly bars as the initial supported frequencies.
- Manual morning execution through a CLI.
- Asset selection by explicit symbol, with optional configurable screening.
- Historical OHLCV data, volume and metadata available from the chosen venue.
- Data validation, normalisation, storage and provenance.
- A small baseline strategy library.
- Backtesting with configurable fees, spread and slippage.
- Train/validation/test or walk-forward evaluation.
- Performance, risk and robustness reporting.
- Local reproducibility and basic automated tests.
- Optional n8n orchestration for a manual or scheduled trigger, run-status capture and report notification, subject to the deployment controls in Section 4.3.

### Out of scope for the MVP

- Live order placement or automated execution.
- Custody, withdrawals, deposits or wallet management.
- Leverage, margin, perpetuals, futures, options or borrowing.
- High-frequency trading or latency-sensitive strategies.
- Predicting prices with machine learning as a first release.
- Social-media sentiment ingestion.
- Tax calculation or investment advice.
- A public web application or multi-user account system.
- n8n as the quantitative calculation engine, market-data adapter or source of strategy logic.
- Guaranteed profitability or an optimisation target based only on gross return.

## 3. Stakeholders and decision rights

| Stakeholder | Need or concern | Decision or contribution |
|---|---|---|
| Product owner / operator | A practical morning workflow and understandable report | Approves scope, asset universe and acceptance gates |
| Research user | Fast strategy comparison and transparent assumptions | Defines research questions and reviews results |
| Implementing LLM or engineer | Clear interfaces, testable requirements and constraints | Builds, tests and documents the system |
| Exchange/API provider | Acceptable API usage and rate-limit compliance | Source of market data and venue rules |
| Future operations owner | Secure, repeatable deployment and observability | Owns any later VPS automation |
| Compliance/tax adviser, if trading or promotion is introduced | UK regulatory, tax and consumer-protection implications | Validates the operating model before expansion |

**Accountability:** The product owner approves the research methodology. The implementer is responsible for technical correctness and test evidence. No strategy result is treated as a trading recommendation without explicit human review.

## 4. Research findings and technology assessment

### 4.1 Exchange and data-source findings

**Kraken.** Kraken publishes Spot REST, WebSocket and FIX documentation. Its public market-data capability includes trade data and WebSocket OHLC updates. Kraken’s API-key documentation supports fine-grained permissions, including separate query and trade permissions, which supports a least-privilege design. The MVP should use public endpoints only and create no private API key until a later, separately approved paper-trading phase.

**Coinbase Advanced Trade.** Coinbase documents REST and WebSocket access for market data and provides an official Python SDK. Its public API includes product, candle, book and trade access. It is a credible alternative, particularly if the operator prefers Coinbase’s product model or existing account and regional support, but availability, product coverage, authentication and current terms must be revalidated before selection.

**CoinGecko.** CoinGecko provides broad market and historical data across assets. Its documentation states that historical availability and granularity vary by plan, with daily and hourly data broadly available and higher-resolution data subject to plan restrictions. It is useful for asset discovery, market-wide screening and a cross-source comparison. It should not be the sole execution-venue proxy for a backtest, because aggregated prices, liquidity and fees may differ from the venue where a future trade would be placed.

**CCXT.** CCXT provides a unified interface across many cryptocurrency exchanges, including Python and Rust support, market metadata, OHLCV access and rate-limit handling. It improves portability and allows an exchange adapter to be changed later. The project must still preserve the native venue identifier, raw response and request metadata because a unified API cannot remove venue-specific semantics or data-quality differences.

### 4.2 Library and storage findings

**`uv`.** Astral’s `uv` manages project environments, dependencies and a cross-platform `uv.lock` file. `uv run` verifies that the project and environment match the lockfile, supporting reproducible manual runs and later deployment.

**VectorBT.** VectorBT operates on pandas and NumPy objects and uses Numba, with optional Rust acceleration, for fast parameter sweeps and portfolio simulation. It is a strong fit for an MVP that needs to compare many strategy configurations quickly. Its speed does not validate a strategy: the project must control leakage, costs, multiple testing and out-of-sample evaluation.

**Pandas/NumPy versus Polars.** VectorBT’s core interface makes pandas/NumPy the lowest-friction strategy boundary. Polars is attractive for larger ingestion and transformation workloads because its lazy API can apply predicate and projection pushdown and process Parquet efficiently. It should remain optional in the MVP until a measured data-volume bottleneck exists. Moving to Polars everywhere too early would add conversion and ecosystem complexity.

**Parquet and DuckDB.** Parquet is suitable for immutable, columnar data snapshots. DuckDB provides a lightweight local analytical layer over Parquet without requiring a server database. This combination keeps the MVP portable and makes later migration to object storage or a larger analytical engine possible.

**Testing and configuration.** Use typed configuration, schema validation, deterministic random seeds where relevant, pytest tests, and a structured result schema. Secrets must be supplied through environment variables or a secrets manager in later phases, never committed to source control or placed in notebooks.

### 4.3 n8n assessment and orchestration boundary

n8n is suitable for coordinating the workflow, but it is not a substitute for the Python research engine. The recommended boundary is:

- **n8n may:** provide a manual or scheduled trigger; pass a versioned run configuration; invoke the Python CLI or a narrowly scoped container; capture the run ID and exit status; send a success, failure or data-quality notification; link to the report and result bundle; and apply bounded orchestration-level retries.
- **Python shall:** own market-data retrieval, provenance, validation, feature construction, strategy execution, cost modelling, backtesting, risk metrics, rejection gates and report generation.
- **n8n shall not:** contain the canonical strategy logic, perform numerical backtests in workflow nodes, hold the source of truth for configuration, or become a prerequisite for a manual run.

The user’s familiarity with n8n is a valid usability advantage. However, the technically simpler first implementation is a Python CLI plus cron or systemd timer: it has a smaller attack surface, fewer moving parts and no workflow-service dependency. The recommendation is therefore **n8n as an optional orchestration layer after the manual CLI is proven**, rather than n8n as the foundation of the MVP.

For a later VPS deployment, use n8n’s Docker Compose route rather than npm installation. The official n8n guidance identifies Docker Compose as the production-oriented option for persistent data and additional services, and warns that self-hosting requires server, container, security, configuration and operational knowledge. The n8n instance should use a pinned stable image, persistent storage for its `.n8n` directory and database, HTTPS behind a reverse proxy, strong authentication, a protected encryption key, restricted ingress, backups, UTC timezone configuration, health checks and a documented upgrade/restore process. n8n’s availability must not prevent the operator from running the Python CLI manually.

**Preferred orchestration options:**

1. **CLI plus cron/systemd:** simplest and preferred for the first dry runs.
2. **Self-hosted n8n plus Python container:** preferred once the morning process is stable and visual orchestration, notifications and run history justify the additional operational overhead.
3. **n8n Cloud plus Python execution service:** lower infrastructure burden, but introduces subscription, external data-flow and execution-environment dependencies; assess separately before selecting it.

## 5. Options appraisal

| Option | Description | Strengths | Weaknesses / risks | Assessment |
|---|---|---|---|---|
| A. Kraken-first, exchange-native research | Kraken Spot public data; CCXT adapter; direct Kraken calls where needed; Parquet/DuckDB; VectorBT | Closest match between research data and a potential future execution venue; low MVP complexity; public-data start; portable adapter | One venue’s market and asset coverage; must validate historical depth, pair naming and UK account availability | **Recommended** |
| B. Coinbase-first, official SDK | Coinbase Advanced Trade public data and official Python SDK; Parquet/DuckDB; VectorBT | Official Python SDK; REST and WebSocket documentation; credible alternative venue | Product, authentication, regional support and API-policy details must be revalidated; less exchange-neutral | Strong alternative |
| C. Aggregated market-data first | CoinGecko for universe discovery and history, then add exchange adapters later | Broad asset coverage; useful for screening and cross-market research; historical API options | Aggregated prices may not represent executable venue prices; plan limits and granularity; provenance and survivorship risks | Good discovery layer, weak sole backtest source |
| D. Paid specialist data vendor | Contract a professional market-data provider and connect the chosen venue later | Potentially broader history, quality controls and support | Cost, contract dependence, implementation time and still requires execution-venue modelling | Defer until data requirements justify it |

### Recommendation and conditions

Back **Option A** for the MVP, subject to a timeboxed technical spike whose duration is agreed at mobilisation and which confirms:

- the required symbols are available on Kraken Spot;
- the required bar frequencies and historical lookback can be retrieved reliably;
- the data can be stored and reloaded without timestamp or duplication defects;
- the operator can lawfully and practically access the venue from the intended jurisdiction; and
- fees, spread and slippage can be represented conservatively.

Change to Option B if Kraken’s coverage, reliability or account access is inadequate. Add CoinGecko as a discovery and cross-check source, not as an unqualified replacement for venue data. Adopt Option D only if the MVP demonstrates that exchange history and data quality are the binding constraints.

## 6. Target operating model

### Manual morning workflow

1. **Select asset or universe.** Read a versioned configuration containing symbol, quote currency, timeframe, lookback and screening rules.
2. **Fetch.** Retrieve market metadata and the required OHLCV range. Record provider, venue, symbol, timeframe, request time and raw response checksum.
3. **Validate.** Check timezone, monotonic timestamps, duplicates, missing bars, impossible prices, zero or negative values, stale latest bars and unexpected schema changes.
4. **Curate.** Convert to a canonical schema and write an immutable raw snapshot plus a curated Parquet dataset.
5. **Run baselines.** At minimum, compare buy-and-hold and a no-trade baseline against candidate strategies.
6. **Run strategies.** Execute a controlled strategy registry with fixed configuration and an explicit cost model.
7. **Evaluate.** Split data chronologically. Do not use future data in feature construction, parameter selection or asset screening.
8. **Stress-test.** Vary fees, slippage, execution timing, lookback and key parameters. Run multiple periods and, where possible, multiple assets.
9. **Gate.** Reject results that fail data, risk, robustness or out-of-sample criteria. Do not force a trade signal.
10. **Report.** Write a dated report and machine-readable result bundle, including a clear status: pass, fail, inconclusive or data-quality blocked.

### Future automated workflow

Automation is a later phase. It may run the same commands on a VPS using Docker or a locked `uv` environment, with either cron/systemd or self-hosted n8n as the scheduler/orchestrator, structured logs, health checks, alerting and object-storage backups. No automated order placement should be added until paper trading, operational controls, security review and separate approval are complete.

## 7. Functional requirements

Priority uses MoSCoW: Must, Should, Could and Won’t for the MVP.

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| FR-001 | The system shall accept an explicit asset symbol, venue, quote currency, timeframe and lookback configuration. | Must | A valid configuration produces a run manifest; invalid configuration fails with an actionable message. |
| FR-002 | The system shall retrieve public market data through an exchange adapter. | Must | A successful run stores raw data, provider, venue, symbol, timeframe and retrieval metadata. |
| FR-003 | The system shall support Kraken through CCXT for the initial adapter. | Must | A configured Kraken symbol can be fetched, normalised and persisted in a repeatable test. |
| FR-004 | The system shall preserve native venue identifiers and raw responses or checksums. | Must | Each curated dataset can be traced to a provider, endpoint, request time and raw artefact. |
| FR-005 | The system shall validate data quality before a backtest runs. | Must | Missing, duplicated, non-monotonic or invalid bars generate a blocking or warning status according to configuration. |
| FR-006 | The system shall run a buy-and-hold and no-trade baseline. | Must | Baselines appear in every report and use the same date range and cost assumptions where applicable. |
| FR-007 | The system shall support a registry of strategy implementations. | Must | A new strategy can be added without modifying ingestion or reporting code. |
| FR-008 | The initial strategy library shall include moving-average trend, breakout or momentum, mean reversion and a configurable volatility or position-sizing rule. | Should | Each strategy has tests, configuration metadata and a report entry. |
| FR-009 | The system shall model fees, spread, slippage, position sizing and execution timing. | Must | A report shows gross and net results and the active assumptions. |
| FR-010 | The system shall support chronological train, validation and out-of-sample evaluation. | Must | The report identifies each period and demonstrates that test-period values were not used for selection. |
| FR-011 | The system shall run parameter sensitivity and at least one robustness test. | Must | The result includes a parameter surface or neighbouring-parameter comparison and a robustness outcome. |
| FR-012 | The system shall rank strategies using net return, volatility, maximum drawdown, Sharpe-like risk-adjusted return, turnover, win rate and trade count. | Must | Metrics are calculated consistently and displayed with definitions. |
| FR-013 | The system shall apply configurable rejection gates. | Must | Strategies can be rejected for insufficient data, negative net return, excessive drawdown, inadequate trade count or failed out-of-sample performance. |
| FR-014 | The system shall produce a human-readable report and machine-readable results. | Must | A run creates a Markdown or HTML report plus JSON or Parquet results. |
| FR-015 | The system shall support a dry-run mode that never places orders. | Must | No private API endpoint or order method is reachable from the MVP execution path. |
| FR-016 | The system should support a Coinbase adapter without changing the strategy interface. | Should | The adapter contract is documented and a later implementation can satisfy it. |
| FR-017 | The system could use CoinGecko for asset discovery and cross-source checks. | Could | Discovery data is clearly labelled and never silently substitutes for execution-venue prices. |
| FR-018 | The system shall support a repeatable CLI command for the morning workflow. | Must | A clean environment can run the command using the checked-in lockfile and configuration example. |
| FR-019 | The core workflow shall run successfully without n8n. | Must | The documented CLI completes a dry run when the n8n service is unavailable. |
| FR-020 | The solution should support an n8n manual or scheduled trigger for the Python workflow. | Should | A workflow can pass a validated run configuration and invoke the documented CLI or container. |
| FR-021 | The n8n workflow shall record the run ID, status, timestamps and report location. | Should | A completed or failed run produces an operator-visible status record. |
| FR-022 | The n8n workflow shall send bounded success, failure and data-quality notifications. | Should | Notifications contain the run ID, status, concise cause and report link where available. |
| FR-023 | Orchestration retries shall be bounded and idempotent. | Must for automation | A retry cannot silently create duplicate snapshots or duplicate result bundles. |
| FR-024 | No exchange credentials shall be required by n8n for the research-only MVP. | Must | The n8n workflow invokes public-data paths only and contains no private exchange secret. |
| FR-025 | n8n workflows and configuration shall be exportable and version-controlled. | Should | A workflow export and its non-secret configuration are stored with the project release artefacts. |

## 8. Non-functional requirements

### Reproducibility and auditability

- Every run has a unique run ID, UTC timestamps, Git commit or source version, dependency lock hash, configuration hash and data snapshot identifier.
- Raw data is immutable; corrections create a new version rather than silently overwriting history.
- Reports distinguish observed data, calculated metrics, assumptions and analyst conclusions.
- Results can be reproduced from a stored snapshot and configuration.

### Data integrity

- Use UTC internally and record exchange timestamps without converting away the original value.
- Define candle boundary, inclusion and incomplete-candle rules.
- Use decimal-safe handling for prices and quantities where needed.
- Detect gaps and document whether they block a strategy.
- Record symbol changes, delistings and asset-universe rules to reduce survivorship bias.

### Performance

- A normal single-asset daily or hourly run should be practical on a developer laptop; an exact time target is to be established during the technical spike.
- Do not optimise for scale before measuring the manual workload.
- Use VectorBT’s vectorised and compiled paths for parameter sweeps where compatible; use profiling before introducing Polars, Rust or distributed execution.

### Security

- No private keys or exchange secrets in Git, notebooks, logs, reports or shell history.
- Public-data mode must not require exchange credentials.
- Any future credentials must be read-only and IP-restricted where supported; withdrawal permissions must remain disabled.
- VPS deployment must use least privilege, patched images, firewall rules, secret injection and backups.
- If n8n is self-hosted, use Docker Compose with a pinned image, persistent `.n8n` storage, protected encryption key, HTTPS, strong authentication, restricted ingress, backups, health checks and an upgrade/restore runbook.
- n8n must not be the only scheduler or execution path until operational resilience is demonstrated; the Python CLI remains the recovery path.

### Usability

- CLI errors must identify the cause and corrective action.
- Reports must be understandable to a non-specialist operator and include a plain-English conclusion.
- A “no strategy passed” outcome is a successful run, not an error.

## 9. Backtesting methodology and controls

The backtest engine must include the following controls:

1. **Look-ahead control:** signals at time *t* can only use information available before the simulated fill.
2. **Chronological splitting:** never randomly shuffle time-series observations.
3. **Walk-forward evaluation:** periodically fit or select on past data and evaluate on the next unseen segment.
4. **Transaction costs:** include venue fees, spread and conservative slippage; document whether fees vary by tier.
5. **Execution convention:** define whether signals execute at next open, next available price, close or a simulated limit fill.
6. **Liquidity controls:** cap position size relative to volume or estimated market depth; reject assets with insufficient data or volume.
7. **Corporate and token events:** document treatment of splits, redenominations, migrations, delistings and symbol changes where relevant.
8. **Multiple testing control:** report the number of strategies and parameter combinations tested; avoid selecting solely on the best historical result.
9. **Benchmarking:** compare against buy-and-hold, cash or stable-value proxy where appropriate, and a no-trade baseline.
10. **Failure handling:** a missing or suspect data period must produce a warning or blocked result, never silent interpolation.

### Suggested initial gates

These are provisional requirements, not evidence-based profit thresholds. Confirm them during the technical spike and calibration phase:

- minimum data completeness and minimum number of observations;
- non-negative net out-of-sample performance after conservative costs;
- maximum acceptable drawdown set by the product owner;
- minimum trade count sufficient for interpretation but not artificial over-trading;
- performance that remains acceptable under adverse cost and parameter scenarios; and
- no unresolved data-quality or leakage warning.

## 10. Conceptual architecture

**Manual CLI or n8n trigger** → **Configuration validation** → **Asset and venue discovery** → **Market-data adapter** → **Raw snapshot store** → **Validation and normalisation** → **Curated Parquet/DuckDB layer** → **Feature and signal layer** → **Backtest engine** → **Risk and robustness gates** → **Report and result bundle** → **Optional n8n notification/run-status update**

n8n is an outer control-plane component, not part of the quantitative data path. The run manifest and Python-generated result bundle remain authoritative.

Cross-cutting controls are provenance, logging, UTC time, configuration hashing, error handling, tests and secrets isolation.

### Recommended project structure

```text
crypto-trading-mvp/
├── pyproject.toml
├── uv.lock
├── README.md
├── src/crypto_trading/
│   ├── cli.py
│   ├── config.py
│   ├── venues/
│   │   ├── protocol.py
│   │   └── kraken.py
│   ├── data/
│   │   ├── fetch.py
│   │   ├── validate.py
│   │   └── store.py
│   ├── strategies/
│   │   ├── protocol.py
│   │   ├── baselines.py
│   │   └── library.py
│   ├── backtest/
│   │   ├── costs.py
│   │   ├── runner.py
│   │   └── metrics.py
│   └── reporting/
│       └── report.py
├── configs/
│   └── example.toml
├── data/                 # ignored locally or mounted storage
├── reports/
├── tests/
└── docs/
```

The strategy protocol should accept canonical market data and return signals or orders in a venue-neutral format. The backtest runner, cost model and reporting layer should not import exchange-specific code.

## 11. Delivery plan

### Increment 0: technical spike

Validate venue access, symbol mapping, historical depth, timestamp semantics, rate limits, data shape, `uv` dependency compatibility and VectorBT integration. Produce a short evidence note and revise this BRD if a gating assumption fails.

### Increment 1: data foundation

Implement configuration, Kraken adapter, raw snapshot storage, canonical schema, validation and a reproducible fetch command.

### Increment 2: research engine

Implement baselines, strategy registry, cost model, chronological splits, metrics and first report.

### Increment 3: robustness and operator workflow

Add sensitivity analysis, rejection gates, run manifest, result bundle, error messages and tests for the full morning workflow.

### Increment 3.5: optional n8n orchestration

After the CLI workflow is stable, add an n8n workflow for manual triggering, optional scheduling, bounded retries, run-status capture and notifications. Validate that the Python CLI still works independently, that workflow exports are version-controlled, and that failed n8n runs do not create duplicate data or reports.

### Increment 4: review and automation decision

Run a controlled research review. Decide whether results justify a paper-trading phase. Do not move directly from backtest to live execution.

## 12. Risks, mitigations and evidence gaps

| Risk | Impact | Mitigation | Evidence gap / trigger |
|---|---|---|---|
| Data looks profitable because of look-ahead or leakage | False confidence and financial loss | Chronological design, leakage tests, walk-forward validation | Confirm with deliberately adversarial tests |
| Aggregated data differs from executable venue data | Unrealistic fills | Backtest on primary venue data and retain provenance | Validate against sampled venue trades |
| Fees and slippage are understated | Net returns overstated | Conservative scenarios and sensitivity tests | Confirm current venue fee schedule and account tier |
| Exchange/API changes or outages | Missing or corrupted runs | Adapter contract, retries, caching, raw snapshots and alerts | Test failure and schema-change paths |
| Survivorship bias or delisted assets | Inflated historical results | Versioned universe and delisting treatment | Determine asset-history data requirements |
| Strategy overfitting | Poor live performance | Holdout data, walk-forward, parameter stability and multiple-testing reporting | Define minimum evidence standard |
| Crypto market and counterparty risk | Loss of funds or access | No live trading in MVP; later read-only keys and separate approvals | Legal and venue due diligence before trading |
| UK regulatory perimeter changes | Compliance or operational risk | Keep the MVP research-only; obtain specialist advice before promotion or managed trading | Recheck FCA rules at each phase gate |
| VPS compromise or key leakage | Account or data compromise | No secrets in MVP; later least privilege, IP restrictions and secret management | Security review before automation |
| n8n self-hosting adds an avoidable operational dependency | Availability, security or maintenance burden | Keep CLI independent; use Docker Compose, pinned images, protected encryption key, HTTPS, backups and an upgrade runbook | Confirm operator capacity to maintain a self-hosted service |
| n8n retries duplicate a run or report | Conflicting results or corrupted audit trail | Use run IDs, idempotency keys, bounded retries and atomic result publication | Test interruption and retry scenarios |
| Workflow logic drifts from Python logic | Inconsistent research outcomes | Keep quantitative logic in Python; version-control n8n exports and invoke a stable CLI contract | Review every workflow change with the project release |
| “Maximise return” drives unsafe selection | Excessive drawdown or turnover | Optimise risk-adjusted net outcomes with explicit gates | Product owner to approve risk limits |

## 13. Benefits and measures

| Benefit | Measure | Baseline / target to confirm |
|---|---|---|
| Repeatable morning research | Time and manual steps per run | Baseline during Increment 0; target agreed after first dry runs |
| Higher research integrity | Percentage of runs with complete provenance and no unresolved data warnings | Baseline from pilot; target should approach 100% for publishable reports |
| Faster strategy comparison | Time to evaluate configured strategy set | Measure on representative laptop and dataset |
| Reduced false positives | Percentage of candidate strategies rejected by out-of-sample or robustness gates | Track by run; no fixed “good” percentage assumed |
| Portability | Ability to swap venue adapter without changing strategies | Demonstrate with a test double, then Coinbase or another adapter only if justified |

## 14. Critical review and appraisal

### Findings

- The original request combines data engineering, quantitative research, exchange integration and eventual operations. Treating it as one automated trading build would create avoidable technical and financial risk.
- “Scrape prices” is an imprecise solution. Official APIs are more reliable, auditable and respectful of provider terms than scraping exchange webpages.
- The best MVP data source is the venue whose prices would eventually be used for execution. Aggregators are useful for discovery and cross-checking but should not silently define execution assumptions.
- VectorBT offers the right research speed for parameter sweeps, but speed can increase overfitting if the evaluation discipline is weak.
- Moving to Rust is not currently justified by the stated manual workflow. The architecture should preserve a later migration path while keeping the first build Python-native.
- n8n is useful for the user-facing workflow and notifications, but a pure CLI plus cron/systemd remains the lower-risk technical baseline. n8n should be an optional control-plane addition, not the quantitative engine or a single point of failure.

### Assumptions to validate

- The intended assets are spot instruments and the desired base or quote currency is available on the selected venue.
- Daily or hourly bars are sufficient for the first strategy questions.
- The operator will not place real orders from the MVP.
- The operator can access the selected exchange and data sources from the intended jurisdiction.
- The expected dataset size fits local Parquet/DuckDB and VectorBT workflows.

### Corrections made during review

- Reframed “maximise returns” as risk-adjusted net performance with drawdown and robustness controls.
- Separated research data from execution-venue data and made provenance a requirement.
- Added baselines, walk-forward evaluation, leakage controls, cost modelling and multiple-testing safeguards.
- Removed live trading and credentials from MVP scope.
- Added UK regulatory and exchange-access validation as a phase gate rather than asserting that any venue is suitable by default.
- Made Rust a later performance option, not an upfront dependency.
- Added n8n as an optional orchestration layer, with an explicit Python ownership boundary, self-hosting controls, fallback execution path and retry/idempotency requirements.
- Corrected the functional-requirements catalogue so requirement identifiers remain unique.

### Final recommendation

Approve a Kraken-first, spot-only, public-data research MVP with a narrow strategy library and strict rejection gates. Build the venue adapter and data-quality tests before adding strategy complexity. Start with the Python CLI as the independent execution path. Once that workflow is stable, add n8n as an optional orchestration and notification layer because it matches the operator’s familiarity, while retaining cron/systemd as the simpler baseline and recovery path. Only proceed to paper trading if the system can reproduce its own results and the selected strategies remain credible after costs, out-of-sample testing and sensitivity analysis. Live automation should be a separate decision supported by new operational, security, legal and financial evidence.

## 15. Source register

- [CCXT documentation](https://docs.ccxt.com/docs/index) and [CCXT manual](https://github.com/ccxt/ccxt/wiki/manual): unified exchange APIs, OHLCV and rate-limit controls.
- [Kraken API documentation](https://docs.kraken.com/api/docs/) and [Kraken OHLC/WebSocket documentation](https://docs-legacy.kraken.com/api/docs/websocket-v1/ohlc/): official venue data interfaces.
- [Coinbase Advanced Trade API overview](https://docs.cdp.coinbase.com/advanced-trade/docs/ws-overview/) and [official Python SDK documentation](https://coinbase.github.io/coinbase-advanced-py/): alternative venue and SDK evidence.
- [CoinGecko API](https://www.coingecko.com/en/api): aggregated market and historical-data capabilities and plan considerations.
- [VectorBT documentation](https://vectorbt.dev/) and [features](https://vectorbt.dev/getting-started/features/): vectorised backtesting, Numba and optional Rust acceleration.
- [Polars lazy API documentation](https://github.com/pola-rs/polars/blob/main/docs/source/user-guide/concepts/lazy-api.md): optional high-volume data-transformation approach.
- [uv project guide](https://docs.astral.sh/uv/guides/projects/) and [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/): reproducible Python environments and lockfiles.
- [FCA cryptoassets work](https://www.fca.org.uk/firms/cryptoassets) and [cryptoasset financial-promotion guidance](https://www.fca.org.uk/publication/finalised-guidance/fg23-3.pdf): UK regulatory context. This BRD is not legal advice.
- [n8n hosting guidance](https://docs.n8n.io/deploy/host-n8n), [Docker Compose installation](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose.md) and [Docker/self-hosting guidance](https://docs.n8n.io/hosting/installation/docker/): deployment options, persistence, security and self-hosting considerations.

**Document status:** Final reviewed BRD with n8n orchestration update. Technical, regulatory, data-access, fee and n8n deployment assumptions must be revalidated at implementation and before any paper-trading or live-trading phase.
