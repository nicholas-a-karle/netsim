import random
import networkx as nx

from circle_social_graph import CircleGraph
from raw_social_graph import SocialGraph

# long process
# cluster finding needed
def to_circle_from_social(socialGraph: SocialGraph, n=2, m=5, self_enumerate=True) -> CircleGraph:
    clusters = []

    if self_enumerate:
        clusters = socialGraph.find_clusters()
    else:
        for i in range(n, m):
            clusters_group = socialGraph.find_k_clusters(i)
            for cluster in clusters_group:
                clusters.append(cluster)


    interconnectivity = [[0 for _ in clusters] for __ in clusters]

    for i in range(len(clusters)):
        for j in range(len(clusters)):
            cluster_a = clusters[i]
            cluster_b = clusters[j]

            c_sum = 0
            c_max = len(cluster_a) * len(cluster_b)
            for a in cluster_a:
                for b in cluster_b:
                    if socialGraph.has_edge(a, b): c_sum += 1

            interconnectivity[i][j] = c_sum / c_max
    
    circleGraph = CircleGraph()
    for i in range(len(clusters)):
        circleGraph.add_node(i, len(clusters[i]))

    for i in range(len(interconnectivity)):
        for j in range(len(interconnectivity[i])):
            circleGraph.add_edge(i, j, interconnectivity[i][j])

    return circleGraph

#
# runs a basic simulation on a raw Social Graph
# type indicates what level of complexity it does
# where r = reconnectivity
# where P = P(edge appears)
# type:
# random    -> Complete Random (base case)          P = r / (max(|E|) - |E|)
# neighbors -> Neighbors increase likelihood        P = r * |N| / (avg(|N|) * (max(|E|) - |E|))
# distance  -> Distance decreases likelihood        P = r * avg(|D|) / (D * (max(|E|) - |E|))
#                   avg(|D|) is graph wide for all pairs, not for single node
# 
# This function maintains a similar amount of reconnections no matter the type or state of the graph
# If a different reconnecitivty is needed, use the functin social_sim_reconnect (tbd)
# 
def reconnect(socialGraph: SocialGraph, type = "distance", reconnectivity = 0.1) -> None:

    max_e_min_e = socialGraph.graph.number_of_nodes * (socialGraph.graph.number_of_nodes - 1) - socialGraph.graph.number_of_edges
    
    # random    -> Complete Random (base case)          P = r / (max(|E|) - |E|)
    if type == "random":
        # check each node
        for i in range(socialGraph.graph.number_of_nodes):
            for j in range(socialGraph.graph.number_of_nodes):
                if i == j or socialGraph.has_edge(i, j): continue
                p = reconnectivity / max_e_min_e
                if random.random() < p: socialGraph.add_edge(i, j)
    
    # neighbors -> Neighbors increase likelihood        P = r * |N| / (avg(|N|) * (max(|E|) - |E|))
    elif type == "neighbors":

        # find avg(|N|)
        avg_n = sum(dict(socialGraph.graph.degree()).values()) / len(socialGraph.graph.nodes())

        # check each node
        for i in range(socialGraph.graph.number_of_nodes):
            for j in range(socialGraph.graph.number_of_nodes):
                if i == j or socialGraph.has_edge(i, j): continue
                p = reconnectivity * len(socialGraph.get_neighbors(i)) / (avg_n * max_e_min_e)
                if random.random() < p: socialGraph.add_edge(i, j)
    
    # distance  -> Distance decreases likelihood        P = r * avg(|D|) / (D * (max(|E|) - |E|))
    elif type == "distance":

        # find distances
        dist = nx.floyd_warshall(socialGraph)

        # get the average distance
        total_dist = 0
        count = 0
        for source, target_lengths in dist.items():
            for target, length in target_lengths.items():
                total_dist += length
                count += 1
        avg_dist = total_dist / count

        # check each node
        for i in range(socialGraph.graph.number_of_nodes):
            for j in range(socialGraph.graph.number_of_nodes):
                if i == j or socialGraph.has_edge(i, j): continue
                p = reconnectivity * avg_dist / (dist[i][j] * max_e_min_e)
                if random.random() < p: socialGraph.add_edge(i, j)