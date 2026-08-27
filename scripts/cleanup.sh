#!/bin/bash
set -euo pipefail
echo "Cleaning up dangling images and stopped containers"

docker container prune -f 

docker image prune -f 

rm -rf .pytest_cache/ sample-app/.pytest_cache/

echo "[CLEANUP] Cleanup completed successfully"


