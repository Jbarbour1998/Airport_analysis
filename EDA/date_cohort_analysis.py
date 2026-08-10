# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%

# LOADING THE DATA
retailer_data = pd.read_excel(
    "../data/commercial_analyst_task_processed.xlsx", 
    sheet_name="retailerData")

# passengers = pd.read_excel(
#     "../data/commercial_analyst_task_processed.xlsx", 
#     sheet_name="unpivoted_passneger_data")
# retailer_data
# passengers


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

# passengers["month"] = passengers["month"].astype("string")
# print(passengers.info())


# %%
retailer_data[['transactions', 'total_sales']].describe()


# %%

