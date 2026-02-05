# ============================================
# WhoseOnFirst - Production Docker Image
# ============================================
# Multi-stage build for efficient container size
# Target: RHEL 10 / Kubernetes / Podman compatible
# Base: Red Hat UBI9 with Python 3.12
# Version: 1.1.0
# ============================================

# ============================================
# Stage 1: Builder
# ============================================
FROM registry.access.redhat.com/ubi9/python-312 AS builder

# Set working directory
WORKDIR /app

# Switch to root for package installation (UBI9 runs as non-root by default)
USER 0

# Note: UBI9 Python image already includes gcc, gcc-c++, libffi-devel
# No additional build packages needed

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies to UBI9's site-packages location
# UBI9 Python uses /opt/app-root for packages, not /usr/local
RUN pip install --no-cache-dir --target=/install/site-packages -r requirements.txt

# Switch back to non-root user (satisfies security scanners)
USER 1001

# ============================================
# Stage 2: Runtime
# ============================================
FROM registry.access.redhat.com/ubi9/python-312

# Set working directory
WORKDIR /app

# Note: UBI9 already includes curl-minimal which provides the curl command
# No additional runtime packages needed

# Switch to root for setup (UBI9 runs as non-root user 1001 by default)
USER 0

# Copy installed Python packages from builder stage to UBI9's site-packages
COPY --from=builder /install/site-packages /opt/app-root/lib/python3.12/site-packages

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
# Note: Using python -m for cross-platform compatibility with UBI9
# In production, you may want to run migrations separately
CMD ["sh", "-c", "python -m alembic upgrade head && python -m uvicorn src.main:app --host 0.0.0.0 --port 8000"]
