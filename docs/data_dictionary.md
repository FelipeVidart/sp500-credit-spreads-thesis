
# Data Dictionary — Master Panel (firm–month)

This document describes the variables contained in the final firm–month panel used in the thesis:
**“Identificación estructural de shocks agregados de mercado y crédito en los credit spreads del S&P 500 (2015–2025)”**.

The master dataset is produced by `notebooks/02_construccion_panel.ipynb` and used by
`notebooks/03_runer_econometrico.ipynb` to estimate Models **M0–M6**.

---

## Unit of observation and frequency

- **Unit**: issuer \(i\) × month \(t\)
- **Frequency**: monthly (calendar month)
- **Sample period**: 2015–2025 (monthly)
- **Data sources**:
  - Refinitiv (Eikon / RDP) via Python for equity, indices, fundamentals
  - LSEG Workspace manual exports for bond yield histories (licensed; not redistributed)

> **Important**: Some bond-level time series (e.g., YTM histories by bond RIC) were exported manually from LSEG Workspace and are therefore not included in the repository. See `data/inputs/README_inputs.md`.

---

## Notes on naming conventions

- Variables with spaces (e.g., `total assets`) are raw Refinitiv fundamentals as downloaded.
- Variables in `snake_case` (e.g., `log_assets`, `cash_to_assets`) are constructed features used in the econometric models.
- The dependent variable used in regressions is typically `log_spread_mean_bps`, which may be **created in the econometric notebook** from `spread_mean_bps` after filtering/winsorization rules (depending on your implementation).

---

## Variable list (ordered as in the final panel)

### Identifiers and time

| Variable | Type | Description |
|---|---|---|
| `issuer` | string | Issuer identifier used internally in the project (firm-level entity). |
| `ticker` | string | Equity ticker used for equity returns and firm matching. |
| `date` | datetime | Month identifier (typically month-end). |
| `sector` | string | Sector label used in the project (may map to GICS/TRBC depending on construction). |
| `gics_sector` | string/int | GICS sector classification (as used for grouping/controls). |
| `ric` | string | Bond identifier RIC (bond-level; used for traceability/merges). |
| `ric_fund` | string | Refinitiv identifier used to retrieve fundamentals (firm-level). |
| `Ticker` | string | Alternative ticker field from fundamentals downloads (kept for merge traceability). |
| `issuer_fund` | string | Issuer name/id from fundamentals file (kept for merge traceability). |

---

### Dependent variable construction inputs (credit spreads)

| Variable | Unit | Description / construction |
|---|---:|---|
| `spread_mean_bps` | bps | Firm–month **average credit spread** (mean across active bonds). Constructed as YTM minus matched UST yield at comparable maturity, then aggregated to firm–month. In regressions, the dependent is typically `log(spread_mean_bps)` after restricting to positive spreads (per thesis). |
| `n_bonds` | count | Number of active bond issues used to compute the firm–month spread. |
| `ytm_mean` | % or decimal | Firm–month average yield-to-maturity across active bonds (as aggregated from bond-level series). |
| `residual_maturity_mean` | years | Firm–month average residual maturity across active bonds. |

---

### Equity systematic risk and volatility

| Variable | Unit | Description / construction |
|---|---:|---|
| `mkt_ret` | log return | Aggregate **market shock**: monthly log return of market proxy (SPY / S&P 500), built from daily adjusted prices and summed within month. |
| `mkt_vol_60d` | std (daily) | Aggregate **realized volatility**: 60-trading-day rolling standard deviation of daily market returns (not annualized), mapped to month-end. Used as aggregate uncertainty proxy. |
| `beta_252` | beta | Rolling CAPM beta estimated using 252 trading days of daily returns (firm vs market). Daily beta is then aligned to month (typically last observation in month). |
| `ivol_252` | std (daily) | Firm-level idiosyncratic volatility proxy computed over a 252-day rolling window (as implemented in your pipeline). Conceptually treated as “zero-beta / residual risk”. |
| `ivol_sector` | std (daily) | Sector-level volatility proxy (sector uncertainty / “zero-beta” component in thesis narrative). Used as direct determinant, conceptually separate from aggregate market/credit shocks. |

---

### Aggregate credit factors (external indices)

| Variable | Unit | Description / construction |
|---|---:|---|
| `credit_level` | log return (signed) | Aggregate **credit level shock** from iBoxx USD IG index. Defined as negative monthly log return so that positive values represent worsening/tightening credit conditions. |
| `credit_slope` | return spread | Aggregate **credit slope** factor: long-minus-short segment difference (e.g., 10y+ vs 1–5y) built from iBoxx sub-indices (captures term structure changes in credit). |

---

### “CRC” / credit correlation block (diagnostics and legacy measures)

These variables capture your constructed “CRC-style” credit sensitivity/correlation outputs (kept in the panel for traceability/diagnostics). In the **final identification strategy**, CRC is not used mechanically as a standalone regressor; rather, credit risk is modeled via explicit aggregate credit factors and heterogeneous exposure.

| Variable | Unit | Description |
|---|---:|---|
| `crc_beta` | loading | Firm-level sensitivity/loading from the CRC construction (as implemented in your codebase). |
| `crc_level_beta` | loading | Component/loading associated with the **level** credit factor in the CRC construction. |
| `crc_slope_beta` | loading | Component/loading associated with the **slope** credit factor in the CRC construction. |
| `crc_r2` | [0,1] | Goodness-of-fit measure from the CRC estimation step. |
| `crc_nobs` | count | Number of observations used in the CRC estimation step. |

---

### Capital structure, liquidity, maturity, rollover (constructed controls)

| Variable | Unit | Description / construction |
|---|---:|---|
| `cash_to_assets` | ratio | Cash (and short-term investments) divided by total assets (liquidity proxy). |
| `leverage` | ratio | Total debt / total assets (financial leverage proxy). |
| `log_assets` | log(USD) | Natural log of total assets (firm size). |
| `ltdebt_share` | ratio | Share of long-term debt in total debt (constructed). |
| `rollover_12m` | ratio | Debt maturing within 12 months divided by total debt (refinancing risk). |
| `current_ratio` | ratio | Current assets / current liabilities (liquidity proxy). |
| `interest_coverage` | ratio | Interest coverage proxy (EBITDA or operating income over interest expense, per implementation). |

---

### Market power block

| Variable | Unit | Description |
|---|---:|---|
| `market_share` | ratio | Firm revenue share within sector/industry (unweighted definition retained for traceability). |
| `market_share_w` | ratio | Preferred market power proxy used in models: firm revenue share within **GICS Industry Group** (or your selected industry mapping), forward-filled to monthly frequency. |
| `sector_etf` | string | Sector ETF identifier used to compute sector-based measures (if applicable in your pipeline). |

---

### Raw fundamentals (as downloaded; names preserved)

These fields are raw Refinitiv fundamentals (currency typically USD). Frequency is originally quarterly/annual and converted to monthly via forward fill.

| Variable | Unit | Description |
|---|---:|---|
| `total assets` | USD | Total assets. |
| `total liabilities` | USD | Total liabilities. |
| `total shareholders' equity incl minority intr & hybrid debt` | USD | Total equity including minority interest & hybrid debt (as per Refinitiv field naming). |
| `total current assets` | USD | Total current assets. |
| `total current liabilities` | USD | Total current liabilities. |
| `total debt - actual` | USD | Total debt (actual). |
| `cash & short term investments` | USD | Cash and short-term investments. |
| `short-term debt & current portion of long-term debt` | USD | Short-term debt plus current portion of long-term debt. |
| `debt - long-term - total` | USD | Long-term debt total. |
| `revenue from business activities - total` | USD | Total revenue / sales. |
| `earnings before interest taxes depreciation & amortization` | USD | EBITDA. |
| `net cash flow from operating activities` | USD | Operating cash flow. |
| `interest expense - broker estimate` | USD | Interest expense (broker estimate). |
| `capital expenditures - total` | USD | Capital expenditures. |

---

### Additional derived / convenience fields

| Variable | Unit | Description |
|---|---:|---|
| `total_debt` | USD | Convenience field aggregating debt components (constructed in pipeline; used for leverage/rollover). |

---

## Expected transformations in the econometric notebook

Depending on the final implementation of `03_runer_econometrico.ipynb`, the following common transformations are typically applied:

- Dependent variable: `log_spread_mean_bps = ln(spread_mean_bps)` after restricting to `spread_mean_bps > 0`
- Winsorization: symmetric winsorization (often 1%) applied to dependent and/or continuous regressors (as specified in thesis)
- Fixed effects: firm FE always; time FE only in baseline model M0 (others include explicit aggregate shocks)

If you want, we can add a short “Derived Variables in Models” section once you confirm exactly which derived columns are created inside `03_runer_econometrico.ipynb` vs already stored in the panel.

---

## Quick mapping to thesis notation

- **Dependent**: `log(spread_mean_bps)` (constructed from `spread_mean_bps`)
- **Market shock**: `mkt_ret`
- **Aggregate uncertainty**: `mkt_vol_60d`
- **Credit shock (level)**: `credit_level`
- **Credit term structure**: `credit_slope`
- **Heterogeneity drivers \(Z_{i,t}\)**: `leverage`, `rollover_12m`, `residual_maturity_mean`, `market_share_w`
- **Controls \(X_{i,t}\)**: `leverage`, `log_assets`, `residual_maturity_mean`, `cash_to_assets`, `current_ratio` (plus any additional controls as implemented)

---