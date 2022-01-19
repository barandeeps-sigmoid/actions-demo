#!/bin/bash

TEMP_DIR_PATH=$1
FILTER_DIR=$2
PR_NUMBER=$3
echo "TEMP_DIR_PATH=>$TEMP_DIR_PATH"
echo "FILTER_DIR=>$FILTER_DIR"
echo "PR_NUMBER=>$PR_NUMBER"

python get_changed_files.py $PR_NUMBER snowflake/> result.log

cat result.log

RESULT=$(tail -1 result.log)
echo "Final changed files detected"
echo $RESULT
mkdir -p $TEMP_DIR_PATH
my_array=($(echo $RESULT | tr ";" "\n"))
for file_name in "${my_array[@]}";do
   echo "::set-output name=VALIDATE_CHANGES_SCHEMACHANGE::TRUE"
   EPOCH_TIMESTAMP_WITH_MILLIS=".$(date +%s%3)_"
   echo "Original file name $file_name"
   EXTRACTED_FILE_NAME=$(echo "$file_name" | sed "s/.*\///")
   echo "Extracted file name $EXTRACTED_FILE_NAME"
   REPLACED_FILE_NAME=${EXTRACTED_FILE_NAME/_/$EPOCH_TIMESTAMP_WITH_MILLIS}
   echo "Replaced file name $REPLACED_FILE_NAME"
   cp "$file_name" "$TEMP_DIR_PATH/$REPLACED_FILE_NAME"
   echo "============================================="
done

echo "Files copied to tmp location $TEMP_DIR_PATH"
ls -ltr $TEMP_DIR_PATH

