#!/bin/bash
set -euo pipefail
echo "Cleaning up dangling images and stopped containers"

docker container prune -f >/dev/null 2>&1 ||true

docker image prune -f >/dev/null 2>&1 ||true


echo "[CLEANUP] Docker resources cleaned successfully"


