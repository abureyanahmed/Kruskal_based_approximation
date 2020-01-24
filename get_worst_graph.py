import networkx as nx

def get_worst_TD(l, w):
  '''
  Ts[0] has the maximum number of terminals, this is the lower level
  '''
  # edges = 1 + 2 + 2*2 + 2*2*2 + 2*2*2*2 + ...
  m = sum([1]+ [2**i for i in range(1, l)])
  n = 2**(l-1) + 1
  G = nx.Graph()
  Ts = []
  #w = 10
  #w = 100
  d = 1
  while d<n:
    #print("d:", d)
    T = []
    for i in range(0, n-d, d):
      G.add_weighted_edges_from([(i, i+d, w)])
      #print(i, i+d, w)
      T.append(i)
    T.append(i+d)
    Ts.append(T)
    w = 2*w - 1
    d *= 2
  return G, Ts

#G, Ts = get_worst_TD(4)
#print(G.edges(data="weight"), Ts)

def get_worst_BU(l):
  '''
  Ts[0] has the maximum number of terminals, this is the lower level
  '''
  n = 100
  #n = 3
  Ts = [[i for i in range(n)]]
  w = 5
  for j in range(l-1):
    Ts.append([0, n-1])
  G = nx.Graph()
  for i in range(n-1):
    G.add_weighted_edges_from([(i, i+1, w)])
  G.add_weighted_edges_from([(0, n-1, w+1)])
  return G, Ts

#G, Ts = get_worst_BU(4)
#print(G.edges(data="weight"), Ts)

