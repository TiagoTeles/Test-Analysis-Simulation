''' Code for determination of node degree '''
import numpy as np

def node_degree(weight_matrix):
    
    #expected input of weight matrix is a square matrix
    #column represents origin, row represents destination

    transposed_weight_matrix = np.transpose(weight_matrix)

    #get in degree
    in_degree_list = np.count_nonzero(transposed_weight_matrix, axis=1)

    #get out degree
    out_degree_list = np.count_nonzero(weight_matrix, axis=1)

    #get total degree

    degree_list = []
    
    for i in range(len(weight_matrix)):
        row = weight_matrix[i]
        row[i] = 0
        
        column = transposed_weight_matrix[i]
        column[i] = 0

        degree_check = row+column
        degree_list.append(np.count_nonzero(degree_check))
        
                   
    return out_degree_list, in_degree_list, degree_list


def average_degree(degree_list):
    
    total = sum(degree_list)

    av_degree = total/len(degree_list)

    return av_degree

#Testing

array = np.array([[0,3,10,0,5,0],[3,3,0,0,5,6],[0,0,0,0,0,0],[1,3,10,4,5,3],[0,3,10,5,5,0],[0,0,0,0,5,0]])

out_degree_list, in_degree_list, degree_list = node_degree(array)

print(out_degree_list, '\n',in_degree_list, '\n',degree_list)

av_deg = average_degree(degree_list)
print(av_deg)

