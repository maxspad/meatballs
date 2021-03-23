#!/bin/bash

docker build --no-cache -t imax32/mb \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) .