FROM mcr.microsoft.com/devcontainers/python:3.13

# Create workspace
USER root
RUN mkdir -p /home/vscode/workspace && chown -R vscode:vscode /home/vscode/workspace
COPY .bashrc /tmp/custom_bashrc
RUN if [ -f /home/vscode/.bashrc ]; then \
        cat /tmp/custom_bashrc >> /home/vscode/.bashrc; \
    else \
        mv /tmp/custom_bashrc /home/vscode/.bashrc; \
    fi && \
    chown vscode:vscode /home/vscode/.bashrc && rm -f /tmp/custom_bashrc

# Switch to vscode user
USER vscode
WORKDIR /home/vscode/workspace

# Copy project files (for installation)
COPY pyproject.toml requirements.txt requirements-dev.txt ./
COPY src ./src

# Install dependencies (main and dev)
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

EXPOSE 8080
