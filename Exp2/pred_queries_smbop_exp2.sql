SELECT syntax_terminal_nodes.word FROM syntax_terminal_nodes JOIN syntax_graph ON syntax_terminal_nodes.syntax_terminal_graph_id = syntax_graph.sentence_number WHERE info_status_target_syn_root.sentence_number = 3 GROUP BY syntax_terminal_nodes.word
SELECT COUNT( * ) FROM syntax_graph WHERE syntax_graph.sentence_number = 3
SELECT syntax_terminal_nodes.pos FROM syntax_terminal_nodes WHERE syntax_terminal_nodes.word = 3
SELECT syntax_terminal_nodes.pos FROM syntax_terminal_nodes WHERE syntax_terminal_nodes.word = 3
SELECT node.graph_id FROM syntax_nonterminal_nodes JOIN node ON syntax_nonterminal_nodes.syntax_nonterminal_node_id = node.node_id WHERE info_status_target_syn_root.sentence_number = 3
SELECT prosody_nodes.accents FROM prosody_nodes WHERE prosody_nodes.file_sequence = 'dlf-nachrichten-200703262000' EXCEPT SELECT prosody_nodes.accents FROM prosody_nodes WHERE prosody_nodes.tone = 'dlf-nachrichten-200703262000'
SELECT info_status_target_syn_root.info_status_label FROM info_status_target_syn_root JOIN node ON info_status_target_syn_root.syn_graph_id = node.graph_id WHERE node.node_id = 900514
SELECT node.node_type, node.node_group FROM node WHERE node.node_id = '900620'
SELECT edge.edge_group FROM edge WHERE edge.source_graph = 56666 AND edge.target_graph = 56690
SELECT graph_type_definition.name FROM graph_type_definition JOIN node ON graph_type_definition.graph_type_def_id = node.node_type WHERE node.node_group = 'tigerXML_node'
