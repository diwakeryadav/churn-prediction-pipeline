FROM python:3.11-slim
WORKDIR /app
COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV CHURN_MODEL_PATH=/app/models/artifacts/churn_model.pkl
CMD ["uvicorn","api.app:app","--host","0.0.0.0","--port","8000"]
