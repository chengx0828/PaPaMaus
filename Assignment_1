# %% [markdown]
# Excercise 0
# 
# Please write a function that takes no arguments and returns a link to your solutions on GitHub.

# %%
def github() -> str:
    """
    Some docstrings.
    """


    return "https://github.com/chengx0828/PaPamaus/blob/main/Assignment_1"

github()

# %% [markdown]
# Excercise 2
# 
# Please write a function called evens_and_odds that takes as argument a natural number n and returns a dictionary with two keys, “evens” and “odds”. “evens” should be the sum of all the even natural numbers less than n, and “odds” the sum of all natural numbers less than n.
# 
# For example, evens_and_odds(4) should return
# 
# {'evens': 2, 'odds': 4}

# %%
def evens_and_odds(n: int) -> dict:
    """
    A function that calculate the sum of even and odd numbers less than n.
    """

    even_sum = sum(n for n in range(n) if n % 2 == 0)
    odd_sum = sum(n for n in range(n) if n % 2 == 1)

    return {'evens': even_sum, 'odds': odd_sum}

evens_and_odds(18)

# %% [markdown]
# Exercise 3
# 
# Please write a function called time_diff that takes as arguments two strings in the format ‘YYYY-MM-DD’ and a keyword out dictating the output. If the keyword is “float”, return the time between the two dates (in absolute value) in days. If the keyword is “string”, return “There are XX days between the two dates”. If not specified, the out keyword should be assumed to be “float”. You should use the datetime package, and no others.
# 
# For example, time_diff('2020-01-01', '2020-01-02', 'float') should return 
# 
# "1"
# 
# For example, time_diff('2020-01-03', '2020-01-01', 'string') should return
# 
# "There are 2 days between the two dates"

# %%
from typing import Union
from datetime import datetime

def time_diff(date_1: str, date_2: str, out: str = 'float') -> Union[str,float]:
    """
    A function that calculate the absolute difference in days between two dates.
    """
    d1 = datetime.strptime(date_1, '%Y-%m-%d')
    d2 = datetime.strptime(date_2, '%Y-%m-%d')

    if out == 'string':
        return f"There are {abs((d2 - d1).days)} days between the two dates"
    return {abs((d2 - d1).days)}

time_diff('2022-11-02', '2024-04-05','string')

# %% [markdown]
# Exercise 4
# 
# Please write a function called reverse that takes as its argument a list and returns a list of the arguments in reverse order (do not use any built-in sorting methods).
# 
# For example, reverse(['a', 'b', 'c']) should return
# 
# ['c', 'b', 'a']

# %%
def reverse(in_list: list) -> list:
    """
    A function that can reverse the order of the elements in the list.
    """
    reversed_list = []
    for i in range(len(in_list) - 1, -1, -1):
        reversed_list.append(in_list[i])
    return reversed_list

reverse(['T', 'E', 'N', 'E', 'T'])

# %% [markdown]
# Exercise 5
# 
# Write a function called prob_k_heads that takes as its arguments natural numbers n and k with n>k and returns the probability of getting k heads from n flips3.
# 
# For example, prob_k_heads(1,1) should return
# 
# .5

# %%
def prob_k_heads(n: int, k: int) -> float:
    """
    Calculate the probability of getting k heads from n coin flips
    Hint: n>k
    """
    def factorial(x):
        return 1 if x == 0 else x * factorial(x - 1)
    def binom_coeff(n, k):
        return factorial(n) // (factorial(k) * factorial(n-k))
    
    probability = binom_coeff(n, k) * (0.5 ** k) * (0.5 ** (n-k))

    return probability

prob_k_heads(1, 1)



