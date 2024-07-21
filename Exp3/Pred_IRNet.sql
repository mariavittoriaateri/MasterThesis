# When running: sh ./preprocess/run_me.sh ./data/dev.json ./data/tables.json ./data/predict.json
# I get the error: "Finished 1 datas and failed 3 datas."
# For this reason there is only one prediction:

SELECT T1.created FROM graph_type_definition AS T1 WHERE T1.graph_type_def_id NOT IN (SELECT T2.source_id FROM edge AS T2 JOIN node AS T4 JOIN prosody_nodes AS T3 WHERE T3.word like 1       )       
