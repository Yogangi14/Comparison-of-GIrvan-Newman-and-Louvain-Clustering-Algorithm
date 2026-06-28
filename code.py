#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# In[3]:


data_wiki = pd.read_csv('C:/Users/yogan/Downloads/wiki.txt', delimiter=" ")


# In[7]:


file_path = 'C:/Users/yogan/Downloads/wiki.txt'


# In[9]:


with open('C:/Users/yogan/Downloads/wiki.txt', 'r') as file:
    wiki_data = file.read()


# In[11]:


#creation of array nodes connectivity list
pair = [int(num) for num in wiki_data.split()]


# In[13]:


matrix_wiki = np.array(pair).reshape(-1, 2)


# In[15]:


np.set_printoptions(formatter={'int': lambda x: f'{x:,.0f}'})
print(matrix_wiki)


# In[17]:


shape = matrix_wiki.shape
print (shape)


# In[19]:


nodes_connectivity_list_wiki = np.unique(matrix_wiki, axis=0)


# In[21]:


import networkx as nx


# In[22]:


# creating a graph
wiki_graph = nx.Graph()
wiki_graph.add_edges_from(nodes_connectivity_list_wiki)


# In[25]:


import gc
gc.collect()


# In[27]:


from collections import defaultdict


# In[29]:


## for edge betweeness function
def calculate_edge_betweenness(G):
    edge_betweenness = defaultdict(float)

    for source in G.nodes():
        # Perform a BFS from each node
        shortest_paths, predecessors = single_source_shortest_path(G, source)

        # Counting the number of shortest paths passing through each edge
        edge_flow = defaultdict(float)
        for target in G.nodes():
            if target == source:
                continue
            stack = []
            node_dependencies = defaultdict(float)
            stack.append(target)
            
            while stack:
                current_node = stack.pop()
                if current_node not in predecessors:
                    continue
                for pred in predecessors[current_node]:
                    proportion = shortest_paths[pred] / shortest_paths[current_node]
                    flow_contribution = (1 + node_dependencies[current_node]) * proportion
                    edge = tuple(sorted([pred, current_node]))
                    edge_flow[edge] += flow_contribution
                    node_dependencies[pred] += flow_contribution
                    if pred != source:
                        stack.append(pred)
                        
        # summation of edge flow to the overall betweenness score
        for edge, flow in edge_flow.items():
            edge_betweenness[edge] += flow
    
    # Normalization of the edge betweenness values
    for edge in edge_betweenness:
        edge_betweenness[edge] /= 2

    return edge_betweenness

def single_source_shortest_path(G, source):
    """Helper function to calculate shortest paths and predecessors for BFS."""
    # Shortest path counts to each node from source
    shortest_paths = defaultdict(lambda: 0)
    shortest_paths[source] = 1

    # BFS to calculate shortest paths and their predecessors
    queue = [source]
    predecessors = defaultdict(list)

    levels = defaultdict(lambda: float('inf'))
    levels[source] = 0

    while queue:
        current_node = queue.pop(0)
        current_level = levels[current_node]
        
        for neighbor in G.neighbors(current_node):
            if levels[neighbor] == float('inf'):  # First time visiting this node
                levels[neighbor] = current_level + 1
                queue.append(neighbor)
            if levels[neighbor] == current_level + 1:  # Shortest path to this neighbor found
                shortest_paths[neighbor] += shortest_paths[current_node]
                predecessors[neighbor].append(current_node)

    return shortest_paths, predecessors


# In[31]:


edge_betweenness = calculate_edge_betweenness(wiki_graph)

# Print the edge betweenness centrality
for edge, betweenness in edge_betweenness.items():
    print(f"Edge {edge}: Betweenness = {betweenness:.4f}")


# In[ ]:


## calculation of modularity

def calculate_modularity(G, partition):
    """
    Calculate the modularity of a given partition for an unweighted graph G.

    Parameters:
    - G (networkx.Graph): The graph for which modularity is calculated.
    - partition (dict): A dictionary where keys are nodes and values are community IDs.

    Returns:
    - modularity (float): The modularity of the partition.
    """
    # No. of edges in the graph
    m = G.number_of_edges()
    
    # Initial modularity
    Q = 0.0
    
    # Degree of each node
    degree = dict(G.degree())
    
    # Iterate over each pair of nodes
    for i in G.nodes():
        for j in G.nodes():
            if partition[i] == partition[j]:  # Check if nodes are in the same community
                A_ij = 1 if G.has_edge(i, j) else 0  # Adjacency matrix entry
                Q += A_ij - ((degree[i] * degree[j]) /(2* m))
    
    # Normalize by the number of edges
    Q /= (2 * m)
    
    return Q




# In[674]:


## COMMUNITY DISTRIBUTION USING GIRVAN NEWMAN****
# Calculate betweenness centrality for edges
edge_betweenness = calculate_edge_betweenness(G)

# Sort edges by betweenness centrality
sorted_edges = sorted(edge_betweenness.items(), key=lambda x: x[1], reverse=True)

# Remove the edge with the highest betweenness centrality
G.remove_edge(*sorted_edges[0][0])

# my stopping criterion is by observing the graph
plt.figure(figsize=(10, 6))
nx.draw(wiki_graph, with_labels=True, node_color='lightblue', edge_color='gray')
plt.title("Graph of wiki (Girvan-Newman Algorithm)")
plt.savefig("grirvan_wiki_communities.png", format="png")
plt.show()

# Check connected components (communities)
communities = list(nx.connected_components(wiki_graph))
print("Communities after Girvan-Newman algorithm:")
for i, community in enumerate(communities):
    print(f"Community {i+1}: {community}")


# In[974]:


def communities_to_partition(communities):
    """
    Parameters:
    - communities (list of sets or tuples): A list where each element is a set/tuple of nodes belonging to the same community.

    Returns:
    - partition_dict: A dictionary with nodes as keys and community IDs as values.
    """
    partition_dict = {}
    for idx, community in enumerate(communities):
        for node in community:
            partition_dict[node] = idx
    return partition_dict
    
partition_dict_wiki = communities_to_partition(communities)

# Print the resulting partition dictionary
print(partition_dict_wiki)


# In[1000]:


modularity_score_wiki = calculate_modularity(wiki_graph, partition_dict_wiki)
print("Modularity wiki:", modularity_score_wiki)


# In[891]:


#question 2 for community matrix(to be run)
def girvan_newman_community_matrix(G):
    n = len(G.nodes)
    community_mat = []
    
    # Clone the graph so we don't modify the original
    G_copy = wiki_graph.copy()
    
    # Keep track of the initial community (all nodes in one community)
    communities = [list(G.nodes)]
    community_mat.append([0] * n)
    
    while len(G_copy.edges) > 0:
        # Calculate edge betweenness
        edge_betweenness = calculate_edge_betweenness(G_copy)
        
        # Find the edge with the highest betweenness and remove it
        max_betweenness_edge = max(edge_betweenness, key=edge_betweenness.get)
        G_copy.remove_edge(*max_betweenness_edge)
        
        # Find the current communities
        communities = list(nx.connected_components(G_copy))
        
        # Create a community label array for this level
        current_level = np.zeros(n, dtype=int)
        
        for i, community in enumerate(communities):
            for node in community:
                current_level[node] = i
                
        community_mat.append(current_level.tolist())
    
    # Convert the community matrix to a numpy array and transpose it
    community_mat = np.array(community_mat).T
    
    return community_mat



print("Community Matrix (nodes x levels):")
print(wiki_graph)


# In[941]:


import time


# In[893]:


#question 3 dendogramfrom scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import linkage

def create_linkage_matrix(data, method='ward'):
    """
    Creates a linkage matrix for hierarchical clustering.
    """
    linked = linkage(community_mat, method=method)
    return linked

   


# In[895]:


print(community_mat)


# In[897]:


linked_matrix_wiki = create_linkage_matrix(community_mat, method='ward')

print("Linkage Matrix:")
print(linked_matrix_wiki)


# In[78]:


import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt


# In[805]:


# Plot the dendrogram
plt.figure(figsize=(10, 7))
dendrogram = sch.dendrogram(linked_matrix)
plt.title("Community Wiki")
plt.xlabel("Communities")
plt.ylabel("Distance")
plt.savefig("community_wiki_dendrogram.png", format='png', dpi=100)
plt.show()


# In[40]:


# creating a graph
wiki_graph = nx.Graph()
wiki_graph.add_edges_from(nodes_connectivity_list_wiki)


# In[42]:


import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

def compute_modularity_gain_unweighted(G, node, community, partition, degree_sum, m):
    in_degree = sum(1 for neighbor in G.neighbors(node) if partition[neighbor] == community)
    total_degree = degree_sum[community]
    node_degree = G.degree(node)
    gain = (in_degree / m) - (total_degree * node_degree) / (2 * m * m)
    return gain

def louvain_full_phase_iteration_unweighted(G, max_iterations=10):
    m = G.number_of_edges()
    degree_sum = defaultdict(float)
    
    partition = {node: node for node in G.nodes()}
    
    for node, comm in partition.items():
        degree_sum[comm] += G.degree(node)
    
    improvement = True
    iteration_count = 0
    
    while improvement and iteration_count < max_iterations:
        improvement = False
        iteration_count += 1
        
        for node in G.nodes():
            current_community = partition[node]
            best_community = current_community
            best_gain = 0.0
            
            for neighbor in G.neighbors(node):
                community = partition[neighbor]
                if community != current_community:
                    gain = compute_modularity_gain_unweighted(G, node, community, partition, degree_sum, m)
                    if gain > best_gain:
                        best_gain = gain
                        best_community = community
            
            if best_community != current_community:
                partition[node] = best_community
                degree_sum[current_community] -= G.degree(node)
                degree_sum[best_community] += G.degree(node)
                improvement = True
    
    # Count the number of unique partitions (communities)
    num_partitions = len(set(partition.values()))
    print(f"Iterations completed: {iteration_count}")
    print(f"Number of partitions: {num_partitions}")
    
    return partition, num_partitions

def plot_communities(G, partition, title="Louvain Algorithm: Communities After One Full Phase"):
    colors = [partition[node] for node in G.nodes()]
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_size=300, cmap=plt.cm.Set3, node_color=colors)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color="black")
    plt.title(title)
    plt.savefig("community_louvain.png", format='png', dpi=100)
    plt.show()

# Run one full phase iteration of the Louvain algorithm for unweighted graphs with limited iterations
partition, num_partitions = louvain_full_phase_iteration_unweighted(wiki_graph, max_iterations=1)

# Plot the resulting communities
plot_communities(wiki_graph, partition, title=f"Communities After One Full Phase Iteration ({num_partitions} Partitions)")


# In[7]:


from collections import defaultdict


# In[852]:


#import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage


# In[859]:


import networkx as nx
import matplotlib.pyplot as plt


# In[861]:


import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch


# In[ ]:


get_ipython().run_cell_magic('time', '', '# Example code block to measure execution time\nimport time\n\ntime.sleep(8612)\nprint("This code took some time to execute.")\n')


# In[44]:


data_latfm_edges = pd.read_csv('C:/Users/yogan/Downloads/lastfm_asia/lasftm_asia/lastfm_asia_edges.csv', delimiter=" ")


# In[46]:


with open('C:/Users/yogan/Downloads/lastfm_asia/lasftm_asia/lastfm_asia_edges.csv', 'r') as file:
    lastfm = file.read()


# In[48]:


file_path2 = 'C:/Users/yogan/Downloads/lastfm_asia/lasftm_asia/lastfm_asia_edges.csv'
lastfm_edges = np.loadtxt(file_path2, delimiter=',')

# n*2 matrix nodes connectivity list
print(lastfm_edges)


# In[50]:


array_scientific = np.array(lastfm_edges)


# In[52]:


matrix_lastfm_edges = array_scientific.astype(int)
print(matrix_lastfm_edges)


# In[54]:


nodes_connectivity_list_lastfm = np.unique(matrix_lastfm_edges, axis=0)


# In[56]:


lastfm_graph = nx.Graph()
lastfm_graph.add_edges_from(nodes_connectivity_list_lastfm)


# In[58]:


oop = nodes_connectivity_list_lastf.shape
print(oop)


# In[1049]:


## Girvan newman algo for lastfm
# Calculate betweenness centrality for edges
edge_betweenness = calculate_edge_betweenness(G)

# Sort edges by betweenness centrality
sorted_edges = sorted(edge_betweenness.items(), key=lambda x: x[1], reverse=True)

# Remove the edge with the highest betweenness centrality
G.remove_edge(*sorted_edges[0][0])

# my stopping criterion is by observing the graph
plt.figure(figsize=(10, 6))
nx.draw(wiki_graph, with_labels=True, node_color='lightblue', edge_color='gray')
plt.title("Graph of lastfm (Girvan-Newman Algorithm)")
plt.savefig("grirvan_lastfm_communities.png", format="png")
plt.show()

# Check connected components (communities)
communities_lastfm = list(nx.connected_components(lastfm_graph))
print("Communities after Girvan-Newman algorithm:")
for i, community in enumerate(communities_lastfm):
    print(f"Community {i+1}: {community}")


# In[1103]:


## modularity test for lastfm
partition_dict_lastfm = communities_to_partition(communities_lastfm)
modularity_score_lastfm = calculate_modularity(lastfm_graph, partition_dict_lastfm)
print("Modularity lastfm gn:", modularity_score_lastfm)


# In[1101]:


def girvan_newman_community_matrix(G):
    n = len(G.nodes)
    community_mat_lastfm = []
    
    # Clone the graph so we don't modify the original
    G_copy_lastfm = lastfm_graph.copy()
    
    # Keep track of the initial community (all nodes in one community)
    communities = [list(G.nodes)]
    community_mat_lastfm.append([0] * n)
    
    while len(G_copy.edges) > 0:
        # Calculate edge betweenness
        edge_betweenness = calculate_edge_betweenness(G_copy_lastfm)
        
        # Find the edge with the highest betweenness and remove it
        max_betweenness_edge = max(edge_betweenness, key=edge_betweenness.get)
        G_copy_lastfm.remove_edge(*max_betweenness_edge)
        
        # Find the current communities
        communities = list(nx.connected_components(G_copy_lastfm))
        
        # Create a community label array for this level
        current_level = np.zeros(n, dtype=int)
        
        for i, community in enumerate(communities):
            for node in community:
                current_level[node] = i
                
        community_mat_lastfm.append(current_level.tolist())
    
    # Convert the community matrix to a numpy array and transpose it
    community_mat_lastfm = np.array(community_mat_lastfm).T
    
    return community_mat_lastfm



print("Community Matrix (nodes x levels):")
print(lastfm_graph)


# In[1117]:


## dendrogram for lastfm
from scipy.cluster.hierarchy import linkage


linked_lastfm= linkage(nodes_connectivity_list_lastfm, method='ward')



# In[1120]:


# Plot the dendrogram
plt.figure(figsize=(10, 7))
dendrogram = sch.dendrogram(linked_lastfm)
plt.title("Community lastfm")
plt.xlabel("Communities")
plt.ylabel("Distance")
plt.savefig("community_lastfm_dendrogram.png", format='png', dpi=100)
plt.show()


# In[60]:


def plot_communities(G, partition, title="Louvain Algorithm: Communities After One Full Phase"):
    colors = [partition[node] for node in G.nodes()]
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(G, pos, node_size=300, cmap=plt.cm.Set3, node_color=colors)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color="black")
    plt.title(title)
    plt.savefig("community_louvain_lastfm.png", format='png', dpi=100)
    plt.show()

# Run one full phase iteration of the Louvain algorithm for unweighted graphs with limited iterations
partition, num_partitions = louvain_full_phase_iteration_unweighted(lastfm_graph, max_iterations=1)

# Plot the resulting communities
plot_communities(lastfm_graph, partition, title=f"Communities After One Full Phase Iteration ({num_partitions} Partitions)")


# In[62]:


pip install ipynb-py-converter


# In[ ]:




