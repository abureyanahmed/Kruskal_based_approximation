import networkx as nx
from get_worst_graph import *
import copy
import random
import sys
from input_functions import *
import time

def mlst_kruskal_old(G, Ts):
  '''
  Ts[0] is the bottom level and contains maximum number of elements
  '''
  # find the root: a vertex in top level
  # while not all terminals are covered
  #  find minimum with local cost
  #  find min with global cost
  #  if global cost is less than twice the local cost take global path, else local path

  # find all pair shortest path on terminals
  # put all the shortest path in a set
  # take the min from the set that does not form cycle, this is local
  # take the min from root that does not form a cycle, this is global

  # The above idea is more advanced
  # A simple idea is to select a root
  # consider all terminals of all levels
  # partition this terminals in to two sets, connected and disconnected
  # initially connected has only root vertex
  # find all the shortest path between conneccted terminals and disconnected terminals
  # Take the minimum path
  # continue while disconnected terminal set is not empty
  MLST = []
  for i in range(len(Ts)):
    MLST.append(nx.Graph())
  r = Ts[len(Ts)-1][0]
  con_ts = [(r, len(Ts)-1)]
  dis_ts = [(x, len(Ts)-1) for x in Ts[len(Ts)-1][1:]]
  for i in range(len(Ts)-1):
    for x in Ts[i][1:]:
      dis_ts.append((x, i))
  #print(con_ts, dis_ts)
  while len(dis_ts)>0:
    min_d = None
    min_u = None
    min_v = None
    for u in con_ts:
      for v in dis_ts:
        #print("u, v:", u, v)
        v1, l1 = u
        v2, l2 = v
        if l1<l2: continue
        if v1==v2: continue
        d = nx.shortest_path_length(G, v1, v2, 'weight')
        if min_d == None:
          min_d = d
          min_u = u
          min_v = v
        else:
          if min_d>d:
            min_d = d
            min_u = u
            min_v = v
    v1, l1 = min_u
    v2, l2 = min_v
    #for i in range(min(l1, l2)+1):
    #  MLST[i].add_weighted_edges_from([(v1, v2, min_d)])
    #  u = (v2, i)
    #  if u in dis_ts:
    #    dis_ts.remove(u)
    #  if u not in con_ts:
    #    con_ts.append(u)
    MLST[min(l1, l2)].add_weighted_edges_from([(v1, v2, min_d)])
    for i in range(min(l1, l2)+1):
      u = (v2, i)
      if u in dis_ts:
        dis_ts.remove(u)
      if u not in con_ts:
        con_ts.append(u)
  cost = 0
  for G2 in MLST:
    for e in G2.edges():
      cost += G.get_edge_data(e[0],e[1])['weight']
  return MLST, cost

def InclusiveTerminals(TT):
    M=len(TT)
    Tm = list(TT)
    for m in range(1,M):
        Tm[m] = Tm[m-1]+TT[m]
    return(tuple(Tm))

def Kruskal(G):

    MST=nx.create_empty_copy(G); # MST(G)
    N=nx.number_of_nodes(G)
    E=nx.number_of_edges(G)
    i=0; # counter for edges of G
    k=0; # counter for MST(G)

    edge_list = sorted(G.edges(data=True), key=lambda x:x[2]['weight'])

    while k<(N-1) and i<(E):
        e=edge_list[i];
        i+=1
        if not nx.has_path(MST,e[0],e[1]):
            MST.add_edge(e[0],e[1],weight=e[2]['weight'])
            k+=1

    return(MST)

def SteinerTree(G,T):

    HG=nx.Graph()
    HG.add_nodes_from(T)  # Hyper graph with nodes T and edges with weight equal to distance
    n=len(T)

    for i in range(n):
        for j in range(i+1,n):
            HG.add_edge(T[i], T[j], weight=nx.shortest_path_length(G,T[i], T[j],'weight'))

    HG_MST = Kruskal(HG)

    G_ST=nx.Graph()
    for e in HG_MST.edges(data=False):
        P=nx.shortest_path(G,e[0],e[1],'weight')
        G_ST.add_path(P)

    # find the minimum spanning tree of the resultant graph

    return(G_ST)

def PruneBranches(G,T):
    has_one=False
    for v in G.nodes(data=False):
        if (v not in T) and (G.degree(v)==1):
            has_one=True
            G.remove_edge(v,*G.neighbors(v))
    if has_one:
        PruneBranches(G,T)

def MLST_BOT(G,TT):
    M=len(TT)
    Tm = InclusiveTerminals(TT)

    G_ST_BOT=[None]*M
    #G_ST_BOT[M-1] = SteinerTree(G,Tm[M-1])
    G_ST_BOT[M-1] = SteinerTree(G,Tm[M-1])

    for m in range(M-2,-1,-1):
        G_ST_BOT[m] = copy.deepcopy(G_ST_BOT[m+1])
        PruneBranches(G_ST_BOT[m],Tm[m])
    return(tuple(G_ST_BOT))
    
def MLST_Costs(G,G_MLST):
    M=len(G_MLST)
    C=[0]*M
    for m in range(M):
        #print(G_MLST[m].edges(data=False))
        #print_edges(G_MLST[m])
        for e in G_MLST[m].edges(data=False):
            C[m]+=G.get_edge_data(e[0],e[1])['weight']
            #print(str(e[0])+","+str(e[1])+":"+str(G.get_edge_data(e[0],e[1])['weight']))
    #print(C)
    #print(sum(C))
    return(C,sum(C))

def MLST_TOP(G,TT):

    M=len(TT);
    Tm= InclusiveTerminals(TT)

    G_ST_TOP=[None]*M
    G_ST_TOP[0] = SteinerTree(G,Tm[0])
    #G_ST_TOP[0] = SteinerTree2Approx(G,Tm[0])
    #print(G_ST_TOP[0].edges())

    for m in range(1,M):
        G2=copy.deepcopy(G)
        for e in G_ST_TOP[m-1].edges(data=True):
            #nx.set_edge_attributes(G2, 'weight', {(e[0],e[1]):0})
            nx.set_edge_attributes(G2, {(e[0],e[1]):{'weight':0}})
        #G_ST_TOP[m] = SteinerTree2Approx(G2,Tm[m])
        G_ST_TOP[m] = SteinerTree(G2,Tm[m])

    return(tuple(G_ST_TOP))

def mlst_kruskal(G, Ts):
  '''
  G is the input graph
  Ts[0] is the bottom level and contains maximum number of elements
  '''
  TT = [Ts[0]]
  for i in range(1, len(Ts)):
    TT.append(list(set(Ts[i])-set(Ts[i-1])))
  BOT = MLST_BOT(G,TT)
  #for graph in BOT:
  #  print([(u, v, G.get_edge_data(u, v)['weight'])for u, v in graph.edges()])
  #print("BU cost", MLST_Costs(G,BOT)[1])
  Ts.reverse()
  #MLST_bot_level = [(u, v, G.get_edge_data(u, v)['weight'])for u, v in BOT[0].edges()]
  MLST_bot_level = BOT[len(BOT)-1]
  #print(Ts)
  for l in range(1, len(Ts)):
    #print("l:", l)
    #print("MLST_bot_level", MLST_bot_level.edges())
    sp_arr = []
    for i in range(len(Ts[l])):
      for j in range(i+1, len(Ts[l])):
        pth = nx.shortest_path(G, source=Ts[l][i], target=Ts[l][j])
        pth_len = sum([G.get_edge_data(pth[i-1], pth[i])['weight'] for i in range(1, len(pth))])
        sp_arr.append((pth, pth_len))
    sp_arr = sorted(sp_arr, key=lambda x: x[1])
    components = [set([T]) for T in Ts[l]]
    for pth, pth_len in sp_arr:
      #print("components:", components)
      #print("pth:", pth)
      s, t = pth[0], pth[len(pth)-1]
      for i in range(len(components)):
        if s in components[i]:
          s_cmp = i
        if t in components[i]:
          t_cmp = i
      if s_cmp==t_cmp:
        continue
      #print(components, s, t, s_cmp, t_cmp)
      if s_cmp<t_cmp:
        components[s_cmp] = components[s_cmp] | components[t_cmp]
        components.pop(t_cmp)
      else:
        components[t_cmp] = components[t_cmp] | components[s_cmp]
        components.pop(s_cmp)
      p1 = pth
      #print("p1", p1)
      p2 = nx.shortest_path(MLST_bot_level, source=s, target=t)
      #print("p2", p2)
      p1_n_p2 = set([(p1[i-1], p1[i]) for i in range(1, len(p1))]) - set([(p2[i-1], p2[i]) for i in range(1, len(p2))])
      p1_and_p2 = set([(p1[i-1], p1[i]) for i in range(1, len(p1))]) & set([(p2[i-1], p2[i]) for i in range(1, len(p2))])
      x = sum([G.get_edge_data(u, v)['weight'] for u, v in p1_n_p2])
      w_p1_and_p2 = sum([G.get_edge_data(u, v)['weight'] for u, v in p1_and_p2])
      w_p2 = sum([G.get_edge_data(p2[i-1], p2[i])['weight'] for i in range(1, len(p2))])
      #if w_p2>((i+1)*x + w_p1_and_p2):
      if w_p2>((l+1)*x + w_p1_and_p2):
        MLST_bot_level.add_edges_from([(u, v) for u, v in p1_n_p2])
        cut_edges = []
        while len(MLST_bot_level.nodes())<=len(MLST_bot_level.edges()):
          heav_w = 0
          heav_u = None
          heav_v = None
          #for i in range(1, len(p2)):
          #  u, v = p2[i-1], p2[i]
          for u, v in MLST_bot_level.edges():
            if G.get_edge_data(u, v)['weight']>heav_w and ((u, v) not in cut_edges):
              heav_w = G.get_edge_data(u, v)['weight']
              heav_u = u
              heav_v = v
          MLST_bot_level.remove_edge(heav_u, heav_v)
          if not nx.is_connected(MLST_bot_level):
            cut_edges.append((heav_u, heav_v))
            cut_edges.append((heav_v, heav_u))
            MLST_bot_level.add_edge(heav_u, heav_v)
  MLST = []
  MLST.append(MLST_bot_level)
  PruneBranches(MLST[0],Ts[0]) # newly added
  #print(MLST)
  for l in range(1, len(Ts)):
    MLST.append(copy.deepcopy(MLST[l-1]))
    PruneBranches(MLST[l],Ts[l])
  #print(MLST)
  c = 0
  for l in range(len(MLST)):
    #print(MLST[l].edges())
    for u, v in MLST[l].edges():
      c += G.get_edge_data(u, v)['weight']
  return MLST, c

def check_mlst_kruskal(folder_name, file_name_without_ext, output_file):
  filename = folder_name + '/' + file_name_without_ext +'.txt'
  G, subset_arr = build_networkx_graph(filename)
  #subset_arr.reverse()
  start_time = time.time()
  MLST, kruskal_cost = mlst_kruskal(G, subset_arr)
  total_time = time.time() - start_time
  # append the outputs to a csv file
  #f = open(folder_name + '/' + output_file, 'a')
  #f.write(folder_name + ';' + file_name_without_ext + ';' + str(kruskal_cost) + ';\n')
  #f.close()
  print(folder_name + ';' + file_name_without_ext + ';' + str(kruskal_cost) + ';' + str(total_time) + ';\n')

if __name__ == '__main__':
  # 1. Folder name
  # 2. File name
  # 3. Output File name
  check_mlst_kruskal(sys.argv[1], sys.argv[2], sys.argv[3])

