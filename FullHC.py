import networkx as nx
from collections import defaultdict
import numpy
from scipy.cluster import hierarchy
from scipy.spatial import distance
import matplotlib.pyplot as plt


class FullHC:
    def __init__(self):
        self.clusters = []
        self.blockmodels = []
        self.graph = nx.Graph()

    def create_hc(self, G, t=1.0, method='complete', metric='euclidean', sci = False):
        #adopted from: Tsvetovat, Maksim; Kouznetsov, Alexander (2011-09-29). Social Network Analysis for Startups (p. 85). O'Reilly Media. Kindle Edition.
        labels=G.nodes()
        matrix=nx.to_numpy_recarray(G)
        distances=numpy.zeros((len(G),len(G)))
        i=0
        for x in matrix:
            j=0
            for y in x:
                distances[i][j]=y[0]
                distances[j][i]=y[0]
                if i==j: distances[i][j]=0
                j+=1
            i+=1
    
        #Create hierarchical cluster
        Y=distance.pdist(distances, metric)

        #numpy.clip(Y,0, 10000, Y) // implement if you get negative value errors
        if sci == True:
            Z=hierarchy.linkage(Y, method, metric)
        elif method == 'complete':
            print("complete")
            Z=hierarchy.complete(Y)  # Creates HC using farthest point linkage
        elif method == 'average':
            print("average")
            Z=hierarchy.average(Y)
        elif method == 'single':
            print("single")
            Z=hierarchy.single(Y)
        
        membership=list(hierarchy.fcluster(Z,t=t))
        # Create collection of lists for blockmodel
        partition=defaultdict(list)
        for n,p in zip(list(range(len(G))),membership):
            partition[p].append(labels[n])
        return list(partition.values())

    def next_labeled_hc(self, hc, bm, method, metric):
        """
        This function takes a hc and a blockmodel and makes the next hc labeled
        using the bm to index the initially labeled hc.
        Note: HC is a list of node labels, and bm is a block model derived from that graph
        """
        next_hc = self.create_hc(bm, method=method, metric=metric) # create a hc from a bm 
        block_ids_in_list = []
        #iterate through the new cluster graph
        for cluster in next_hc:
            block_list = []
            #iterate through all the members of the cluster
            for member in cluster:
                block_list += hc[member]
            block_ids_in_list.append(block_list)
        return block_ids_in_list

    def full_hc(self, G, hc = None, clusters = [], clear = True, method='complete', metric ='euclidean'):
        """ 
        All this function needs is G and it will do a full hierarchical clustering of a graph
        You could also seed it with an initial clustering of your own choosing by setting hc
        Note: hc is a list of node labels
        """
        #clears cached clusters so that clusters are not appended endlessly
        if clear:
            self.clear()
            clear = False

        if hc and len(hc) == 1:
            self.clusters.append(hc)
            clusters.append(hc)
            return clusters
        else:
            if not hc:
                hc = self.create_hc(G, method=method, metric=metric)
            
            bm = nx.blockmodel(G, hc)
            #append to local variable
            clusters.append(hc)
            #append to properties
            self.clusters.append(hc)
            self.blockmodels.append(bm)
            #grab next hc
            next_hc = self.next_labeled_hc(hc, bm, method = method, metric = metric)
            return self.full_hc(G, hc=next_hc, clusters=clusters, clear=clear, method = method, metric =metric)

    def full_hc_from_gexf(self, path, method='complete', metric='euclidean'):
        graph = nx.read_gexf(path)
        self.graph = graph
        self.full_hc(graph, method=method, metric=metric)

    def clear(self):
        print("clear called")
        self.clusters = []
        self.blockmodels = []

    def show(self, convert = None, arg = None):
        current = 1
        for cluster in self.clusters:
            print("-------- " + str(current) + " -------- \n")
            for group in cluster:
                if convert:
                    print(convert(group, arg))
                else:
                    print(group)
                print("\n")
            current += 1






