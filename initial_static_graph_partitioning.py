import networkx as nx
import metis
import matplotlib.pyplot as plt
import pandas as pd 

data = pd.read_csv('initial_static_graph_partitioning.csv')
start_vertices = data['start_vertex'].tolist()
end_vertices = data['end_vertex'].tolist()
weightList = data['avg_mobility'].tolist()

adjacencyListSrcToDestes = {}


G = nx.Graph()

for i in range(1, no_of_grids + 1):
	G.add_node(i)
	adjacencyListSrcToDestes[i] = []

duplicate_catching_dict = {}
start_vertices_length = len(start_vertices)
for i in range(start_vertices_length):
	first_vertex = start_vertices[i]
	second_vertex = end_vertices[i]
	adjacencyListSrcToDestes[first_vertex].append(second_vertex)

	if(first_vertex > second_vertex):
		first_vertex, second_vertex = second_vertex, first_vertex
	currWeight = weightList[i]
	currTuple = (first_vertex, second_vertex)
	if currTuple not in duplicate_catching_dict:
		duplicate_catching_dict[currTuple] = currWeight
		G.add_edge(first_vertex, second_vertex, weight = currWeight)
	else:
		prevWeight = duplicate_catching_dict[currTuple]
		if prevWeight < currWeight:
			duplicate_catching_dict[currTuple] = currWeight
			G.remove_edge(first_vertex, second_vertex)
			G.add_edge(first_vertex, second_vertex, weight = currWeight)

G.graph['edge_weight_attr']='weight'
no_of_servers = 3
(edgecuts, parts) = metis.part_graph(G, no_of_servers)
colors = ['red','blue','green']
color_map = []
for i, p in enumerate(parts):
     # G.node[i]['color'] = colors[p]
     color_map.append(colors[p])

# nx.drawing.nx_pydot.write_dot(G, 'example1.dot', node_color = color_map)
nx.draw(G, node_color=color_map, with_labels=True)
plt.show()

#Oth iteration er jonno SIR:

population_volume = {}

for eachGrid in (1, no_of_grids+1):
	population_volume[eachGrid] = 70

sir_s_dictionary = {}
sir_i_dictionary = {}
sir_r_dictionary = {}

for eachGrid in (1, no_of_grids + 1):
	sir_s_dictionary[eachGrid] = population_volume[eachGrid]
	sir_i_dictionary[eachGrid] = 0
	sir_r_dictionary[eachGrid] = 0

threashold_population = 50

for eachGrid in (1, no_of_grids + 1):
	if population_volume[eachGrid] > threashold_population:
		first_infection_population = population_volume[eachGrid] // 20
		sir_s_dictionary[eachGrid] = sir_s_dictionary[eachGrid] - first_infection_population
		sir_i_dictionary[eachGrid] = sir_i_dictionary[eachGrid] + first_infection_population

for eachGrid in (1, no_of_grids + 1):
	total_sum = sir_s_dictionary[eachGrid] + sir_i_dictionary[eachGrid] + sir_r_dictionary[eachGrid]
	sir_s_dictionary[eachGrid] = sir_s_dictionary[eachGrid] / total_sum
	sir_i_dictionary[eachGrid] = sir_i_dictionary[eachGrid] / total_sum
	sir_r_dictionary[eachGrid] = sir_r_dictionary[eachGrid] / total_sum


current_iteration = 0
# next_iteration = prev_iteration + 1
fileName = "SIR_values_itr_"+str(current_iteration)+".txt"
with open(fileName, 'w', encoding='utf8') as outputFile:
	for eachGrid in range(1, no_of_grids + 1):
		outputFile.write(str(eachGrid)+" ")
		# currAdjacencyList = adjacencyListSrcToDestes[eachGrid]
		# for eachDestNode in currAdjacencyList:
		# 	outputFile.write(str(eachDestNode)+" ")
		outputFile.write(str(sir_s_dictionary[eachGrid])+" ")
		outputFile.write(str(sir_i_dictionary[eachGrid])+" ")
		outputFile.write(str(sir_r_dictionary[eachGrid])+"\n")
		# outputFile.write("\n")


# next_iteration = prev_iteration + 1
next_iteration = current_iteration + 1
fileName = "graph_structure_itr_"+str(next_iteration)+".txt"
with open(fileName, 'w', encoding='utf8') as outputFile:
	for eachGrid in range(1, no_of_grids + 1):
		outputFile.write(str(eachGrid)+" ")
		currAdjacencyList = adjacencyListSrcToDestes[eachGrid]
		for eachDestNode in currAdjacencyList:
			outputFile.write(str(eachDestNode)+" ")
		outputFile.write("\n")

next_iteration = current_iteration + 1
fileName = "placement_of_primary_copies_"+str(next_iteration)+".txt"
with open(fileName, 'w', encoding='utf8') as outputFile:
	for eachGrid in range(1, no_of_grids + 1):
		outputFile.write(str(eachGrid)+" "+str(parts[eachGrid - 1] + 1))
		outputFile.write("\n")








