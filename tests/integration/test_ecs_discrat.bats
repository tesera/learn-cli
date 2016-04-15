#!/usr/bin/env bats

setup () {

    output_folder="./tests/integration/output/discrat"
    data_xy="data_xy.csv"
    data_x_filtered="data_x_filtered.csv"
    lda_x_dfunct="lda_x_dfunct.csv"
    data_idf="data_idf.csv"
    s3_bucket="s3://tesera.svc.learn"
    s3_fixture_prefix="tests/fixtures"
    s3_wd_prefix="tests/discrat"
    s3_output_prefix="tests/output/discrat"
    s3_wd_path="$s3_bucket/$s3_wd_prefix"
    s3_fixture_path="$s3_bucket/$s3_fixture_prefix"
    s3_output_path="$s3_bucket/$s3_output_prefix"

    mkdir -p "$output_folder"
    aws s3 cp "$s3_fixture_path/$data_xy" "$s3_wd_path/$data_xy"
    aws s3 cp "$s3_fixture_path/$data_x_filtered" "$s3_wd_path/$data_x_filtered"
    aws s3 cp "$s3_fixture_path/$lda_x_dfunct" "$s3_wd_path/$lda_x_dfunct"
    aws s3 cp "$s3_fixture_path/$data_idf" "$s3_wd_path/$data_idf"

    cat << EOF > $output_folder/overrides.json
    {
      "containerOverrides": [
        {
          "name": "learn",
          "command": [
            "discrat",
            "--xy-data=$s3_wd_path/$data_xy",
            "--x-data=$s3_wd_path/$data_x_filtered",
            "--dfunct=$s3_wd_path/$lda_x_dfunct",
            "--idf=$s3_wd_path/$data_idf",
            "--varset=10",
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
        --started-by test_ecs_discrat@$(date +"%m-%d-%y-%T"))

    task_arn=$(echo $task | jq -r '.tasks[0].taskArn')

    aws ecs wait tasks-stopped --cluster learn --tasks $task_arn

    aws s3 sync $s3_output_path $output_folder

}

@test "discrat runs on ecs and output expected files" {
    expected_files=(
        forecasts.csv
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
