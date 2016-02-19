#!/bin/bash

aws ecs register-task-definition \
    --family varselect \
    --cli-input-json file://task-definition.json
