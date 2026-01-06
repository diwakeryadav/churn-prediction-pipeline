import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--out", default="data/staging_transactions.parquet")
args = parser.parse_args()

print("Loading", args.input)
df = pd.read_csv(args.input, parse_dates=["timestamp"])

df = df[df.amount >= 0]

ndf = df.copy()
ndf.to_parquet(args.out, index=False)
print("Wrote staging parquet to", args.out)
