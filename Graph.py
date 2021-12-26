import math


class Graph:
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        graph = {}
        for node in nodes:
            graph[node] = {}
        graph.update(init_graph)

        for node,edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False)==False:
                    graph[adjacent_node][node] = value
        return graph

    def get_nodes(self):
        return self.nodes

    def get_connections(self, node):
        connections = []
        for o_node in self.nodes:
            if self.graph[node].get(o_node, False) != False:
                connections.append(o_node)
        return connections

    def get_value(self, node1, node2):
        return self.graph[node1][node2]

def dijkstra_algo(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    print(f"Running dijkstra algo on a graph of {len(unvisited_nodes)} nodes, starting node {start_node}")
    shortest_path = {}
    prev_nodes = {}
    max_val = math.inf
    for node in unvisited_nodes:
        shortest_path[node] = max_val
    shortest_path[start_node] = 0

    while(unvisited_nodes):
        # print(f"have {len(unvisited_nodes)} left")
        cur_min_node = None
        for node in unvisited_nodes:
            if cur_min_node == None:
                cur_min_node = node
            elif shortest_path[node] < shortest_path[cur_min_node]:
                cur_min_node = node
        neighbors = graph.get_connections(cur_min_node)
        # print(f"Checking {len(neighbors)} neighbors")
        for n in neighbors:
            val = shortest_path[cur_min_node] + graph.get_value(cur_min_node,n)

            if val < shortest_path[n]:
                shortest_path[n] = val
                prev_nodes[n] = cur_min_node
        unvisited_nodes.remove(cur_min_node)

    return prev_nodes, shortest_path

def print_result(prev_nodes, shortest_path, start_node, end_node):
    path = []
    node = end_node

    while node != start_node:
        path.append(node)
        node = prev_nodes[node]

    path.append(start_node)

    print(f"Shortest path from f{start_node} to {end_node} has a value of {shortest_path[end_node]}")
    print(' -> '.join(reversed(path)))