
# write files with node_dict, edges_list to be digested by a networkx graph, with schema and type as node attributes
# remark: if you want to avoid using pickle, use json_dumps / json_loads for the dict. edge_list
# is a list of tuples, which makes things complicated and me use pickle.
#  
import csv, pickle

def tableload_prepare_graph_input(prefix, write_file=True):
    """ reads from  <prefix>_tableload.csv
    writes to <prefix>_tableload_nodes.pickle, <prefix>_tableload_edges.pickle """
    # read from csv generated from table load tool
    # DEST_SCHEMA_NAME,DEST_TABLE_NAME,SRC_SCHEMA_NAME,SRC_TABLE_NAME,REFERENCED_OBJECT_TYPE
    # B,T_B1,A,T_A1,BASE TABLE
    # B,T_B2,A,T_A2,BASE TABLE
    # Tables and Views will be nodes, edges will go from the src object to the dest table
    # Schema and object type are added as attributes
    inputfile = "./data/input/{0}_tableload.csv".format(prefix)
    node_outputfile = "./data/intermediate/{}_tableload_nodes.pickle".format(prefix)
    edge_outputfile = "./data/intermediate/{}_tableload_edges.pickle".format(prefix)
    node_dict = {}
    edge_list = []

    with open(inputfile) as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                node_dict[row[1]] = { 'schema': row[0], 'type': 'BASE TABLE'} 
                # referenced tables / view
                node_dict[row[3]] = { 'schema': row[2], 'type': row[4]} 
                # edges
                edge_list.append( (row[3], row[1] ))
                line_count += 1
    if write_file:
        with open(node_outputfile,'wb') as node_dict_file:
            pickle.dump( node_dict, node_dict_file )
        with open(edge_outputfile,'wb') as edge_list_file:
            pickle.dump( edge_list, edge_list_file)
    return node_dict, edge_list

def tableload_schemaonly_prepare_graph_input(prefix, write_file=True):
    """ reads from  <prefix>_tableload.csv
    writes to <prefix>_tableload_schemaonly_nodes.pickle, <prefix>_tableload_schemaonly_edges.pickle """
    # read from csv generated from table load tool
    # DEST_SCHEMA_NAME,DEST_TABLE_NAME,SRC_SCHEMA_NAME,SRC_TABLE_NAME,REFERENCED_OBJECT_TYPE
    # B,T_B1,A,T_A1,BASE TABLE
    # B,T_B2,A,T_A2,BASE TABLE
    # Schemas will be nodes, edges will go from the src schema to the dest schema
    # Object name and type are ignored
    inputfile = "./data/input/{0}_tableload.csv".format(prefix)
    node_outputfile = "./data/intermediate/{}_tableload_schemaonly_nodes.pickle".format(prefix)
    edge_outputfile = "./data/intermediate/{}_tableload_schemaonly_edges.pickle".format(prefix)
    node_dict = {}
    edge_list = []

    with open(inputfile) as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[0] not in node_dict:
                    node_dict[row[0]] = {'type': 'SCHEMA'}
                if row[2] not in node_dict:
                    node_dict[row[2]] = {'type': 'SCHEMA'}
                edge_list.append( (row[2], row[0] ))
                line_count += 1
    if write_file:
        with open(node_outputfile,'wb') as node_dict_file:
            pickle.dump( node_dict, node_dict_file )
        with open(edge_outputfile,'wb') as edge_list_file:
            pickle.dump( edge_list, edge_list_file)
    return node_dict, edge_list

def viewdefinitions_graph_input(prefix, write_file=True):
    """ reads from  <prefix>_viewdefinitions.csv
    writes to <prefix>_viewdefinitions_nodes.pickle, <prefix>_viewdefinitions_edges.pickle """
    # read from csv from parsed view definitions
    # SCHEMA_NAME,OBJECT_NAME,REFERENCED_SCHEMA_NAME,REFERENCED_OBJECT_NAME,REFERENCED_OBJECT_TYPE
    # STG_C,V_C1,B,T_B1,BASE TABLE
    # STG_C,V_C2,B,T_B2,BASE TABLE
    # tables and views will be nodes
    # edges go from the tables used to the view
    inputfile = "./data/input/{0}_viewdefinitions.csv".format(prefix)
    node_outputfile = "./data/intermediate/{}_viewdefinitions_nodes.pickle".format(prefix)
    edge_outputfile = "./data/intermediate/{}_viewdefinitions_edges.pickle".format(prefix)
    node_dict = {}
    edge_list = []

    with open(inputfile) as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                # some functions diguise as views - this should move into a cleanup step
                if not '(' in row[1]:
                    node_dict[row[1].strip('\"')] = { 'schema': row[0].strip('\"'), 'type': 'VIEW'} 
                    # referenced tables / view
                    node_dict[row[3].strip('\"')] = { 'schema': row[2].strip('\"'), 'type': row[4].strip('\"')} 
                    # edges
                    edge_list.append( (row[3].strip('\"'), row[1].strip('\"') ))
                    line_count += 1
    if write_file:
        with open(node_outputfile,'wb') as node_dict_file:
            pickle.dump( node_dict, node_dict_file )
        with open(edge_outputfile,'wb') as edge_list_file:
            pickle.dump( edge_list, edge_list_file)
    return node_dict, edge_list

def viewdefinitions_schemaonly_graph_input(prefix, write_file=True):
    """ reads from  <prefix>_primary_keys.csv
    writes to <prefix>_primary_keys_nodes.pickle, <prefix>_primary_keys_edges.pickle """
    # read from csv from parsed view definitions
    # SCHEMA_NAME,OBJECT_NAME,REFERENCED_SCHEMA_NAME,REFERENCED_OBJECT_NAME,REFERENCED_OBJECT_TYPE
    # STG_C,V_C1,B,T_B1,BASE TABLE
    # STG_C,V_C2,B,T_B2,BASE TABLE
    # Schemas will be nodes, edges will go from the source schema to the schema of the view
    # Object name and type are ignored
    # ignore views and tables, and types
    inputfile = "./data/input/{0}_viewdefinitions.csv".format(prefix)
    node_outputfile = "./data/intermediate/{}_viewdefinitions_schemaonly_nodes.pickle".format(prefix)
    edge_outputfile = "./data/intermediate/{}_viewdefinitions_schemaonly_edges.pickle".format(prefix)
    node_dict = {}
    edge_list = []

    with open(inputfile) as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if not '(' in row[1]:
                    # some functions diguise as views - this should move into a cleanup step
                    # source views
                    node_dict[row[0].strip('\"')] = {'type': 'SCHEMA'}
                    # referenced tables / view
                    node_dict[row[2].strip('\"')] = {'type': 'SCHEMA'}
                    # edges
                    edge_list.append( (row[2].strip('\"'), row[0].strip('\"') ))
                    line_count += 1
    if write_file:
        with open(node_outputfile,'wb') as node_file:
            pickle.dump( node_dict, node_file )
        with open(edge_outputfile,'wb') as edge_file:
            pickle.dump( edge_list, edge_file )
    return node_dict, edge_list

def columns_prepare_graph_input(prefix, write_file = True):
    """ reads from  <prefix>_columns.csv
    writes to <prefix>_columns_nodes.pickle, <prefix>_columns_edges.pickle """
    # read from csv created from information schema
    # TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME
    # A,A_T1,cola
    # A,A_T1,colb
    # columns will be nodes
    # tables are expected to already exist in the graph
    # edges go from the column to the table / view they are part of. They are identified by their 
    #  name, which means that one column can have edges to many tables.
    # Schema information is ignored. 
    # We assume that the table names are unique across schemas ( we could check the schema attribute but don't )
    inputfile = "./data/input/{0}_columns.csv".format(prefix)
    node_outputfile = "./data/intermediate/{}_columns_nodes.pickle".format(prefix)
    edge_outputfile = "./data/intermediate/{}_columns_edges.pickle".format(prefix)
    node_dict = {}
    edge_list = []

    with open(inputfile) as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                node_dict[row[2]] = { 'type': 'COLUMN'}
                edge_list.append((row[2], row[1] ))
                line_count += 1
    if write_file:
        with open(node_outputfile,'wb') as node_dict_file:
            pickle.dump( node_dict, node_dict_file )
        with open(edge_outputfile,'wb') as edge_list_file:
            pickle.dump( edge_list, edge_list_file)
    return node_dict, edge_list

def primary_keys_prepare_graph_input(prefix, write_file=True):
    """ reads from  <prefix>_primary_keys.csv
    writes to <prefix>_primary_keys_nodes.pickle, <prefix>_primary_keys_edges.pickle """
    # read from csv created from information schema
    # "schema_name","table_name","column_name","key_sequence"
    # A,T_A1,cola,1
    # A,T_A3,cola,1
    # A,T_A3,colf,2
    # tables and primary keys will be nodes
    # edges go from the pk to the table
    # ignoring the key_sequence info (or cons_columns.position in Oracle
    inputfile = "./data/input/{0}_primary_keys.csv".format(prefix)
    node_outputfile = "./data/intermediate/{}_primary_keys_nodes.pickle".format(prefix)
    edge_outputfile = "./data/intermediate/{}_primary_keys_edges.pickle".format(prefix)
    node_dict = {}
    edge_list = []

    with open(inputfile) as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                node_dict[row[1]] = { 'type': 'BASE TABLE', 'schema': row[0]}
                node_dict[row[2]]  = { 'type': 'PK'}
                edge_list.append((row[2], row[1] ))
                line_count += 1
    if write_file:
        with open(node_outputfile,'wb') as node_dict_file:
            pickle.dump( node_dict, node_dict_file )
        with open(edge_outputfile,'wb') as edge_list_file:
            pickle.dump( edge_list, edge_list_file)
    return node_dict, edge_list

def tables_prepare_graph_input(prefix, write_file=True):
    """ reads from  <prefix>_columns.csv
    writes to <prefix>_table_nodes.pickle """
    # read from csv created from information schema
    # TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME
    # A,A_T1,cola
    # A,A_T1,colb
    # tables will be nodes.
    # no edges. columns are ignored. schema is added as attribute.
    # Usage: to add tables that are missing in the table load infos
    inputfile = "./data/input/{0}_columns.csv".format(prefix)
    node_outputfile = "./data/intermediate/{}_table_nodes.pickle".format(prefix)
    node_dict = {}

    with open(inputfile) as f:
        csv_reader = csv.reader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                node_dict[row[1]] = { 'type': 'BASE TABLE', 'schema': row[0]}
                line_count += 1
    if write_file:
        with open(node_outputfile,'wb') as node_dict_file:
            pickle.dump( node_dict, node_dict_file )
    return node_dict

if __name__ == "__main__":
    node_dict, edge_list = tableload_prepare_graph_input("test", write_file=False)
    print("table load nodes: {0}, table load edges: {1}".format(len(node_dict), len(edge_list)))
    node_dict, edge_list = tableload_schemaonly_prepare_graph_input("test", write_file=False)
    print("table load schema nodes: {0}, table load schema edges: {1}".format(len(node_dict), len(edge_list)))
    node_dict, edge_list = viewdefinitions_graph_input("test", write_file=False)
    print("viewdefinition nodes: {0}, viewdefinition edges: {1}".format(len(node_dict), len(edge_list)))
    node_dict, edge_list = viewdefinitions_schemaonly_graph_input("test", write_file=False)
    print("viewdefinition scheme nodes: {0}, viewdefinition schema edges: {1}".format(len(node_dict), len(edge_list)))
    node_dict, edge_list = columns_prepare_graph_input("test", write_file=False)
    print("column nodes: {0}, column edges: {1}".format(len(node_dict), len(edge_list)))
    node_dict, edge_list = primary_keys_prepare_graph_input("test", write_file=True)
    print("primary key nodes: {0}, primary key edges: {1}".format(len(node_dict), len(edge_list)))
    node_dict = tables_prepare_graph_input("test", write_file=False)
    print("table nodes: {0}".format(len(node_dict)))
    
    