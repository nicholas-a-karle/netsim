
import math
import random
import networkx as nx

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class social_network(nx.DiGraph):

    # s0 -> s1 indicates s0 likes s1

    def randomly_form_edges(self, form_chance = 0.1):
        for i in range(len(self)):
            for j in range(len(self)):
                if i == j: continue
                if random.random() < form_chance:
                    self.add_edge(i, j)

    def clear_edges(self):
        for i in range(len(self)):
            for j in range(len(self)):
                if self.has_edge(i, j):
                    self.remove_edge(i, j)

    def set_social_parameters(self, transitivity = 0.1, reciprocity = 0.1, negative_transitivity = 0.1, negative_reciprocity = 0.1, random_additions = 0.1, random_removals = 0.1):
        self.social_transitivity = transitivity
        self.social_reciprocity = reciprocity
        self.negative_social_transitivity = negative_transitivity
        self.negative_social_reciprocity = negative_reciprocity
        self.random_additions = random_additions
        self.random_removals = random_removals

    def add_nodes(self, num): 
        for i in range(num): self.add_node(len(self))
    
    # sims
    # the general rule is successors lower the likelihood of a new successor

    # node pair sims

    # make transitivity happen
    def transfer_sim(self, n0, n1):
        s0 = self.successors(n0)
        p0 = self.predecessors(n0)
        s1 = self.successors(n1)
        p1 = self.predecessors(n1)

        # the successors are liked by n
        # the predecessors like n

        # where the third node is m
        # if a succ of n0 is a pred of n1
        #   n0 -> m -> n1 => n0 -> n1
        #   n0 should become a pred of n1 (strong)

        # if a succ of n0 is a succ of n1
        #   n0 -> m <- n1 => n0 <-> n1
        #   n0 and n1 should like each other (weak)

        # if a pred of n0 is a pred of n1
        #   n0 <- m -> n1
        #   n0 and n1 should like each other (very weak)
        
        # if a pred of n0 is a succ of n1
        #   n0 <- m <- n1
        #   n0 should become a succ of n1 (strong)

        # if both have m as a predecessor
        #   very weak reciprocal positivity

        # if both have m as a successor
        #   weak reciprocal positivity

        # if m is pred in one and succ in the other
        #   the other has positive of the first

        # finding the predecessor -> m -> successor cases
        # brute force
        # note: the more successors, the weaker the transitivity of a single successor
        # n0 -> m -> n1
        n0_m_n1 = 0
        for s in s0:
            for p in p1:
                if s == p: n0_m_n1 += 1
        n0_m_n1 /= len(s0)
        n0_m_n1 *= self.social_transitivity
        # p = sum(n0_m_n1) * soc_trans / len(s0)
        if n0_m_n1 > random.random():
            self.add_edge(n0, n1)

        # n1 -> m -> n0
        n1_m_n0 = 0
        for s in s1:
            for p in p0:
                if s == p: n1_m_n0 += 1
        n1_m_n0 /= len(s1)
        n1_m_n0 *= self.social_transitivity
        if n1_m_n0 > random.random():
            self.add_edge(n1, n0)
        
    def neg_transfer_sim(self, n0, n1):
        # n0 -> m -> n1
        if self.has_edge(n0, n1):
            s0 = self.successors(n0)
            p1 = self.predecessors(n1)
            n0_m_n1 = 0
            for s in s0:
                for p in p1:
                    if s == p: n0_m_n1 += 1
            n0_m_n1 /= len(s0)
            n0_m_n1 = 1 - n0_m_n1
            n0_m_n1 *= self.negative_social_transitivity
            # p = neg_soc_tran (1 - sum(n0_m_n1) / len(s0))
            if n0_m_n1 > random.random():
                self.remove_edge(n0, n1)

        # n1 -> m -> n0
        if self.has_edge(n1, n0):
            p0 = self.predecessors(n0)
            s1 = self.successors(n1)
            n1_m_n0 = 0
            for s in s1:
                for p in p0:
                    if s == p: n1_m_n0 += 1
            n1_m_n0 /= len(s1)
            n1_m_n0 = 1 - n1_m_n0
            n1_m_n0 *= self.negative_social_transitivity
            if n1_m_n0 > random.random():
                self.remove_edge(n1, n0)

    def reciprocate_sim(self, n0, n1):
        n0_n1 = self.has_edge(n0, n1)
        n1_n0 = self.has_edge(n1, n0)

        # if neither: do nothing
        # if both: do nothing
        # if one: remove it or add the other

        # the more succ, the weaker the reciprocity
        # the more pred, the weaker the reciprocity
        if n0_n1 != n1_n0:
            if n0_n1:
                numall = len(self.successors(n1)) + len(self.predecessors(n1))
                # = sr * (1 / num succ + num pred)
                pp = self.social_reciprocity / numall
                # = nsr * (1 - 1 / num succ + num pred)
                pn = self.negative_social_reciprocity * (1 - 1 / numall)
                r = random.random()
                if r < pp:
                    self.add_edge(n1, n0)
                elif r < pp + pn:
                    self.remove_edge(n0, n1)
            elif n1_n0: # technically not needed
                numall = len(self.successors(n0)) + len(self.predecessors(n0))
                pp = self.social_reciprocity / numall 
                pn = self.negative_social_reciprocity * (1 - 1 / numall)
                r = random.random()
                if r < pp:
                    self.add_edge(n0, n1)
                elif r < pp + pn:
                    self.remove_edge(n1, n0)

    def random_actions_sim(self, n0, n1):
        if self.has_edge(n0, n1) and random.random() < self.random_removals:
            self.remove_edge(n0. n1)
        elif not self.has_edge(n0, n1) and random.random() < self.random_additions:
            self.add_edge(n0, n1)
        if self.has_edge(n1, n0) and random.random() < self.random_removals:
            self.remove_edge(n1, n0)
        elif not self.has_edge(n1, n0) and random.random() < self.random_additions:
            self.add_edge(n1, n0)

    # full graph sims (slight optimizations)

    # random actions on full graph
    def random_actions(self):
        for i in range(len(self)):
            for j in range(len(self)):
                if i == j: continue
                if self.has_edge(i, j):
                    if random.random() < self.random_removals:
                        self.remove_edge(i, j)
                else:
                    if random.random() < self.random_additions:
                        self.add_edge(i, j)
    """
    # found no significant improvement in any of these
    def random_actions_1(self):
        if self.random_removals > 0 or self.random_additions > 0:
            for i in range(len(self)):
                for j in range(len(self)):
                    if i == j: continue
                    
                    if self.random_removals > 0 and self.has_edge(i, j):
                        if random.random() < self.random_removals:
                            self.remove_edge(i, j)
                    elif self.random_additions > 0:
                        if random.random() < self.random_additions:
                            self.add_edge(i, j)

    def random_actions_2(self):
        if self.random_removals > 0 and not self.random_additions > 0:
            # only do removals
            for i in range(len(self)):
                for j in range(len(self)):
                    if i == j: continue
                    if self.has_edge(i, j) and random.random() < self.random_removals:
                        self.remove_edge(i, j)
                    

        elif not self.random_removals > 0 and self.random_additions > 0:
            # only do additions
            for i in range(len(self)):
                for j in range(len(self)):
                    if i == j: continue
                    if not self.has_edge(i, j) and random.random() < self.random_additions:
                        self.add_edge(i, j)

        elif self.random_removals > 0 and self.random_additions > 0:
            # do all
            for i in range(len(self)):
                for j in range(len(self)):
                    if i == j: continue
                    if self.has_edge(i, j):
                        if random.random() < self.random_removals:
                            self.remove_edge(i, j)
                    else:
                        if random.random() < self.random_additions:
                            self.add_edge(i, j)
        """
    #next

    # reciprocity on full graph
    def reciprocate(self, use_edgelist = True):
        # find all pairs of nodes i, j
        # where edge[i, j] and not edge[i, j]:
        #   on such edges:
        #       depending on chance:
        #           add edge[j, i]
        #           or
        #           del edge[i, j]
        
        # main issue: find all node pairs [i, j] where edge[i, j] != edge[j, i]

        # two algos:
        # O(|V|^2) vs. O(|E|)
        # use edge list if |E| < 2*|V|^2
        #
        # 0 <= |E| <= |V| * (|V| - 1)
        # N = |V|
        #
        # N * (N-1) < 2*N^2
        # N^2 - N < 2*N^2 is always true
        #
        #use_edgelist = True #self.number_of_edges() < 2 * (len(self) ** 2)
        if use_edgelist:
            # |E| iterations, |E| checks
            rem_es = []
            add_es = []
            for edge in self.edges:
                # check inverse edge
                if not self.has_edge(edge[1], edge[0]):
                    # = sr * (1 / num succ + num pred)
                    pp = self.social_reciprocity / self.degree(edge[1])
                    # = nsr * (1 - 1 / num succ + num pred)
                    pn = self.negative_social_reciprocity * (1 - 1 /self.degree(edge[1]))
                    r = random.random()
                    if r < pp:
                        add_es.append((edge[1], edge[0]))
                    elif r < pp + pn:
                        rem_es.append((edge[0], edge[1]))
            for edge in add_es:
                self.add_edge(edge[1], edge[0])
            for edge in rem_es:
                self.remove_edge(edge[0], edge[1])

        else:
            # |V|^2 iterations, 2*|V|^2 checks
            for i in range(len(self)):
                for j in range(i + 1, len(self)):
                    # check if [i, j] and not [j, i] or vice versa
                    if self.has_edge(i, j) and not self.has_edge(j, i):
                        # = sr * (1 / num succ + num pred)
                        pp = self.social_reciprocity / self.degree(j)
                        # = nsr * (1 - 1 / num succ + num pred)
                        pn = self.negative_social_reciprocity * (1 - 1 / self.degree(j))
                        r = random.random()
                        if r < pp:
                            self.add_edge(j, i)
                        elif r < pp + pn:
                            self.remove_edge(i, j)

                    elif not self.has_edge(i, j) and self.has_edge(j, i):
                        # = sr * (1 / num succ + num pred)
                        pp = self.social_reciprocity / self.degree(i)
                        # = nsr * (1 - 1 / num succ + num pred)
                        pn = self.negative_social_reciprocity * (1 - 1 / self.degree(i))
                        r = random.random()
                        if r < pp:
                            self.add_edge(i, j)
                        elif r < pp + pn:
                            self.remove_edge(j, i)

    # reciprocity on full graph
    def reciprocate_no_numall(self, use_edgelist = True):
        # find all pairs of nodes i, j
        # where edge[i, j] and not edge[i, j]:
        #   on such edges:
        #       depending on chance:
        #           add edge[j, i]
        #           or
        #           del edge[i, j]
        
        # main issue: find all node pairs [i, j] where edge[i, j] != edge[j, i]

        # two algos:
        # O(|V|^2) vs. O(|E|)
        # use edge list if |E| < 2*|V|^2
        #
        # 0 <= |E| <= |V| * (|V| - 1)
        # N = |V|
        #
        # N * (N-1) < 2*N^2
        # N^2 - N < 2*N^2 is always true
        #
        #use_edgelist = True #self.number_of_edges() < 2 * (len(self) ** 2)
        if use_edgelist:
            # |E| iterations, |E| checks
            rem_es = []
            add_es = []
            for edge in self.edges:
                # check inverse edge
                if not self.has_edge(edge[1], edge[0]):
                    numall = 1#len(list(self.successors(edge[1]))) + len(list(self.predecessors(edge[1])))
                    # = sr * (1 / num succ + num pred)
                    pp = self.social_reciprocity / numall
                    # = nsr * (1 - 1 / num succ + num pred)
                    pn = self.negative_social_reciprocity * (1 - 1 / numall)
                    r = random.random()
                    if r < pp:
                        add_es.append((edge[1], edge[0]))
                    elif r < pp + pn:
                        rem_es.append((edge[0], edge[1]))
            for edge in add_es:
                self.add_edge(edge[1], edge[0])
            for edge in rem_es:
                self.remove_edge(edge[0], edge[1])

        else:
            # |V|^2 iterations, 2*|V|^2 checks
            for i in range(len(self)):
                for j in range(i + 1, len(self)):
                    # check if [i, j] and not [j, i] or vice versa
                    if self.has_edge(i, j) and not self.has_edge(j, i):
                        numall = 1#len(list(self.successors(j))) + len(list(self.predecessors(j)))
                        # = sr * (1 / num succ + num pred)
                        pp = self.social_reciprocity / numall
                        # = nsr * (1 - 1 / num succ + num pred)
                        pn = self.negative_social_reciprocity * (1 - 1 / numall)
                        r = random.random()
                        if r < pp:
                            self.add_edge(j, i)
                        elif r < pp + pn:
                            self.remove_edge(i, j)

                    elif not self.has_edge(i, j) and self.has_edge(j, i):
                        numall = 1#len(list(self.successors(i))) + len(list(self.predecessors(i)))
                        # = sr * (1 / num succ + num pred)
                        pp = self.social_reciprocity / numall
                        # = nsr * (1 - 1 / num succ + num pred)
                        pn = self.negative_social_reciprocity * (1 - 1 / numall)
                        r = random.random()
                        if r < pp:
                            self.add_edge(i, j)
                        elif r < pp + pn:
                            self.remove_edge(j, i)
        