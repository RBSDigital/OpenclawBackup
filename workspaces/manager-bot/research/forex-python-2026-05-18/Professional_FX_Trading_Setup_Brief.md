# Professional FX Trading Setup Brief

This is systems research only, not trading advice.

## Broker/API Connection Patterns

Retail FX setups usually expose HTTPS REST APIs for account state and order entry, plus streaming price feeds over websocket or long-lived HTTP connections. OANDA's v20 API is a typical pattern: REST resources for accounts, instruments, pricing, trades, positions, and orders, with separate streaming endpoints for live prices and transactions. Order models include market, limit, stop, market-if-touched, take-profit, stop-loss, and trailing-stop definitions.

Retail/pro-am brokerage setups may also use a local gateway model. Interactive Brokers' TWS API connects client software to Trader Workstation or IB Gateway, which then handles order routing, market data, and account operations. This adds a broker-managed desktop/server process between the algorithm and venue connectivity.

Professional FX connectivity is commonly built around FIX sessions, broker-specific binary/streaming APIs, hosted gateways, VPNs, cross-connects, or colocated infrastructure. LMAX, for example, documents API connectivity for trading and market data through its exchange-style infrastructure.

Common architecture:
- Strategy engine: signal generation, portfolio logic, order intent.
- Risk gateway: validates all orders before release.
- Execution adapter: broker/FIX/REST-specific translation.
- Market-data handler: normalizes quotes, depth, timestamps, and venue status.
- Reconciliation service: compares internal state to broker execution reports, positions, balances, and fills.

## FIX Protocol Basics

FIX is the dominant professional messaging protocol for electronic order routing and market data. FIX defines session behavior, message types, tags, sequencing, heartbeats, resend logic, and application-level messages.

Relevant order-routing messages:
- `NewOrderSingle (D)`: submit a new order.
- `ExecutionReport (8)`: broker response for acknowledgements, partial fills, fills, cancels, rejects, and order-status changes.
- `OrderCancelRequest (F)`: request cancellation.
- `OrderCancelReplaceRequest (G)`: amend an existing order.
- `OrderStatusRequest (H)`: query order state.

Key fields:
- `ClOrdID (11)`: client order ID; critical for idempotency and reconciliation.
- `Symbol (55)`: instrument, often broker-specific for FX pairs.
- `Side (54)`: buy/sell.
- `OrderQty (38)`: quantity.
- `OrdType (40)`: market, limit, stop, etc.
- `Price (44)`: limit/stop price where applicable.
- `TimeInForce (59)`: day, IOC, FOK, GTC, etc.
- `TransactTime (60)`: event timestamp.

FIX market-data messages include `MarketDataRequest (V)` and `MarketDataSnapshotFullRefresh (W)`, with entries such as bid, offer, trade, size, and depth levels.

Session controls matter operationally:
- Maintain sequence numbers.
- Respond to heartbeats/test requests.
- Detect stale sessions quickly.
- Handle resend requests without duplicating orders.
- Reconcile after disconnects before resuming trading.

## Execution Concerns

Order types:
- Market orders prioritize immediacy but expose the system to slippage.
- Limit orders control price but may not fill.
- Stop orders convert conditionally and can slip during fast markets.
- IOC/FOK orders are useful when partial fills or resting exposure must be controlled.
- Broker-attached take-profit, stop-loss, and trailing-stop orders can reduce dependency on local system uptime, but implementation details vary by broker.

Latency:
- REST APIs are simpler but often unsuitable for very low-latency execution.
- FIX sessions reduce per-order overhead and provide deterministic sequencing.
- Physical distance, broker gateway load, TLS/VPN overhead, market-data latency, and internal risk checks all contribute to round-trip time.

Liquidity and spreads:
- FX liquidity is fragmented across banks, ECNs, internalizers, and broker pools.
- Top-of-book spread may not represent executable size.
- Depth, last-look practices, reject rates, and fill ratios matter as much as quoted spread.
- Wider spreads and thinner depth are common around rollovers, macro releases, holidays, and stressed conditions.

Slippage and transaction costs:
- Expected transaction cost should include spread, commissions, financing/rollover, market impact, reject/retry cost, and adverse selection.
- BIS research on FX execution algorithms notes that execution quality depends on market conditions, liquidity fragmentation, and how algorithms interact with market functioning.

## Risk Controls For Algorithmic FX Systems

Pre-trade controls:
- Max order quantity and notional by symbol, account, strategy, and venue.
- Max net and gross exposure by currency and currency pair.
- Price collars against reference mid, top-of-book, or recent volatility.
- Fat-finger checks for size, price, side, and duplicate orders.
- Margin and free-equity checks before order release.
- Kill switch by strategy, account, venue, and global system.
- Throttles for order rate, cancel/replace rate, and reject rate.
- Stale market-data guard: block trading when quotes are old or crossed beyond tolerance.

Runtime controls:
- Real-time PnL, drawdown, exposure, and margin monitoring.
- Circuit breakers for abnormal slippage, reject spikes, disconnects, or spread widening.
- Heartbeat monitoring for FIX sessions, broker APIs, pricing streams, and internal services.
- Idempotent order handling using stable client order IDs.
- State-machine enforcement so orders cannot move through impossible states.
- Graceful degrade modes: cancel open orders, stop new orders, or flatten only if explicitly approved by policy.

Post-trade controls:
- Broker reconciliation for orders, fills, positions, cash, financing, and commissions.
- Immutable audit logs for order intent, risk checks, outbound messages, broker responses, and operator actions.
- Replayable event logs for incident review.
- Independent limit configuration, change approval, and versioned deployment records.

Regulatory/supervisory guidance for automated order-routing systems emphasizes written procedures, supervisory controls, pre-trade limits, monitoring, and the ability to disable malfunctioning systems.

## Practical Design Pattern

1. Strategy emits order intent.
2. Risk gateway validates exposure, price, margin, rate limits, and venue status.
3. Execution adapter translates to FIX, REST, or broker-native API.
4. Broker/venue returns acknowledgements and execution reports.
5. Reconciliation service updates the source-of-truth order and position state.
6. Monitoring layer watches latency, rejects, slippage, spreads, PnL, and connectivity.

The key engineering principle is that the strategy should never be the only place where risk is enforced. Risk controls should sit on the path to the broker, operate independently, and fail closed when market data, session state, or account state is unreliable.

## Sources

1. OANDA v20 REST API: <https://developer.oanda.com/rest-live-v20/introduction/>
2. OANDA order definitions: <https://developer.oanda.com/rest-live-v20/order-df/>
3. Interactive Brokers TWS API: <https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/>
4. LMAX API documentation: <https://docs.lmax.com/>
5. FIX Trading Community standards: <https://www.fixtrading.org/standards/>
6. FIX online specification: <https://www.fixtrading.org/online-specification/>
7. OnixS FIX 4.4 NewOrderSingle: <https://www.onixs.biz/fix-dictionary/4.4/msgtype_d_68.html>
8. OnixS FIX 4.4 MarketDataSnapshotFullRefresh: <https://www.onixs.biz/fix-dictionary/4.4/msgtype_W_87.html>
9. BIS, FX execution algorithms and market functioning: <https://www.bis.org/publ/qtrpdf/r_qt1909f.htm>
10. NFA automated order-routing systems supervisory guidance: <https://www.nfa.futures.org/rulebooksql/rules.aspx?Section=4&RuleID=9068>

