# ============================================
# WhoseOnFirst - Production Docker Image
# ============================================
# Multi-stage build for efficient container size
# Target: RHEL 10 / Podman compatible
# Version: 1.0.0
# ============================================

# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies to a local directory
# This allows us to copy only the installed packages to the final image
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Create non-root user for security
RUN groupadd -r whoseonfirst && useradd -r -g whoseonfirst whoseonfirst

# Create directories with proper permissions
RUN mkdir -p /app/data /app/frontend /app/src /app/alembic && \
    chown -R whoseonfirst:whoseonfirst /app

# Copy application code
COPY --chown=whoseonfirst:whoseonfirst src/ /app/src/
COPY --chown=whoseonfirst:whoseonfirst frontend/ /app/frontend/
COPY --chown=whoseonfirst:whoseonfirst alembic/ /app/alembic/
COPY --chown=whoseonfirst:whoseonfirst alembic.ini /app/

# Switch to non-root user
USER whoseonfirst

# Environment variables (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL=sqlite:///./data/whoseonfirst.db \
    HOST=0.0.0.0 \
    PORT=8000 \
    LOG_LEVEL=INFO

# Expose port
EXPOSE 8000

# Health check using the built-in /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Volume for persistent data (SQLite database)
VOLUME ["/app/data"]

# Run database migrations and start the application
# Note: In production, you may want to run migrations separately
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
