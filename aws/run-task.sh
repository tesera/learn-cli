#!/bin/bash

aws ecs run-task \
    --cluster learn \
    --task-definition learn \
    --overrides file://overrides.json \
    --started-by task:learn
