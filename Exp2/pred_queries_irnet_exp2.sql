SELECT T1.sentence_number FROM syntax_terminal_nodes AS T1 JOIN node AS T3 JOIN prosody_nodes AS T2 WHERE T2.word = 1
SELECT count(*) FROM prosody_nodes AS T1 WHERE T1.word like 1
SELECT T1.pos FROM syntax_terminal_nodes AS T1 JOIN node AS T3 JOIN prosody_nodes AS T2 WHERE T2.word like 1
SELECT T1.pos FROM syntax_terminal_nodes AS T1 JOIN node AS T3 JOIN prosody_nodes AS T2 WHERE T2.word like 1
SELECT T1.graph_id FROM node AS T1 JOIN syntax_terminal_nodes AS T2 WHERE T2.sentence_number = 1
SELECT T1.tone FROM prosody_nodes AS T1 WHERE T1.file_sequence NOT IN (SELECT T2.node_id FROM node AS T2)
SELECT T1.info_status_label FROM info_status_target_syn_root AS T1 WHERE T1.info_status_node_descr = 1
SELECT T1.node_type, T1.node_group FROM node AS T1 JOIN edge AS T2 WHERE T2.source_node = 1
SELECT T1.edge_group FROM edge AS T1 JOIN node AS T2 WHERE T1.target_node = 1 and T1.source_node = 1 and T2.node_id = 1
SELECT T1.name FROM graph_type_definition AS T1 JOIN node AS T3 JOIN closure AS T2 WHERE T2.closure_name = 1
