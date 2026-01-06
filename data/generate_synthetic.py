#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=10000)
parser.add_argument("--out", type=str, default="data/sample_transactions.csv")
args = parser.parse_args()

np.random.seed(42)

n = args.n
now = datetime.utcnow()

users = [f"user_{i}" for i in np.random.randint(0, max(1,n//3), size=n)]
merchants = [f"m_{i}" for i in np.random.randint(0, 200, size=n)]
amounts = np.round(np.random.exponential(scale=100.0, size=n), 2)
statuses = np.random.choice(["success","failed"], size=n, p=[0.95,0.05])
pm = np.random.choice(["card","upi","wallet"], size=n, p=[0.6,0.3,0.1])

dates = [now - timedelta(seconds=int(x)) for x in np.random.randint(0, 60*60*24*90, size=n)]

df = pd.DataFrame({
    "transaction_id": [f"tx_{i}" for i in range(n)],
    "user_id": users,
    "merchant_id": merchants,
    "amount": amounts,
    "status": statuses,
    "payment_method": pm,
    "timestamp": dates
})

# create a simple churn label: users with fewer than 2 transactions in last 30 days are churned
recent_cutoff = now - timedelta(days=30)
df_recent = df[df["timestamp"] >= recent_cutoff]
counts = df_recent.groupby("user_id").size()
churned_users = set(counts[counts < 2].index.tolist())

# assign churn per-transaction as 1 if that user is churned overall
df["churn_label"] = df["user_id"].apply(lambda u: 1 if u in churned_users else 0)

# save
df.to_csv(args.out, index=False)
print(f"Wrote {len(df)} rows to {args.out}")
