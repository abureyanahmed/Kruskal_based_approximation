from subprocess import call
import math
from get_worst_graph import *

def generate():
  #root_folder = "experiment_qos_krus"
  root_folder = "experiment_qos_krus_2"
  #root_folder = "experiment_ER"
  #root_folder = "experiment_WS"
  #root_folder = "experiment_2"
  #root_folder = "experiment_4"
  #call(["rm", "-rf", "Graph_generator/"+experiment_name])
  call(["mkdir", root_folder])
  #name_of_graph_class = ['WS','ER','BA','GE']
  #name_of_graph_class_code = ['0','1','2','3']
  name_of_graph_class = ['ER']
  #name_of_graph_class = ['WS']
  name_of_graph_class_code = ['1']
  #name_of_graph_class_code = ['0']
  #number_of_nodes_progression = [100, 100, 100]
  #number_of_nodes_progression = [80, 80, 80]
  number_of_nodes_progression = [100, 100, 100, 100, 100, 100]
  #number_of_levels = [1, 2, 3]
  number_of_levels = [2, 3, 4, 5, 6, 7]
  #number_of_nodes_progression = [15, 15, 15]
  #number_of_levels = [1, 2, 3]
  node_distribution_in_levels = ['L','E']
  node_distribution_in_levels_code = ['0','1']
  #node_distribution_in_levels = ['L']
  #node_distribution_in_levels_code = ['0']
  #param1 = ['6', '.25', '5', '1.62']
  #param2 = ['.2', '0', '0', '0']
  param1 = ['.25']
  param2 = ['0']
  #param1 = ['6']
  #param2 = ['.2']
  initial_nodes = 10
  node_increment = 5
  #initial_nodes = 20
  #node_increment = 20
  curr_id = 1
  f1 = open(root_folder + '/id_to_file.csv', 'w')
  f2 = open(root_folder + '/id_to_file_qos.csv', 'w')
  f3 = open(root_folder + '/id_to_file_cmp.csv', 'w')
  #f4 = open(root_folder + '/id_to_file_CMP_exact.csv', 'w')
  f5 = open(root_folder + '/id_to_file_kruskal.csv', 'w')
  #for cl in range(len(name_of_graph_class)):
  for l in range(len(number_of_levels)):
    for w in range(10, 101):
  #  for nd in range(len(node_distribution_in_levels)):
      common_part_of_name = str(number_of_levels[l]) + '_' + str(w)
      #call(["mkdir", root_folder + "/" + common_part_of_name])
      #for p in range(initial_nodes, number_of_nodes_progression[l]+1, node_increment):
       #if name_of_graph_class[cl] == 'ER':
       # param1[cl] = str((1+1)*math.log(p)/p)
       #elif name_of_graph_class[cl] == 'GE':
       # param1[cl] = str(math.sqrt((1+1)*math.log(p)/(math.pi*p)))
       #call(["python3", "graph_generator.py", str(number_of_levels[l]), str(p), root_folder + "/graph_" + common_part_of_name + '_' + str(p), name_of_graph_class_code[cl], param1[cl], param2[cl], node_distribution_in_levels_code[nd]])
      filename = root_folder + "/graph_" + common_part_of_name
      #G, Ts = get_worst_TD(number_of_levels[l], w)
      #Ts.reverse()
      #write_graph(G, Ts, filename)
      f1.write(str(curr_id) + ';' + 'mlst_exact.py' + ';' + root_folder + ';' + "graph_" + common_part_of_name + ';' + 'output_exact.csv' + ';\n')
      f2.write(str(curr_id) + ';' + 'mlst_qos.py' + ';' + root_folder + ';' + "graph_" + common_part_of_name + ';' + 'output_qos.csv' + ';\n')
      f3.write(str(curr_id) + ';' + 'mlst_cmp.py' + ';' + root_folder + ';' + "graph_" + common_part_of_name + ';' + 'output_cmp.csv' + ';\n')
      f5.write(str(curr_id) + ';' + 'mlst_kruskal.py' + ';' + root_folder + ';' + "graph_" + common_part_of_name + ';' + 'output_kruskal.csv' + ';\n')
      curr_id = curr_id + 1
  f1.close()
  f2.close()
  f3.close()
  #f4.close()
  f5.close()

def write_graph(graph, Ts, filename):
  file = open(filename+".txt","w")
  file.write(str(graph.number_of_edges())+"\n");
  edges = graph.edges()
  for e in edges:
        file.write(str(e[0])+" "+str(e[1])+" "+str(graph.get_edge_data(e[0],e[1])['weight'])+"\n")
  levels = len(Ts)
  file.write(str(levels)+"\n")
  for l in range(levels):
        steiner_nodes = len(Ts[l])
        steiner_nodes_str = ""
        for j in range(steiner_nodes-1):
                steiner_nodes_str = steiner_nodes_str + str(Ts[l][j]) + " "
        steiner_nodes_str = steiner_nodes_str + str(Ts[l][steiner_nodes-1]);
        file.write(steiner_nodes_str+"\n")
  #file.write(stretch_factor+"\n")
  file.close()


generate()
