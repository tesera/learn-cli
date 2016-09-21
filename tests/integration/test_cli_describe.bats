#!/usr/bin/env bats

setup () {

    data_xy="data_xy.csv"
    input="./tests/integration/input"
    output_dir="./tests/integration/output"

    mkdir -p "$output_dir"
}

@test "describe runs and output expected files without optional args" {
    run learn describe \
        --xy-data=$input/$data_xy \
        --output=$output_dir

    [ -f "$output_dir/describe.json" ]
    [ -f "pylearn.log" ]
}

@test "describe runs and output expected files with json and quartile" {
    run learn describe \
        --xy-data=$input/$data_xy \
        --output=$output_dir \
        --format=json \
        --quantile-type=quartile

    [ -f "$output_dir/describe.json" ]
    [ -f "pylearn.log" ]
}

@test "describe runs and output expected files with csv and decile" {
    run learn describe \
        --xy-data=$input/$data_xy \
        --output=$output_dir \
        --format=csv \
        --quantile-type=decile

    [ -f "$output_dir/describe.csv" ]
    [ -f "pylearn.log" ]
}

teardown () {
    rm $output_dir/*
    rm *.log
}
