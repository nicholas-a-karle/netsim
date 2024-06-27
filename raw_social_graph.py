import networkx as nx
import community
from sklearn.cluster import KMeans

class SocialGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def remove_edge(self, node1, node2):
        self.graph.remove_edge(node1, node2)

    def has_node(self, node):
        return self.graph.has_node(node)

    def has_edge(self, node1, node2):
        return self.graph.has_edge(node1, node2)

    def get_edge(self, node1, node2):
        return self.graph.has_edge(node1, node2)

    def get_neighbors(self, node):
        return list(self.graph.successors(node))
    
    def find_clusters(self):
        partition = community.best_partition(self.graph.to_undirected())
        clusters = {}
        for node, comm_id in partition.items():
            if comm_id not in clusters:
                clusters[comm_id] = []
            clusters[comm_id].append(node)
        return list(clusters.values())
    
    def find_k_clusters(self, n_clusters):
        # Convert graph to an adjacency matrix
        adj_matrix = nx.to_numpy_array(self.graph)
        
        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(adj_matrix)
        
        # Create clusters based on KMeans labels
        clusters = {i: [] for i in range(n_clusters)}
        for node, label in zip(self.graph.nodes, kmeans.labels_):
            clusters[label].append(node)
        
        return list(clusters.values())
    
    def display_simple(self):
        print(f"Raw Social Graph:")
        connectivity = self.graph.number_of_edges() / ((self.graph.number_of_nodes() - 1) * self.graph.number_of_nodes())
        print(f"\tNumber of nodes: {self.graph.number_of_nodes()}")
        print(f"\tNumber of edges: {self.graph.number_of_edges()}")
        print(f"\tConnectivity:    {connectivity:.4f}")
        return self.graph.number_of_nodes(), self.graph.number_of_edges(), connectivity

    def display_complex(self):
        print(f"Raw Social Graph:")
        for node in self.graph.nodes:
            print(f"{node}: {self.get_neighbors(node)}")
        print("Edges with weights:")
        for edge in self.graph.edges(data=True):
            print(f"{edge[0]} -> {edge[1]}: {edge[2]['weight']}")

    def display(self, complex = False):
        if complex: return self.display_complex()
        else: return self.display_simple()