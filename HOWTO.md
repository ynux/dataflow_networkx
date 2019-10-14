# How this Works

### Assumption on the Underlying Data Flow

This code was written to create a graph from a data flow like the following one:

1 - Tables are loaded, either from other tables, or from Views
2 - Views are built from tables

We can extract information from the load toal and the view defining sql:

1 - For every loaded table: schema_name, table_name, source_schema_name, source_object_name, source_object_type. 
2 - For every created view: schema_name, view_name, referenced_schema_name, referenced_object_name, referenced_object_type

### Input Format, and Rewriting it for Graph Digestion

This information comes as csv, like `test_tableload.csv` and `test_viewdefinitions.csv`. In our test data flow, a table is always created from only one view (or table). A view may use several tables, and a table may be referenced by several views.

Put your real data into `<prefix>_tableload.csv` and `<prefix>_viewdefinitions.csv`.

From one csv file, two pickle files are created: One containing the nodes (views and tables, with schema and type as attributes), the other the edges (references / loaded from). 
`viewdefinitions_graph_input.py` takes `prefix` as input and creates `<prefix>_viewdefinitions_nodes.pickle` and `<prefix>_viewdefinitions_edges.pickle`, 
`tableload_graph_input.py` takes `prefix` as input and creates `<prefix>_tableload_nodes.pickle` and `<prefix>_tableload_edges.pickle`. 

If you are only interested in the schemas:
`viewdefinitions_schemaonly_graph_input.py` creates `<prefix>_viewdefinitions_schemaonly_nodes.pickle` and `<prefix>_viewdefinitions_schemaonly_edges.pickle`, 
`tableload_schemaonly_graph_input.py` creates `<prefix>_tableload_schemaonly_nodes.pickle` and `<prefix>_tableload_schemaonly_edges.pickle`. 

### Playing With Graphs

_from here on, only notes_

Load the pickled node and edge information into a graph. DiGraph, MultiDiGraph

Create images, lists of predecessors, list of successors
Analysis of centrality

Bipartite graphs?

### Remark on Test Data

The test data is a simplified model of a datawarehouse with six layers:

* An input layer of tables **A**
* a second layer of tables **B** (e.g. to create history tables)
* a third layer of views **STG_C** (e.g. for some data cleaning)
* a fourth layer of tables **D** (think of these as materialized views of STG_C)
* a fifth layer of views **STG_D** (here, some serious joining is happening)
* a sixth layer of tables **D** (like materialized views of STG_D); this could be the final layer for consumption

While the first four layers are separate tracks and the relations are 1:1, from C to STG_D some join logic is applied and we have n:m dependencies. 
The table `T_B4` is a dead end and never consumed.
The table `T_C4` is a table coming in from some other system.
	

