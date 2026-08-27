#!/bin/bash
set -euo pipefail
APP_NAME="sample-app-live"
IMAGE_NAME="sample-app:latest"
if [ "$(docker ps -q -f name=^/${APP_NAME}$)" ]
then
    echo "Stopping existing container: ${APP_NAME}...."
    docker stop ${APP_NAME}
    docker rm ${APP_NAME}
fi
echo " Starting new container: ${APP_NAME}"
docker run -d \
    --name ${APP_NAME} \
    --restart unless-stopped \
    ${IMAGE_NAME}
sleep 2
if [ "$(docker inspect -f '{{.State.Running}}'${APP_NAME})" = "true" ]
then
    echo "Deployment SUCCESSFUL! Container ${APP_NAME} is healthy and running."
    exit 0
else
    echo "Deployment FAILED! Container ${APP_NAME} crashed on startup."
    exit 1  
fi


