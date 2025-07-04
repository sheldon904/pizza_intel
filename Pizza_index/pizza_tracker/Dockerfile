# pizza_tracker/Dockerfile

# Use a base image with Chrome pre-installed
FROM selenium/standalone-chrome:latest-amd64

# Switch to root user to install packages
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip

# Set the working directory
WORKDIR /app

# Copy the application code
COPY ./src /app/src
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch back to the default user
USER seluser

# Set the command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]