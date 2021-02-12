#!/bin/bash

# Create a Docker image
docker build -t gadi-spec:1.0 .
docker tag gadi-spec:1.0 gadi-spec:latest
