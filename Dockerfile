# Use the official Python image.
FROM python:3.11-slim

# Set environment variables
ENV DD_SERVICE="my-service"
ENV DD_ENV="staging"
ENV DD_AGENT_HOST="datadog-agent"

# Install required packages
RUN pip install openai datadog ddtrace

# Copy the script into the container
COPY client.py /app/client.py

# Set the working directory
WORKDIR /app

# Run the script with ddtrace-run
CMD ["ddtrace-run", "python", "client.py"]
