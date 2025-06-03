# Build stage
FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set PATH to include uv
ENV PATH="/root/.local/bin:$PATH"

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app

# Remove any existing virtual environment.
ENV VIRTUAL_ENV="" 
RUN rm -rf .venv    # Remove any existing .venv directory

# Install the application dependencies using uv.
RUN uv sync --no-dev --python-preference=only-system


# Run the application.

# Run the FastAPI application using uv
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]