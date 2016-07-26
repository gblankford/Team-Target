"""
George's version of data generator
"""

import numpy as np
import random 





def datagenerator(n1,n2,n3,n4):
    import numpy as np
    import random 
    
    n = np.sum([n1,n2,n3,n4]) # number of parameters: cookies1, cookies2, ID1, ID2, email1, email2
                           #email1, email2
    print(n)

    mat = np.zeros((n,n))


        
    for i in range(n1):
        for j in range(n1,n-n4):
            mat[i,j]= random.randint(0,int(40/max([n2,n3]))) #entries for IDs and guest emails          
        upper = sum([mat[i,j]for j in range(n1,n-n4)]) #sum of all IDs and emails
        lower = min([mat[i,j]for j in range(n1+n2,n-n4)]) 
        print(lower,upper)
        
        mat[i,n-n4] = random.randint(lower, upper)#generating credit card 
        
        for j in range(n- n4 +1,n):
            mat[i,j]= random.randint( 0, upper - sum([mat[i,k] for k in range(n-n4,j)]))
        
        
    
    for i in range(n):
        for j in range(n):
            if j>i :
                mat[j,i]=mat[i,j]
               

            
#    for i in range(n1,n-n4):
#        for j in range(n1+n2,n-n4):
#            upper = mat[i,1]+mat[i,2]
#        mat[i,n-2]= random.randint(0,upper) #need to fix this 
#        mat[i,n-1]= upper - mat[i,n-n4]
 
    for i in range(n1,n-n4):
        for j in range(n1+n2,n-n4):
            upper = mat[i,0]+mat[i,1]
        mat[i,n-n4] = random.randint(0, upper)#generating credit card 
        
          
  
 
 
    for i in range(n):
        for j in range(n):
            if j>i :
                mat[j,i]=mat[i,j]
    
    print(mat)
    
            
    return(mat)
    
######################################    
    
import numpy
import networkx as nx
import matplotlib.pyplot as plt



A = datagenerator(1,1,1,1)

print(A)

G=nx.from_numpy_matrix(A)

nx.draw(G)

  
        