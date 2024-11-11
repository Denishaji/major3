import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV data
file_path = 'data_scopus.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Data Cleaning: Drop rows with missing values in 'Authors' and 'Authors with affiliations'
df.dropna(subset=['Authors', 'Authors with affiliations'], inplace=True)

# Initialize a NetworkX graph
G = nx.Graph()

# Iterate through each row to build nodes and edges
for _, row in df.iterrows():
    # Parse authors
    authors = [author.strip() for author in row['Authors'].split(',')]
    
    # Parse authors with affiliations
    affiliations_list = row['Authors with affiliations'].split(';')
    
    # Add nodes with attributes
    for affiliation in affiliations_list:
        if affiliation.strip():
            # Extract the author's name from the affiliation (first part before the comma)
            author_name = affiliation.split(',')[0].strip()
            # Extract the country (last part after the comma)
            country = affiliation.split(',')[-1].strip()
            
            # Add node with attributes
            for author in authors:
                if author_name.split()[0] in author:  # Check if the first name matches
                    if author not in G:
                        G.add_node(author, 
                                   country=country,
                                   title=row['Title'],  # Add title as a node attribute
                                   year=row['Year'])  # Add year as a node attribute

    # Create links between co-authors (edges)
    for i in range(len(authors)):
        for j in range(i + 1, len(authors)):
            # Add edges between co-authors
            G.add_edge(authors[i], authors[j])

# Export the graph to JSON
graph_data = nx.node_link_data(G)

# Save the graph data to a file
output_path = 'author_network_graph.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=4)

print("NetworkX graph data in JSON format created successfully")

# Drawing the graph
plt.figure(figsize=(12, 12))

# Layout the graph
pos = nx.spring_layout(G, k=0.15, iterations=20)

# Draw the nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue', alpha=0.7)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color='gray')

# Add labels for the nodes
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

# Display the graph
plt.title("Author Collaboration Network")
plt.axis('off')  # Hide the axes
plt.show()
