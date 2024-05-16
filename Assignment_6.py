# %% [markdown]
# # Problem Set 6

# %%
import numpy as np
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
import pandas as pd

# %%

path = 'auctions.db'
engine = create_engine(f'sqlite:///{path}')
def add_custom_functions(dbapi_connection, connection_record):
    dbapi_connection.create_function("sqrt", 1, np.sqrt)

event.listen(engine, 'connect', add_custom_functions)

Session = sessionmaker(bind=engine)

class DataBase:
    def __init__(self, engine):
        self.engine = engine

    def query(self, q: str) -> pd.DataFrame:
        """Execute a SQL query and return a pandas DataFrame."""
        with Session() as session:
            return pd.read_sql(q, session.bind)

auctions = DataBase(engine)


# %% [markdown]
# ## Exercise 0

# %%
def github(a, b, c) -> str:
    """
    A link to the solutions on GitHub.
    """
    user = a
    repo = b
    filename = c


    return "https://github.com/{user}/{repo}/blob/main/{filename}".format(user=user, repo=repo, filename=filename)

github("chengx0828", "UW-ECON481", "Assignment_6.py")

# %% [markdown]
# ## Exercise 1
# 
# Please write a function called std that takes no arguments and returns a string containing a SQL query that can be run against the auctions.db database that outputs a table that has two columns: itemId and std, the standard deviation of bids for that item. Include only bids for which the unbiased standard deviation can be calculated (that is, those with at least two bids). Calculate standard deviation as
# 
# <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
#   <mi>s</mi>
#   <mo>=</mo>
#   <mrow data-mjx-texclass="ORD">
#     <msqrt>
#       <mfrac>
#         <mrow>
#           <munderover>
#             <mo data-mjx-texclass="OP">&#x2211;</mo>
#             <mrow data-mjx-texclass="ORD">
#               <mi>i</mi>
#               <mo>=</mo>
#               <mn>1</mn>
#             </mrow>
#             <mrow data-mjx-texclass="ORD">
#               <mi>n</mi>
#             </mrow>
#           </munderover>
#           <mo stretchy="false">(</mo>
#           <msub>
#             <mi>x</mi>
#             <mrow data-mjx-texclass="ORD">
#               <mi>i</mi>
#             </mrow>
#           </msub>
#           <mo>&#x2212;</mo>
#           <mrow data-mjx-texclass="ORD">
#             <mover>
#               <mi>x</mi>
#               <mo accent="true">&#x2015;</mo>
#             </mover>
#           </mrow>
#           <msup>
#             <mo stretchy="false">)</mo>
#             <mrow data-mjx-texclass="ORD">
#               <mn>2</mn>
#             </mrow>
#           </msup>
#         </mrow>
#         <mrow>
#           <mi>n</mi>
#           <mo>&#x2212;</mo>
#           <mn>1</mn>
#         </mrow>
#       </mfrac>
#     </msqrt>
#   </mrow>
# </math>

# %%
def std():
    q1 = """
    SELECT Items.itemId,
        sqrt(SUM((Bids.bidAmount - Items.avgBid) * (Bids.bidAmount - Items.avgBid)) / (COUNT(Bids.bidAmount) - 1)) AS std_dev
    FROM Bids
    JOIN (
        SELECT itemId, AVG(bidAmount) AS avgBid
        FROM Bids
        GROUP BY itemId
        HAVING COUNT(bidAmount) > 1
    ) AS Items ON Bids.itemId = Items.itemId
    GROUP BY Items.itemId
    """
    return(auctions.query(q1))

std()

# %% [markdown]
# ## Exercise 2
# 
# Please write a function called bidder_spend_frac that takes no arguments and returns a string containing a SQL query that can be run against the auctions.db database that outputs a table that has four columns:
# 
# ###### bidderName: the name of the bidder
# ###### total_spend: the amount the bidder spent (that is, the sum of their winning bids)
# ###### total_bids: the amount the bidder bid, regardless of the outcome. NB: bidders may submit multiple bids for an item – if this is the case only count their highest bid for an item for this calculation.
# ###### spend_frac: total_spend/total_bids

# %%
def bidder_spend_frac() -> str:
    q2 = """
    SELECT 
        b.bidderName,
        COALESCE(SUM(CASE WHEN b.itemId = w.itemId THEN b.bidAmount ELSE 0 END), 0) AS total_spend,
        SUM(b.maxBid) AS total_bids,
        COALESCE(SUM(CASE WHEN b.itemId = w.itemId THEN b.bidAmount ELSE 0 END), 0) * 1.0 / SUM(b.maxBid) AS spend_frac
    FROM
        (SELECT bidderName, itemId, MAX(bidAmount) AS maxBid, bidAmount
         FROM Bids
         GROUP BY bidderName, itemId) b
    LEFT JOIN
        (SELECT itemId, MAX(bidAmount) AS maxWinningBid
         FROM Bids
         GROUP BY itemId) w ON b.maxBid = w.maxWinningBid AND b.itemId = w.itemId
    GROUP BY b.bidderName
    """
    return auctions.query(q2)

bidder_spend_frac()

# %% [markdown]
# ## Exercise 3
# 
# Please write a function called min_increment_freq that takes no arguments and returns a string containing a SQL query that can be run against the auctions.db database that outputs a table that has one column (freq) which represents the fraction of bids in the database that are exactly the minimum bid increment (items.bidIncrement) above the previous high bid. For this exercise, exclude items where isBuyNowUsed=1.

# %%
def min_increment_freq() -> str:
    q3 = """
    SELECT
        COUNT(*) FILTER (WHERE bidIncrementExact) * 1.0 / COUNT(*) AS freq
    FROM (
        SELECT
            Bids.itemId,
            Bids.bidAmount,
            LAG(Bids.bidAmount) OVER (PARTITION BY Bids.itemId ORDER BY Bids.bidAmount) AS prevBid,
            Items.bidIncrement,
            (Bids.bidAmount - LAG(Bids.bidAmount) OVER (PARTITION BY Bids.itemId ORDER BY Bids.bidAmount)) = Items.bidIncrement AS bidIncrementExact
        FROM 
            Bids
        JOIN 
            Items ON Bids.itemId = Items.itemId
        WHERE 
            Items.isBuyNowUsed = 0
    ) AS FilteredBids
    """
    return auctions.query(q3)

min_increment_freq()

# %% [markdown]
# ## Exercise 4
# 
# Please write a function called win_perc_by_timestamp that takes no arguments and returns a string containing a SQL query that can be run against the auctions.db database that outputs a table that has two columns:
# 
# timestamp_bin: Using the same methodology as in the slides to normalize the percentage of time remaining in the auction when a bid is placed, normalize the bid timestamp and classify it as one of ten bins: 1 corresponds to 0-.1, 2 corresponds to .1-.2, etc.
# 
# win_perc: the frequency with which a bid placed with this timestamp bin won the auction.

# %%
def win_perc_by_timestamp() -> str:
    query = """
    WITH AuctionTimes AS (
        SELECT
            itemId,
            MIN(bidTime) AS startTime,
            MAX(bidTime) AS endTime
        FROM bids
        GROUP BY itemId
    ),
    NormalizedBids AS (
        SELECT
            b.itemId,
            b.bidAmount,
            CAST(10 * (1 - (julianday(b.bidTime) - julianday(t.startTime)) / (julianday(t.endTime) - julianday(t.startTime))) AS INTEGER) + 1 AS timestamp_bin
        FROM bids b
        JOIN AuctionTimes t ON b.itemId = t.itemId
    ),
    WinningBids AS (
        SELECT
            itemId,
            MAX(bidAmount) AS winningBid
        FROM bids
        GROUP BY itemId
    )
    SELECT
        n.timestamp_bin,
        ROUND(100.0 * SUM(CASE WHEN n.bidAmount = w.winningBid THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_perc
    FROM NormalizedBids n
    JOIN WinningBids w ON n.itemId = w.itemId
    WHERE n.timestamp_bin BETWEEN 1 AND 10
    GROUP BY n.timestamp_bin
    ORDER BY n.timestamp_bin
    """
    return auctions.query(query)

win_perc_by_timestamp()


