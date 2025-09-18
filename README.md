# medleys-love-notes-automation

Services to automate Medleys A Cappella's Love Notes.

## Setup

This assumes you have [Git](https://git-scm.com/downloads),
[Visual Studio Code](https://code.visualstudio.com/Download) and
[Docker](https://docs.docker.com/desktop/) installed.

<!-- prettier-ignore-start -->
> [!NOTE]
> The hyperlinked URLs are not necessarily what should be used.
<!-- prettier-ignore-end -->

First, clone the repository. Either run the following as a script and open in VS
Code, or open directly in VS Code with `Git: Clone`.

```sh
# cd into a development directory
git clone https://github.com/wu-warren/medleys-love-notes-automation.git
cd medleys-love-notes-automation
```

Then, either locally setup your environment, or use the provided dev container.

| Local                                                            | Dev Container                                                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1. Run this setup script: `./devcontainer/post-create`           | 1. Install the Remote Development extension pack. (`@id:ms-vscode-remote.vscode-remote-extensionpack`) |
| 2. Activate the virtual environment: `source .venv/bin/activate` | 2. When prompted, reopen in a dev container, or use `Dev Containers: Rebuild and Reopen in Container`. |

Optionally, install VS Code extensions. The dev container does this
automatically; if you are not using the dev container, see
`.devcontainer/devcontainer.json` for the recommended extensions.

Finally, open an integrated terminal in VS Code. When you run `which pip`, it
should end with something like `.venv/bin/pip`. If not, close and reopen the
integrated terminal.

## How to Update the Development Environment

<!-- prettier-ignore-start -->

- Runtime dependency: update `requirements.txt`
- Development tool dependency: if it is a Python package, update
  `requirements-dev.txt`; otherwise, update `.devcontainer/Dockerfile`
- Add new secret: `detect-secrets scan > .secrets.baseline` <!-- pragma: allowlist secret -->

<!-- prettier-ignore-end -->
