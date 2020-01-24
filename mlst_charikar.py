import networkx as nx
import math
import copy
from get_worst_graph import *
#from mlst_kruskal import *
import sys
from input_functions import *
import time

def MLST_charikar(Gs, TT):
  MLST = []
  cost = 0
  G_res = nx.Graph()
  G_res.add_node(TT[0][0])
  l = len(TT)
  for Ti in TT:
    for ti in Ti:
      mn_pth = None
      mn_pth_len = -1
      for tar in G_res.nodes():
        pth = nx.shortest_path(Gs[l-1], source=ti, target=tar)
        pth_len = sum([Gs[l-1].get_edge_data(pth[i-1], pth[i])['weight'] for i in range(1, len(pth))])
        if mn_pth_len==-1:
          mn_pth_len = pth_len
          mn_pth = pth
        elif mn_pth_len>pth_len:
          mn_pth_len = pth_len
          mn_pth = pth
      G_res.add_edges_from([(mn_pth[i-1], mn_pth[i]) for i in range(1, len(mn_pth))])
      cost += mn_pth_len
    l -= 1
  MLST = G_res.edges()
  return MLST, cost

def check_mlst_charikar(folder_name, file_name_without_ext, output_file):
  filename = folder_name + '/' + file_name_without_ext +'.txt'
  Gs, Ts = build_networkx_non_uniform_graph(filename)
  #Ts.reverse()
  TT = [Ts[0]]
  for i in range(1, len(Ts)):
    TT.append(list(set(Ts[i])-set(Ts[i-1])))
  #TOP = MLST_TOP(G,TT)
  start_time = time.time()
  MLST, cost = MLST_charikar(Gs,TT)
  total_time = time.time() - start_time
  # append the outputs to a csv file
  #f = open(folder_name + '/' + output_file, 'a')
  #f.write(folder_name + ';' + file_name_without_ext + ';' + str(MLST_Costs(G,QOS)[1]) + ';\n')
  #f.close()
  print(folder_name + ';' + file_name_without_ext + ';' + str(cost) + ';' + str(total_time) + ';\n')

if __name__ == '__main__':
  # 1. Folder name
  # 2. File name
  # 3. Output File name
  check_mlst_charikar(sys.argv[1], sys.argv[2], sys.argv[3])

