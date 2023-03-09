#!/usr/bin/env bash

EXERCISE_ID=7048492d-e454-489e-bf73-fead60ee1ad0

docker build --no-cache --label=pytm.exercise="$EXERCISE_ID" -t $EXERCISE_ID .
docker stop $EXERCISE_ID && docker rm $EXERCISE_ID
docker run -p 8000:8080 -d --name $EXERCISE_ID $EXERCISE_ID:latest
