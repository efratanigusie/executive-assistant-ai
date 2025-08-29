# Cloud Run compatible Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps (for Google auth)
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose Cloud Run port
ENV PORT=8080
CMD ["gunicorn", "-b", ":8080", "app:app"]
