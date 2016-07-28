# Team-Target
We just wanted to add a few notes on the files we are sending.

UIDalgorithm.py:

The main function is graph_construction(G) where G is a graph.
This initiates that entire algorithm and returns a list of subgraphs formed from cutting.
The bulk of this process can be found within the target_cut function.

datageneration.py:

The function data_for_npeople(n), where n should be a positive integer, creates a 
graph for n people with no connects between them. Then the graph can be fed into 
the function add_noise_graph(G) which will randomly add connections (noise) between 
the components (people) of the graph. You will note that during this construction 
we must label our graph and add appropriate node types/attributes so that it will be 
compatible with the graph_construction function.
