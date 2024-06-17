SELECT T1.word FROM prosody_nodes AS T1 JOIN node AS T3 JOIN is_target_syn_root AS T2 WHERE T2.is_label like 1
SELECT count(*) FROM prosody_nodes AS T1 WHERE T1.word like 1
SELECT T1.pos FROM syntax_terminal_nodes AS T1 JOIN node AS T3 JOIN prosody_nodes AS T2 WHERE T2.filesequence like 1
SELECT T1.pos FROM syntax_terminal_nodes AS T1 JOIN node AS T3 JOIN prosody_nodes AS T2 WHERE T2.word like 1
SELECT T1.is_graph_id FROM is_target_syn_root AS T1 WHERE T1.syn_graph_id = 1
SELECT T1.tone FROM prosody_nodes AS T1 WHERE T1.filesequence NOT IN (SELECT T2.node_id FROM node AS T2)
SELECT T1.is_label FROM is_target_syn_root AS T1 WHERE T1.is_node_descr = 1
SELECT T1.node_type, T2.is_node_descr FROM node AS T1 JOIN is_target_syn_root AS T2 WHERE T2.is_node_id = 1
SELECT T1.name FROM graph_type_definition AS T1 JOIN syntax_terminal_nodes AS T2 JOIN prosody_nodes AS T3 WHERE T2.node_id = 1 and T3.filesequence > 1
SELECT T1.name FROM graph_type_definition AS T1 JOIN node AS T3 JOIN closure AS T2 WHERE T2.closure_name = 1