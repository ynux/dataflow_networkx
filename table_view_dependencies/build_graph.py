# build graphs from pickled files created from functions in prepare_graph_input.py
import pickle
import networkx as nx

def build_schema_graph(prefix='test', write_file=False):
    # read from files created by write_node_set_edge_list.py 
    viewdefs_node_inputfile = "./data/intermediate/{}_viewdefinitions_schemaonly_nodes.pickle".format(prefix)
    viewdefs_edge_inputfile = "./data/intermediate/{}_viewdefinitions_schemaonly_edges.pickle".format(prefix)
    tableload_node_inputfile = "./data/intermediate/{}_tableload_schemaonly_nodes.pickle".format(prefix)
    tableload_edge_inputfile = "./data/intermediate/{}_tableload_schemaonly_edges.pickle".format(prefix)

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

    if write_file:
        nx.write_graphml(G, './data/output/{}_schema.xml'.format(prefix))
    
    return(G)

def build_object_graph(prefix='test', add_columns=False, write_file=False):
    # read from files created by write_node_set_edge_list.py 
    viewdefs_node_inputfile = "./data/intermediate/{}_viewdefinitions_nodes.pickle".format(prefix)
    viewdefs_edge_inputfile = "./data/intermediate/{}_viewdefinitions_edges.pickle".format(prefix)
    tableload_node_inputfile = "./data/intermediate/{}_tableload_nodes.pickle".format(prefix)
    tableload_edge_inputfile = "./data/intermediate/{}_tableload_edges.pickle".format(prefix)

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

    if add_columns:
        G = add_columns_graph(G, prefix=prefix)
    if write_file:
        nx.write_graphml(G, './data/output/{}_object.xml'.format(prefix))
 
    return(G)

def build_pk_graph(prefix='test', add_tab_cols = False, write_file=False):
    """ prefix: input / output file name prefix
        add_tab_cols: if tables (without pk) from table-column csv should be added
        write_file: Write graph to xml file """
    # read from files created by pk_graph_input.py 
    pk_node_inputfile = "./data/intermediate/{}_primary_keys_nodes.pickle".format(prefix)
    pk_edge_inputfile = "./data/intermediate/{}_primary_keys_edges.pickle".format(prefix)
 
    with open(pk_node_inputfile,'rb') as node_file:
        pk_node_dict = pickle.load(node_file)

    with open(pk_edge_inputfile, 'rb') as edge_file:
        pk_edge_list = pickle.load(edge_file)
 
    G = nx.Graph()
    G.add_nodes_from(pk_node_dict, label='pk')
    G.add_edges_from(pk_edge_list, label='pk')
    for n,d in G.nodes(data=True):
        d['type']=pk_node_dict[n]['type']
        if pk_node_dict[n]['type'] == "BASE TABLE":
            d['schema']=pk_node_dict[n]['schema']

    if add_tab_cols:
        table_node_inputfile = "./data/intermediate/{}_tableload_nodes.pickle".format(prefix)
        with open(table_node_inputfile,'rb') as node_file:
            tb_node_dict = pickle.load(node_file)
        for node in tb_node_dict:
            if node not in G and tb_node_dict[node]['type'] == "BASE TABLE":
                G.add_node(node, label='added table')

    if write_file:
        nx.write_graphml(G, './data/output/{}_table_pk.xml'.format(prefix))
    return(G)

def add_columns_graph(G, prefix='test'):
    """
    add columns to graph, tables and views have to already be the graph as nodes
    columns are nodes of type COLUMN. "table a has column b" is an edge. 
    """
    # Columns are identified by names, so one column can have edges to many nodes.
    # We assume table names to be unique across schemas.
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
    Gsch = build_schema_graph()
    print("Schema Graph nodes: {0}, Schema Graph edges: {1}".format(len(Gsch.nodes()), len(Gsch.edges())))
    Gobj = build_object_graph(add_columns=False)
    print("Object Graph nodes: {0}, Object Graph edges: {1}".format(len(Gobj.nodes()), len(Gobj.edges())))
    Gobjcol = build_object_graph(add_columns=True)
    print("Object Graph with Cols nodes: {0}, Object Graph with Cols edges: {1}".format(len(Gobjcol.nodes()), len(Gobjcol.edges())))
    Gpk = build_pk_graph(add_tab_cols=False)
    print("Primary Key Graph nodes: {0}, Primary Key Graph edges: {1}".format(len(Gpk.nodes()), len(Gpk.edges())))
    Gpk = build_pk_graph(add_tab_cols=True, prefix="test", write_file=False)
    print("Primary Key Graph with lonely Tables nodes: {0}, Primary Key Graph with lonely Tables edges: {1}".format(len(Gpk.nodes()), len(Gpk.edges())))
