#BUILD STAGE
FROM python:3.13-slim-bookworm AS builder

#COPY UV binanary from offical image 
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

WORKDIR /app

#UV Docker optimizations

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy 
ENV UV_PYTHON_DOWNLOADS=0

#Install dependencies first  (cache if unchanged)

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

#COPY app code and install project 
COPY . ./
RUN uv sync --locked --no-dev

# PRODUCTION STAGE
FROM python:3.13-slim-bookworm 

WORKDIR /app

# RUN as non-root user for security 
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# COPY app and dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /app /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python" , "main.py"]