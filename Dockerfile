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

# Note: rasa/rasa:3.6.0 image already includes Rasa and all dependencies
# No need to install requirements.txt again

# Copy project files
COPY domain.yml config.yml endpoints.yml credentials.yml ./
COPY data ./data

# Train model during build (required for production)
RUN rasa train --out models

# Switch back to non-root user
USER 1001

# Expose port
EXPOSE 5005

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5005/ || exit 1

# Default command
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
