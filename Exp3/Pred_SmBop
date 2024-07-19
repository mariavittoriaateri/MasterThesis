SELECT node.node_id , prosody_nodes.word FROM prosody_nodes JOIN node ON prosody_nodes.node_id = node.node_id WHERE node.node_type = 'syntactic leaf' INTERSECT SELECT prosody_nodes.word FROM prosody_nodes JOIN node ON prosody_nodes.node_id = node.node_id WHERE node.node_type = 'syntactic leaf'	dirndl3
SELECT prosody_nodes.word FROM prosody_nodes WHERE prosody_nodes.word LIKE '%nuclear%'	dirndl3
SELECT sentences.sentence_array FROM sentences WHERE sentences.sentence_length<(SELECT MAX( sentences.sentence_length ) FROM sentences WHERE sentences.sentence_length LIKE '%DPs%')	dirndl3
SELECT prosody_nodes.word FROM prosody_nodes JOIN syntax_graph ON prosody_nodes.graph_id = syntax_graph.graph_id	dirndl3
