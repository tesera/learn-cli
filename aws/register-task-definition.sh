#!/bin/bash

aws ecs register-task-definition \
    --family learn \
    --cli-input-json file://task-definition.json
