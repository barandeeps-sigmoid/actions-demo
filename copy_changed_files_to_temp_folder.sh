#!/bin/bash

BRANCH_NAME=$1
TEMP_DIR_PATH=$2
FILTER_DIR=$3
echo "BRANCH_NAME=>$BRANCH_NAME"
echo "TEMP_DIR_PATH=>$TEMP_DIR_PATH"
echo "FILTER_DIR=>$FILTER_DIR"

python git_rest_api_call.py $BRANCH_NAME> result.log

cat result.log

result=$(tail -1 result.log)
IFS="," read -r PREVIOUS_SHA CURRENT_SHA<<< "${result}"
echo $PREVIOUS_SHA
echo $CURRENT_SHA

echo "Files changed:"
git diff --name-status $PREVIOUS_SHA $CURRENT_SHA


ADDED=$(git diff --diff-filter=A --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | awk -v d=";" '{s=(NR==1?s:s d)$0}END{print s}')
MODIFIED=$(git diff --diff-filter=M --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | awk -v d=";" '{s=(NR==1?s:s d)$0}END{print s}')
DELETED=$(git diff --diff-filter=D --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | awk -v d=";" '{s=(NR==1?s:s d)$0}END{print s}')

echo "added files: $ADDED"
echo "modified files: $MODIFIED"
echo "deleted files: $DELETED"


 my_array=($(echo $ADDED | tr ";" "\n"))
         mkdir -p $TEMP_DIR_PATH
         for file_name in "${my_array[@]}";do
         if [[ $file_name = $FILTER_DIR/** ]]; then
             echo "Added file => $file_name"
             echo "::set-output name=VALIDATE_ADDED_SCHEMACHANGE::TRUE"
             cp $file_name $TEMP_DIR_PATH/

         fi
         done


my_array=($(echo $MODIFIED | tr ";" "\n"))
         mkdir -p $2
         for file_name in "${my_array[@]}";do
         if [[ $file_name = $FILTER_DIR/** ]]; then
             echo "Modified file => $file_name"
             echo "::set-output name=VALIDATE_ADDED_SCHEMACHANGE::TRUE"
             cp $file_name $TEMP_DIR_PATH/

         fi
         done

echo "Files copied to tmp location $TEMP_DIR_PATH"
ls -ltr $TEMP_DIR_PATH
