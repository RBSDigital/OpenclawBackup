# Wolfram Mathematica Trading Strategy Research Brief

This is implementation research only, not trading advice.

## Strategy Implementation Patterns

Use `TimeSeries` as the main data contract. Normalize all market data into timestamped series, then keep strategy functions pure:

```text
prices -> signals -> positions -> trades -> equity
```

Practical Wolfram pattern:

```wolfram
prices = TimeSeries[data];

indicator[ts_, n_] := MovingAverage[ts["Values"], n];

signal[fast_, slow_] := UnitStep[fast - slow] - UnitStep[slow - fast];

positions[signals_] := Lag[signals, 1];

returns[prices_] := Differences[Log[prices["Values"]]];

equity[pos_, rets_, costs_] := Accumulate[pos*rets - costs];
```

Keep each stage separately testable. Avoid burying signal logic, execution assumptions, and portfolio accounting in one notebook cell.

## Indicators, Signals, Sweeps, and Optimization

For indicators, Wolfram has built-ins such as `MovingAverage` and `ExponentialMovingAverage`, useful for moving-average crossover, momentum, mean reversion, volatility filters, and smoothed trend signals.

For visualization and inspection, `TradingChart` supports OHLC-style financial charts and indicators, while `DateListPlot` works well for equity curves, drawdowns, rolling metrics, and diagnostics.

For parameter sweeps, use `Table`, `ParallelTable`, `Association`, and `Dataset` to preserve inputs and results:

```wolfram
results =
  Dataset @ Flatten[
    Table[
      <|
        "Fast" -> f,
        "Slow" -> s,
        "Sharpe" -> backtestSharpe[f, s],
        "MaxDrawdown" -> backtestDrawdown[f, s]
      |>,
      {f, {5, 10, 20}},
      {s, {50, 100, 200}}
    ],
    1
  ];
```

For optimization, use `NMaximize` for global numerical search with constraints, and `FindArgMax` when local optimization is appropriate. Penalize turnover, drawdown, parameter instability, and constraint violations instead of maximizing raw return alone.

## Monte Carlo and Random Processes

Use Wolfram stochastic-process tools for synthetic paths, stress tests, and scenario analysis. `RandomFunction` generates sample paths from stochastic processes; `GeometricBrownianMotionProcess` can model stylized price paths, though it is too simple for realistic market microstructure.

Use Monte Carlo to test sensitivity to:

- execution cost assumptions
- volatility regimes
- gap risk
- signal delay
- missing bars
- spread widening
- parameter perturbation
- correlated assets

Use `BlockRandom` and `SeedRandom` to make simulations reproducible without contaminating global randomness.

## Realistic Backtesting Concerns

Backtests should model executable prices, not just close-to-close returns.

Include:

- Bid/ask: long entries usually pay ask and exits receive bid; shorts invert that logic.
- Spread: model dynamic spread, not a fixed optimistic constant.
- Slippage: add market-impact or volatility-based slippage, especially around opens, closes, news, and low-liquidity periods.
- Fees and financing: include commissions, exchange fees, broker financing, and rollover/swap.
- Margin and leverage: track initial margin, maintenance margin, liquidation rules, and leverage caps.
- Partial fills: relevant for limit orders and thin markets.
- Latency: shift signals forward so execution occurs after the information would have been available.
- Walk-forward validation: fit parameters on an in-sample window, trade only the next out-of-sample segment, then roll forward.

## Package and Notebook Architecture

```text
StrategyProject/
  PacletInfo.wl
  Kernel/
    StrategyProject.wl
  Strategies/
    MovingAverageCross.wl
    MeanReversion.wl
  Backtest/
    Engine.wl
    Costs.wl
    Metrics.wl
  Data/
    raw/
    processed/
  Tests/
    BacktestTests.wlt
  Notebooks/
    Research.nb
    WalkForwardReport.nb
```

Use notebooks for exploration and reporting, but move reusable logic into `.wl` package files. Package strategy code as a paclet when it becomes shared infrastructure.

For reproducibility:

- pin raw data snapshots
- store data vendor, timestamp, timezone, corporate-action policy, and instrument identifiers
- version parameter sets
- save random seeds
- keep walk-forward splits explicit
- run `VerificationTest` for accounting, cost models, and signal edge cases

## Sources

1. Wolfram `TimeSeries`: <https://reference.wolfram.com/language/ref/TimeSeries.html>
2. Wolfram Time Series Processes guide: <https://reference.wolfram.com/language/guide/TimeSeriesProcesses.html>
3. Wolfram `MovingAverage`: <https://reference.wolfram.com/language/ref/MovingAverage.html>
4. Wolfram `ExponentialMovingAverage`: <https://reference.wolfram.com/language/ref/ExponentialMovingAverage.html>
5. Wolfram `TradingChart`: <https://reference.wolfram.com/language/ref/TradingChart.html>
6. Wolfram `DateListPlot`: <https://reference.wolfram.com/language/ref/DateListPlot.html>
7. Wolfram `NMaximize`: <https://reference.wolfram.com/language/ref/NMaximize.html>
8. Wolfram `RandomFunction`: <https://reference.wolfram.com/language/ref/RandomFunction.html>
9. Wolfram `GeometricBrownianMotionProcess`: <https://reference.wolfram.com/language/ref/GeometricBrownianMotionProcess.html>
10. Wolfram `VerificationTest`: <https://reference.wolfram.com/language/ref/VerificationTest.html>
11. Interactive Brokers margin overview: <https://www.interactivebrokers.com/en/trading/margin.php>
12. CME futures expiration and contract roll: <https://www.cmegroup.com/education/courses/introduction-to-futures/understanding-futures-expiration-contract-roll.html>

