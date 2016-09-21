#!/usr/bin/env bats

setup () {

    data_xy="data_xy.csv"
    input="./tests/integration/input"
    output_dir="./tests/integration/output"

    mkdir -p "$output_dir"

    learn describe \
        --xy-data=$input/$data_xy \
        --output=$output_dir
}

@test "describe runs and output expected files" {
    [ -f "$output_dir/describe.json" ]
    [ -f "pylearn.log" ]
}

teardown () {
    rm $output_dir/*
    rm *.log
}
