import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

G=nx.Graph()

G.add_edge('EM_1','CC_1',weight=2)
G.add_edge('EM_1','Cook_1',weight=5)
G.add_edge('CC_1','Cook_1',weight=2)
G.add_edge('Login_1','Cook_1',weight=1)
G.add_edge('Login_1','Cook_2',weight=5)
G.add_edge('Login_2','Cook_2',weight=8)
G.add_edge('CC_2','Cook_2',weight=1)
G.add_edge('CC_2','Login_1',weight=1)
G.add_edge('CC_3','EM_2',weight=12)
G.add_edge('Cook_2','EM_3',weight=7)
G.add_edge('Cook_2','CC_3',weight=8)

G.node['EM_1']['type']='email'
G.node['EM_2']['type']='email'
G.node['EM_3']['type']='email'
G.node['CC_1']['type']='creditcard'
G.node['CC_2']['type']='creditcard'
G.node['CC_3']['type']='creditcard'
G.node['Login_1']['type']='login'
G.node['Login_2']['type']='login'
G.node['Cook_1']['type']='cookie'
G.node['Cook_2']['type']='cookie'

#pos=nx.spring_layout(G) # positions for all nodes
#
#edge_labels=dict([((u,v,),d['weight'])
#             for u,v,d in G.edges(data=True)])
#nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
#
## nodes
#nx.draw_networkx_nodes(G,pos,node_size=1500)
#
## edges
#nx.draw_networkx_edges(G,pos)
#
## labels
#nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
#
#plt.axis('off')
#
#plt.show()

def compositions(n,k):
  """Returns all the weak integer compositions of n into k parts"""
  if n < 0 or k < 0:
    return
  elif k == 0:
    # the empty sum, by convention, is zero, so only return something if
    # n is zero
    if n == 0:
      yield []
    return
  elif k == 1:
    yield [n]
    return
  else:
    for i in range(0,n+1):
      for comp in compositions(n-i,k-1):
        yield [i] + comp

def emcomps(n,k):
  """Returns the email probability for each composition of n into k parts in a list"""
  if n < 0 or k < 0:
    return
  elif k == 0:
    # the empty sum, by convention, is zero, so only return something if
    # n is zero
    if n == 0:
      yield []
    return
  elif k == 1:
    yield emprob(n)
    return
  else:
    for i in range(0,n+1):
      for comp in emcomps(n-i,k-1):
        yield emprob(i)*comp

def cccomps(n,k):
  """Returns the card probability for each composition of n into k parts in a list"""
  if n < 0 or k < 0:
    return
  elif k == 0:
    # the empty sum, by convention, is zero, so only return something if
    # n is zero
    if n == 0:
      yield []
    return
  elif k == 1:
    yield ccprob(n)
    return
  else:
    for i in range(0,n+1):
      for comp in cccomps(n-i,k-1):
        yield ccprob(i)*comp      

        

def emprob(n):
    """This returns the probability of one person having n email accounts
            according to some data on the internet"""
    if n == 0:
        return 0.0668
    if n == 1:
        return 0.2417
    if n == 2:
        return 0.3829
    if n == 3:
        return 0.2417
    if n == 4:
        return 0.0606
    if n >= 5:
        return 0.0062
        
def ccprob(n):
    """This returns the probability of one person having n credit cards
            according to some data on the internet"""
    if n == 0:
        return 0.29
    if n == 1 or n == 2:
        return 0.33
    if n == 3 or n == 4:
        return 0.18
    if n == 5 or n == 6:
        return 0.09
    if n >= 7:
        return 0.07

############ This is the new one that's much more efficient and compact.
def feas2(em,cc,log):
    """Returns the most feasible number of people associated with em emails
            and cc credit cards"""
    problist = []  # initialize the list of probabilities
    for i in range(1,em+log+1):  # i is the number of people we're splitting them among
        emlist_i = list(emcomps(em,i)) # This gives the email probability for each composition into i parts in a list.
        ccprob_i = sum(list(cccomps(cc,i))) # This gives the SUM of the card probabilities for all the compositions into i parts.
        totprob_i = sum(ccprob_i*np.array(emlist_i))  # This multiplies each email probability by the sum of the card probabilities, then sums it all up
        problist.append(totprob_i)  # Throw it in the list
    #print(problist)  # Boom.
    return problist.index(max(problist)) + 1 # plus 1 to get the actual number of people (since it starts at zero)


def GraphFeas(G):
    emails = 0
    ccs = 0
    logins = 0
    # First for the 'graph' nodes
    graph_nodes=[n for n in G.nodes() if G.node[n]['type']=='graph']
    for N in graph_nodes:  # Iterate through all such graph-nodes
        #print(N.nodes(data=True))
        #print(N.nodes(data=True)[1][1]['type'])
        for i in range(len(N.nodes(data=True))):  # Then through each node in that graph. 
            if N.nodes(data=True)[i][1]['type']=='email':  # +1 for each email. Ignore the weird way of getting at the type...
                emails = emails + 1     # It's because of an unexpected strange error about the key being hashable.
            if N.nodes(data=True)[i][1]['type']=='creditcard':  # +1 for each credit card
                ccs = ccs + 1
            if N.nodes(data=True)[i][1]['type']=='login':  # +1 for each login
                logins = logins + 1
    # Count the 'email' nodes
    email_nodes=[n for n in G.nodes() if G.node[n]['type']=='email']
    emails = emails + len(email_nodes) 
    # Count the 'creditcard' nodes
    cc_nodes=[n for n in G.nodes() if G.node[n]['type']=='creditcard']
    ccs = ccs + len(cc_nodes)
    # Count the 'login' nodes
    login_nodes=[n for n in G.nodes() if G.node[n]['type']=='login']
    logins = logins + len(login_nodes)
    #print(emails,ccs,logins)
    return feas2(emails,ccs,logins)
    
    
def edges_to_merge(G):
    cook_cc_nodes=[]
    merge_edges=[]
    for n0 in G.nodes():
        if G.node[n0]['type']=='cookie' or G.node[n0]['type']=='creditcard':
            cook_cc_nodes=cook_cc_nodes+[n0]
    
    for N in cook_cc_nodes:
        
        L=list(nx.all_neighbors(G,N))
    
        #P will only be the neighbors of type login or email
        P=[]
        for n1 in L:
            if G.node[n1]['type']=='login' or G.node[n1]['type']=='email':
                P=P+[n1]
    
        #Grab and store, in a list W, the edge data from original node and its neighbors from P
        W=[]
        for n2 in P:
            b=G.get_edge_data(N,n2)
            W=W+[b]
    
        #w will be the weight of the edges that have been stored in W
        w=[]
        s=len(W)
        i=0
        while (i<s):
            w=w+[W[i]['weight']]
            i=i+1
            m=max(w)
    
        #enumerate w and store the exact position the maximum weight occurs
        position=[k for k, j in enumerate(w) if j == m]
        #grab the node from P that is in the position stored in position. This is the node it should merge with.
        maxnhbr=[(P[pos]) for pos in position]
        #Now store the edges the need to be merged
        for n3 in maxnhbr:
            merge_edges=merge_edges+[(N,n3)]
    #print(merge_edges)
    return merge_edges


def merge(G,Eg):
    """Returns a new graph with edge merged, and the new node containing the
            information lost in the merge. The weights from common neighbors
            are added together, a la Stoer-Wagner algorithm."""
    H = nx.Graph()  # The graph that will become our new node after merging.
    Egflip = (Eg[1],Eg[0])
    #print(Eg,Egflip,G.edges())
    if Eg not in G.edges() and Egflip not in G.edges():       
        edge = []
        if G.node[Eg[0]]['type'] == 'creditcard' or G.node[Eg[0]]['type'] == 'cookie':
            CorC=Eg[0]
            LorE=Eg[1]
        else:
            CorC=Eg[1]
            LorE=Eg[0]
        nbrs = list(nx.all_neighbors(G,CorC))
        for node in nbrs:
            if G.node[node]['type'] == 'graph':
                if LorE in node.nodes():
                    edge=edge+[node]
#            else:
#                print("You screwed up")
        edge = [CorC]+edge
    else:
        edge = Eg
        
    edge_w = G[edge[0]][edge[1]]['weight'] # Get weight of the edge that about to be contracted
    if nx.get_node_attributes(G,'type')[edge[0]] == 'graph':
        #print(edge[0].nodes(data=True))
        H.add_nodes_from(edge[0].nodes(data=True))  # Copy all the nodes with their types       
        H.add_edges_from(edge[0].edges(data=True))  # Copy all the edges of that graph into H with their weights
        for node in edge[0].nodes():  # Now want to reduce that graph to a basic node
            if nx.get_node_attributes(edge[0],'type')[node] == 'email' \
             or nx.get_node_attributes(edge[0],'type')[node] == 'login': # by finding either the email or login in that graph
                 leftnode = node  # so that our soon-to-be-contracted edge will connect
                 attr = edge[0].node[leftnode]['type']
                 G = nx.relabel_nodes(G,{edge[0]:leftnode})   # to that node in H
                 nx.set_node_attributes(G,'type',{leftnode:attr})
    else:
        leftnode = edge[0]
    if nx.get_node_attributes(G,'type')[edge[1]] == 'graph': # if the second node of the edge happens to be a merged graph already
        edge = edge[::-1]
        H.add_nodes_from(edge[0].nodes(data=True))  # same thing...
        H.add_edges_from(edge[0].edges(data=True))  
        for node in edge[0].nodes():
            if nx.get_node_attributes(edge[0],'type')[node] == 'email' \
             or nx.get_node_attributes(edge[0],'type')[node] == 'login':
                 rightnode = node
                 attr = edge[0].node[rightnode]['type']
                 G = nx.relabel_nodes(G,{edge[0]:rightnode}) 
                 nx.set_node_attributes(G,'type',{rightnode:attr})
    else:
        rightnode = edge[1]
    H.add_node(leftnode,type=nx.get_node_attributes(G,'type')[leftnode])
    H.add_node(rightnode,type=nx.get_node_attributes(G,'type')[rightnode])
    H.add_edge(leftnode,rightnode,weight= edge_w)  # now actually add that edge to H
    #drawnice(H)    
    
    J = nx.contracted_edge(G,(leftnode,rightnode),self_loops = False)  #Contract edge without self-loop
    #print(J.nodes(data=True))
    N = nx.common_neighbors(G,leftnode,rightnode) #find common nodes
    
    for i in N:
        J[i][leftnode]['weight'] = G[leftnode][i]['weight'] + G[rightnode][i]['weight'] #modify the weight after contraction

    B = nx.relabel_nodes(J,{leftnode:H}) # Replace the merged node with the graph H
    nx.set_node_attributes(B,'type',{H:'graph'})
    return B,H


def drawnice(G):
    posG=nx.spring_layout(G,k=0.5)
    labelsG = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_nodes(G,posG,node_size=800)
    nx.draw_networkx_labels(G,posG,font_size=8,font_family='sans-serif')
    nx.draw_networkx_edges(G,posG,width=1)
    nx.draw_networkx_edge_labels(G,posG,edge_labels=labelsG,fontsize='1')

########################################################################################################
##################### THE ABOVE FUNCTIONS ARE USED IN CODE BELOW ############################
def target_cut(G):
    graphs = list(nx.connected_component_subgraphs(G))
    after_cut = []
    for sub_G in graphs:
        people = GraphFeas(sub_G)
        print('people = ',people)
        if people == 1:
            after_cut = after_cut + [sub_G]
        else:
            edges = edges_to_merge(sub_G)
            A = sub_G
            for Eg in edges:
                A,B = merge(A,Eg)
            #plt.figure('A')
            #drawnice(A)
            cut_val, cuts = nx.stoer_wagner(A)
            sub1 = A.subgraph(cuts[0])
            #plt.figure('sub1')
            #drawnice(sub1)
            #plt.figure('inside sub1')
            #drawnice(sub1.nodes()[0])
            #print(sub1.nodes(data=True))
            sub2 = A.subgraph(cuts[1])
            #plt.figure('sub2')
            #drawnice(sub2)
            after_cut = after_cut + target_cut(sub1)
            #blah = target_cut(sub2)
            #plt.figure('blah')
            #drawnice(blah[0])
            after_cut = after_cut + target_cut(sub2)
            ## Make the actual subgraph from the result without 'graph' nodes
    return after_cut
            
def graph_construction(G):
    A = target_cut(G)
    final_list = []
    for j in range(len(A)):
        node_list_j = []
        for ND in A[j].nodes():
            if A[j].node[ND]['type'] == 'graph':
                node_list_j = node_list_j + ND.nodes()
            else:
                node_list_j = node_list_j + [ND]
        final_list = final_list + [node_list_j]
    final_subgraphs = []
    for lst in final_list:
        final_subgraphs = final_subgraphs + [G.subgraph(lst)]   
    return final_subgraphs         
            