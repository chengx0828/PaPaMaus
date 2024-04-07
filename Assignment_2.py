# %% [markdown]
# Problem Set 2

# %%
import numpy as np
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

github("chengx0828", "UW-ECON481", "Assignment_2.py")

# %% [markdown]
# Exercise 1

# %%
def simulate_data(seed: int = 481) -> tuple:
    """
    Some docstrings.
    """
    np.random.seed(seed)
    X = np.random.normal(0, np.sqrt(2), (1000, 3))
    errors = np.random.normal(0, 1, 1000)
    y = 5 + 3 * X[:, 0] + 2*X[:, 1] + 6*X[:, 2] + errors
    y = y.reshape(-1, 1)
    return (y, X)

y, X = simulate_data(481)
print(X.shape)
print(y.shape)


# %% [markdown]
# Exercise 2

# %%
def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Some docstrings.
    """
    def likelihood(beta, y, X):
        predicted = np.dot(X, beta)
        residuals = y - predicted
        return -np.sum(np.log(1 / np.sqrt(2 * np.pi)) - 0.5 * residuals**2)
    
    intercept = np.ones((X.shape[0], 1))
    X_with_intercept = np.hstack((intercept, X))
    beta_init = np.zeros(X_with_intercept.shape[1])
    result = minimize(likelihood, beta_init, args=(y.flatten(), X_with_intercept))
    result.x = result.x.reshape(-1, 1)
    return result.x

estimate_mle(y, X)
print(estimate_mle(y, X).shape)
print(estimate_mle(y, X))


# %% [markdown]
# Exercise 3

# %%
def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Some docstrings.
    """
    X_with_intercept = np.hstack((np.ones((X.shape[0], 1)), X))
    def objective_function(beta):
        return np.sum((y - X_with_intercept @ beta) ** 2)
    beta_init = np.zeros(X_with_intercept.shape[1])
    result = minimize(objective_function, beta_init)
    beta_hat = result.x.reshape(-1, 1)
    return beta_hat

shapetest = estimate_ols(y, X)
print(shapetest.shape)
print(estimate_mle(y, X))



