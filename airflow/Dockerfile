FROM apache/airflow:2.8.1-python3.10

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy requirements and install Python dependencies
COPY --chown=airflow:root api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install Airflow extras (if needed)
RUN pip install --no-cache-dir \
    apache-airflow-providers-postgres \
    apache-airflow-providers-http
