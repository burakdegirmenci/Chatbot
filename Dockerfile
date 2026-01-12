# Rasa Chatbot Dockerfile - Production Optimized
FROM rasa/rasa:3.6.0

# Set production environment
ENV PYTHONUNBUFFERED=1
ENV RASA_HOME=/app

# Working directory
WORKDIR /app

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY domain.yml config.yml endpoints.yml credentials.yml ./
COPY data ./data

# Train model (uncomment for auto-training during build)
# RUN rasa train --out models

# Switch back to non-root user
USER 1001

# Expose port
EXPOSE 5005

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5005/ || exit 1

# Default command
CMD ["run", "--enable-api", "--cors", "*", "--port", "5005"]
