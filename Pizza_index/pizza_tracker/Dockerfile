# pizza_tracker/Dockerfile

FROM python:3.9-slim

# Install system dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium (works on ARM64)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the web assets
COPY ./web /app/web

# Copy the application code
COPY ./src /app/src

# Set environment variables
ENV CHROME_BINARY_LOCATION=/usr/bin/chromium
ENV CHROMEDRIVER_BINARY_LOCATION=/usr/bin/chromedriver

# Expose port
EXPOSE 8000

# Set the command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]