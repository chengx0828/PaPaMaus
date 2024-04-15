# %% [markdown]
# Problem Set 2

# %%
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# %% [markdown]
# Exercise 0

# %%
def github(a, b, c) -> str:
    """
    A link to the solutions on GitHub.
    """
    user = a
    repo = b
    filename = c


    return "https://github.com/{user}/{repo}/blob/main/{filename}".format(user=user, repo=repo, filename=filename)

github("chengx0828", "UW-ECON481", "Assignment_3.py")

# %% [markdown]
# Exercise 1

# %%
def import_yearly_data(years: list) -> pd.DataFrame:
    
    data_frames = []
    for year in years:
        url = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"
        dfE1 = pd.read_excel(url, 
            sheet_name='Direct Emitters', 
            header=3)
        dfE1['Year'] = year
        data_frames.append(dfE1)
    
    concentrated_data = pd.concat(data_frames, ignore_index=True)
    return concentrated_data

import_yearly_data([2019, 2020, 2021, 2022])



# %% [markdown]
# Exercise 2

# %%
def import_parent_companies(years: list) -> pd.DataFrame:

    data_frames = []
    for year in years:
        dfE2 = pd.read_excel("https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb", 
            sheet_name = f"{year}",
            header=0)
        data_frames.append(dfE2)
    
    concentrated_data = pd.concat(data_frames, ignore_index=True)
    return concentrated_data

import_parent_companies([2019,2020, 2021, 2022])

# %% [markdown]
# Exercise 3

# %%
def n_null(df: pd.DataFrame, col: str) -> int:

    return df[col].isnull().sum()

n_null(import_yearly_data([2019, 2020, 2021, 2022]), 'Electricity Generation') 



# %% [markdown]
# Exercise 4

# %%
def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:

    merged_data = pd.merge(
        emissions_data,
        parent_data,
        how='left',
        left_on=['Facility Id'],
        right_on=['GHGRP FACILITY ID']
    )

    subset_data = merged_data[[
        'Facility Id',
        'Year',
        'State',
        'Industry Type (sectors)',
        'Total reported direct emissions',
        'PARENT CO. STATE',
        'PARENT CO. PERCENT OWNERSHIP'
    ]]
    
    subset_data.columns = [col.lower() for col in subset_data.columns]

    return subset_data

clean_data(import_yearly_data([2019, 2020, 2021, 2022]), import_parent_companies([2019, 2020, 2021, 2022]))



# %% [markdown]
# Exercise 5

# %%
def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:

    agg_df = df.groupby(group_vars).agg({
        'total reported direct emissions': ['min', 'median', 'mean', 'max'],
        'parent co. percent ownership': ['min', 'median', 'mean', 'max']
    })
    
    agg_df = agg_df.sort_values(('total reported direct emissions', 'mean'), ascending=False)
    
    return agg_df

aggregate_emissions(clean_data(import_yearly_data([2019, 2020, 2021, 2022]), import_parent_companies([2019, 2020, 2021, 2022])), ['state', 'facility id'])


