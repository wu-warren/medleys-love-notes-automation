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
EXPOSE 8080
