import math
import networkx as nx
import random

class CircleGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node, size = None):
        if size is None:
            size = 0
        elif not (0 <= size):
            raise ValueError("Node size must be positive")
        self.graph.add_node(node, size=size)

    def add_edge(self, node1, node2, weight=None):
        if weight is None:
            weight = random.uniform(0, 1)
        elif not (0 <= weight <= 1):
            raise ValueError("Edge weight must be between 0 and 1")
        if not self.graph.has_node(node1):
            self.add_node(node1)
        if not self.graph.has_node(node2):
            self.add_node(node2)
        self.graph.add_edge(node1, node2, weight=weight)

    def get_circle_size(self, node):
        if self.graph.has_node(node):
            return self.graph.nodes[node]['size']
        return None

    def get_connectivity(self, node1, node2):
        if self.graph.has_edge(node1, node2):
            return self.graph[node1][node2]['weight']
        return None
    
    def get_neighbors(self, node):
        return list(self.graph.successors(node))
    
    def find_inefficiencies(self):
        # any circle whose interconnectivity is less than its connectivity to another circle
        inefficiencies = []
        for i in range(self.graph.number_of_nodes()):
            for j in range(self.graph.number_of_nodes()):
                if i == j: continue
                if self.get_connectivity(i, j) > self.get_connectivity(i, i):
                    inefficiencies.append([i, j])
        return inefficiencies

    def get_intraconnectivities(self):
        return [self.get_connectivity(i, i) for i in range(self.graph.number_of_nodes())]
    
    # adding a connection between two nodes in two circles
    def add_connection(self, node1, node2, n=1):
        # will increase connectivity between the two circles by 1 / (n1 * n2)
        new_value = min(1, self.graph[node1][node2]['weight'] + n / 
                        (self.graph.nodes[node1]['size'] * self.graph.nodes[node2]['size']))
        self.graph[node1][node2]['weight'] = new_value

    # adding a member to a circle with no connections
    def add_member(self, node, connect_self=0.0):
        # will reduce connectivity between node and all nodes
        # conn = sum / (n1*n2)
        # conn_new = sum / ((n1+1)*n2)
        # We know: n1, n2, and conn
        # sum = conn * n1 * n2
        # conn_new = conn * n1 * n2 / (n1 + 1) * n2
        # conn_new = (conn * n1) / (n1 + 1)
        for i in range(self.graph.number_of_nodes):
            self.graph[node][i]['weight'] = (self.graph[node][i]['weight'] * self.graph.nodes[node]['size']) / (self.graph.nodes[node]['size'] + 1)
        # for connect_self percentage
        self.add_connection(node, node, math.floor(self.graph.nodes[node]['size'] * connect_self))

    def display(self):
        print("Circle sizes")
        for node in self.graph.nodes:
            print(f"Circle {node}: {self.get_circle_size(node)} members")
        print("\nCircle to Circle Connectivity:")
        for edge in self.graph.edges(data=True):
            print(f"{edge[0]} -> {edge[1]}: {edge[2]['weight']:.3f}")
