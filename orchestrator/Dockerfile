FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy orchestrator code
COPY orchestrator/ .
COPY tools/ ./tools/

# Expose port
EXPOSE 8000

# Run service
CMD ["python", "main.py"]



