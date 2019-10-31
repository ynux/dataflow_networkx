# add columns to graph, tables and views are already in the graph
# columns are nodes of type COLUMN. "table a has column b" is an undirected edge. 
# Columns are identified by names, so one column can have edges to many nodes.
# We assume table names to be unique across schemas.

import pickle
import networkx as nx

def add_columns_graph(G, prefix='test'):
    # read from files created by write_node_set_edge_list.py 
    node_inputfile = "./data/intermediate/{}_columns_nodes.pickle".format(prefix)
    edge_inputfile = "./data/intermediate/{}_columns_edges.pickle".format(prefix)

    with open(node_inputfile,'rb') as node_file:
        node_dict = pickle.load(node_file)

    with open(edge_inputfile, 'rb') as edge_file:
        edge_list = pickle.load(edge_file)

    G.add_nodes_from(node_dict, label='column')
    for n,d in G.nodes(data=True):
        if d['label'] == 'column':
            d['type'] = 'COLUMN'

    G.add_edges_from(edge_list, label='column')

    
    return(G)

if __name__ == '__main__':
    import build_graph
    G = build_graph.build_object_graph()
    print("original G has {} nodes, {} edges".format(len(G.nodes()), len(G.edges())))
    add_columns_graph(G, prefix='test')
    print("with columns, G has {} nodes, {} edges".format(len(G.nodes()), len(G.edges())))
