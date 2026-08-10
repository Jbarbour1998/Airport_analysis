# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
retailer_data = pd.read_excel(
    "../data/commercial_analyst_task_processed.xlsx", 
    sheet_name="retailerData")
passengers = pd.read_excel(
    "../data/commercial_analyst_task_processed.xlsx", 
    sheet_name="unpivoted_passneger_data")
retailer_data
passengers


# %% SAINTY CHECK


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

# %%
print(passengers.info())


# %% GROUP BY 
print(retailer_data.groupby("outlet_name")["date"].agg(["min", "max", "count"]))


# %%
print(passengers.groupby("month_number")["date"].agg(["min", "max", "count"]))

# %%

last_actual_date = passengers.loc[
    passengers["passenger_amount"].gt(0),
    "date"
].max()

passengers.loc[
    passengers["date"].gt(last_actual_date),
    "passenger_amount"
] = pd.NA

print(last_actual_date)

# %% checking data end

sky_deli = retailer_data.loc[
    retailer_data["outlet_name"] == "Sky Deli",
    "date"
]

expected_dates = pd.date_range(
    start=sky_deli.min(),
    end=sky_deli.max(),
    freq="MS"
)

missing_dates = expected_dates.difference(sky_deli)

print(missing_dates)

# %%
passengers_actual = passengers.loc[
    passengers["date"] <= last_actual_date
].copy()


# %%

print(passengers_actual["date"].min())
print(passengers_actual["date"].max())
print(passengers_actual.tail())

# %%
duplicates = retailer_data[
    retailer_data.duplicated(
        subset=["outlet_name", "date"],
        keep=False
    )
].sort_values(["outlet_name", "date"])

print(duplicates)

# %%


outlet_coverage = (
    retailer_data
    .groupby("outlet_name")["date"]
    .agg(["min", "max"])
)

common_start = max(
    passengers_actual["date"].min(),
    outlet_coverage["min"].max()
)

common_end = min(
    passengers_actual["date"].max(),
    outlet_coverage["max"].min()
)


# %%

passengers_comparison = passengers_actual.loc[
    passengers_actual["date"].between(common_start, common_end)
].copy()

retail_comparison = retailer_data.loc[
    retailer_data["date"].between(common_start, common_end)
].copy()


passengers_comparison = (
    passengers_comparison
    .sort_values("date")
    .reset_index(drop=True)
)

retail_comparison = (
    retail_comparison
    .sort_values(["outlet_name", "date"])
    .reset_index(drop=True)
)






##########################################################################
# PLOTTING THE GRAPGHS NOW
##########################################################################

# %% THE FIRST PLOT: passenger trends
from matplotlib.ticker import StrMethodFormatter

ax = passengers_comparison.plot(
    
    x= 'date',
    y= 'passenger_amount',
    kind = 'line',
    marker = 'o',
    figsize = (10,5),
    legend = False
)

ax.set_title("Monthly Passenger Numbers")
ax.set_xlabel("Date")
ax.set_ylabel("Passengers")

# Show full passenger values, such as 1,500,000
ax.ticklabel_format(axis="y", style="plain", useOffset=False)
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#"
# The trend is that around Jan the flights are the lowest, and the steadily increase upward and then peak
# around about Jun and Aug. The passenegers then seem to fall but a strange trend is that around about Nov to
# to Decemeber there is a quick spike then ofter that it drops quite a from Dec to Jan. 
# Asssumtions for this trend are that around about Novemeber 2 or maybe 3 things are happening 
#   1) Students are heading home for Christmas 
#   2) Plane tickets are increasing around this period so people are flying then in a big rush 
#   3) January Not many are flying because of Holidays and Plane tickets being expensive
# "

# %%
# PLOTTING MONTHLY REATIAL SALES
# 1st agrregating the five outlets into one montly business total

monthly_retail = (
    retail_comparison
    .groupby("date", as_index=False)
    .agg(
        total_sales=("total_sales", "sum"),
        total_transactions=("transactions", "sum")
    )
    .sort_values("date")
)

# %%
# Now I plot

monthly_retail.plot(
    x="date",
    y="total_sales",
    kind="line",
    marker="o",
    figsize=(10, 5),
    legend=False
)

# 


plt.title("Total monthly retail sales")
plt.xlabel("Date")
plt.ylabel("Total sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Comparing Outlet sales trends

# %%
outlet_sales = retail_comparison.pivot(
    index="date",
    columns="outlet_name",
    values="total_sales"
)

outlet_sales.plot(
    kind="line",
    marker="o",
    figsize=(11, 6)
)

plt.title("Monthly sales by outlet")
plt.xlabel("Date")
plt.ylabel("Total sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
## Now compare total sales against passengers


monthly_comparison = monthly_retail.merge(
    passengers_comparison[["date", "passenger_amount"]],
    on="date",
    how="inner"
)




monthly_comparison.plot(
    x="date",
    y="passenger_amount",
    kind="line",
    marker="o",
    figsize=(10, 5),
    legend=False
)

plt.title("Monthly passenger trend")
plt.xlabel("Date")
plt.ylabel("Passengers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% SCATTER PLOT OF MONTHLY COMPARISON

monthly_comparison.plot(
    x="passenger_amount",
    y="total_sales",
    kind="scatter",
    figsize=(8, 5)
)

plt.title("Passenger numbers versus retail sales")
plt.xlabel("Passenger numbers")
plt.ylabel("Total retail sales")
plt.tight_layout()
plt.show()
# %%
