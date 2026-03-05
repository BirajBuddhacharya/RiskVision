FROM python:3.11-slim

# Prevents Python from writing pyc files and buffers stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /RiskVision

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

EXPOSE 5000 8501

# Default command (can be overridden by compose)
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]