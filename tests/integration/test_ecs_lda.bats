#!/usr/bin/env bats

setup () {

    output_folder="./tests/integration/output/lda"
    data_xy="data_xy.csv"
    vsel_x_config="vsel_x_config.csv"
    s3_bucket="s3://tesera.svc.learn"
    s3_fixture_prefix="tests/fixtures"
    s3_wd_prefix="tests/lda"
    s3_output_prefix="tests/output/lda"
    s3_wd_path="$s3_bucket/$s3_wd_prefix"
    s3_fixture_path="$s3_bucket/$s3_fixture_prefix"
    s3_output_path="$s3_bucket/$s3_output_prefix"

    mkdir -p "$output_folder"
    aws s3 cp "$s3_fixture_path/$data_xy" "$s3_wd_path/$data_xy"
    aws s3 cp "$s3_fixture_path/$vsel_x_config" "$s3_wd_path/$vsel_x_config"

    cat << EOF > $output_folder/overrides.json
    {
      "containerOverrides": [
        {
          "name": "learn",
          "command": [
            "lda",
            "--xy-data=$s3_wd_path/$data_xy",
            "--config=$s3_wd_path/$vsel_x_config",
            "--output=$s3_output_path"
          ]
        }
      ]
    }
EOF

    task=$(aws ecs run-task \
        --cluster learn \
        --task-definition learn \
        --overrides file://$output_folder/overrides.json \
        --started-by learn-ecs/tests/lda)

    task_arn=$(echo $task | jq -r '.tasks[0].taskArn')

    aws ecs wait tasks-stopped --cluster learn --tasks $task_arn

    aws s3 sync $s3_output_path $output_folder

}

@test "lda runs on ecs and output expected files" {
    expected_files=(
        ASSESS.csv
        AVGP.csv
        BWRATIO.csv
        CTABALL.csv
        CTABSUM.csv
        CTABULATION.csv
        DFUNCT.csv
        POSTERIOR.csv
        PRIOR.csv
        RLOADRANK.csv
        VARMEANS.csv
        pylearn.log
    )

    for expected_file in $expected_files
    do
        [ -f $output_folder/$expected_file ]
    done
}

teardown () {
    rm $output_folder/*
    aws s3 rm "$s3_output_path" --recursive
}
