# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:04:07 2016

@author: dingzhao
"""

import numpy as np
import random 
from scipy.linalg import block_diag
import networkx as nx

def labeled_graph(adjacency_matrix, max_cookie, max_login, max_email, max_creditcard, ith_person):
    """     Takes an adjacency matrix of a certain type (i.e. block matrix (mostly) 
        with number of blocks = "number_people", each person with "max_cookie" 
        cookie nodes, "max_login" login nodes, "max_email" email nodes, 
        and "max_creditcard" creditcard nodes). 
            Translates this matrix into a graph with nodes labeled by 0,1,2,...
            Returns a graph with the right labels ('EM_1','EM_2',..., 'Login_1',
        'Login_2',..., etc.) and, more importantly, the right 'type' attribute 
        for each label so that it can be fed directly into the cutting algorithm."""
    
    # First, translate the matrix into a graph.
    graph = nx.from_numpy_matrix(adjacency_matrix)
    Cook_list=[]
    Login_list=[]
    EM_list=[]
    CC_list=[]    
    for i in range(0,max_cookie):
        Cook_list=Cook_list+['Cook_{},{}'.format(ith_person,i+1)]       
    for i in range(0,max_login):
        Login_list=Login_list+['Login_{},{}'.format(ith_person,i+1)]
    for i in range(0,max_email):
        EM_list=EM_list+['EM_{},{}'.format(ith_person,i+1)]
    for i in range(0,max_creditcard):
        CC_list=CC_list+['CC_{},{}'.format(ith_person,i+1)]
    # Make the lists of labels for our nodes that we'll pull from later.    
#    Cook_list = ['Cook_{0}'.format(x) for x in range(1,max_cookie + 1)]
#    Login_list = ['Login_{0}'.format(x) for x in range(1,max_login + 1)]
#    EM_list = ['EM_{0}'.format(x) for x in range(1,max_email + 1)]
#    CC_list = ['CC_{0}'.format(x) for x in range(1,max_creditcard + 1)]
    
    # This is the size of each block of the matrix.
    total = max_cookie + max_email + max_login + max_creditcard
    # These are the dictionaries that will define our retyping and relabeling. Keys will be nodes (0,1,2,...), and values will be the types or new node labels.
    type_dictionary = {}
    relabeling_dictionary = {}
    list_dict={}

    # Now we want to fill the dictionaries. Indices are annoying.
    for cookie_number in range(0, max_cookie):  
        type_dictionary[cookie_number] = 'cookie'
        relabeling_dictionary[cookie_number] = Cook_list[cookie_number] 
    for login_number in range(max_cookie, max_cookie + max_login): 
        type_dictionary[login_number] = 'login'
        list_dict[login_number]=[]
        relabeling_dictionary[login_number] = Login_list[login_number - max_cookie]
    for email_number in range(max_cookie + max_login, max_cookie + max_login + max_email):
        type_dictionary[email_number] = 'email'
        list_dict[email_number]=[]
        relabeling_dictionary[email_number] = EM_list[email_number - (max_cookie + max_login)]
    for creditcard_number in range(max_cookie + max_login + max_email, max_cookie + max_login + max_email + max_creditcard):
        type_dictionary[creditcard_number] = 'creditcard'
        relabeling_dictionary[creditcard_number] = CC_list[creditcard_number - (max_cookie + max_login + max_email)]
    # Now actually change the graph using our dictionaries. First types, then actual node labels.
    nx.set_node_attributes(graph, 'type', type_dictionary)
    nx.set_node_attributes(graph,'list',list_dict)
    labeled_graph = nx.relabel_nodes(graph, relabeling_dictionary)
    
    return labeled_graph


def data_person(ith_person):
    """  This function generates data for one person   """
    CK_num = random.randint(1,10)    
    # generate the number of cookie a person has
    
    n1 = CK_num # num cookies
    IDEM_num = np.random.choice([1,2,3,4,5],1,p=[0.3085,0.3829,0.2417,0.0606,0.0063])
    
    if IDEM_num==5:
        ID_num=2
    if IDEM_num==4:        
        ID_num = random.randint(1,2)
    else:
        ID_num=min(random.randint(0,2),IDEM_num)
    
    n2=ID_num    #generate the number of login id the person has
    if ID_num>IDEM_num:    
        n2 = IDEM_num
        
    
    EM_num = IDEM_num - ID_num    #generate the number of email the person has
    if EM_num < 0:
        EM_num = 0
    
    n3 = int(EM_num) # num emails
    n4 = max(1,int(np.random.choice([0,random.randint(1,2),random.randint(3,4),5],1,p=[0.18,0.48,0.18,0.16])))
    # generate number of creditcard the person has    
    
    
    
    Max = n1 + n2 + n3 + n4    
    
    A = np.zeros((Max,Max))                       
    # generate a graph with only nodes
    
    G = labeled_graph(A,n1,n2,n3,n4,ith_person)   
    # add label them
    
    
    # now add edges to nodes 
    
    # First randomly grab a node with attribute cookie and link it to either 
    # email or login. If the link is cookie to email, then find a credit card  
    # node and link both the cookie and email node found before to it to make 
    # a triangle. If the link is cookie is cookie to login, then under 50%  
    # chance to make the triangle. Run it 30 times
    
    temp = []    
    
    for nd in G.nodes():    # generate a list of nodes with attribute cookie
            if G.node[nd]['type'] == 'cookie':
                temp.append(nd) 
        
    for i in range(30):    
        
        ran1 = random.choice(temp)    
        # randomly grab a node with attribute cookie and start to look for 
        #nodes with attribute email or login
        
        possiblenodes1 = G.nodes()    
        # generate a list of nodes where ran1 can be linked to
        
        typecheck = []
        
        for nodes in possiblenodes1:
            if G.node[nodes]['type'] == 'cookie' or G.node[nodes]['type'] == 'creditcard':
                typecheck.append(nodes)                
                
        possiblenodes2 = [item for item in possiblenodes1 if item not in typecheck]
        # update the list so that it only contains nodes with attribute email or login        
        
        ran2 = random.choice(possiblenodes2)    
        # randomly choose a node and start to make connection
        
        wei1 = 2
        
        if G.node[ran2]['type'] == 'email':    
        # If ran2 has attribute email, then automatically choose a node with 
        # attribute creditcard and link ran2 to it. If this link already exits,
        # just update the weight.
        
            creditcard = []
            for nodes in possiblenodes1:
                if G.node[nodes]['type'] == 'creditcard':
                    creditcard.append(nodes)                    
            ran3 = random.choice(creditcard)
            if G.has_edge(ran1,ran3):
                G.edge[ran1][ran3]['weight'] += wei1
            else:    
                G.add_edge(ran1,ran3,weight = wei1)
            
            if G.has_edge(ran1,ran2):
                G.edge[ran1][ran2]['weight'] += wei1
            else:    
                G.add_edge(ran1,ran2,weight = wei1)
            
            if G.has_edge(ran2,ran3):
                G.edge[ran2][ran3]['weight'] += wei1 
            else:    
                G.add_edge(ran2,ran3,weight = wei1)
        
        if G.node[ran2]['type']=='login':    
        # If ran2 has attribute login, then with 50% chance choose a node 
        # with attribute creditcard and link ran2 to it or add weight to it
            creditcard = []
            for nodes in possiblenodes1:
                if G.node[nodes]['type'] == 'creditcard':
                    creditcard.append(nodes)                    
            ran3 = random.choice(creditcard)
            choice=random.randint(0,1)
            if G.has_edge(ran2,ran1):
                G.edge[ran1][ran2]['weight'] +=wei1
            else:
                G.add_edge(ran1,ran2,weight=wei1)
            if choice==1:
                if G.has_edge(ran2,ran3):
                    G.edge[ran2][ran3]['weight']+=wei1
                else:
                    G.add_edge(ran2,ran3,weight=wei1)
                if G.has_edge(ran1,ran3):
                    G.edge[ran1][ran3]['weight']+=wei1
                else:
                    G.add_edge(ran1,ran3,weight=wei1)
    
    for i in G.nodes(): # get rid of the nodes that never picked
        if len(G.neighbors(i))==0:
            G.remove_node(i)
    return G 
        
def data_for_npeople(n):
    """ This function creates n person and put them in one graph """
    list_of_people=[]
    for i in range(1,n+1):
        list_of_people=list_of_people+[data_person(i)]
    A=list_of_people[0]
    for i in range(1,n):
        A=nx.compose(A,list_of_people[i])
    return A

def add_noise_graph(H):
    """This function adds noise,in the form of weighted edges, between 
    connected components in your graph."""
    
    # First randomly grab a node with attribute cookie and link it to either 
    # email or login from anther connected component(anther person). 
    # If the link is cookie to email, then find a credit card  
    # node from the that connected component and link both the cookie and email 
    # node found before to it to make a triangle between two  
    # connected components(two person).
    # If the link is cookie is cookie to login, then under 50%  
    # chance to make the triangle. Run it (total number of edges)/10 times   
    
    n = nx.number_of_edges(H)
    n = int(n/10)
    # 1/10 of number of total edges
     
    
    H2 = H.copy()    
    # make a copy of the clean graph for reference
    
    temp = []     
    for nd in H.nodes():   # make a list of all nodes with attribute cookie
        if H.node[nd]['type'] == 'cookie':
            temp.append(nd) 
           
    for i in range(n): 
        ran1 = random.choice(temp)  
        #randomly choose a node ran1 with attribute cookie    
        
        possiblenodes1 = H.nodes()  
        #generate a list of nodes where ran1 can be linked to
        
        neighbors = nx.node_connected_component(H2,ran1)   
        # find all the nodes that in the same connected component as ran1
        
        possiblenodes2 = [item for item in possiblenodes1 if item not in neighbors]    
        # update possiblenodes1 to be the nodes from other connected components
        
        typecheck = []
        
        for nodes in possiblenodes2:    
        # generate a list of nodes with attribute cookie from possiblenodes2
            if H.node[nodes]['type'] == 'cookie' or H.node[nodes]['type'] == 'creditcard':
                typecheck.append(nodes)                
                
        possiblenodes3 = [item for item in possiblenodes2 if item not in typecheck]    
        # make a list from possiblenodes2 to be all the nodes that are not in 
        # the same connected component as ran1 and with attributes 
        # login or email         
        
        ran2 = random.choice(possiblenodes3)    
        # randomly choose a node ran2 from possiblenodes to 
        # make connection with ran1
        
        neighbors2 = nx.node_connected_component(H2,ran2)   
        #find all the nodes in the same connected component as ran2     
        
        wei3 = 1
        
        if H.node[ran2]['type'] == 'email':    
        # If ran2 has attribute email, then automatically find a 
        # node in neighbors2 with attribute creditcard and 
        # make connection with ran2 
            creditcard = []
            for nodes in neighbors2:
                if H.node[nodes]['type'] == 'creditcard':
                    creditcard.append(nodes)                    
            ran3 = random.choice(creditcard)
            
            if H.has_edge(ran1,ran3):
                H.edge[ran1][ran3]['weight'] = H.edge[ran1][ran3]['weight'] + wei3
            else:                                    
                H.add_edge(ran1,ran3,weight = wei3)

            if H.has_edge(ran1,ran2):
                H.edge[ran1][ran2]['weight'] = H.edge[ran1][ran2]['weight'] + wei3
            else:  
                H.add_edge(ran1,ran2,weight = wei3)
            
            if H.has_edge(ran2,ran3):
                H.edge[ran2][ran3]['weight'] = H.edge[ran2][ran3]['weight'] + wei3
            else:
                H.add_edge(ran2,ran3,weight=wei3)
            
        if H.node[ran2]['type'] == 'login':    
        # If ran2 has attribute login, then under 50% chance 
        # find a node in neighbors2 with attribute creditcard and 
        # make connection with ran2
            creditcard = []
            for nodes in neighbors2:
                if H.node[nodes]['type'] == 'creditcard':
                    creditcard.append(nodes)
            ran3 = random.choice(creditcard)
            ran_num = random.randint(0,1)
            if ran_num == 0:
                if H.has_edge(ran1,ran2):
                    H.edge[ran1][ran2]['weight'] = H.edge[ran1][ran2]['weight'] + wei3 
                else:                
                    H.add_edge(ran1,ran2,weight = wei3)
            else:
                if H.has_edge(ran1,ran3):
                    H.edge[ran1][ran3]['weight'] = H.edge[ran1][ran3]['weight'] + wei3
                else:                                    
                    H.add_edge(ran1,ran3,weight = wei3)

                
                if H.has_edge(ran1,ran2):
                    H.edge[ran1][ran2]['weight'] = H.edge[ran1][ran2]['weight'] + wei3 
                else:                
                    H.add_edge(ran1,ran2,weight = wei3)
                
                if H.has_edge(ran2,ran3):
                    H.edge[ran2][ran3]['weight'] = H.edge[ran2][ran3]['weight'] + wei3
                else:
                    H.add_edge(ran2,ran3,weight = wei3)
    return H