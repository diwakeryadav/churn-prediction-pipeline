import argparse
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

parser = argparse.ArgumentParser()
parser.add_argument("--features", required=True)
parser.add_argument("--out", default="models/artifacts/churn_model.pkl")
args = parser.parse_args()

df = pd.read_parquet(args.features)

X = df[['tx_count','tx_sum','tx_mean','days_since_last']].fillna(0)
y = df['churn_label'].fillna(0)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X_train, y_train)

proba = clf.predict_proba(X_val)[:,1]
print('AUC', roc_auc_score(y_val, proba))

Path = args.out
# ensure directory exists
import os
os.makedirs(os.path.dirname(Path), exist_ok=True)
joblib.dump(clf, Path)
print('Saved model to', args.out)
