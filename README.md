## 1. Generating DIRNDL instances for Spider-formatted `tables.json` and `dev.json`

Given the simplified and smaller version of the DIRNDL database, created by me and to be found at: [DIRNDL Database](https://drive.google.com/drive/folders/1reK5Lx7EgKV2ooR0cYOrBXOPUOId43lH?usp=drive_link), the first step consists in obtaining the files representing the structure of the database in the formats required by the systems, as outlined in Section 7 of my thesis work. For this purpose, these steps must be followed:

1. Create a database directory in `spider/preprocess/`.
   ```sh
   mkdir -p spider/preprocess/database
2. Store `dirndl.sql` and `dirndl.sqlite` (available at the link above) in `spider/preprocess/database/dirndl`
3. Generate the `tables.json` file for the dirndl database with the `get_tables.py` script. This script reads sqlite files from the `database/` directory and previous `tables.json` with hand-corrected names. This means that the keys of the dictionary which will be populated by the script with the values from DIRNDL must be already specified in the pre-existing `tables.json` file. The command to be run is:
    ```sh
    python process/get_tables.py [directory including many subdirectories containing database.sqlite files] [output file name e.g. output.json] [existing tables.json file to be inherited]
    ```
    After running this, `output.json` will contain the dictionary with the corresponding DIRNDL description, which can be added as new instance into the pre-existing `tables.json` file.
4. Obtain development instances for DIRNDL with the `parse_sql_one.py` script. Given a NL question, the golden SQL query, and the golden information output, as outlined for instance in Table 3 in Section 8.1 of my thesis work, one should specify (in the main method of the script) the golden SQL query, the id of the database (“dirndl” in this case), and the table file (`tables.json`). By running the following command:
    ```sh
    python parse_sql_one.py
    ```
    the version of the SQL query parsed corresponding the development format defined by authors of Spider is printed. The output is the value of only the `sql` key in a development instance. A development instance must also contain the golden query and the corresponding NL question as specified in Listing 4 of my thesis work. Hence, while the value for the `sql` key is automatically generated by `parse_sql_one.py`, the values for the other keys of the instance must be filled out manually.

## 2. Generating predicted queries from IRNet

IRNet does not allow for direct inference without explicitly stating development instances.

To obtain the predictions from IRNet, first the IRNet system has to be set-up following these steps in the IRNet directory:

* Download [Glove Embedding](https://nlp.stanford.edu/data/wordvecs/glove.42B.300d.zip) and put `glove.42B.300d` under `./data/` directory
* Download [Pretrained IRNet](https://drive.google.com/open?id=1VoV28fneYss8HaZmoThGlvYU3A-aK31q) and put `IRNet_pretrained.model` under `./saved_model/` directory
* Download preprocessed train dataset from [here](https://drive.google.com/drive/folders/1reK5Lx7EgKV2ooR0cYOrBXOPUOId43lH?usp=drive_link) and put `train.json` under `./data/` directory

The steps outlined at point 1 allow to obtain DIRNDL instances in the tables.json and the dev.json files as described by the authors of Spider. These two resulting files for Experiment 1 can be found [here](https://drive.google.com/drive/folders/1DAtm1dUvHx8-auFl2gHaRk_qAhRe4GR5?usp=drive_link). Nevertheless, the IRNet system uses a modified version of the original dev.json file, as described in Listing 5 of my thesis work. For this reason, before obtaining the predictions from the system, these preprocessing steps must be carried out:

* Save the new tables.json and dev.json files under `./data/` directory
* Run `./preprocess/run_me.sh`. This script will process the dev.json file and generate the IRNet-specific development format file, which is needed to generate the predictions and for evaluation. The generated `predict.json` file (or any other name chosen for it) must then renamed as `dev.json` and substitute the previous `dev.json` file.
* Run `eval.sh` to generate the predictions. More specifically, this script produces a file named e.g. `output` with the SQL queries predicted by the system given the NL questions contained in the `dev.json` file, and a `gold.txt` file with the golden queries, extrapolated from the `dev.json` file.
`sh eval.sh [GPU_ID] [OUTPUT_FOLD]`


## 3. Generating predicted queries from SmBop

SmBop allows both for direct inference without development instances and also for prediction based on development instances.

Follow these steps in the SmBop directory:

1. Download the pretrained model from [here](https://drive.google.com/file/d/1jdS7VJ5fB3ZUvokCOAosk-N5tAbi9BoI/view?usp=drive_link).
2. Create a dataset directory.
   ```sh
   mkdir -p `./dataset`
2. Store the Spider data from [here](https://drive.google.com/open?id=1YFV1GoLivOMlmunKW0nkzefKULO4wtrn) into `./dataset`.
3. Store `dirndl.sql` and `dirndl.sqlite` (available at the link above) in `./dataset/database/dirndl`.
4. Substitute the original tables.json file with the one containing the DIRNDL description as well.

### A) Perform direct inference

One way to go with the SmBop system is to perform direct inference using the `start_demo.py` script, where one must simply pass the NL question and the database id into `print(inference())`.

### B) Obtain predictions based on development instances

Another way to go with the SmBop system is to run eval.py which takes as input: /database directory path, tables.json, dev.json (in the original Spider format) and outputs the prediction file. The command to be run is:
```sh
python eval.py --archive_path {model_path} --output {output file name}
```

## 4. Evaluation

### A) Evaluation via official Spider evaluation script

A way to evaluate the results is by using the official Spider evaluation script of Spider, to be found at `spider/evaluation.py`.
```sh
python evaluation.py --gold {file with golden queries} --pred {file with predicted queries} --etype {evaluation metrics type} --db  {directory with databases}  --table {tables.json file}
```

Please note the following when passing the arguments:
- {file with golden queries} must be a .sql file where each line is `a gold SQL \t db_id`
- {file with predicted queries} must be a .sql file where each line is a predicted SQL
- {evaluation metrics type} is a field that specifies the type of evaluation metrics desired; "match" is for exact set matching score, "exec" is for execution score, and "all" is for both.

The `evaluation.py` and `process_sql.py` scripts are to be found is `/spider` and must be present together when copied in other directories (in this case in the IRNet and in the SmBop directories) since `evaluation.py` inherits some modules from `process_sql.py`.

The results of the official Spider evaluation script based on Experiment 1 are found at `./official_evaluation_irnet_exp1.yml` and `./official_evaluation_smbop_exp1.yml`

### B) Custom Evaluation script

Another way to evaluate the results is by using the tailor-made evaluation script, to be found at `./dirndl_evaluation_exp1.py`. This one allows for a more fine-grained analysis of the similarity between the predicted and the gold queries, based both on full-word and n-gram overlaps.
```sh
python dirndl_evaluation_exp1.py
```

In the `main` method, two file paths must be specified:
- `gold_file` must correspond to a `gold_queries.sql` file where each line is a gold SQL.
- `predicted_file` must correspond to a `predicted_queries.sql` file where each line is a predicted SQL.

The gold and predicted files resulting from IRNet in Experiment 1 are found at `./gold_queries_irnet_exp1.sql` and `./pred_queries_irnet_exp1.sql`.
The gold and predicted files resulting from SmBop in Experiment 1 are found at `./gold_queries_smbop_exp1.sql` and `./pred_queries_smbop_exp1.sql`.

The results of the evaluation script are found at `./dirndl_eval_exp1_irnet.yml` and `./dirndl_eval_exp1_smbop.yml`.

In order to see the information retrieval resulting from the execution of the queries, the `./sqlexecution.py` script must be run. The results for Experiment 1 are found at `./sqlexecution_output_exp1_irnet.yml` and `./sqlexecution_output_exp1_smbop.yml`. (STATE ARGUMENTS TAKEN BY SCRIPT)
Note: Query 4 from the IRNet predicted queries is excluded when running `sqlexecution.py` because it generates a bug in the system which blocks it.

## Citations

```markdown
This repository makes use of the following projects:

1. Spider (https://github.com/taoyds/spider)
2. IRNet(https://github.com/microsoft/IRNet)
3. SmBop(https://github.com/OhadRubin/SmBop)


