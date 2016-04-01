#!/bin/bash

aws ecs run-task \
    --cluster learn \
    --task-definition learn \
    --overrides file://overrides-${1-varsel}.json \
    --started-by task:learn
