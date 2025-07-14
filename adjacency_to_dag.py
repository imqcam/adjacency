import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

# Load the CSV file (update the file path as needed)
file_path = "Table2.csv"
df = pd.read_csv(file_path)

# Standardize and Clean Names
standard_names = {
    "Rollett": "Rollett", "Ma": "Ma", "Wong": "Wong", "Sun": "Sun",
    "Taheri-Mousavi": "Taheri-Mousavi", "Webler": "Webler", "Narra": "Narra",
    "Oskay": "Oskay", "Lewandowski": "Lewandowski", "Ghosh": "Ghosh",
    "Mahadevan & Karve": "Mahadevan & Karve", "SWRI": "SWRI", "Green": "Green"
}

def clean_name(name):
    name = str(name).strip().replace("\n", " ")
    for key in standard_names.keys():
        if key.lower() in name.lower():
            return standard_names[key]
    return name

# Convert all values to strings and handle missing values
df = df.fillna("")
donors = df.iloc[:, 0].astype(str).apply(clean_name)
recipients = df.iloc[:, 1].astype(str).apply(lambda x: [clean_name(name) for name in x.split("\n") if name.strip()])

# Create Weighted Adjacency Graph
G_weighted = nx.DiGraph()
weighted_edges = {}
for donor, rec_list in zip(donors, recipients):
    for recipient in rec_list:
        if donor and recipient:
            weighted_edges[(donor, recipient)] = weighted_edges.get((donor, recipient), 0) + 1

for (donor, recipient), weight in weighted_edges.items():
    G_weighted.add_edge(donor, recipient, weight=weight)

# Display Weighted Adjacency Matrix
adj_matrix = nx.to_pandas_adjacency(G_weighted, dtype=int)
display(adj_matrix)

# Force-Directed Graph Visualization
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_weighted, seed=42, k=0.5)
edges = G_weighted.edges(data=True)
weights = [d['weight'] for _, _, d in edges]

nx.draw(G_weighted, pos, with_labels=True, node_size=2500, node_color="lightblue", edge_color="gray", font_size=10, font_weight="bold", arrows=True, width=weights)
plt.title("Force-Directed Weighted Adjacency Graph", fontsize=14)
plt.show()

# Hierarchical Graph Visualization
plt.figure(figsize=(12, 8))
pos_hierarchy = graphviz_layout(G_weighted, prog="dot")
nx.draw(G_weighted, pos_hierarchy, with_labels=True, node_size=2500, node_color="lightblue", edge_color="gray", font_size=10, font_weight="bold", arrows=True, width=weights)
plt.title("Hierarchical Weighted Adjacency Graph", fontsize=14)
plt.show()

# Nauru-Style (Radial) Graph Visualization
plt.figure(figsize=(12, 8))
pos_radial = nx.shell_layout(G_weighted)
nx.draw(G_weighted, pos_radial, with_labels=True, node_size=2500, node_color="lightblue", edge_color="gray", font_size=10, font_weight="bold", arrows=True, width=weights)
plt.title("Radial (Nauru-Style) Weighted Adjacency Graph", fontsize=14)
plt.show()

# Convert to DAG if possible
def check_and_convert_to_dag(G):
    try:
        cycle = nx.find_cycle(G, orientation="original")
        print("Cycle detected! The graph is not a DAG. Suggested edges to remove:")
        print(cycle)
        return None
    except nx.NetworkXNoCycle:
        print("No cycles detected. The graph is a DAG.")
        return nx.DiGraph(G)  # Return a copy as DAG

G_dag = check_and_convert_to_dag(G_weighted)

# Visualize DAG if valid
if G_dag:
    plt.figure(figsize=(12, 8))
    pos_dag = graphviz_layout(G_dag, prog="dot")
    nx.draw(G_dag, pos_dag, with_labels=True, node_size=2500, node_color="lightblue", edge_color="gray", font_size=10, font_weight="bold", arrows=True, width=weights)
    plt.title("Directed Acyclic Graph (DAG) Representation", fontsize=14)
    plt.show()