FROM python:3.11-slim

WORKDIR /app

# No need for system packages – all dependencies are pure Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]