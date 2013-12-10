FullHC
======

This allows you to access the power of SciPy's clustering algorithms from a weighted NetworkX graph.  It supports complete, average, and single linkage clustering, as well as all of SciPy's distance algorithms 
(such as euclidean, correlation, and jaccard coefficients).  Note, this performs clustering on each consecutive blockmodel, or position, and does not rely on data of nodes in each cluster as traditional blockmodeling would.  This method has been used to cluster similar webpages, and a comparison of its effectiveness to other methods can be found here: http://www.sciencedirect.com/science/article/pii/S0952197612000073.

Impetous
===========

As readers of social science literature may know, the idea behind an agglomerative hierarchical clustering is to iterate from n clusters to just one cluster, where n is the number of nodes in the graph.  This is often shown in a dendrogram.  The challenge is often to figure out where to stop clustering in order to find relevent results. In SciPy and other related programs  (see: http://www.mathworks.com/help/stats/hierarchical-clustering.html#bq_6_ia) they use an inconsistency coefficient in order to gauge when a clustering would combine two clusters that are too different from one another. The number increases as each cluster becomes too "inconsistent" and then stop the clustering afterward.

I found this metric to be somewhat conservative, and wanted to do a more robust clustering in order to become more familiar with the data I was working with, and thus I wrote this class.

Prerequisites
============

A weighted, undirected network graph in networkx graph format or gexf format.  You must also have SciPy, NumPy, and NetworkX installed.

How to Use
===========

It's very simple to generate a complete agglomerative clustering with this framework:
    
    import FullHC
    fhc = FullHC.FullHC()
    fhc.full_hc_from_gexf("/Where/gexf/is/stored.gexf", method='complete', metric='euclidean')

Supported methods are 'complete', 'average', 'single'. You can access the list of clusters with the following property:
    
    fhc.clusters

This is a list of lists of lists.  You can access each subgroup like so:

    for cluster in fhc.clusters:
        for group in cluster:
            print(str(group))

Note though, this is only a list of the names in each subgroup.  Unfortunately because of how blockmodeling works in NetworkX the block model does not retain the information about each subgroup in terms of which nodes are in each block. However, it does retain information about relationships between blocks. If you want to see the ties between the different block models you can do that like this:

    fhc.blockmodels

You could run some sort of NetworkX algorithm on any of the blockmodels to learn more about relationships between them, such as which block is the most central.

If you have a graph already built just use:

    fhc.full_hc(graph, method='complete', metric ='euclidean')

You can set clear = False if you want to keep all the old clustering information.  Also you can set clip = True if you for some reason get errors related to negative values (normally as a result of floating point numbers.)

If you want to play around with the data more, then you should use the following:

    partition_list = fhc.create_hc(graph, t=t, citerion='your-criterion')

Where t is the threshold that you want and the criterion is your choice (for example, 'maxclust' would return at most the number of clusters that t is equal to). It defaults to 'inconsistent' and t = 1.0.

For more on what these metrics mean, please check out http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html#scipy.cluster.hierarchy.fcluster and also http://www.mathworks.com/help/stats/hierarchical-clustering.html#bq_6_ia.

Feel free to contribute or reach out!
