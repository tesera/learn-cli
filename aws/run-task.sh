#!/bin/bash

aws ecs run-task \
    --cluster varselect \
    --task-definition varselect \
    --overrides file://overrides.json \
    --started-by yr:varselect
