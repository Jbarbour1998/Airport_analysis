# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%

# LOADING THE DATA
retailer_data = pd.read_excel(
    "../Edinburgh_airport_analysis_challenege/data/commercial_analyst_task_processed.xlsx", 
    sheet_name="retailerData")
passengers = pd.read_excel(
    "../Edinburgh_airport_analysis_challenege/data/commercial_analyst_task_processed.xlsx", 
    sheet_name="unpivoted_passneger_data")
retailer_data
passengers

# %% SAINTY CHECK
# TURING ALL THE OBJECT DATA POINTS INTO STINGS

text_columns = [
    "category_group",
    "outlet_name",
    "outlet_type",
    "month_of_month_start_date",
    "unit_location"
]

retailer_data[text_columns] = retailer_data[text_columns].astype("string")
print(retailer_data.info())

passengers["month"] = passengers["month"].astype("string")
print(passengers.info())

# GROUP BY 
print(retailer_data.groupby("outlet_name")["date"].agg(["min", "max", "count"]))
print(passengers.groupby("month_number")["date"].agg(["min", "max", "count"]))

retail_full = retailer_data.copy()
passengers_full = passengers.copy()



# %%

# these are all the calculated Columns
# ATV OR Sales per transaction | sales_per_sqm

retail_full["sales_per_transaction"] = (
    retail_full["total_sales"]
    / retail_full["transactions"]
)

# Sales Per Square Meter
retail_full["sales_per_sqm"] = (
    retail_full["total_sales"]
    / retail_full["unit_size_sqm"]
)


passengers_full
retail_full

# %%
# MERGING THE TWO DATA SET 'PASSENGER' AND 'RETAIL' FOR EASIER ANALYSIS
retail_passenger_comparison = retail_full.merge(
    passengers_full[["date", "passenger_amount"]],
    on="date",
    how="inner"
)
retail_passenger_comparison


# %%

retail_passenger_comparison.shape # SHAPE = [ 122, 13] - THIS IS CORRECT 30 + 30 + 30 + 19 + 13 = 122 OBSERVATIONS

# %%
# PASSENGER TO RETAIL SALES CALCULATED COLUMNS
#  sales_per_passenger | capture_rate | capture_rate_percentage

# sales_per_passenger
retail_passenger_comparison["sales_per_passenger"] = (
    retail_passenger_comparison["total_sales"]
    / retail_passenger_comparison["passenger_amount"]
)

# capture_rate
retail_passenger_comparison["capture_rate"] = (
    retail_passenger_comparison["transactions"]
    / retail_passenger_comparison["passenger_amount"]
)

# capture_rate_percentage
retail_passenger_comparison["capture_rate_percentage"] = (
    retail_passenger_comparison["transactions"]
    / retail_passenger_comparison["passenger_amount"]
) * 100

# sales_per_1000_passengers
retail_passenger_comparison["sales_per_1000_passengers"] = (
    retail_passenger_comparison["total_sales"]
    / retail_passenger_comparison["passenger_amount"]
    * 1000
)

# transactions_per_1000_passengers
retail_passenger_comparison["transactions_per_1000_passengers"] = (
    retail_passenger_comparison["transactions"]
    / retail_passenger_comparison["passenger_amount"]
    * 1000
)


# %% EXPORT TO EXCEL WITH LIVE EXCEL FORMULAS

# %% EXPORT RETAIL-PASSENGER DATA WITH LIVE EXCEL FORMULAS

import pandas as pd


# Convert an Excel column number into a letter:
# 1 = A, 2 = B, 27 = AA, etc.
def excel_column_letter(column_number):
    column_letter = ""

    while column_number > 0:
        column_number, remainder = divmod(column_number - 1, 26)
        column_letter = chr(65 + remainder) + column_letter

    return column_letter


# Columns that will be recreated as Excel formulas
calculated_columns = [
    "sales_per_transaction",
    "sales_per_sqm",
    "sales_per_passenger",
    "capture_rate",
    "capture_rate_percentage",
    "sales_per_1000_passengers",
    "transactions_per_1000_passengers"
]


# Remove existing calculated values from the export copy
# so they can be replaced with Excel formulas
excel_output = retail_passenger_comparison.drop(
    columns=calculated_columns,
    errors="ignore"
).copy()


# Check that all required source columns exist
required_columns = [
    "total_sales",
    "transactions",
    "unit_size_sqm",
    "passenger_amount"
]

missing_columns = [
    column
    for column in required_columns
    if column not in excel_output.columns
]

if missing_columns:
    raise KeyError(
        f"These required columns are missing: {missing_columns}"
    )


# Find the Excel letter for each source column dynamically
sales_column = excel_column_letter(
    excel_output.columns.get_loc("total_sales") + 1
)

transactions_column = excel_column_letter(
    excel_output.columns.get_loc("transactions") + 1
)

unit_size_column = excel_column_letter(
    excel_output.columns.get_loc("unit_size_sqm") + 1
)

passenger_column = excel_column_letter(
    excel_output.columns.get_loc("passenger_amount") + 1
)


number_of_rows = len(excel_output)
excel_rows = range(2, number_of_rows + 2)


# Average sales generated per transaction
excel_output["sales_per_transaction"] = [
    (
        f'=IFERROR('
        f'{sales_column}{row}/{transactions_column}{row},'
        f'0)'
    )
    for row in excel_rows
]


# Sales generated per square metre
excel_output["sales_per_sqm"] = [
    (
        f'=IFERROR('
        f'{sales_column}{row}/{unit_size_column}{row},'
        f'0)'
    )
    for row in excel_rows
]


# Sales generated per airport passenger
excel_output["sales_per_passenger"] = [
    (
        f'=IFERROR('
        f'{sales_column}{row}/{passenger_column}{row},'
        f'0)'
    )
    for row in excel_rows
]


# Transactions per passenger
excel_output["capture_rate"] = [
    (
        f'=IFERROR('
        f'{transactions_column}{row}/{passenger_column}{row},'
        f'0)'
    )
    for row in excel_rows
]


# Transactions per 100 passengers
excel_output["capture_rate_percentage"] = [
    (
        f'=IFERROR(('
        f'{transactions_column}{row}/{passenger_column}{row})*100,'
        f'0)'
    )
    for row in excel_rows
]


# Sales generated per 1,000 passengers
excel_output["sales_per_1000_passengers"] = [
    (
        f'=IFERROR(('
        f'{sales_column}{row}/{passenger_column}{row})*1000,'
        f'0)'
    )
    for row in excel_rows
]


# Transactions generated per 1,000 passengers
excel_output["transactions_per_1000_passengers"] = [
    (
        f'=IFERROR(('
        f'{transactions_column}{row}/{passenger_column}{row})*1000,'
        f'0)'
    )
    for row in excel_rows
]


# Export to Excel
excel_output.to_excel(
    "retail_passenger_comparison.xlsx",
    sheet_name="Retail Passenger Comparison",
    index=False
)

print("retail_passenger_comparison.xlsx created successfully.")
# %%
