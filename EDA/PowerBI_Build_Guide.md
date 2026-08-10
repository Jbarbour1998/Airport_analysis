# Edinburgh Airport Catering — Power BI Build Guide

## What is included

- `edinburgh_airport_catering_challenge.xlsx`
- `Edinburgh_Airport_Catering_Theme.json`
- `Date_Table.dax`
- `PowerBI_Measures.dax`

A native `.pbix` file is not included because Power BI Desktop is required to author and validate that proprietary report file. This pack contains the prepared data, model design, DAX and theme needed to build the dashboard quickly.

## 1. Load the Excel tables

In Power BI Desktop:

1. Select **Get data → Excel workbook**.
2. Open `edinburgh_airport_catering_challenge.xlsx`.
3. Select the Excel tables:
   - `RetailDataTable`
   - `PassengerDataTable`
4. Select **Transform Data**.
5. Rename the queries:
   - `RetailDataTable` → `Retail`
   - `PassengerDataTable` → `Passengers`
6. Confirm:
   - `date` is Date
   - `year`, `month_number` and `unit_size_sqm` are Whole number
   - `transactions`, `total_sales` and `passenger_amount` are Decimal or Whole number as appropriate
   - outlet and descriptive fields are Text

Do not load the Excel `Output` sheet into the model. It is formula evidence for the assessment, not a fact table.

## 2. Create the Date table

Open **Table tools → New table** and paste the expression from `Date_Table.dax`.

Then:

- Mark `Date` as the model's date table using the `Date` column.
- Sort `Month` by `Month Number`.
- Sort `Year Month` by `Year Month Sort`.

## 3. Create relationships

Create these one-to-many, single-direction relationships:

- `Date[Date]` → `Retail[date]`
- `Date[Date]` → `Passengers[date]`

The Date table must be on the one side.

Do not directly relate Retail to Passengers.

## 4. Create measures

Create a blank measure table, or place the measures in `Retail`.

Paste the measures from `PowerBI_Measures.dax` one at a time.

Recommended formatting:

- Sales measures: Currency, 0 or 2 decimals
- Transactions and passengers: Whole number
- Average transaction value and sales per sqm: Currency, 2 decimals
- Percentage measures: Percentage, 1 decimal
- Per-1,000 measures: Decimal, 1 or 2 decimals

## 5. Import the theme

Select **View → Themes → Browse for themes** and choose:

`Edinburgh_Airport_Catering_Theme.json`

## 6. Report pages

### Page 1 — Executive Overview

Slicers:
- `Date[Year]`
- `Date[Date]` as Between
- `Retail[outlet_name]`
- `Retail[unit_location]`

Cards:
- `Sales YTD`
- `Sales YTD YoY %`
- `Transactions YTD`
- `Average Transaction Value YTD`
- `Transactions per 1,000 Passengers YTD`

Visuals:
1. Line chart:
   - X-axis: `Date[Year Month]`
   - Values: `Total Sales`, `Sales Prior Year`
2. Clustered bar chart:
   - Y-axis: `Retail[outlet_name]`
   - X-axis: `Sales YTD`
3. Line chart:
   - X-axis: `Date[Year Month]`
   - Value: `Transactions per 1,000 Passengers`
4. Matrix:
   - Rows: `Retail[outlet_name]`
   - Values: `Sales YTD`, `Sales YTD Prior Year`, `Sales YTD YoY %`,
     `Transactions YTD`, `Average Transaction Value YTD`, `Estate Sales Share`

### Page 2 — Outlet Performance

Slicer:
- `Retail[outlet_name]`, single select

Cards:
- `Total Sales`
- `Total Transactions`
- `Average Transaction Value`
- `Sales per Sqm`
- `Estate Sales Share`

Visuals:
1. Line chart — monthly sales:
   - X-axis: `Date[Year Month]`
   - Values: `Total Sales`, `Sales Prior Year`
2. Line chart — monthly transactions:
   - X-axis: `Date[Year Month]`
   - Values: `Total Transactions`, `Transactions Prior Year`
3. Scatter chart:
   - X-axis: `Total Transactions`
   - Y-axis: `Total Sales`
   - Details: `Date[Year Month]`
4. Table:
   - `Date[Year Month]`
   - `Total Sales`
   - `Total Transactions`
   - `Average Transaction Value`
   - `Sales YoY %`

### Page 3 — YoY and YTD

Cards:
- `Sales YTD`
- `Sales YTD Prior Year`
- `Sales YTD YoY %`
- `Transactions YTD YoY %`
- `Passengers YTD YoY %`

Visuals:
1. Line chart:
   - X-axis: `Date[Year Month]`
   - Values: `Sales YTD`, `Sales YTD Prior Year`
2. Clustered bar chart:
   - Axis: `Retail[outlet_name]`
   - Values: `Sales YTD`, `Sales YTD Prior Year`
3. Matrix:
   - Rows: `Retail[outlet_name]`
   - Values: `Sales YTD`, `Sales YTD Prior Year`, `Sales YTD YoY %`,
     `Transactions YTD`, `Average Transaction Value YTD`
4. Line chart:
   - X-axis: `Date[Year Month]`
   - Values: `Total Passengers`, `Total Transactions`

### Page 4 — Data Quality and Sensitivity

Cards:
- `Flagged Row Count`
- `Flagged Sales`
- `Total Sales Excluding Flagged Rows`
- `Flagged Sales Impact`

Table:
- `Retail[date]`
- `Retail[outlet_name]`
- `Retail[transactions]`
- `Retail[total_sales]`
- `Retail[sales_per_transaction]`
- `Retail[data_quality_flag]`

Filter this page to `data_quality_flag = Review`.

## 7. Interaction settings

- Synchronise the Year, Date and Outlet slicers across pages.
- Use Edit interactions so the outlet bar chart filters the other visuals.
- Keep tooltips enabled.
- Use conditional formatting on YoY percentages:
  - Positive: green
  - Negative: red
- Add a Reset Filters bookmark and button.

## 8. Important interpretation rules

- Passenger totals must come only from the `Passengers` table.
- Use the common 12-month period when directly comparing totals across all five outlets.
- Use full history when analysing an outlet against its own previous performance.
- Retain the Terminal Kitchen August 2024 source value, but flag it and show the sensitivity result.
- Do not infer causation from passenger-sales correlation; the sample is short and outlet coverage changes over time.

## 9. Suggested five-bullet summary structure

Complete the exact figures after validating the report:

- Overall catering YTD sales changed by **[x%]** versus the equivalent prior-year period.
- **[Outlet]** generated the largest YTD sales contribution, accounting for **[x%]** of estate sales.
- Transaction volume changed by **[x%]**, while average transaction value changed by **[x%]**, showing whether performance was volume- or spend-led.
- Transactions per 1,000 passengers changed by **[x%]**, indicating whether the estate improved its passenger conversion.
- Terminal Kitchen's August 2024 result is a material outlier; conclusions should be checked both including and excluding that source value.
