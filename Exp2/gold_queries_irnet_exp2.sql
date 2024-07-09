SELECT word FROM syntax_terminal_nodes WHERE sentence_number = 3 AND sequence = 1
SELECT MAX(sequence) FROM syntax_terminal_nodes WHERE sentence_number = 3
SELECT pos FROM syntax_terminal_nodes WHERE sentence_number = 3 ORDER BY sequence
SELECT pos FROM syntax_terminal_nodes WHERE sentence_number = 3 AND sequence = 1
SELECT syntax_graph_id FROM syntax_graph WHERE sentence_number = 3
SELECT word FROM prosody_nodes WHERE tone = 'NONE' AND file_sequence = 'dlf-nachrichten-200703262000'
SELECT info_status_label FROM info_status_target_syn_root WHERE syn_root_id = 900614
SELECT node_type, node_group FROM node WHERE node_id = 900620
SELECT edge_group FROM edge WHERE source_node = 56666 AND source_graph = 1349 AND target_node = 56690
SELECT name FROM graph_type_definition WHERE graph_type_group = 'tigerXML_node'
