#!/usr/bin/env bats

setup () {

    data_xy="data_xy.csv"
    data_x_filtered="data_xy.csv"
    lda_x_dfunct="lda_x_dfunct.csv"
    data_idf="data_idf.csv"
    input="./tests/integration/input"
    output="./tests/integration/output"

    mkdir -p "$output"

    learn discrat \
        --xy-data=$input/$data_xy \
        --x-data=$input/$data_x_filtered \
        --dfunct=$input/$lda_x_dfunct \
        --idf=$input/$data_idf \
        --varset=10 \
        --output=$output
}

@test "discrat runs and output expected files" {
    [ -f "$output/forecasts.csv" ]
    [ -f "pylearn.log" ]
}

teardown () {
    rm $output/*
    rm *.log
}
