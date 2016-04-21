#!/usr/bin/env bats

setup () {

    output_folder="./tests/integration/output/varsel"
    data_xy="data_xy.csv"
    vsel_xy_config="vsel_xy_config.csv"
    s3_bucket="s3://tesera.svc.learn"
    s3_fixture_prefix="tests/fixtures"
    s3_fixture_path="$s3_bucket/$s3_fixture_prefix"

    mkdir -p "$output_folder"
    aws s3 cp "$s3_fixture_path/$data_xy" "$output_folder/$data_xy"
    aws s3 cp "$s3_fixture_path/$vsel_xy_config" "$output_folder/$vsel_xy_config"

    learn varsel --xy-data "$output_folder/$data_xy" --config "$output_folder/$vsel_xy_config" --output "$output_folder"

}

@test "varsels runs on ecs and output expected files" {
    expected_files=(
        UCORCOEF.csv
        UNIQUEVAR.csv
        VARRANK.csv
        VARSELECT.csv
        XVARSELV.csv
        XVARSELV1_XCOUNT.csv
        pylearn.log
    )
    for expected_file in $expected_files
    do
        [ -f "$output_folder/$expected_file" ]
    done
}

teardown () {
    rm $output_folder/*
}
