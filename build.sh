#!/usr/bin/env bash

EXERCISE_ID=f3369972-d63a-4a22-a652-ca221dc1e47a

docker build --no-cache --label=pytm.exercise="$EXERCISE_ID" -t $EXERCISE_ID .
docker stop $EXERCISE_ID && docker rm $EXERCISE_ID
docker run -p 8000:8080 -d --name $EXERCISE_ID $EXERCISE_ID:latest
