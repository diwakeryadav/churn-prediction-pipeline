import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--out", default="data/features.parquet")
args = parser.parse_args()

df = pd.read_parquet(args.input)

# compute per-user aggregates
agg = df.groupby('user_id').agg(
    tx_count=('transaction_id','count'),
    tx_sum=('amount','sum'),
    tx_mean=('amount','mean'),
    last_ts=('timestamp','max')
).reset_index()


agg['last_ts'] = pd.to_datetime(agg['last_ts'], errors='coerce')

import numpy as np

last_vals = None
try:
    last_vals = agg['last_ts'].dt.tz_convert('UTC').values.astype('datetime64[ns]')
except Exception:
    try:
        last_vals = agg['last_ts'].dt.tz_localize(None).values.astype('datetime64[ns]')
    except Exception:
        last_vals = pd.to_datetime(agg['last_ts'].astype(str)).values.astype('datetime64[ns]')


now_np = np.datetime64(pd.Timestamp.utcnow().to_datetime64())
diff_days = (now_np - last_vals).astype('timedelta64[D]')

days_int = np.where(pd.isna(diff_days), 9999, diff_days.astype(int))

agg['days_since_last'] = days_int

labels = df.groupby('user_id').churn_label.max().reset_index()

out = agg.merge(labels, on='user_id', how='left')
out.to_parquet(args.out, index=False)
print('Wrote features to', args.out)