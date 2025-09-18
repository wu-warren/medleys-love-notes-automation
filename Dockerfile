FROM python:3.13-slim

WORKDIR /app
COPY pyproject.toml requirements.txt README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .
EXPOSE 8080

ENTRYPOINT ["mlna-cli"]
CMD ["--host", "0.0.0.0", "--port", "8080"]
