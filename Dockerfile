# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads outputs

# Expose ports
EXPOSE 5000 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create startup script
RUN echo '#!/bin/bash\n\
python app.py &\n\
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]
