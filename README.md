# Razorpay Analytics Cloud — Starter Scaffold

This repository scaffold contains a **drop-in, runnable local prototype** of the Razorpay-style AI-Powered Business Intelligence Platform. It includes:

- Synthetic data generator
- Minimal ETL loader
- Feature builder stub
- Simple churn model training script (RandomForest)
- FastAPI model-serving skeleton
- Dockerfiles and docker-compose to run everything locally
- README with step-by-step local run instructions

> **Goal for today:** get an end-to-end *local* demo running: generate data → ETL → train a simple model → serve predictions via API → view the API health. Dashboard is scaffolded as a placeholder (instructions included) so you can add UI quickly.

## Quick local run (what we will do)

1. Create Python venv and install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r api/requirements.txt`
2. Generate synthetic data: `python data/generate_synthetic.py --n 10000 --out data/sample_transactions.csv`
3. Run ETL loader: `python etl/load_raw.py --input data/sample_transactions.csv --out data/staging_transactions.parquet`
4. Build features: `python features/build_features.py --input data/staging_transactions.parquet --out data/features.parquet`
5. Train churn model: `python models/churn/train.py --features data/features.parquet --out models/artifacts/churn_model.pkl`
6. Start API: `uvicorn api.app:app --reload --host 0.0.0.0 --port 8000`
7. Test: `curl http://localhost:8000/health` and `curl -X POST http://localhost:8000/predict/churn -H 'Content-Type: application/json' -d '{"features": [10, 2, 500.0, 7]}'`

## Repo structure

```
razorpay-analytics-cloud/
├─ README.md
├─ data/
├─ etl/
├─ features/
├─ models/
├─ api/
├─ docker-compose.yml
└─ .env.example
```
