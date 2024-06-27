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

def reconnect(socialGraph: SocialGraph, type = "distance", reconnectivity = 0.1, base_rand = 0.2) -> None:
    #
    # runs a basic simulation on a raw Social Graph
    # type indicates what level of complexity it does
    # where r = reconnectivity
    # where P = P(edge appears)
    # type:
    # random    -> Complete Random (base case)          P = r
    # neighbors -> Neighbors increase likelihood        P = r * |N| / avg(|N|)
    # distance  -> Distance decreases likelihood        P = r * avg(D) / D
    # distrand  -> Distance decreases likelihood        P = (r * avg(D) / D) * a + (r) * b
    #                   avg(|D|) is graph wide for all pairs, not for single node
    #                   a and b set in formula
    # 
    # This function maintains a similar amount of reconnections no matter the type or state of the graph
    # If a different reconnecitivty is needed, use the functin social_sim_reconnect (tbd)
    # 
    # base_rand: takes proportion of function away and makes it only based on the reconnectivity
    # 
    # random    -> Complete Random (base case)          P = r 
    if type == "random":
        # check each node
        for i in range(socialGraph.graph.number_of_nodes()):
            for j in range(socialGraph.graph.number_of_nodes()):
                if i == j or socialGraph.has_edge(i, j): continue
                p = reconnectivity
                #print(f"Prob({i}, \t{j}): \t{p}")
                if random.random() < p: socialGraph.add_edge(i, j)
    
    # neighbors -> Neighbors increase likelihood        P = r * |N| / avg(|N|)
    elif type == "neighbors":

        # find avg(|N|)
        avg_n = sum(dict(socialGraph.graph.degree()).values()) / len(socialGraph.graph.nodes())

        # check each node
        for i in range(socialGraph.graph.number_of_nodes()):
            for j in range(socialGraph.graph.number_of_nodes()):
                if i == j or socialGraph.has_edge(i, j): continue
                p = reconnectivity * len(socialGraph.get_neighbors(i)) / avg_n
                p = (1 - base_rand) * p + base_rand * reconnectivity
                #print(f"Prob({i}, \t{j}): \t{p}")
                if random.random() < p: socialGraph.add_edge(i, j)
    
    # distance  -> Distance decreases likelihood        P = r * avg(D) / D
    elif type == "distance":

        # find distances
        dist = nx.floyd_warshall(socialGraph.graph)

        # get the average distances
        avg_dist = [0.0 for i in range(len(socialGraph.graph))]
        for i in range(len(socialGraph.graph)):
            count = 0
            for j in range(len(socialGraph.graph)):
                if dist[i][j] != float("inf"):
                    count += 1
                    avg_dist[i] += dist[i][j]
            if count != 0:
                avg_dist[i] /= count
            else:
                avg_dist[i] = float("inf")

        # check each node
        for i in range(socialGraph.graph.number_of_nodes()):
            for j in range(socialGraph.graph.number_of_nodes()):
                if i == j or socialGraph.has_edge(i, j): continue

                if avg_dist[i] == float("inf") or dist[i][j] == float("inf"):
                    p = 0
                else:
                    p = reconnectivity * avg_dist[i] / dist[i][j]

                p = (1 - base_rand) * p + base_rand * reconnectivity
                #print(f"Prob({i}, \t{j}): \t{p}")
                if random.random() < p: socialGraph.add_edge(i, j)

def deconnect(socialGraph: SocialGraph, type = "distance", deconnectivity = 0.1, base_rand = 0.2) -> None:

    # fundamentally the same formula as above, but runs deconnections
    #
    # runs a basic simulation on a raw Social Graph
    # type indicates what level of complexity it does
    # where r = deconnectivity
    # where P = P(edge disappears)
    # type:
    # random    -> Complete Random (base case)          P = r
    # neighbors -> Neighbors decrease likelihood        P = r * avg(|N|) / |N|
    # distance  -> Distance increases likelihood        P = r * D / avg(D)
    #                   avg(|D|) is graph wide for all pairs, not for single node
    # 
    # This function maintains a similar amount of reconnections no matter the type or state of the graph
    # If a different reconnecitivty is needed, use the functin social_sim_reconnect (tbd)
    # 
    # random    -> Complete Random (base case)          P = r 
    if type == "random":
        # check each node
        for i in range(socialGraph.graph.number_of_nodes()):
            for j in range(socialGraph.graph.number_of_nodes()):
                if i == j or not socialGraph.has_edge(i, j): continue
                p = deconnectivity
                if random.random() < p: socialGraph.remove_edge(i, j)
    
    # neighbors -> Neighbors increase likelihood        P = r * |N| / avg(|N|)
    elif type == "neighbors":

        # find avg(|N|)
        avg_n = sum(dict(socialGraph.graph.degree()).values()) / len(socialGraph.graph.nodes())

        # check each node
        for i in range(socialGraph.graph.number_of_nodes()):
            for j in range(socialGraph.graph.number_of_nodes()):
                if i == j or not socialGraph.has_edge(i, j): continue
                p = deconnectivity * avg_n / len(socialGraph.get_neighbors(i))
                p = (1 - base_rand) * p + base_rand * deconnectivity
                if random.random() < p: socialGraph.remove_edge(i, j)
                
    
    # distance  -> Distance decreases likelihood        P = r * avg(D) / D
    elif type == "distance":

        # find distances
        dist = nx.floyd_warshall(socialGraph.graph)

        # get the average distances
        avg_dist = [0.0 for i in range(len(socialGraph.graph))]
        for i in range(len(socialGraph.graph)):
            count = 0
            for j in range(len(socialGraph.graph)):
                if dist[i][j] != float("inf"):
                    count += 1
                    avg_dist[i] += dist[i][j]
            if count != 0:
                avg_dist[i] /= count
            else:
                avg_dist[i] = float("inf")

        # check each node
        for i in range(socialGraph.graph.number_of_nodes()):
            for j in range(socialGraph.graph.number_of_nodes()):
                if i == j or not socialGraph.has_edge(i, j): continue

                if avg_dist[i] == float("inf") or dist[i][j] == float("inf"):
                    # Impossible for disconnect, left here anyways
                    p = 1
                else:
                    p = deconnectivity * dist[i][j] / avg_dist[i]
                
                p = (1 - base_rand) * p + base_rand * deconnectivity
                if random.random() < p: socialGraph.remove_edge(i, j)

def soc_sim(socialGraph: SocialGraph, dunbar = 100):
    # function to semi-realistically simulate socialization
    # all members of the graph have no geography
    # this means that the physical distance is not considered
    # only social distance will affect them
    
    # there will be a dunbar's number established
    # eventually will add ranks of dunbar-ity
    # ex:
    # rank          max
    # known         ~ 500
    # acquanited    ~ 200
    # friend        ~ 100
    # close         ~ 50
    # best          ~ 10
    #
    # dunbar's number will establish a multiplier to interactions
    # 
    # each person will
    # 



    return