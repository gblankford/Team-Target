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
G.node['EM_1']['list']=[]
G.node['EM_2']['list']=[]
G.node['EM_3']['list']=[]
G.node['CC_1']['type']='creditcard'
G.node['CC_2']['type']='creditcard'
G.node['CC_3']['type']='creditcard'
G.node['Login_1']['type']='login'
G.node['Login_2']['type']='login'
G.node['Login_1']['list']=[]
G.node['Login_2']['list']=[]
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
        emlist_i = list(emcomps(em+log,i)) # This gives the email probability for each composition into i parts in a list.
        ccprob_i = sum(list(cccomps(cc,i))) # This gives the SUM of the card probabilities for all the compositions into i parts.
        totprob_i = sum(ccprob_i*np.array(emlist_i))  # This multiplies each email probability by the sum of the card probabilities, then sums it all up
        problist.append(totprob_i)  # Throw it in the list
    #print(problist)  # Boom.
    return problist.index(max(problist)) + 1 # plus 1 to get the actual number of people (since it starts at zero)


def GraphFeas(G):
    email_nodes=[n for n in G.nodes() if G.node[n]['type']=='email']
    emails=len(email_nodes)
    #Count the 'creditcard' nodes
    cc_nodes=[n for n in G.nodes() if G.node[n]['type']=='creditcard']
    ccs=len(cc_nodes)
    #Count the 'login' nodes
    login_nodes=[n for n in G.nodes() if G.node[n]['type']=='login']
    logins=len(login_nodes)
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


def merge(G,edge):
    """Returns a new graph with edge merged, and the new node containing the
            information lost in the merge. The weights from common neighbors
            are added together, a la Stoer-Wagner algorithm."""            
    if G.node[edge[1]]['type'] == 'login' or G.node[edge[1]]['type'] == 'email':
        edge = edge[::-1] # If login/email is on the right, flip the order, so it's always on the left
    
    nx.set_node_attributes(G,'list',{edge[0]:G.node[edge[0]]['list']+[edge[1]]})

    J = nx.contracted_edge(G,(edge[0],edge[1]),self_loops = False)  #Contract edge without self-loop
    # Weight stuff
    N = nx.common_neighbors(G,edge[0],edge[1]) #find common nodes
    for i in N:
        J[i][edge[0]]['weight'] = G[edge[0]][i]['weight'] + G[edge[1]][i]['weight'] #modify the weight after contraction
    return J
    
#nx.set_node_attributes(graphname,'list',{'em_3':graphname.node[nodename]['list']+[thingtoaddin]})


def drawnice(G):
    posG=nx.spring_layout(G,k=0.6)
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
            after_cut = after_cut + [sub_G.nodes()]
        else:
            edges = edges_to_merge(sub_G)
            A = sub_G
            for Eg in edges:
                A = merge(A,Eg)
            #plt.figure('A')
            #drawnice(A)
            cut_val, cuts = nx.stoer_wagner(A)
            #print(cuts[0])
            #plt.figure('aftercutting0')
            #drawnice(A.subgraph(cuts[0]))
            #plt.figure('aftercutting1')
            #drawnice(A.subgraph(cuts[1]))
            nodelist1 = []
            for nd in cuts[0]:
                #if G.node[nd]['type'] == 'login' or G.node[nd]['type'] == 'email':
                nodelist1 = nodelist1 + A.node[nd]['list']
                nodelist1 = nodelist1 + [nd]
            nodelist2 = []
            for nd in cuts[1]:
                #if G.node[nd]['type'] == 'login' or G.node[nd]['type'] == 'email':
                nodelist2 = nodelist2 + A.node[nd]['list']
                nodelist2 = nodelist2 + [nd]   
            #print(nodelist1)
            #print(nodelist2)
            #plt.figure('sub1')
            sub1 = sub_G.subgraph(nodelist1)
            #drawnice(sub1)
            #print(sub1.nodes(data=True))
            #print(sub1.node['Login_1']['list'])
            sub2 = sub_G.subgraph(nodelist2)
            #print(sub2.nodes(data=True))
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
    print(A)
    graph_list = []
    for lst in A:
        graph_list = graph_list + [G.subgraph(lst)]
    return graph_list        
            