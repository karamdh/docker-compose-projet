FROM python:3.12-slim

WORKDIR /app
COPY backend/etc/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src ./src
WORKDIR /app/src
CMD ["python", "app.py"]
