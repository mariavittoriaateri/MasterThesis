SELECT word FROM syntax_terminal_nodes WHERE s_num = 3 AND seq = 1
SELECT MAX(seq) FROM syntax_terminal_nodes WHERE s_num = 3
SELECT pos FROM syntax_terminal_nodes WHERE s_num = 3 ORDER BY seq
SELECT pos FROM syntax_terminal_nodes WHERE s_num = 3 AND seq = 1
SELECT graph_id FROM syntax_graph WHERE s_num = 3
SELECT word FROM prosody_nodes WHERE tone = 'NONE' AND filesequence = 'dlf-nachrichten-200703262000'
SELECT is_label FROM is_target_syn_root WHERE syn_root_id = 900614
SELECT node_type, grp FROM node WHERE node_id = 900620
SELECT grp FROM edge WHERE source_id = 56666 AND source_graph = 1349 AND target_id = 56690
SELECT name FROM graph_type_definition WHERE grp = 'tigerXML_node'
