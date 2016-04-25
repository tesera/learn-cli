#!/usr/bin/env bats

setup () {

    data_xy="data_xy.csv"
    vsel_x="vsel_x.csv"
    input="./tests/integration/input"
    output="./tests/integration/output"

    mkdir -p "$output"

    learn lda \
        --xy-data "$input/$data_xy" \
        --config "$input/$vsel_x" \
        --yvar VAR47 \
        --output "$output"

}

@test "lda runs and output expected files" {
    [ -f "$output/lda_x_assess.csv" ]
    [ -f "$output/lda_x_dfunct.csv" ]
    [ -f "pylearn.log" ]
    [ -f "rlearn.log" ]
}

teardown () {
    rm $output/*
    rm *.log
}
