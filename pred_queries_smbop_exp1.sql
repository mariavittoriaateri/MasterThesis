SELECT prosody_nodes.word FROM prosody_nodes, prosody_nodes WHERE prosody_graph.filesequence = 1 AND syntax_terminal_nodes.word = 3
SELECT COUNT( * ) FROM prosody_nodes WHERE prosody_nodes.word LIKE '%3%'
SELECT prosody_nodes.word FROM prosody_nodes WHERE prosody_nodes.ts = 3
SELECT syntax_terminal_nodes.pos FROM prosody_nodes WHERE prosody_nodes.word = 3
SELECT prosody_graph.graph_id FROM prosody_graph WHERE prosody_graph.filesequence = 3
SELECT prosody_nodes.word FROM prosody_nodes WHERE closure.closure_name = 'dlf-nachrichten-200703262000'
SELECT is_target_syn_root.is_label FROM node WHERE node.node_id = 900514
SELECT node.node_type FROM node WHERE node.node_id = 900620
SELECT edge.edge_type FROM edge WHERE edge.source_id = 56666 AND edge.target_graph = 56690
SELECT graph_type_definition.name FROM graph_type_definition JOIN node ON graph_type_definition.graph_type_def_id = node.node_type WHERE syntax_nonterminal_nodes.tiger_node_id = 'tigerXML_node'