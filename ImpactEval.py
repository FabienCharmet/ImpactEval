# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
import random

G=nx.DiGraph()
Gfunc=nx.DiGraph()

"""
IMPORT FUNCTION OF THE RESOURCE GRAPH
"""

# Rarray = [[0,1,0.1],[1,0,0.7],[0,2,0.4],[2,0,0.1],[0,3,0.2],[3,0,0.1],
#           [1,3,0.6],[3,1,0.9],[2,3,0.9],[3,2,0.5]]

# SEarray = [[4,1,0.3],[5,2,0.9]]

# BFarray = [[0,6,0.9],[0,7,0.1],[1,6,0.6],[6,8,0.8],[7,8,0.7]]



Rarray = [[0,1,0.8],[1,0,0.6]]

SEarray = [[2,0,0.8],[3,0,0.8]]

BFarray = [[0,4,0.7],[1,4,0.6]]


Rnodes = set()
for g in Rarray:
    Rnodes.add(g[0])


SEnodes = set()
for se in SEarray:
    SEnodes.add(se[0])

# Calculating which nodes are Business Resource nodes
# i.e. nodes from Rarray (resource graph) connected to BFarray (business graph)
set_infranodes = set((x[0] for x in Rarray)).union((x[1] for x in Rarray))
BRnodes = set_infranodes.intersection((x[0] for x in BFarray))
# print(BRnodes)

BFnodes = set()
for bf in BFarray:
    BFnodes.add(bf[1])
BFnodes = sorted(BFnodes)

Gtemp=Rarray
Gtemp+=SEarray
Gtemp+=BFarray

# print(Gnodes)
# print(SEnodes)
# print(BFnodes)
# print(BRnodes)

for a in Gtemp:
    G.add_edge(a[0],a[1],weight=a[2])
    
for a in BFarray:
    Gfunc.add_edge(a[0],a[1],weight=a[2])

"""
IMPORT FUNCTION OF THE TRANSITION MATRICES
"""
# np.random.seed()




"""
COMPUTING THE IMPACT ON A TARGET NODE
"""
def compute_impact_proba(ntimes):
    counter_array=[0]*G.number_of_nodes()
    # np.random.seed(42)
    for i in range(ntimes):
        var_sampling = []
        for i in Gtemp:
            var_sampling.append([i[0],i[1],np.random.rand()])
    # print(var_sampling)
        number_of_ticks=0
        tick_array=[0]*G.number_of_nodes()
        # Checking if business resources are impacted
        for brsource in BRnodes:
            varcont=True
            # print("\n\n")
            for sesource in SEnodes:
                paths = nx.all_simple_paths(G, source=sesource, target=brsource)
                pathlist = list(paths)
                random.shuffle(pathlist)
                # print(type(pathlist))
                for p in pathlist:
                    # print(p)
                    ind=0
                    path_array=[0] * len(p)
                    path_array[0]=1
                    while(ind<len(p)-1):
                        proba = np.random.rand()
                        proba = (x for x in var_sampling if x[0]==p[ind] and x[1]==p[ind+1])
                        proba = list(proba)
                        proba = proba[0][2]
                        # print(G[p[ind]][p[ind+1]]["weight"])
                        # print(str(proba) + " " + str(G[p[ind]][p[ind+1]]["weight"]) + "  " + str(proba<=G[p[ind]][p[ind+1]]["weight"])) 
                        if(proba<=G[p[ind]][p[ind+1]]["weight"]):                   
                            path_array[ind+1]=1
                        # else:
                        #     print(str(proba) + " " + str(G[p[ind]][p[ind+1]]["weight"]) + "  " + str(proba<=G[p[ind]][p[ind+1]]["weight"])) 
                        # print(ind)
                        # print(G[p[ind]][p[ind+1]]["weight"])
                        ind+=1
                    if(0 not in path_array):
                        # print(p)
                        # print(path_array)
                        # print("success for br: " + str(brsource) + " and se: " + str(sesource))
                        varcont=False
                        if(tick_array[brsource]==0):
                            # if(brsource==1):
                            #     print(path_array)
                            tick_array[brsource]=1
                            counter_array[brsource]+=1
                            number_of_ticks+=1
                            break
                        else:
                            print("error")
                if(varcont==False):
                    break
                
        for bfsource in BFnodes:
            varcont=True
            for brsource in BRnodes:
                if(tick_array[brsource]==1):
                    paths = nx.all_simple_paths(G, source=brsource, target=bfsource)
                    pathlist=list(paths)
                    random.shuffle(pathlist)
                    gen = (p for p in pathlist if len(p)==2)
                    # gen = (p for p in list(paths))
                    for p in gen:
                        ind=0
                        path_array=[0] * len(p)
                        path_array[0]=tick_array[brsource]
                        # print(p)
                        while(ind<len(p)-1):
                            proba = np.random.rand()
                            proba = (x for x in var_sampling if x[0]==p[ind] and x[1]==p[ind+1])
                            proba = list(proba)
                            proba = proba[0][2]
                            if(proba<=G[p[ind]][p[ind+1]]["weight"]):   
                                path_array[ind+1]=1
                            # print(ind)
                            # print(G[p[ind]][p[ind+1]]["weight"])
                            ind+=1
                        if(0 not in path_array):
                            # print(path_array)
                            # print(p)
                            # print("success for bf: " + str(bfsource) + " and br: " + str(brsource))
                            varcont=False
                            if(tick_array[bfsource]==0):
                                tick_array[bfsource]=1
                                counter_array[bfsource]+=1
                                number_of_ticks+=1
                            else:
                                print("error")
                            break
                    if(varcont==False):
                        break
                    
        if(number_of_ticks>len(BFnodes + list(BRnodes))):
            print("error")
        for bftarget in BFnodes:
            if(tick_array[bfsource]==1):
                break
            varcont=True
            for bfsource  in BFnodes:
                if(tick_array[bfsource]==1) and (bfsource != bftarget):
                    paths = nx.all_simple_paths(G, source=bfsource, target=bftarget )
                    pathlist=list(paths)                
                    random.shuffle(pathlist)
                    gen = (p for p in pathlist if len(p)==2)
                    for p in gen:
                        path_array=[0] * len(p)
                        path_array[0]=tick_array[bfsource]
                        # print(p)
                        proba = np.random.rand()
                        proba = (x for x in var_sampling if x[0]==p[ind] and x[1]==p[ind+1])
                        proba = list(proba)
                        proba = proba[0][2]
                        if(proba<=G[p[0]][p[1]]["weight"]):   
                            path_array[1]=1
                        # print(ind)
                        # print(G[p[ind]][p[ind+1]]["weight"])
                        if(0 not in path_array):
                            # print(path_array)
                            # print(p)
                            # print("success for bf: " + str(bfsource) + " and br: " + str(brsource))
                            varcont=False
                            if(tick_array[bftarget]==0):
                                tick_array[bftarget]=1
                                counter_array[bftarget]+=1
                                number_of_ticks+=1
                            else:
                                print("error")
                            break
                    if(varcont==False):
                        break
    proba_array = [x / ntimes for x in counter_array]
    for i in SEnodes:
        proba_array[i]=1.0
    print(proba_array)

def verbose_compute_impact_proba(ntimes):
    counter_array=[0]*G.number_of_nodes()
    # np.random.seed(42)
    print("Evaluating each random variable\n")
    for i in range(ntimes):
        var_sampling = []
        for i in Gtemp:
            var_sampling.append([i[0],i[1],np.random.rand()])
        print("Current state: \n")
        print(var_sampling)
    # print(var_sampling)
        number_of_ticks=0
        tick_array=[0]*G.number_of_nodes()
        # Checking if business resources are impacted
        print("\nChecking if resource nodes are impacted\n")
        
        for brsource in BRnodes:
            print("Evaluating resource node: " + str(brsource) + "\n")
            varcont=True
            # print("\n\n")
            for sesource in SEnodes:
                print("Evaluating the impact of shock event " + str(sesource) + " on node " + str(brsource))
                paths = nx.all_simple_paths(G, source=sesource, target=brsource)
                pathlist = list(paths)
                print("List of paths between shock event" + str(sesource)+ " and node " + str(brsource))
                print(pathlist)
                random.shuffle(pathlist)
                # print(type(pathlist))
                for p in pathlist:
                    print("\nEvaluating impact of SE: " + str(sesource) + " on node: " + str(brsource) + " via path: " + str(p))
                    # print(p)
                    ind=0
                    path_array=[0] * len(p)
                    path_array[0]=1
                    while(ind<len(p)-1):
                        proba = np.random.rand()
                        proba = (x for x in var_sampling if x[0]==p[ind] and x[1]==p[ind+1])
                        proba = list(proba)
                        proba = proba[0][2]
                        # print(G[p[ind]][p[ind+1]]["weight"])
                        # print(str(proba) + " " + str(G[p[ind]][p[ind+1]]["weight"]) + "  " + str(proba<=G[p[ind]][p[ind+1]]["weight"])) 
                        if(proba<=G[p[ind]][p[ind+1]]["weight"]):                   
                            path_array[ind+1]=1
                        # else:
                        #     print(str(proba) + " " + str(G[p[ind]][p[ind+1]]["weight"]) + "  " + str(proba<=G[p[ind]][p[ind+1]]["weight"])) 
                        # print(ind)
                        # print(G[p[ind]][p[ind+1]]["weight"])
                        ind+=1
                    print("Instantiation of random variables in path: " + str(p))
                    print(path_array)
                    if(0 not in path_array):
                        print("SE: " + str(sesource) + " has impacted node: " + str(brsource) + ". No need for further checks.\n")

                        # print(p)
                        # print(path_array)
                        # print("success for br: " + str(brsource) + " and se: " + str(sesource))
                        varcont=False
                        if(tick_array[brsource]==0):
                            # if(brsource==1):
                            #     print(path_array)
                            tick_array[brsource]=1
                            counter_array[brsource]+=1
                            number_of_ticks+=1
                            break
                        else:
                            print("error")
                if(varcont==False):
                    break
                print("SE: " + str(sesource) + " has not impacted node: " + str(brsource) + ". Continuing checks for next SE.\n")              
        for bfsource in BFnodes:
            print("Evaluating Business Function node: " + str(bfsource) + "\n")
            varcont=True
            print("For each resource nodes connected to "+ str(bfsource))
            for brsource in BRnodes:
                if(tick_array[brsource]==1):
                    print("Evaluating impact of resource node " + str(brsource) + " on node " + str(bfsource))
                    paths = nx.all_simple_paths(G, source=brsource, target=bfsource)
                    pathlist=list(paths)
                    random.shuffle(pathlist)
                    gen = (p for p in pathlist if len(p)==2)
                    # gen = (p for p in list(paths))
                    for p in gen:
                        ind=0
                        path_array=[0] * len(p)
                        path_array[0]=tick_array[brsource]
                        # print(p)
                        while(ind<len(p)-1):
                            proba = np.random.rand()
                            proba = (x for x in var_sampling if x[0]==p[ind] and x[1]==p[ind+1])
                            proba = list(proba)
                            proba = proba[0][2]
                            if(proba<=G[p[ind]][p[ind+1]]["weight"]):   
                                path_array[ind+1]=1
                            # print(ind)
                            # print(G[p[ind]][p[ind+1]]["weight"])
                            ind+=1
                        print("Instantiation of random variables in path: " + str(p))
                        print(path_array)   
                        if(0 not in path_array):
                            print("Node " + str(brsource) + " has impacted node: " + str(bfsource) + ". No need for further checks.\n")
                            # print(path_array)
                            # print(p)
                            # print("success for bf: " + str(bfsource) + " and br: " + str(brsource))
                            varcont=False
                            if(tick_array[bfsource]==0):
                                tick_array[bfsource]=1
                                counter_array[bfsource]+=1
                                number_of_ticks+=1
                            else:
                                print("error")
                            break
                    if(varcont==False):
                        break
                    print("Node " + str(brsource) + " has not impacted node: " + str(bfsource) + ". Continuing checks for next SE.\n")              

                    
        if(number_of_ticks>len(BFnodes + list(BRnodes))):
            print("error")
        for bftarget in BFnodes:
            if(tick_array[bfsource]==1):
                break
            print("Evaluating Business Function node " + str(bftarget) + "\n")
            varcont=True
            for bfsource  in BFnodes:
                if(tick_array[bfsource]==1) and (bfsource != bftarget):
                    paths = nx.all_simple_paths(G, source=bfsource, target=bftarget )
                    pathlist=list(paths)                
                    if(len(pathlist)>0):
                        print("Evaluating impact of business node " + str(bfsource) + " on node " + str(bftarget))
                    else:
                        print("There are no business function nodes impacting node " + str(bftarget))
                        break
                    gen = (p for p in pathlist if len(p)==2)
                    for p in gen:
                        print(p)
                        path_array=[0] * len(p)
                        path_array[0]=tick_array[bfsource]
                        # print(p)
                        proba = np.random.rand()
                        proba = (x for x in var_sampling if x[0]==p[ind] and x[1]==p[ind+1])
                        proba = list(proba)
                        proba = proba[0][2]
                        if(proba<=G[p[0]][p[1]]["weight"]):   
                            path_array[1]=1
                        # print(ind)
                        # print(G[p[ind]][p[ind+1]]["weight"])
                        print("Instantiation of random variables in path: " + str(p))
                        print(path_array)   
                        if(0 not in path_array):
                            print("BF: " + str(bfsource) + " has impacted node: " + str(bftarget) + ". No need for further checks.\n")

                            # print(path_array)
                            # print(p)
                            # print("success for bf: " + str(bfsource) + " and br: " + str(brsource))
                            varcont=False
                            if(tick_array[bftarget]==0):
                                tick_array[bftarget]=1
                                counter_array[bftarget]+=1
                                number_of_ticks+=1
                            else:
                                print("error")
                            break
                    if(varcont==False):
                        break
                    print("BF: " + str(bfsource) + " has not impacted node: " + str(bftarget) + ". Continuing checks for next SE.\n")              

    proba_array = [x / ntimes for x in counter_array]
    for i in SEnodes:
        proba_array[i]=1.0
    print("Final array after one iteration:")
    print(proba_array)

def verbose_inclusion_exclusion():
    proba_array=[0]*G.number_of_nodes()
    print("Evaluating all possible target nodes\n")
    for bf in BFnodes + list(BRnodes):
        print("Evaluating node: " + str(bf))
        # print("\n\n\n")
        list_of_paths = []
        list_of_proba = []
        bfproba=0
        sbfproba=""
        print("Evaluating all possible shock events\n")
        for se in SEnodes:
            print("Evaluating shock event: " + str(se))
            paths = nx.all_simple_paths(G, source=se, target=bf)
            temp_paths = nx.all_simple_paths(G, source=se, target=bf)
            print("List of paths between shock event " + str(se)+ " and node " + str(bf))
            print(list(temp_paths))

            for p in list(paths):
                list_of_paths.append(list(p))
                probaset = set()
                for ind in range(0,len(p)-1):
                    probaset=probaset.union({tuple([p[ind],p[ind+1],G[p[ind]][p[ind+1]]["weight"]])})
                    # print([p[ind],p[ind+1],G[p[ind]][p[ind+1]]["weight"]])
                    # print(p)
                # print(probaset)
                list_of_proba+=[probaset]
            # print(list_of_proba)
            # print("\n\n")
        # for i in range(len(list_of_paths)):
        #     print(list_of_paths[i])
        #     print(list_of_proba[i])
        # print("\n\n")
        print("\n Aggregating all paths between all shock events and node " + str(bf))
        print(list_of_paths)
        print("\n For each path, generating a set containing all probabilities of variables in the path")
        print(list_of_proba)
        print("Generating all possible probability sets related to path combinations of size 1 to " + str(len(list_of_proba)))
        
        for i in range(1,len(list_of_proba)+1):
            proof_combination = list(itertools.combinations(list_of_proba,i))
            # print(len(proof_combination))
            # print(len(proof_combination[0]))
#            print(proof_combination)
            # temp = proof_combination[0]
            for comb in proof_combination:
                combset = set()
                for elem in comb:
                    # print(set(elem))
                    combset = combset.union(set(elem))
                print("\nCurrent combination : " +str(combset))
            # print("Source: " + str(bf))
#                print(combset)
                proba=1
                sproba=""
                print("\n Computing path probabilities by multiplying all probabilities in " + str(combset))
                for probaelem in combset:
                    # print(probaelem[2])
                    proba*=probaelem[2]
                    sproba+=" * " + str(probaelem[2])
#
                print("\n Path probability: " + str(sproba[2:]) + " = " + str(round(proba,3)))
                # print(elem)
                # print(proba)
                # print(bfproba)
                bfproba+=((-1)**(i+1))*proba
                sbfproba+=" + ((-1)**("+str(i+1)+"))*"+str(round(proba,3))
        print("\n Probability for node " + str(bf) + ": \n" + sbfproba[3:] + " = " + str(round(bfproba,3)))
        # print(len(list_of_proba))
        # print(len(list_of_paths))
        # print("\n\n")
        proba_array[bf]=bfproba
    for i in SEnodes:
        proba_array[i]=1.0
    print("\nProbability array:")
    print(proba_array)

def inclusion_exclusion():
    proba_array=[0]*G.number_of_nodes()
    for bf in BFnodes + list(BRnodes):
        # print("\n\n\n")
        list_of_paths = []
        list_of_proba = []
        bfproba=0
        
        for se in SEnodes:
            paths = nx.all_simple_paths(G, source=se, target=bf )
            for p in list(paths):
                list_of_paths.append(list(p))
                probaset = set()
                for ind in range(0,len(p)-1):
                    probaset=probaset.union({tuple([p[ind],p[ind+1],G[p[ind]][p[ind+1]]["weight"]])})
                    # print([p[ind],p[ind+1],G[p[ind]][p[ind+1]]["weight"]])
                    # print(p)
                # print(probaset)
                list_of_proba+=[probaset]
            # print(list_of_proba)
            # print("\n\n")
        # for i in range(len(list_of_paths)):
        #     print(list_of_paths[i])
        #     print(list_of_proba[i])
        # print("\n\n")
        for i in range(1,len(list_of_proba)+1):
            proof_combination = list(itertools.combinations(list_of_proba,i))
            # print(len(proof_combination))
            # print(len(proof_combination[0]))
            
            # temp = proof_combination[0]
            for comb in proof_combination:
                combset = set()
                for elem in comb:
                    # print(set(elem))
                    combset = combset.union(set(elem))
            # print("Source: " + str(bf))
            # print(combset)
                proba=1
                for probaelem in combset:
                    # print(probaelem[2])
                    proba*=probaelem[2]

                # print(elem)
                # print(proba)
                # print(bfproba)
                bfproba+=((-1)**(i+1))*proba

        # print(len(list_of_proba))
        # print(len(list_of_paths))
        # print("\n\n")
        proba_array[bf]=bfproba
    for i in SEnodes:
        proba_array[i]=1.0
    print(proba_array)

# nx.draw(G)
labeldict={}
for i in range(G.number_of_nodes()):
    labeldict[i]=str(i)

# nx.draw(G,labels=labeldict,with_labels=True)
# plt.show()


sampling = [10**x for x in range(3,4)]
# sampling = [1]
for i in sampling:
    compute_impact_proba(i)
#verbose_compute_impact_proba(1)
verbose_inclusion_exclusion()
#inclusion_exclusion()

# print(BFnodes)       
# print(BRnodes)
# a = set({tuple([0,1]),tuple([0,4]),tuple([0,3]),tuple([0,2]),tuple([0,2])})
# b = set({tuple([1,1]),tuple([1,4]),tuple([1,3]),tuple([1,2]),tuple([0,2])})
# c = set({tuple([2,1]),tuple([2,4]),tuple([2,3]),tuple([2,2]),tuple([1,2])})
# a=a.union({tuple([0,5])})
# for x in list(itertools.combinations(a,2)):
#     print(x)
# d = set.union(a,b,c)
# print(d)
# for x in list(itertools.combinations(d,2)):
#     print(x)
# nx.draw(G)
# plt.savefig("simple_path.png") # save as png
# plt.draw() # display


# print("Nodes of graph: ")
# print(G.nodes())

# print("Edges of graph: ")

# # [print(G.get_edge_data(*e)) for e in G.edges]
# for e in G.edges:
#     print(G.get_edge_data(*e)['weight']) 
#     print(e)

