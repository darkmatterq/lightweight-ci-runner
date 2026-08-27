#!/bin/bash
set -euo pipefail 
for tool in docker python3 pip g++ make
do
    if ! command -v "$tool" >/dev/null 2>&1
    then
        echo "Error: $tool is not installed. Please install $tool first."
        exit 1
    else
        echo "$tool is installed"
    fi
done
if ! docker info >/dev/null 2>&1
then 
    echo "Docker error or not turn"
fi
make venv
make install-deps
make build
for file in scripts/pre-push scripts/deploy.sh scripts/cleanup.sh bin/ci-monitor
do
    chmod +x $file
    echo "$file has permission"
done
if [ -d ".git" ]
then
    cp scripts/pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push
fi
    PROJECT_DIR=$(pwd)
    CURRENT_USER=$(whoami)
    PYTHON_PATH=$(which python3)
    sed -e "s|{{PROJECT_DIR}}|${PROJECT_DIR}|g"\
        -e "s|{{USER}}|${CURRENT_USER}|g"\
        -e "s|{{PYTHON_PATH}}|${PYTHON_PATH}|g"\
        systemd/lightweight-ci.service |sudo tee /etc/systemd/system/lightweight-ci.service > /dev/null 
    sudo systemctl daemon-reload


