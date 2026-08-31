# 🚀 Lightweight GitOps CI/CD Pipeline & Build Engine

[![Linux](https://img.shields.io/badge/Platform-Linux-FCC624?logo=linux&logoColor=black)](https://www.linux.org/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![C++17](https://img.shields.io/badge/C++-17-00599C?logo=c%2B%2B&logoColor=white)](https://isocpp.org/)
[![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?logo=gnu-bash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Cgroups v2](https://img.shields.io/badge/Kernel-Cgroups%20v2-blue)](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, self-hosted **GitOps CI/CD Runner Engine** and **Containerized Build Platform** built from scratch. Engineered for Linux environments, combining Python workflow orchestration, strict POSIX Bash automation, ephemeral Docker container isolation, and real-time Kernel Cgroups v2 resource telemetry in C++17.

---

## 🎯 Architectural Overview

```mermaid
graph TD
    subgraph Tier 1: Local Code Hygiene (Pre-Commit)
        Dev1["👨‍💻 Developer: git commit"] --> Hook1["🪝 scripts/pre-commit\n(Flake8 Linting + YAML Schema Check in <0.1s)"]
        Hook1 --> Hook2["📝 scripts/commit-msg\n(Conventional Commits Enforcement: feat:, fix:, ...)"]
    end

    subgraph Tier 2: Pre-Push Gatekeeper (GitOps Pipeline)
        Hook2 -->|git push| Hook3["🛡️ scripts/pre-push (Automated CI Trigger)"]
        Hook3 --> Engine["⚙️ Python CI Engine (src/engine.py)"]
        Engine --> Parser["📄 Validate .ci-pipeline.yaml (src/parser.py)"]
        Parser --> Stages["🐳 Ephemeral Docker Stages (lint ➔ test ➔ build)"]
    end

    subgraph Tier 3: Kernel Telemetry & CD Operations
        Stages -->|Container ID| Monitor["⚡ C++ Monitor Sidecar (src/monitor.cpp)"]
        Monitor -->|Real-time I/O| Cgroup["📊 Linux Cgroups v2 (/sys/fs/cgroup)"]
        Stages -->|All Stages Passed ✅| Deploy["🚀 scripts/deploy.sh (Healthchecked Rollout)"]
        Deploy --> Cleanup["🧹 scripts/cleanup.sh (Docker Prune GC)"]
        Stages -->|Any Stage Failed ❌| Abort["🛑 Abort Push (Zero Broken Code Upstream)"]
    end
```

---

## ✨ Key Technical Highlights

### 1. Three-Tier Shift-Left GitOps Defense
* **`scripts/pre-commit` (Instant Code Hygiene):** Fast static analysis (`flake8`) and YAML syntax verification executing in $< 0.1s$ before commit creation.
* **`scripts/commit-msg` (Standardization):** Enforces industry-standard [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`, etc.).
* **`scripts/pre-push` (Full CI/CD Verification):** Executes the entire containerized pipeline before code leaves the local machine.

### 2. Isolated Containerized Execution Engine (`src/engine.py`)
* Parses declarative YAML pipeline definitions with strict schema validation.
* Spawns ephemeral, clean-room Docker containers with volume workspace mounting (`/workspace`) and `network_mode='host'` for reliable package resolution.
* Fail-fast execution with ANSI-colored streaming logs and automatic container teardown in `finally` blocks.

### 3. Kernel Cgroups v2 Sidecar Profiler (`src/monitor.cpp`)
* Direct inspection of Linux Cgroups v2 hierarchy (`/sys/fs/cgroup/system.slice/docker-<ID>.scope`).
* Reads `memory.current` and calculates differential CPU usage ($\Delta \text{CPU usec} / \Delta t$) with near-zero observer overhead ($0\%$ CPU).
* Spawns asynchronously via `subprocess.Popen` and handles graceful termination (`SIGTERM`/`SIGINT`).

### 4. Automated CD & Self-Healing Deployment (`scripts/deploy.sh`)
* Performs atomic zero-downtime container rollout (`sample-app-live`).
* Inspects container health status (`docker inspect --format '{{.State.Running}}'`) after startup.
* Automated garbage collection (`scripts/cleanup.sh`) removing dangling images and cache artifacts.

### 5. Linux Daemonization (`systemd/lightweight-ci.service`)
* Managed via Linux Systemd with auto-restart resilience (`Restart=always`, `RestartSec=5s`).
* Dynamic user and directory templating for portable 24/7 background execution on dedicated CI servers.

---

## 📂 Project Structure

```text
lightweight-ci-runner/
├── bin/                          # Compiled C++ binaries (ci-monitor)
├── src/                          # Core source code
│   ├── parser.py                 # [Python] YAML configuration validator
│   ├── engine.py                 # [Python] Docker pipeline orchestrator & sidecar manager
│   └── monitor.cpp               # [C++17] Linux Cgroups v2 resource profiler
├── scripts/                      # GitOps & Automation scripts
│   ├── pre-commit                # [Bash] Fast local syntax & YAML linter hook
│   ├── commit-msg                # [Bash] Conventional Commits validator hook
│   ├── pre-push                  # [Bash] Local CI pipeline execution & auto-deploy trigger
│   ├── deploy.sh                 # [Bash] Safe container deployment with healthcheck
│   └── cleanup.sh                # [Bash] Docker garbage collector (dangling images/containers)
├── systemd/
│   └── lightweight-ci.service    # Linux systemd service unit template
├── sample-app/                   # Reference application
│   ├── app.py                    # Application logic
│   ├── test_app.py               # Unit tests (pytest)
│   ├── Dockerfile                # Production container specification
│   └── .ci-pipeline.yaml         # Declarative 3-stage CI pipeline configuration
├── install.sh                    # 1-Click Zero-Configuration installer & hook setup
├── Makefile                      # Standard build, test, lint, and run workflow
├── requirements.txt              # Isolated Python dependencies
└── README.md                     # Technical architecture documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites
* Linux OS (Ubuntu 22.04+, Debian 12+, Fedora, Arch Linux)
* Docker Engine (`docker`)
* Python 3.10+
* `g++` (C++17 support) & `make`

### 2. 1-Click Automated Setup
Clone the repository and run the setup script:

```bash
git clone https://github.com/your-username/lightweight-ci-runner.git
cd lightweight-ci-runner
chmod +x install.sh
./install.sh
```

**What the installer does automatically:**
1. Validates system dependencies (`docker`, `python3`, `g++`, `make`).
2. Creates an isolated Python virtual environment (`.venv/`) and installs dependencies.
3. Compiles the high-performance C++ monitor binary (`bin/ci-monitor`).
4. Configures executable permissions across all scripts.
5. Installs all 3 Git Hooks (`pre-commit`, `commit-msg`, `pre-push`) into `.git/hooks/`.
6. Generates and registers the `systemd` service unit for 24/7 background execution.

---

## 🧪 Usage & Makefile Commands

| Command | Description |
| :--- | :--- |
| `make run` | **Run the full CI/CD pipeline end-to-end** |
| `make test` | Run unit tests using `pytest` |
| `make lint` | Check Python code style using `flake8` |
| `make build` | Compile the C++ Cgroups v2 monitor binary |
| `make clean` | Remove build binaries, `.pyc`, and `__pycache__` across all subdirectories |
| `make clean-docker` | Clean up dangling Docker images and stopped containers |
| `make clean-all` | Deep clean everything including `.venv` |
| `make help` | Display available targets and descriptions |

---

## ⚙️ Declarative Pipeline Specification (`.ci-pipeline.yaml`)

```yaml
name: Sample App Pipeline

stages:
  - lint
  - test
  - build

lint:
  stage: lint
  image: python:3.12-slim
  timeout: 30
  commands: 
    - pip install flake8
    - flake8 sample-app/

test:
  stage: test
  image: python:3.12-slim
  timeout: 60
  commands:
    - pip install pytest
    - pytest -o cache_dir=/tmp/.pytest_cache sample-app/test_app.py

build:
  stage: build
  image: docker:cli
  timeout: 60
  commands:
    - docker build -t sample-app:latest sample-app/
```

---

## 🖥️ Standalone C++ Cgroups v2 Profiler

You can run the C++ monitor directly against any active Docker container:

```bash
# 1. Start any test container
docker run -d --name test-box alpine sh -c "while true; do :; done"

# 2. Monitor resource usage in real-time (interval: 500ms)
./bin/ci-monitor $(docker inspect --format '{{.Id}}' test-box) 500

# 3. Teardown
docker rm -f test-box
```

---

## 🛡️ Production Systemd Service

To run the CI Runner as a resilient background daemon on a shared build server:

```bash
# Start the background service
sudo systemctl start lightweight-ci

# Check live service status
sudo systemctl status lightweight-ci

# Stream live runner logs
journalctl -u lightweight-ci -f

# Stop the service
sudo systemctl stop lightweight-ci
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
