# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import DateFormatter

# %%

# LOADING THE DATA
retail_passenger_comparison = pd.read_excel(
    "../data/retail_passenger_comparison.xlsx")


# %%
# outlet over its full history
for outlet in retail_passenger_comparison["outlet_name"].unique():

    outlet_data = (
        retail_passenger_comparison[
            retail_passenger_comparison["outlet_name"] == outlet
        ]
        .sort_values("date")
    )
    
    #columns to plot
    columns = ['total_sales', 
           'transactions',
           'sales_per_transaction']

    outlet_data.plot(
        x="date",
        y= columns,
        kind="line",
        marker="o",
        figsize=(10, 5),
        legend=False
    )




    plt.title(f"Monthly sales — {outlet}")
    plt.xlabel("Date")
    plt.ylabel(f"Total {columns}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    

# %%
plot_data = retail_passenger_comparison.copy()
plot_data["date"] = pd.to_datetime(plot_data["date"])

monthly_outlet = (
    plot_data
    .groupby(["date", "outlet_name"], as_index=False)
    .agg(
        total_sales=("total_sales", "sum"),
        transactions=("transactions", "sum")
    )
)

# Recalculate after grouping
monthly_outlet["sales_per_transaction"] = (
    monthly_outlet["total_sales"]
    / monthly_outlet["transactions"].replace(0, np.nan)
)
# %%
def plot_outlet_metric(metric, title, ylabel, formatter):
    
    metric_data = monthly_outlet.pivot(
        index="date",
        columns="outlet_name",
        values=metric
    ).sort_index()

    fig, ax = plt.subplots(figsize=(14, 7))

    for outlet in metric_data.columns:
        ax.plot(
            metric_data.index,
            metric_data[outlet],
            marker="o",
            linewidth=2,
            label=outlet
        )

    ax.set_title(title)
    ax.set_xlabel("Month")
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(formatter)

    ax.grid(True, alpha=0.3)

    ax.legend(
        title="Outlet",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()
    
# %%
# Sales per transaction plot
plot_outlet_metric(
    metric="sales_per_transaction",
    title="Monthly Sales per Transaction by Outlet",
    ylabel="Sales per Transaction (£)",
    formatter=FuncFormatter(
        lambda value, position: f"£{value:,.2f}"
    )
)


# %%
#Total sales plot
plot_outlet_metric(
    metric="total_sales",
    title="Monthly Total Sales by Outlet",
    ylabel="Total Sales (£)",
    formatter=FuncFormatter(
        lambda value, position: f"£{value:,.0f}"
    )
)

# %%
# Transactions plot
plot_outlet_metric(
    metric="transactions",
    title="Monthly Transactions by Outlet",
    ylabel="Number of Transactions",
    formatter=FuncFormatter(
        lambda value, position: f"{value:,.0f}"
    )
)


# %%%

plot_data = retail_passenger_comparison.copy()
plot_data["date"] = pd.to_datetime(plot_data["date"])

# Ensure one observation per outlet per month
monthly_outlet = (
    plot_data
    .groupby(["date", "outlet_name"], as_index=False)
    .agg(
        total_sales=("total_sales", "sum"),
        transactions=("transactions", "sum")
    )
    .sort_values(["outlet_name", "date"])
)

# Recalculate after grouping
monthly_outlet["sales_per_transaction"] = (
    monthly_outlet["total_sales"]
    / monthly_outlet["transactions"].replace(0, np.nan)
)

def plot_metric_by_outlet(
    data,
    metric,
    main_title,
    y_label,
    formatter,
    columns=2
):
    outlets = sorted(data["outlet_name"].dropna().unique())

    number_of_outlets = len(outlets)
    rows = int(np.ceil(number_of_outlets / columns))

    fig, axes = plt.subplots(
        nrows=rows,
        ncols=columns,
        figsize=(15, rows * 4.5),
        sharex=False,
        sharey=False
    )

    # Ensure axes is always a flat list
    axes = np.atleast_1d(axes).flatten()

    for ax, outlet in zip(axes, outlets):

        outlet_data = (
            data[data["outlet_name"] == outlet]
            .sort_values("date")
        )

        ax.plot(
            outlet_data["date"],
            outlet_data[metric],
            marker="o",
            linewidth=2
        )

        ax.set_title(outlet)
        ax.set_xlabel("Month")
        ax.set_ylabel(y_label)

        ax.yaxis.set_major_formatter(formatter)
        ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))

        ax.grid(True, alpha=0.3)
        ax.tick_params(axis="x", rotation=45)

    # Remove empty subplots
    for ax in axes[number_of_outlets:]:
        fig.delaxes(ax)

    fig.suptitle(
        main_title,
        fontsize=16,
        y=1.02
    )

    plt.tight_layout()
    plt.show()
    
# %%
# Transactions: one plot per outlet
plot_metric_by_outlet(
    data=monthly_outlet,
    metric="transactions",
    main_title="Monthly Transactions by Outlet",
    y_label="Number of Transactions",
    formatter=FuncFormatter(
        lambda value, position: f"{value:,.0f}"
    )
)
# %%
# Total sales: one plot per outlet
plot_metric_by_outlet(
    data=monthly_outlet,
    metric="total_sales",
    main_title="Monthly Total Sales by Outlet",
    y_label="Total Sales (£)",
    formatter=FuncFormatter(
        lambda value, position: f"£{value:,.0f}"
    )
)

# %%
# Sales per transaction: one plot per outlet
plot_metric_by_outlet(
    data=monthly_outlet,
    metric="sales_per_transaction",
    main_title="Monthly Sales per Transaction by Outlet",
    y_label="Sales per Transaction (£)",
    formatter=FuncFormatter(
        lambda value, position: f"£{value:,.2f}"
    )
)
# %%
