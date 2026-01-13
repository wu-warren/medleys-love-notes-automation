FROM python:3.13-slim

WORKDIR /app

# Install dependencies first for better caching
COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir -e .

ENV PORT=8080
EXPOSE 8080

# Run your CLI module (adjust if your package entrypoint differs)
CMD ["python", "-m", "mlna.cli", "--host", "0.0.0.0", "--port", "8080"]
