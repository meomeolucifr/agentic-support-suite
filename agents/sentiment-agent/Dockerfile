FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY agents/sentiment-agent/ .
COPY tools/ ./tools/

# Expose port
EXPOSE 8003

# Run service
CMD ["python", "main.py"]



