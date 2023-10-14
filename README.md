# slackpi

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/github/Yoshida24/slackpi)

Preset for development on Python using venv.

**included:**
- Lint and Format
- Task runner
- Env support

## Usage

Depends on:
- Python: 3.11.2
- pip: 22.3.1
- GNU Make: 3.81

Supported Device and OS:
- Raspberry Pi OS (Raspbian GNU/Linux 12 bookworm 32bit on Raspberry Pi Zero W ver1)
- M1 Macbook Air Ventura 13.4.1

## Gettig Started
First of all, install VSCode recommended extensions. This includes Linter, Formatter, and so on. Recommendation settings is written on `.vscode/extensions.json`.

Then, install dependencies:

```bash
make setup
```

Then setup `.env` , and `./key` .

Now you can run script:

```bash
make run
```

> **Note**
This project *does not* depends on `dotenv-python`. Instead, using below script.
> `set -a && . ./.env && set +a`

## Develop App
On usual develop, first you activate `venv` first like below.

```bash
. .venv/bin/activate
```

Save requirements:

```bash
pip freeze > requirements.txt
```

Deactivate venv:

```bash
deactivate
```
