# read from csv generated from a query of the information schema
# 
# TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME
# A,A_T1,cola
# A,A_T1,colb
#
# column info of tables and views that are already nodes in the graph.
# We add columns as nodes, with edges to the table they are part of. They are identified by their 
#  name, which means that one column can have edges to many tables.
# We also assume that the table names are unique across schemas ( we could check the schema attribute but don't )
# The structure is written as files with node_dict, edges_list to be digested by a networkx graph
# 
# Using a dict for the nodes for consistency with the tables / views which have attributes
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--prefix", default="test",
                    help="prefix xxx of data/input/xxx_table_columns.csv", metavar="FILE")

args = parser.parse_args()
inputfile = "./data/input/{0}_table_columns.csv".format(args.prefix)
node_outputfile = "./data/intermediate/{}_columns_nodes.pickle".format(args.prefix)
edge_outputfile = "./data/intermediate/{}_columns_edges.pickle".format(args.prefix)

import csv, pickle

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

with open(node_outputfile,'wb') as node_dict_file:
    pickle.dump( node_dict, node_dict_file )

with open(edge_outputfile,'wb') as edge_list_file:
    pickle.dump( edge_list, edge_list_file)

