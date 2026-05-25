# Use an explicit, stable minimal footprint Python base
FROM python:3.10-slim

# Set working directory layers
WORKDIR /app

# Create an unprivileged system user for runtime execution security
RUN useradd -u 10001 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Copy application logic cleanly
COPY --chown=appuser:appuser app.py .

# Switch context entirely to the non-root execution layer
USER appuser

# Expose microservice networking parameters
EXPOSE 5000

# Explicit execution vector
CMD ["python", "-u", "app.py"]
