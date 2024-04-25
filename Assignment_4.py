# %% [markdown]
# Problem Set 2

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit
from statsmodels.tools import add_constant
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

github("chengx0828", "UW-ECON481", "Assignment_4.py")

# %% [markdown]
# Exercise 1

# %%
import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Load the data from the following URL:
    """
    url_E1 = "https://lukashager.netlify.app/econ-481/data/TSLA.csv"
    data_E1 = pd.read_csv(url_E1)
    return data_E1

load_data()

# %% [markdown]
# Exercise 2

# %%
def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    Plot the closing prices of Tesla stock from the given start date to the given end date.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    mask = (df['Date'] >= start) & (df['Date'] <= end)
    filtered_df = df.loc[mask]
    
    plt.figure(figsize=(15, 5))
    plt.plot(filtered_df['Date'], filtered_df['Close'], label='Closing Price')
    plt.title(f'Tesla Stock Closing Prices from {start} to {end}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.legend()
    plt.grid(True)
    
    plt.show()

plot_close(load_data())

# %% [markdown]
# Exercise 3

# %%
def autoregress(df: pd.DataFrame) -> float:
    """
    Estimate the autoregressive coefficient of the first lag of the closing prices of Tesla stock.
    """
    df['Change'] = df['Close'].diff()
    df = df.dropna()
    df['Lagged_Change'] = df['Change'].shift(1)
    df = df.dropna()
    X = df['Lagged_Change']
    y = df['Change']
    model = sm.OLS(y, X).fit(cov_type='HC1')
    t_statistic = model.tvalues[0]

    return t_statistic

autoregress(load_data())

# %% [markdown]
# Exercise 4

# %%
def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Perform a logistic regression with the lagged change in closing price as the independent variable.
    """
    df['Change'] = df['Close'].diff()
    df['Change_lagged'] = df['Change'].shift(1)
    df = df.dropna()
    df['Target'] = (df['Change'] >= 0).astype(int)
    X = add_constant(df['Change_lagged'])
    Y = df['Target']
    model = Logit(Y, X).fit(disp=0)
    t_stat = model.tvalues[0]
    
    return t_stat

autoregress_logit(load_data())


# %% [markdown]
# Exercise 5

# %%
import matplotlib.pyplot as plt

def plot_delta(df: pd.DataFrame) -> None:
    """
    Plot the daily change in closing price.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df['Delta_Close'] = df['Close'].diff()
    
    plt.figure(figsize=(12, 12))
    plt.plot(df['Date'], df['Delta_Close'], label='ΔClose')
    plt.title('Daily Change in Closing Price (USD)')
    plt.xlabel('Date (Year)')
    plt.ylabel('Change in Closing Price (USD)')
    plt.legend()
    plt.show()

plot_delta(load_data())


