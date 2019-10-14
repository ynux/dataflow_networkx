# build schema graph from pickled files

import pickle
import networkx as nx

def build_schema_graph():
    # read from files created by write_node_set_edge_list.py 
    viewdefs_node_inputfile = './data/intermediate/test_viewdefinitions_schemaonly_nodes.pickle'
    viewdefs_edge_inputfile = './data/intermediate/test_viewdefinitions_schemaonly_edges.pickle'
    tableload_node_inputfile = './data/intermediate/test_tableload_schemaonly_nodes.pickle'
    tableload_edge_inputfile = './data/intermediate/test_tableload_schemaonly_edges.pickle'

    with open(viewdefs_node_inputfile,'rb') as node_file:
        vd_node_set = pickle.load(node_file)

    with open(viewdefs_edge_inputfile, 'rb') as edge_file:
        vd_edge_list = pickle.load(edge_file)

    with open(tableload_node_inputfile,'rb') as node_file:
        tl_node_set = pickle.load(node_file)

    with open(tableload_edge_inputfile, 'rb') as edge_file:
        tl_edge_list = pickle.load(edge_file)

    G = nx.MultiDiGraph()
    G.add_nodes_from(vd_node_set, label='viewdef')
    G.add_nodes_from(tl_node_set, label='tableload')
    G.add_edges_from(vd_edge_list, label='viewdef')
    G.add_edges_from(tl_edge_list, label='tableload')
    
    return(G)


def build_object_graph():
    # read from files created by write_node_set_edge_list.py 
    viewdefs_node_inputfile = './data/intermediate/test_viewdefinitions_nodes.pickle'
    viewdefs_edge_inputfile = './data/intermediate/test_viewdefinitions_edges.pickle'
    tableload_node_inputfile = './data/intermediate/test_tableload_nodes.pickle'
    tableload_edge_inputfile = './data/intermediate/test_tableload_edges.pickle'

    with open(viewdefs_node_inputfile,'rb') as node_file:
        vd_node_dict = pickle.load(node_file)

    with open(viewdefs_edge_inputfile, 'rb') as edge_file:
        vd_edge_list = pickle.load(edge_file)

    with open(tableload_node_inputfile,'rb') as node_file:
        tl_node_dict = pickle.load(node_file)

    with open(tableload_edge_inputfile, 'rb') as edge_file:
        tl_edge_list = pickle.load(edge_file)

    G = nx.MultiDiGraph()
    G.add_nodes_from(vd_node_dict, label='viewdef')
    G.add_nodes_from(tl_node_dict, label='tableload')
    G.add_edges_from(vd_edge_list, label='viewdef')
    G.add_edges_from(tl_edge_list, label='tableload')
    
    # enrich with table type and schema information    
    for n,d in G.nodes(data=True):
        if d['label'] ==  'tableload':
            d['schema']=tl_node_dict[n]['schema']
            d['type']=tl_node_dict[n]['type']
        if d['label'] ==  'viewdef':
            d['schema']=vd_node_dict[n]['schema']
            d['type']=vd_node_dict[n]['type']

    return(G)


if __name__ == '__main__':
    Gsch = build_schema_graph()
    print(len(Gsch.nodes()), len(Gsch.edges()))
    Gobj = build_object_graph()
    print(len(Gobj.nodes()), len(Gobj.edges()))