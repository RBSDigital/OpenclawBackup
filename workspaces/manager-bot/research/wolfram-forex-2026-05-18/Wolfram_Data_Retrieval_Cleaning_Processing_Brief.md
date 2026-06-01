# Forex Data In Wolfram Language

This is engineering and research context only, not trading advice.

## Built-In Capabilities

Wolfram Language can handle the analytical side of a forex workflow: importing vendor files/API responses, converting them into temporal objects, cleaning/resampling, and running descriptive financial analytics.

Key tools:

- `FinancialData` can retrieve financial series by symbol/name and date range. It is useful for quick historical checks where Wolfram has coverage, but it is not a substitute for institutional FX feeds.
- `EntityValue` can query Wolfram-curated entities/properties where financial or currency entities are available. Treat this as structured reference data, not guaranteed market-feed coverage.
- `Import` is the main ingestion layer for CSV, JSON, XML, XLSX, HDF5, URLs, and other vendor/export formats.
- `URLRead` and `HTTPRequest` are useful for REST APIs.
- `TimeSeries` represents dated observations and supports interpolation, arithmetic, resampling, windowing, and plotting.
- `TemporalData` generalizes `TimeSeries` to multiple paths, useful for multi-pair panels like EUR/USD, GBP/USD, and USD/JPY.
- `Dataset` is useful for normalized tabular records before converting to time series.
- Financial plotting is supported through Wolfram financial visualization functions such as `TradingChart`.

## Cleaning, Resampling, and Time Zones

Recommended patterns:

- Normalize timestamps immediately using `DateObject` with explicit time-zone metadata.
- Convert all raw vendor timestamps to one canonical zone, usually UTC, with `TimeZoneConvert`.
- Preserve vendor timestamp, normalized timestamp, pair, bid, ask, spread, mid, source, and pull time.
- Convert imported rows into a clean `Dataset`, validate schema, remove malformed rows, coerce numeric fields, then build `TimeSeries` or `TemporalData`.
- Use `Missing` explicitly, then choose `DeleteMissing`, interpolation, previous-tick carry-forward, or gap-aware filtering depending on the analysis.
- Use `TimeSeriesResample` for regular bars, and distinguish calendar days from trading sessions and vendor cutoffs.
- Use `MovingMap`, `MovingAverage`, or `TimeSeriesAggregate` for rolling and aggregate calculations after cleaning/resampling.

Example pattern:

```wolfram
raw = Import["eurusd.csv", "Dataset"];

clean =
  raw[
    All,
    <|
      "Pair" -> #Pair,
      "Time" -> TimeZoneConvert[
        DateObject[#Timestamp, TimeZone -> "UTC"],
        "UTC"
      ],
      "Bid" -> ToExpression[#Bid],
      "Ask" -> ToExpression[#Ask],
      "Mid" -> Mean[{ToExpression[#Bid], ToExpression[#Ask]}]
    |>&
  ];

ts = TimeSeries[Normal[clean[All, {"Time", "Mid"}]]];
bars = TimeSeriesResample[ts, Quantity[1, "Minutes"]];
```

## Pipeline Structure

Keep notebooks for exploration and reports; keep reusable logic in `.wl` package files.

```text
ForexResearch/
  notebooks/
    01-ingest-check.nb
    02-cleaning-qc.nb
    03-analytics.nb
  Kernel/
    init.wl
  ForexPipeline.wl
  data/
    raw/
    staged/
    curated/
  tests/
```

Suggested package functions:

```wolfram
FetchFX[pair_, range_, source_: "FinancialData"]
ImportVendorFX[file_, schema_]
NormalizeFXRows[data_, opts___]
BuildFXTimeSeries[data_, field_: "Mid"]
ResampleFX[ts_, interval_, method_: Last]
QualityReportFX[data_]
```

Keep raw data immutable. Store transformation metadata: source, pull time, symbol mapping, time-zone assumption, sampling interval, and vendor license.

## Limitations

Wolfram built-in financial data is useful for convenience, teaching, prototyping, and broad historical analysis, but forex production workflows often need external vendors.

Use external APIs/data vendors when you need:

- tick data or true bid/ask history
- intraday bars with guaranteed provenance
- broker-specific spreads or executable prices
- low-latency streaming
- complete historical depth across many pairs
- institutional-quality calendar/reference metadata
- reproducible licensed datasets for audit/compliance

Common vendor/API routes include OANDA, Interactive Brokers, Refinitiv/LSEG, Bloomberg, Polygon.io, Twelve Data, Alpha Vantage, and broker-specific exports. Wolfram can still be the analytics layer by ingesting CSV/JSON/WebSocket-derived files through `Import` and converting them into `Dataset`, `TimeSeries`, and `TemporalData`.

## Sources

1. Wolfram `FinancialData`: <https://reference.wolfram.com/language/ref/FinancialData.html>
2. Wolfram `Import`: <https://reference.wolfram.com/language/ref/Import.html>
3. Wolfram `URLRead`: <https://reference.wolfram.com/language/ref/URLRead.html>
4. Wolfram `HTTPRequest`: <https://reference.wolfram.com/language/ref/HTTPRequest.html>
5. Wolfram `EntityValue`: <https://reference.wolfram.com/language/ref/EntityValue.html>
6. Wolfram `Dataset`: <https://reference.wolfram.com/language/ref/Dataset.html>
7. Wolfram `TimeSeries`: <https://reference.wolfram.com/language/ref/TimeSeries.html>
8. Wolfram `TemporalData`: <https://reference.wolfram.com/language/ref/TemporalData.html>
9. Wolfram `TimeSeriesResample`: <https://reference.wolfram.com/language/ref/TimeSeriesResample.html>
10. Wolfram `TimeZoneConvert`: <https://reference.wolfram.com/language/ref/TimeZoneConvert.html>
11. Alpha Vantage FX documentation: <https://www.alphavantage.co/documentation/>
12. OANDA pricing API: <https://developer.oanda.com/rest-live-v20/pricing-ep/>

