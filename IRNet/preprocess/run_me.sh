# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

#!/bin/bash

data=$1
table_data=$2
output=$3

echo "Start download NLTK data"
python ./preprocess/download_nltk.py

echo "Start process the origin Spider dataset"
python ./preprocess/data_process.py --data_path ${data} --table_path ${table_data} --output "process_data.json"

echo "Start generate SemQL from SQL"
python ./preprocess/sql2SemQL.py --data_path process_data.json --table_path ${table_data} --output ${output} # in the original script, it states ${data} but I believe it is a typo. 

rm process_data.json
