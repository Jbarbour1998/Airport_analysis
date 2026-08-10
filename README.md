# Catering Performance Analysis — Edinburgh Airport (2026 YTD)

## Overview
This analysis reviews catering performance across the Edinburgh Airport retail estate for 2026 year-to-date (YTD), benchmarked against the equivalent 2025 period. It examines performance at both estate level and individual outlet level, using sales, transaction volume, passenger throughput, and average transaction value (ATV) as core metrics.

## Methodology
- **Growth rates** are calculated as YTD 2026 vs. the equivalent YTD 2025 period, for sales, transactions, passengers, and ATV.
- **Average transaction value (ATV)** is derived as sales ÷ transaction count, calculated both at estate level and by individual outlet/month.
- **Correlation analysis** was used to assess the relationship between passenger volume, transaction counts, and sales. This measures association, not causation.
- **Data-quality screening** applied a £50 sales-per-transaction threshold to flag rows for manual review. This is a screening heuristic, not a determination that a value is incorrect.
- **Missing outlet-months** were treated as data gaps (no available record) rather than periods of zero sales, to avoid distorting growth calculations.
- Flagged historic outliers (e.g. Terminal Kitchen, August 2024) were retained in the dataset rather than altered, as there was no independent basis to correct the source value. Where relevant, results were tested both including and excluding flagged observations.

## Key Findings
- **Overall performance:** YTD catering sales reached £14.42m, up 8.8% year-on-year. Transactions rose 6.6%, passengers 5.4%, and average transaction value 2.1%, indicating growth came from both higher volume and higher spend per transaction.
- **Passenger traffic is a driver, not a determinant:** Passenger volume correlates positively with sales and transactions, confirming it as a key demand driver. However, monthly variation between passenger growth, transaction growth, and ATV shows that conversion efficiency also plays a significant, distinct commercial role.
- **Concentration of contribution — North Kitchen:** North Kitchen is the estate's largest contributor, generating approximately £8.15m (56.5% of total sales) from around 545,540 transactions, reflecting both high transaction throughput and its larger unit size.
- **Outlet-level divergence:** Performance varied by outlet — Oak Coffee Bar grew 25.3%, while Gate Bistro and Terminal Kitchen declined 12.0% and 13.3% respectively. Sky Deli grew 99.1%, though this comparison is not fully like-for-like due to incomplete prior-year data.
- **Data quality observations:** Two ATV outliers were flagged, the most notable being Terminal Kitchen in August 2024, where an average of £134.41 was recorded from £5.16m in sales across 38,398 transactions. The value was retained rather than altered; results should be interpreted both including and excluding it.

## Assumptions and Limitations
- Missing outlet-months are treated as data gaps, not as periods of zero sales.
- Passenger figures reflect total airport passenger volume and may not correspond to footfall at individual outlet locations.
- Transactions are counted as completed purchases, not unique customers; repeat purchases by the same customer are not distinguished.
- Statistical correlation between passengers, transactions, and sales is descriptive only and does not establish causation.
- A threshold of £50 sales-per-transaction was used to flag rows for review. This threshold is a screening heuristic, not a determination of error.
- The Sky Deli year-on-year comparison is not fully like-for-like, owing to incomplete prior-year data.
- Candidate explanations involving pricing, opening hours, weather, construction, or outlet location are hypotheses only; the dataset does not contain the information required to verify causal mechanisms.

## How to Read This Analysis
Figures are presented at estate level first, then broken down by outlet. Where a result is materially affected by a flagged data-quality observation (e.g. historic ATV outliers), this is noted alongside the figure so it can be interpreted with appropriate caution.
