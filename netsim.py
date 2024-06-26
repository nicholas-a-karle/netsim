# 
# Goal is to simulate an arbitrarily large network with minimal notes on its nature
# 
# Circles:
#   Basically assign each circle a number of nodes
#   Note the interconnectivity of the circle
#   Note the intraconnectivity of the circle with other circles
#   
#   Given N nodes and K Circles
#   Complexity is reliant on K
#   K + K * (K - 1) = K ** 2 in memory
#   Effectively just creates a graph of the groups
#   A node can belong to any number of circles
#   It is possible to have too many circles to make this more efficient
#   This point is where K > N, simple
# 

import random

from circle_social_graph import *
from raw_social_graph import *
from social_graph import *

def sum_true(arr):
    s = 0
    for elem in arr:
        if elem: s += 1
    return s

def true_ind(arr):
    for i in range(len(arr)):
        if arr[i]: return i
    return None


if __name__ == "__main__":
    SG = SocialGraph()
    N = 100
    C = 0.25

    for i in range(N):
        SG.add_node(i)

    for i in range(N):
        for j in range(N):
            if i == j: continue
            if random.random() < C:
                SG.add_edge(i, j)

    print("Running...\n\n")
    CG = to_circle_from_social(SG)

    CG.display()
    
