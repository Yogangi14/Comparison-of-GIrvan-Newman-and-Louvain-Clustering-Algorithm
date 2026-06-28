# Comparison-of-GIrvan-Newman-and-Louvain-Clustering-Algorithm
Just an attempt to implement using Girvan-Newman and Louvain.
# Community Detection in Networks using Girvan–Newman and Louvain Algorithms

## Overview

This project implements and compares two popular community detection algorithms for complex networks:

* **Girvan–Newman Algorithm**
* **Louvain Algorithm**

The objective is to identify communities (clusters of densely connected nodes) in graphs and analyze their effectiveness, computational complexity, and modularity performance on real-world network datasets.

---

## Motivation

Many real-world systems can be represented as graphs, including:

* Social networks
* Citation networks
* Biological interaction networks
* Transportation systems
* Communication networks

Community detection helps uncover hidden structures within these networks by grouping nodes that interact more frequently with each other than with the rest of the network.

This project explores two fundamentally different approaches:

* **Girvan–Newman:** divisive, edge-removal based
* **Louvain:** greedy modularity optimization

---

## Algorithms

### 1. Girvan–Newman Algorithm

The Girvan–Newman algorithm detects communities by progressively removing edges with the highest **edge betweenness centrality**.

### Workflow

1. Compute edge betweenness centrality.
2. Remove the edge with the highest score.
3. Recalculate betweenness.
4. Repeat until communities emerge.

### Advantages

* Produces a hierarchical community structure.
* Easy to interpret.
* Suitable for small networks.

### Limitations

* Computationally expensive.
* Not scalable for large graphs.

---

### 2. Louvain Algorithm

The Louvain algorithm detects communities by maximizing **network modularity** through iterative optimization.

### Workflow

1. Assign every node to its own community.
2. Move nodes to neighboring communities if modularity increases.
3. Collapse detected communities into super-nodes.
4. Repeat until modularity converges.

### Advantages

* Extremely fast.
* Scales to millions of nodes.
* Produces high-quality community partitions.

### Limitations

* Greedy optimization may converge to local optima.
* Different runs can produce slightly different communities.

---

Let the graph be represented as

[
G=(V,E)
]

where

(V) is the set of nodes,
(E) is the set of edges,
(n=|V|),
(m=|E|).

The graph is stored as an adjacency matrix

[
A=[a_{ij}]
]

where

[
a_{ij}=
\begin{cases}
1,& \text{if nodes }i\text{ and }j\text{ are connected}\
0,& \text{otherwise}
\end{cases}
]

The implementation constructs this adjacency matrix using Pandas DataFrames and performs matrix operations using NumPy.

Girvan–Newman Algorithm

The Girvan–Newman algorithm identifies communities by iteratively removing edges with the highest edge betweenness centrality.

The edge betweenness of an edge (e) is

[
BC(e)=\sum_{s\neq t}
\frac{\sigma_{st}(e)}
{\sigma_{st}}
]

where

(\sigma_{st}) is the total number of shortest paths between nodes (s) and (t),
(\sigma_{st}(e)) is the number of those shortest paths passing through edge (e).

Algorithm steps:

Compute shortest paths between all node pairs.
Calculate edge betweenness.
Remove the edge with the maximum betweenness.
Recompute betweenness on the updated graph.
Repeat until the desired number of communities is obtained.
Louvain Algorithm

The Louvain algorithm detects communities by maximizing the network modularity.

The modularity is defined as

\frac{k_i k_j}{2m}
\right)
\delta(c_i,c_j)
]

where

(A_{ij}) is the adjacency matrix,
(k_i) is the degree of node (i),
(m) is the total number of edges,
(c_i) is the community containing node (i),
(\delta(c_i,c_j)=1) if nodes belong to the same community, otherwise (0).

The modularity gain obtained by moving node (i) into community (C) is

\left(
\frac{k_i}
{2m}
\right)^2
\right]
]

where

(\Sigma_{in}) is the total weight of edges inside community (C),
(\Sigma_{tot}) is the sum of degrees of nodes in (C),
(k_i) is the degree of node (i),
(k_{i,in}) is the sum of weights from node (i) to nodes in (C).

The algorithm repeatedly moves nodes to neighboring communities whenever (\Delta Q>0), and then aggregates communities into super-nodes until modularity converges.

Computational Complexity
Algorithm	Time Complexity
Girvan–Newman	(O(nm^2)) (worst case)
Louvain	Approximately (O(n\log n)) in practice

## Usage

Run Girvan–Newman:

```bash
python src/girvan_newman.py
```

Run Louvain:

```bash
python src/louvain.py
```

Or execute the Jupyter notebooks for step-by-step analysis.

---

## Evaluation Metrics

The algorithms are compared using:

* Number of detected communities
* Modularity Score
* Execution Time
* Community Size Distribution
* Graph Visualization

---

## Results

The project compares both algorithms in terms of:

| Metric              | Girvan–Newman | Louvain   |
| ------------------- | ------------- | --------- |
| Speed               | Slow          | Fast      |
| Scalability         | Low           | High      |
| Modularity          | Good          | Excellent |
| Hierarchical Output | Yes           | No        |
| Large Graph Support | Limited       | Excellent |

---

## Applications

Community detection has applications in:

* Social network analysis
* Recommendation systems
* Fraud detection
* Protein interaction networks
* Brain connectivity analysis
* Financial transaction networks
* Transportation planning

---

## Future Improvements

* Leiden community detection algorithm
* Label Propagation Algorithm (LPA)
* Infomap algorithm
* Dynamic community detection
* GPU acceleration for large-scale graphs
* Interactive network visualization

---

## References

* Girvan, M., & Newman, M. E. J. (2002). *Community structure in social and biological networks.*
* Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). *Fast unfolding of communities in large networks.*

---

## License

This project is released under the MIT License.

---

## Author

Developed as part of a Data Analytics and Network Science project to study graph-based community detection techniques and compare classical and modularity-based approaches.
