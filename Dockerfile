# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file and install libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ src/

# Create input and output directories to ensure they exist for volume mapping
RUN mkdir -p input output

# Command to run the pipeline
CMD ["python", "src/main.py"]
