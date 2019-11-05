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

def reduce_pk_graph_to_schemas(schemalist=['A','B'], exclude_pk_list=[], prefix="test", only_connecting_pk=True, add_tab_cols=False, write_file=False):   
    """
    reduce an Primary Graph to the tables in the schemas in the schemalist. Some primary can be excluded (like valid_to in a time slice)
    """
    Gpk = build_pk_graph(add_tab_cols=add_tab_cols, prefix=prefix, write_file=False)
    tables_retain = [n for n,d in Gpk.nodes(data=True) if d['type'] == "BASE TABLE" and d['schema'] in schemalist]
    # now add the primary keys
    neighbors=set()
    for table in tables_retain:
        for n in Gpk.neighbors(table):
            neighbors.add(n)

    for pk in exclude_pk_list:
        if pk in neighbors:
            neighbors.remove(pk)

    neighbor_dict = {}
    for pk in neighbors:
        pk_tables = 0
        for nb in Gpk.neighbors(pk):
            if nb in tables_retain:
                pk_tables += 1
        neighbor_dict[pk] = pk_tables

    if only_connecting_pk:
        # only retain pks with more than one edge    
        neighbor_list =  [pk for pk in neighbor_dict if neighbor_dict[pk] > 1] 
    else:
        neighbor_list = list(neighbors)
    
        
    G_reduced = Gpk.subgraph(tables_retain + neighbor_list)
    if write_file:
        nx.write_graphml(G_reduced, './data/output/{}_pk_reduced.xml'.format(prefix))
    return G_reduced

if __name__ == '__main__':
    #G_reduced = reduce_object_graph_to_schemas()
    #print("Reduced Object Graph nodes: {0}, Reduced Object Graph edges: {1}".format(len(G_reduced.nodes()), len(G_reduced.edges())))
    G_reduced = reduce_pk_graph_to_schemas(schemalist=["A"], exclude_pk_list=["VALID_TO", "DW_FROM_DATE", "DW_TO_DATE","VALID_FROM","VALIDFROM"], prefix="test", write_file=False)
    print("Reduced Primary Key Graph nodes: {0}, Reduced Primary Key Graph edges: {1}".format(len(G_reduced.nodes()), len(G_reduced.edges())))
    print("Reduced Primary Key Graph nodes: {0}, Reduced Primary Key Graph edges: {1}".format(len(G_reduced.nodes()), len(G_reduced.edges())))
