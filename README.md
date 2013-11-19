FullHC
======

This allows you to access the power of SciPy's clustering algorithms from a weighted NetworkX graph.  It supports complete, average, and single linkage clustering, as well as all of SciPy's distance algorithms 
(such as euclidean, correlation, and jaccard coefficients).

How to Use
===========

It's very simple to generate a complete agglomerative clustering with this framework:
    
    import FullHC
    fhc = FullHC.FullHC()
    fhc.full_hc_from_gexf("/Where/gexf/is/stored.gexf", method = 'complete', metric = 'euclidean')

Supported methods are 'complete', 'average', 'single'. You can access the list of clusters with the following property:
    
    fhc.clusters

This is a list of lists of lists.  You can access each subgroup like so:

    for cluster in fhc.clusters:
        for group in cluster:
            print(str(group))

Note though, this is only a list of the names in each subgroup.  Unfortunately because of how blockmodeling works in networkx the block model does not retain the information about each subgroup.  If you want to see the ties between the different block models you can do that like this:

    fhc.blockmodels

You could run some sort of NetworkX algorithm on the blockmodels to learn about relationships between them since edges are retained between the different blocks.

If you have a graph already built just use:

    fhc.full_hc(graph, method='complete', metric ='euclidean')

You can set clear = False if you want to keep all the old clustering information.

