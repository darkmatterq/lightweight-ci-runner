#!/bin/bash
set -euo pipefail
APP_NAME="sample-app-live"
IMAGE_NAME="sample-app:latest"
if [ "$(docker ps -a -q -f name=^/${APP_NAME}$)" ]
then
    echo "Stopping existing container: ${APP_NAME}...."
    docker rm -f ${APP_NAME} >/dev/null 2>&1 || true
fi
echo " Starting new container: ${APP_NAME}"
docker run -d \
    --name ${APP_NAME} \
    -p 8080:8080 \
    --memory="128m" \
    --cpus="1.0" \
    --restart unless-stopped \
    ${IMAGE_NAME}
sleep 2
if curl -s -f http://localhost:8080/healthy >/dev/null 2>&1
then
    echo "Deployment SUCCESSFUL! Container ${APP_NAME} is healthy and running."
    exit 0
else
    echo "Deployment FAILED! Container ${APP_NAME} crashed on startup."
    exit 1  
fi


