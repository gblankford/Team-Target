import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def emcomps(n,k):
  """Returns the email probability for each composition of n emails among k people in a list"""
  if n < 0 or k < 0:
    return
  elif k == 0:
    # the empty sum, by convention, is zero, so only return something if
    # n is zero
    if n == 0:
      yield []
    return
  elif k == 1:
    yield emprob(n) #emprob is the probability that a person has n emails
    return
  else:
    for i in range(0,n+1):
      for comp in emcomps(n-i,k-1):
        yield emprob(i)*comp

def cccomps(n,k):
  """Returns the card probability for each composition of n credit cards among k people in a list"""
  if n < 0 or k < 0:
    return
  elif k == 0:
    # the empty sum, by convention, is zero, so only return something if
    # n is zero
    if n == 0:
      yield []
    return
  elif k == 1:
    yield ccprob(n) #ccprob is the probability that a person has n credit cards
    return
  else:
    for i in range(0,n+1):
      for comp in cccomps(n-i,k-1):
        yield ccprob(i)*comp      

        

def emprob(n):
    """This returns the probability of one person having n email accounts
            according to some data on the internet"""
    #This numbers could and should be changed depending on the data
    if n == 0:
        return 0 #This is the probability that a person has 0 emails
    if n == 1:
        return 0.2417+.0668 #This is the probability that a person has 1 emails
    if n == 2:
        return 0.3829 #This is the probability that a person has 2 emails
    if n == 3:
        return 0.2417 #This is the probability that a person has 3 emails
    if n == 4:
        return 0.0606 #This is the probability that a person has 4 emails
    if n >= 5:
        return 0.0062 #This is the probability that a person has 5 emails
        
def ccprob(n):
    """This returns the probability of one person having n credit cards
            according to some data on the internet"""
    #This numbers could and should be changed depending on the data
    if n == 0:
        return 0.18 #This is the probability that a person has 0 credit/debit cards
    if n == 1 or n == 2: 
        return 0.48 #This is the probability that a person has 1 or 2 credit/debit cards
    if n == 3 or n == 4: 
        return 0.18 #This is the probability that a person has 3 or 4 credit/debit cards
    if n == 5 or n == 6:
        return 0.09 #This is the probability that a person has 5 or 6 credit/debit cards
    if n >= 7:
        return 0.07 #This is the probability that a person has 7+ credit/debit cards

def feas2(em,cc,log):
    """Returns the most feasible number of people associated with em emails
            and cc credit cards"""
    problist = []  # initialize the list of probabilities
    for i in range(1,em+log+1):  # i is the number of people we're splitting them among
        emlist_i = list(emcomps(em+log,i)) # This gives the email probability for each composition into i parts in a list.
        ccprob_i = sum(list(cccomps(cc,i))) # This gives the SUM of the card probabilities for all the compositions into i parts.
        totprob_i = sum(ccprob_i*np.array(emlist_i))  # This multiplies each email probability by the sum of the card probabilities, then sums it all up
        problist.append(totprob_i)  # Throw it in the list
        if i>1:
            if problist[0]<sum(problist[2:]):
                return 1
    return 0 # plus 1 to get the actual number of people (since it starts at zero)


def GraphFeas(G):
    """Uses the feas2 function to compute the most probably number of people represented in the graph.
    This is based on the number of emails, logins, and credit cards."""
    #Count the number of 'email' nodes in the graph G
    email_nodes=[n for n in G.nodes() if G.node[n]['type']=='email']
    emails=len(email_nodes)
    #Count the 'creditcard' nodes in the graph G
    cc_nodes=[n for n in G.nodes() if G.node[n]['type']=='creditcard']
    ccs=len(cc_nodes)
    #Count the 'login' nodes in the graph G
    login_nodes=[n for n in G.nodes() if G.node[n]['type']=='login']
    logins=len(login_nodes)
    return feas2(emails,ccs,logins)
    
    
def edges_to_merge(G):
    """This function decides how the graph G should be merged before cutting.
    It does this by looking at each cookie and credit card node and merging it 
    with the email or login node it is connected to with the highest weight.
    If there is a tie is grabs the first in the list of its neighbors that are 
     an email or a login."""
    cook_cc_nodes=[]
    merge_edges=[]
    
    #First grab all of the cookie or credit card nodes
    for n0 in G.nodes():
        if G.node[n0]['type']=='cookie' or G.node[n0]['type']=='creditcard':
            cook_cc_nodes=cook_cc_nodes+[n0]
    #Now we look at the neighbors that are a login or email node of each cookie/credit card node.
    #Then grab the edge with the highest weight.
    for N in cook_cc_nodes:
        L=list(nx.all_neighbors(G,N))
        P=[]
        #This will make P a list of the neighbors that are logins or emails
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
        for i in range(0,len(W)):
            w=w+[W[i]['weight']]
            i=i+1
            m=max(w)
    
        #enumerate w and store the exact position the maximum weight occurs
        #position=[k for k, j in enumerate(w) if j == m]
        position=[]
        for k,j in enumerate(w):
            if j==m:
                position=position+[k]
        #grab the node from P that is in the position stored in position. This is the node it should merge with.
        #maxnhbr=[(P[pos]) for pos in position]
        maxnhbr=[P[position[0]]]
        #Now store the edges the need to be merged
        for n3 in maxnhbr:
            merge_edges=merge_edges+[(N,n3)]
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

def drawnice(G):
    """Much better than nx.draw"""    
    posG=nx.spring_layout(G,k=0.7)
    labelsG = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_nodes(G,posG,node_size=800)
    nx.draw_networkx_labels(G,posG,font_size=8,font_family='sans-serif')
    nx.draw_networkx_edges(G,posG,width=1)
    nx.draw_networkx_edge_labels(G,posG,edge_labels=labelsG,fontsize='1')

def target_cut(G):
    """Returns a list of lists each of which contain nodes that correspond to unique people represented 
    in the graph G."""
    #First separate the graph into its connected components
    graphs = list(nx.connected_component_subgraphs(G))
    after_cut = []
    #For each connected component we decide whether or the graph should be cut, based
    #on our feas2 function. Then the component is merged and finally cut.
    for sub_G in graphs:
        #If this returns 1 or True then the component should be cut
        if_cut = GraphFeas(sub_G)
        #In the case the component is not cut then store the nodes associated 
        #to that component and move on.
        if if_cut == 0:
            after_cut = after_cut + [sub_G.nodes()]
        #Other wise we merge and cut the component    
        else:
            #First we look at all the edges that should be merged via the 
            #edges_to_merge function
            edges = edges_to_merge(sub_G)
            A = sub_G
            #Then the edges are merged via the merge function
            for Eg in edges:
                A = merge(A,Eg)
            #After all of the merging is done the graph is cut along a minimum 
            #cut into two connected components via stoer_wagner    
            cut_val, cuts = nx.stoer_wagner(A)
            #This is a small note that would take the weights into consideration
            #before cutting. Thus eliminating possible false cuts on high weights.
#                if cut_val>=some reasonably big number:
#                    after_cut=after_cut+A.nodes()
#                else:
#                    Indent the following code to be in this else statement
            nodelist1 = []
            #The nodes for each component after cutting are stored
            for nd in cuts[0]:
            #To get the nodes in these components we must look "inside" at the
            #list attribute of the merged nodes
                nodelist1 = nodelist1 + A.node[nd]['list']
                nodelist1 = nodelist1 + [nd]
            nodelist2 = []
            #Do the samething for the second component
            for nd in cuts[1]:
                nodelist2 = nodelist2 + A.node[nd]['list']
                nodelist2 = nodelist2 + [nd]  
            #Turn the node lists into subgraphs so the target_cut can be 
            #reinitiated on them until they should not be cut anymore.
            sub1 = sub_G.subgraph(nodelist1)
            sub2 = sub_G.subgraph(nodelist2)
            after_cut = after_cut + target_cut(sub1)
            after_cut = after_cut + target_cut(sub2)
    return after_cut
########################################################################################################
##################### THE ABOVE FUNCTIONS ARE USED IN CODE BELOW ############################         
def graph_construction(G):
    """Returns a list of subgraphs of G found by the target_cut function."""
    #Run target_cut on the graph G to generate a list of lists which contains the nodes that should
    #coorespond to subgraphs of G that represent unique people.
    A = target_cut(G)
    graph_list = []
    #From the list of nodes in A we recreate the subgraphs in G that contain these nodes
    for lst in A:
        graph_list = graph_list + [G.subgraph(lst)]
    return graph_list        

def graph_the_components(graph_list):
    """This function graphs all the components constructed by graph_construction"""
    for g in graph_list:
        plt.figure()
        drawnice(g)