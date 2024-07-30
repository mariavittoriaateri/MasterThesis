Error executing query: SELECT node.node_id , prosody_nodes.word FROM prosody_nodes JOIN node ON prosody_nodes.node_id = node.node_id WHERE node.node_type = 'syntactic leaf' INTERSECT SELECT prosody_nodes.word FROM prosody_nodes JOIN node ON prosody_nodes.node_id = node.node_id WHERE node.node_type = 'syntactic leaf';
Error message: SELECTs to the left and right of INTERSECT do not have the same number of result columns

Results for query: SELECT prosody_nodes.word FROM prosody_nodes WHERE prosody_nodes.word LIKE '%nuclear%';
Nothing returned

Results for query: SELECT sentences.sentence_array FROM sentences WHERE sentences.sentence_length<(SELECT MAX( sentences.sentence_length ) FROM sentences WHERE sentences.sentence_length LIKE '%DPs%');
Nothing returned

Results for query: SELECT prosody_nodes.word FROM prosody_nodes JOIN syntax_graph ON prosody_nodes.graph_id = syntax_graph.graph_id;
Nothing returned
