#!/bin/bash

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker pull $Product_images:$Product_tag
docker run -p 8000:8000 --rm -it $Product_images:$Product_tag