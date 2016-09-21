#!/usr/bin/env bats

setup () {
    data_xy="data_xy.csv"
    data_x_filtered="data_xy.csv"
    lda_x_dfunct="lda_x_dfunct.csv"
    data_idf="data_idf.csv"
    input="./tests/integration/input"
    output_dir="./tests/integration/output"

    mkdir -p "$output_dir"
}

@test "discrat runs and output expected files" {
    run learn discrat \
        --xy-data=$input/$data_xy \
        --x-data=$input/$data_x_filtered \
        --dfunct=$input/$lda_x_dfunct \
        --idf=$input/$data_idf \
        --varset=10 \
        --output=$output_dir

    [ -f "$output_dir/forecasts.csv" ]
    [ -f "pylearn.log" ]
}

@test "discrat doesn't run if varset missing" {
    run learn discrat \
        --xy-data=$input/$data_xy \
        --x-data=$input/$data_x_filtered \
        --dfunct=$input/$lda_x_dfunct \
        --idf=$input/$data_idf \
        --varset=100 \
        --output=$output_dir

    [ "$output" = "varset '100' missing from dfunct" ]
    [ "$status" -eq 1 ]
}

teardown () {
    rm -f $output_dir/*
}
