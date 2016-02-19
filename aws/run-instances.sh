#!/bin/bash

count=${1:-1}

aws ec2 run-instances \
    --image-id ami-cb2305a1 \
    --key-name ecs-default \
    --security-group-ids sg-9afde6e3 \
    --instance-type t2.small \
    --subnet-id subnet-3ab9824e \
    --iam-instance-profile Name=ecs-default-ec2-role \
    --count $count \
    --user-data file://user-data.sh
