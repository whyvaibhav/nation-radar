FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory for persistence
RUN mkdir -p /app/data

# Run the scheduler by default
CMD ["python", "scheduler.py"]
