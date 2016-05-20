#!/usr/bin/env bats

setup () {

    data_xy="data_xy.csv"
    input="./tests/integration/input"
    output="./tests/integration/output"

    mkdir -p "$output"

    learn describe \
        --xy-data=$input/$data_xy \
        --output=$output
}

@test "discrat runs and output expected files" {
    [ -f "$output/describe.json" ]
    [ -f "pylearn.log" ]
}

teardown () {
    rm $output/*
    rm *.log
}
