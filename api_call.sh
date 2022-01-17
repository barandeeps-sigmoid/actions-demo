#!/bin/bash

python api_call.py $1> result.log

cat result.log




result=$(tail -1 result.log)
IFS="," read -r PREVIOUS_SHA CURRENT_SHA<<< "${result}"
echo $PREVIOUS_SHA
echo $CURRENT_SHA

echo "Files changed:"
git diff --name-status $PREVIOUS_SHA $CURRENT_SHA



# my_array=($(echo $ADDED | tr ";" "\n"))
#         mkdir -p schemachange_delta/schemachange 
#         for file_name in "${my_array[@]}";do
#         if [[ $file_name = schemachange/** ]]; then
#             echo "Added file => $file_name"
#             echo "::set-output name=VALIDATE_ADDED_SCHEMACHANGE::TRUE"
#             cp $file_name schemachange_delta/$file_name
            
#         fi
#         done
#         ls -ltr $GITHUB_WORKSPACE/schemachange_delta/schemachange






ADDED=$(git diff --diff-filter=A --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | awk -v d=" " '{s=(NR==1?s:s d)$0}END{print s}')
MODIFIED=$(git diff --diff-filter=M --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | awk -v d=" " '{s=(NR==1?s:s d)$0}END{print s}')
DELETED=$(git diff --diff-filter=D --name-only "$PREVIOUS_SHA" "$CURRENT_SHA" | awk -v d=" " '{s=(NR==1?s:s d)$0}END{print s}')

echo "added files: $ADDED"
echo "modified files: $MODIFIED"
echo "deleted files: $DELETED"