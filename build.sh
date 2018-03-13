#!/usr/bin/env bash

CONTAINER_IMAGE="sd2e/sbh_adapter:1.0"

docker build -t ${CONTAINER_IMAGE} .