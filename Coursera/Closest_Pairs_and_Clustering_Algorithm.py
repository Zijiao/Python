"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), idx1, idx2)


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    length = len(cluster_list)
    
    returned  = []
    return_list = []
    index_list = range(length)
    smallest_dist = float("inf")
    
    for dummy_i in range(length):
        for dummy_j in range(length):
            temp_d = cluster_list[dummy_i].distance(cluster_list[dummy_j]) 
            if (dummy_i != dummy_j and temp_d < smallest_dist):               
                smallest_dist = temp_d
    
    while len(index_list) != 0:
        index1 = index_list.pop()
        for dummy_j in range(length):
            temp_d = cluster_list[index1].distance(cluster_list[dummy_j])
            if (index1 != dummy_j and ((index1, dummy_j) not in returned) and temp_d == smallest_dist):
                index2 = dummy_j
                returned.append((index1, index2))
                if index1 in index_list:
                    index_list.remove(index1)
                if index2 in index_list:
                    index_list.remove(index2)
                if index1 < index2:
                    return_list.append((smallest_dist, index1, index2))
                else:
                    return_list.append((smallest_dist, index2, index1))
                    
    return set(return_list)


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
    
    def devide(cluster_list, horiz_order, vert_order):
        """
        used in fast_helper()
        """
        mid_index = int(math.ceil(len(horiz_order) / 2.0)) 
        horiz_order_left = horiz_order[:mid_index]
        horiz_order_right = horiz_order[mid_index:]
        left_set = set(horiz_order_left)
            
        vert_order_left = []
        vert_order_right = []
            
        for elem in vert_order:
            if elem in left_set:
                vert_order_left.append(elem)
            else:
                vert_order_right.append(elem)
                    
        (d_left, i_left, j_left) = fast_helper(cluster_list, horiz_order_left, vert_order_left)
        (d_right, i_right, j_right) = fast_helper(cluster_list, horiz_order_right, vert_order_right)
        if d_left < d_right:
            (d_min, i_min, j_min) = (d_left, i_left, j_left)
        else:
            (d_min, i_min, j_min) = (d_right, i_right, j_right)    
        return (d_min, i_min, j_min)
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        
        # base case

        if len(horiz_order) <= 3:
            temp = []
            for elem in horiz_order:
                temp.append(cluster_list[elem])
            temp = slow_closest_pairs(temp).pop() 
            return (temp[0],horiz_order[temp[1]], horiz_order[temp[2]] )
        
        # divide
        else:
            mid_index = int(math.ceil(len(horiz_order) / 2.0))
            mid = (cluster_list[horiz_order[mid_index - 1]].horiz_center() + cluster_list[horiz_order[mid_index]].horiz_center()) / 2
            (d_min, i_min, j_min) = devide(cluster_list, horiz_order, vert_order)
                   
        # conquer
            s_list = []
            for elem in vert_order:
                if abs(cluster_list[elem].horiz_center() - mid) < d_min:
                    s_list.append(elem)
                    
                    
            return conquer(cluster_list, s_list, d_min, i_min, j_min)
            
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))



def conquer(cluster_list, s_list, d_min, i_min, j_min):
    """
    used in fast_helper()
    """
    k_value = len(s_list)           
    for u_dummy in range(k_value - 1):
        for v_dummy in range(u_dummy + 1, min(u_dummy + 3, k_value - 1) + 1):
            d_temp = cluster_list[s_list[u_dummy]].distance(cluster_list[s_list[v_dummy]])
            if d_temp < d_min:
                (d_min, i_min, j_min) = (d_temp, s_list[u_dummy], s_list[v_dummy])
    return (d_min, i_min, j_min)


    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """

    while len(cluster_list) > num_clusters:
        (_, index1, index2)  = fast_closest_pair(cluster_list)
        cluster_list[index1].merge_clusters(cluster_list[index2])
        cluster_list.pop(index2)
    
    return cluster_list



    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    # initialize k-means clusters to be initial clusters with largest populations
    length = len(cluster_list)
    population_list = []
    for index in range(length):
        population_list.append((cluster_list[index].total_population(), index))
   
    # line 2  
    old_clusters = []
    for dummy_i in range(num_clusters):
        old_clusters.append(cluster_list[max(population_list)[1]])
        population_list.remove(max(population_list))
    
    # line 3 starts
    for dummy_i in range(num_iterations):
        new_clusters = [] #result_list is line 3
        for dummy_j in range(num_clusters):
            new_clusters.append(alg_cluster.Cluster(set([]), old_clusters[dummy_j].horiz_center(), old_clusters[dummy_j].vert_center(), 0, 0))
        
        for dummy_j in range(len(cluster_list)):
            distance_list = []
            for dummy_k in range(num_clusters):
                distance_list.append((cluster_list[dummy_j].distance(old_clusters[dummy_k]), dummy_k))
            (_, k_min) = min(distance_list)
            new_clusters[k_min].merge_clusters(cluster_list[dummy_j])
        old_clusters = new_clusters
    return new_clusters