''' Code for determination of node degree '''
import numpy as np

def node_degree(weight_matrix):
    #expected input of OD_pair_list is lists in a list
    
    #expected input of weight matrix is a square matrix
    #column represents origin, row represents destination

    transposed_weight_matrix = np.transpose(weight_matrix)

    degree = []
    in_degree = []
    out_degree = []

    for i in range(len(weight_matrix):
        
        '''in degree = sum of all nonzero in a column of the weight matrix'''
        Incoming = [transposed_weight_matrix[i]]
        Incoming[i] = 0

        #find number of nonzero entries
        in_degree.append(np.count_nonzero(Incoming))


        '''out degree = sum of all nonzero entries in a row of weight matrix'''
        Outgoing = [weight_matrix[i]]
        Outgoing[i] = 0

        #find number of nonzero entries          
        out_degree.append(np.count_nonzero(Outgoing))


        '''Degree = number off all different airports to have direct edge to an airport'''
        degree_check = []
        for j in range(len(Incoming)):
            degree_check.append(Incoming[j]*Outgoing[j])

        degree.append(np.count_nonzero(degree_check))
                   
    return degree, in_degree, out_degree
