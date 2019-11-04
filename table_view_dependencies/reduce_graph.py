import networkx as nx
from build_graph import build_object_graph, build_pk_graph

def reduce_object_graph_to_schemas(schemalist=['A','B'], prefix="test", add_columns=False, write_file=False):   
    """
    reduce an Object Graph (views and tables) to the objects in the schemas in the schemalist
    """
    Gobj = build_object_graph(prefix=prefix, add_columns=add_columns, write_file=False)
    nodes_retain = [n for n,d in Gobj.nodes(data=True) if d['schema'] in schemalist]
    G_reduced = Gobj.subgraph(nodes_retain)
    if write_file:
        nx.write_graphml(G_reduced, './data/output/{}_object_reduced.xml'.format(prefix))
    return G_reduced

def reduce_pk_graph_to_schemas(schemalist=['A','B'], exclude_pk_list=[], prefix="test", add_tab_cols=False, write_file=False):   
    """
    reduce an Primary Graph to the tables in the schemas in the schemalist. Some primary can be excluded (like valid_to in a time slice)
    """
    Gpk = build_pk_graph(add_tab_cols=add_tab_cols, prefix=prefix, write_file=False)
    tables_retain = [n for n,d in Gpk.nodes(data=True) if d['type'] == "BASE TABLE" and d['schema'] in schemalist]
    # now add the primary keys
    neighbors=[]
    for table in tables_retain:
        for n in Gpk.neighbors(table):
            neighbors.append(n)
    pk_retain = [n for n,d in Gpk.nodes(data=True) if d['type'] == "PK" and n in neighbors and n not in exclude_pk_list]        
        
    G_reduced = Gpk.subgraph(tables_retain + pk_retain)
    if write_file:
        nx.write_graphml(G_reduced, './data/output/{}_pk_reduced.xml'.format(prefix))
    return G_reduced

if __name__ == '__main__':
    G_reduced = reduce_object_graph_to_schemas()
    print("Reduced Object Graph nodes: {0}, Reduced Object Graph edges: {1}".format(len(G_reduced.nodes()), len(G_reduced.edges())))
    G_reduced = reduce_pk_graph_to_schemas(schemalist=['A','B'], prefix="test", write_file=False)
    print("Reduced Primary Key Graph with lonely Tables nodes: {0}, Reduced Primary Key Graph with lonely Tables edges: {1}".format(len(G_reduced.nodes()), len(G_reduced.edges())))
