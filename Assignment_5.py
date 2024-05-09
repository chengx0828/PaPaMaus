# %% [markdown]
# Problem Set 4

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit
from statsmodels.tools import add_constant
import requests
from bs4 import BeautifulSoup

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

github("chengx0828", "UW-ECON481", "Assignment_5.py")

# %% [markdown]
# Exercise 1

# %%
def scrape_code(url: str) -> str:
    """
    
    """
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    code_blocks = soup.find_all('code')
    all_code = []
    for block in code_blocks:
        code = block.get_text()
        filtered_code = '\n'.join(line for line in code.splitlines() if not line.strip().startswith('%'))
        all_code.append(filtered_code)
    combined_code = '\n'.join(all_code)
    return combined_code

scrape_code("https://lukashager.netlify.app/econ-481/01_intro_to_python")


