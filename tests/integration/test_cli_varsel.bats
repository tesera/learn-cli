#!/usr/bin/env bats

setup () {

    data_xy="data_xy.csv"
    vsel_xy_config="vsel_xy_config.csv"
    input="./tests/integration/input"
    output="./tests/integration/output"

    mkdir -p "$output"

    learn varsel \
        --xy-data "$input/$data_xy" \
        --config "$input/$vsel_xy_config" \
        --yvar VAR47 \
        --output "$output"

}

@test "varsels and output expected files" {
    [ -f "$output/vsel_x.csv" ]
    [ -f "$output/vsel_varrank.csv" ]
    [ -f "pylearn.log" ]
    [ -f "rlearn.log" ]
}

teardown () {
    rm $output/*
    rm *.log
}
