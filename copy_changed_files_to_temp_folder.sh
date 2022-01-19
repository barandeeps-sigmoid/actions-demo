#!/bin/bash

BRANCH_NAME=$1
TEMP_DIR_PATH=$2
FILTER_DIR=$3
PR_NUMBER=$4
echo "BRANCH_NAME=>$BRANCH_NAME"
echo "TEMP_DIR_PATH=>$TEMP_DIR_PATH"
echo "FILTER_DIR=>$FILTER_DIR"
echo "PR_NUMBER=>$PR_NUMBER"

python get_changed_files.py $PR_NUMBER snowflake/> result.log

cat result.log

RESULT=$(tail -1 result.log)

mkdir -p $TEMP_DIR_PATH
my_array=($(echo $RESULT | tr ";" "\n"))
for file_name in "${my_array[@]}";do
   echo "Added file => $file_name"
   echo "::set-output name=VALIDATE_ADDED_SCHEMACHANGE::TRUE"
   cp $file_name $TEMP_DIR_PATH/
done

echo "Files copied to tmp location $TEMP_DIR_PATH"
ls -ltr $TEMP_DIR_PATH
