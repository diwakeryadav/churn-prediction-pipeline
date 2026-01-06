from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.bash import BashOperator

# In Docker containers, the repo is mounted at /opt/airflow
# In local dev, this resolves to the project root
PROJECT_DIR = os.getenv('AIRFLOW_PROJECT_DIR', '/opt/airflow')

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='pipeline',
    default_args=default_args,
    description='Run ETL -> features -> train -> serve pipeline',
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['example','pipeline'],
) as dag:

    generate_data = BashOperator(
        task_id='generate_synthetic',
        bash_command=(
            f'python {PROJECT_DIR}/data/generate_synthetic.py '
            f'--n 10000 --out {PROJECT_DIR}/data/sample_transactions.csv'
        ),
    )

    run_etl = BashOperator(
        task_id='run_etl',
        bash_command=(
            f'python {PROJECT_DIR}/etl/load_raw.py '
            f'--input {PROJECT_DIR}/data/sample_transactions.csv '
            f'--out {PROJECT_DIR}/data/staging_transactions.parquet'
        ),
    )

    build_features = BashOperator(
        task_id='build_features',
        bash_command=(
            f'python {PROJECT_DIR}/features/build_features.py '
            f'--input {PROJECT_DIR}/data/staging_transactions.parquet '
            f'--out {PROJECT_DIR}/data/features.parquet'
        ),
    )

    train_model = BashOperator(
        task_id='train_model',
        bash_command=(
            f'python {PROJECT_DIR}/models/churn/train.py '
            f'--features {PROJECT_DIR}/data/features.parquet '
            f'--out {PROJECT_DIR}/models/artifacts/churn_model.pkl'
        ),
    )

    notify = BashOperator(
        task_id='notify_done',
        bash_command=(
            f'echo "Pipeline finished at $(date)" && touch {PROJECT_DIR}/.pipeline_last_run'
        ),
    )

    generate_data >> run_etl >> build_features >> train_model >> notify
