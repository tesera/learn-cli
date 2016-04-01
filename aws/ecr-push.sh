#!/bin/bash

#usage: export GITHUB_TOKEN=<my-gh-personal-access-token>; bash ./ecr-push.sh

docker build --build-arg GITHUB_TOKEN=$GITHUB_TOKEN -t tesera/learn .
docker tag -f tesera/learn:latest 674223647607.dkr.ecr.us-east-1.amazonaws.com/tesera/learn:latest
aws ecr get-login --region us-east-1 | bash
docker push 674223647607.dkr.ecr.us-east-1.amazonaws.com/tesera/learn:latest
