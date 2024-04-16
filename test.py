# # def Dijkstra(graph, source, target):
# #     # Khởi tạo các biến
# #     shortest_distances = {node: float('infinity') for node in graph}
# #     shortest_distances[source] = 0
# #     predecessors = {node: None for node in graph}
# #     unvisited_nodes = graph.copy()
# #
# #     current_node = source
# #
# #     # Lặp cho đến khi tất cả các node đều đã được thăm
# #     while unvisited_nodes:
# #         # Cập nhật khoảng cách ngắn nhất cho các node liền kề
# #         for neighbour, distance in graph[current_node].items():
# #             if neighbour in unvisited_nodes:
# #                 new_distance = shortest_distances[current_node] + distance
# #                 if new_distance < shortest_distances[neighbour]:
# #                     shortest_distances[neighbour] = new_distance
# #                     predecessors[neighbour] = current_node
# #
# #         # Loại bỏ node hiện tại khỏi tập hợp các node chưa được thăm
# #         unvisited_nodes.pop(current_node)
# #
# #         # Chọn node chưa được thăm với khoảng cách ngắn nhất để trở thành node hiện tại
# #         if unvisited_nodes:
# #             current_node = min(unvisited_nodes, key=shortest_distances.get)
# #         else:
# #             break
# #
# #     # Xây dựng đường đi ngắn nhất từ source đến target
# #     path = []
# #     while target:
# #         path.insert(0, target)
# #         target = predecessors[target]
# #
# #     return path
# #
# # # Định nghĩa đồ thị
# # graph = {
# #     'a': {'b': 2, 'c': 7, 'g': 4},
# #     'b': {'a': 2, 'j': 4, 'd': 6},
# #     'c': {'a': 7, 'g': 5, 'h': 3, 'd': 2},
# #     'd': {'b': 6, 'c': 2, 'e': 1},
# #     'e': {'d': 1, 'j': 8, 'f': 1, 'h': 2},
# #     'f': {'e': 1, 'h': 5, 'i': 4, 'k': 3},
# #     'g': {'a': 4, 'c': 5, 'h': 2},
# #     'h': {'g': 2, 'c': 3, 'e': 2, 'f': 5, 'i': 6},
# #     'i': {'f': 4, 'h': 6, 'k': 9},
# #     'j': {'b': 4, 'e': 8, 'k': 5},
# #     'k': {'j': 5, 'f': 3, 'i': 9}
# # }
# #
# # # Gọi hàm Dijkstra
# # path = Dijkstra(graph, 'a', 'k')
# # path1 = Dijkstra(graph, 'k', 'b')
# #
# # # In đường đi
# # print(f"Đường đi từ 'a' đến 'k': {path}")
# # print(f"Đường đi từ 'k' đến 'b': {path1}")
# # Python3 Program for Floyd Warshall Algorithm
#
# # Number of vertices in the graph
# V = 4
#
# # Define infinity as the large
# # enough value. This value will be
# # used for vertices not connected to each other
# INF = 99999
#
# # Solves all pair shortest path
# # via Floyd Warshall Algorithm
#
#
# def floydWarshall(graph):
#     """ dist[][] will be the output
#        matrix that will finally
#         have the shortest distances
#         between every pair of vertices """
#     """ initializing the solution matrix
#     same as input graph matrix
#     OR we can say that the initial
#     values of shortest distances
#     are based on shortest paths considering no
#     intermediate vertices """
#
#     dist = list(map(lambda i: list(map(lambda j: j, i)), graph))
#
#     """ Add all vertices one by one
#     to the set of intermediate
#      vertices.
#      ---> Before start of an iteration,
#      we have shortest distances
#      between all pairs of vertices
#      such that the shortest
#      distances consider only the
#      vertices in the set
#     {0, 1, 2, .. k-1} as intermediate vertices.
#       ----> After the end of a
#       iteration, vertex no. k is
#      added to the set of intermediate
#      vertices and the
#     set becomes {0, 1, 2, .. k}
#     """
#     for k in range(V):
#
#         # pick all vertices as source one by one
#         for i in range(V):
#
#             # Pick all vertices as destination for the
#             # above picked source
#             for j in range(V):
#
#                 # If vertex k is on the shortest path from
#                 # i to j, then update the value of dist[i][j]
#                 dist[i][j] = min(dist[i][j],
#                                  dist[i][k] + dist[k][j]
#                                  )
#     printSolution(dist)
#
#
# # A utility function to print the solution
# def printSolution(dist):
#     print("Following matrix shows the shortest distances\
#  between every pair of vertices")
#     for i in range(V):
#         for j in range(V):
#             if(dist[i][j] == INF):
#                 print("%7s" % ("INF"), end=" ")
#             else:
#                 print("%7d\t" % (dist[i][j]), end=' ')
#             if j == V-1:
#                 print()
#
#
# # Driver's code
# if __name__ == "__main__":
#     """
#                 10
#            (0)------->(3)
#             |         /|\
#           5 |          |
#             |          | 1
#            \|/         |
#            (1)------->(2)
#                 3           """
#     graph = [[0, 5, INF, 10],
#              [INF, 0, 3, INF],
#              [INF, INF, 0,   1],
#              [INF, INF, INF, 0]
#              ]
#     # Function call
#     floydWarshall(graph)

import numpy as np

# Define the vertices
vertices = ['A', 'B', 'C', 'D', 'E', 'F']

# Initialize the adjacency matrix
adjacency_matrix = np.zeros((len(vertices), len(vertices)))

# Define the edges
# edges = {
#     'A': ['B', 'C'],
#     'B': ['A', 'C', 'F'],
#     'C': ['A', 'B', 'D', 'E'],
#     'D': ['C', 'E', 'F'],
#     'E': ['A', 'C', 'D'],
#     'F': ['B', 'D']
# }

# graph = [[0, 1, 1, 0, 0, 0],
#          [1, 0, 1, 0, 0, 1],
#          [1, 1, 0, 1, 1, 0],
#          [0, 0, 1, 0, 1, 1],
#          [1, 0, 1, 1, 0, 0],
#          [0, 1, 0, 1, 0, 0]]
graph = {
    'Z': {'A': 1, 'L': 2},
    'A': {'B': 1, 'Z': 1, 'L': 1},
    'B': {'A': 1, 'C': 1},
    'C': {'B': 1, 'D': 1},
    'D': {'C': 1, 'E': 1},
    'E': {'D': 1, 'F': 1},
    'F': {'E': 1, 'G': 1},
    'G': {'H': 1, 'F': 1, 'R': 1},
    'H': {'G': 1, 'I': 1},
    'I': {'H': 1, 'J': 1},
    'J': {'I': 1, 'K': 1},
    'K': {'J': 1, 'L': 1},
    'L': {'K': 1, 'Z': 2, 'M': 1},
    'M': {'N': 1, 'Z': 2.5, 'L': 1},
    'N': {'O': 1, 'M': 1},
    'O': {'N': 1, 'P': 1},
    'P': {'O': 1, 'Q': 1},
    'Q': {'P': 1, 'R': 1},
    'R': {'Q': 1, 'G': 1},
}


def shortest_path(graph, start, target=''):
    unvisited = list(graph)
    distances = {node: 0 if node == start else float('inf') for node in graph}
    paths = {node: [] for node in graph}
    paths[start].append(start)

    while unvisited:
        current = min(unvisited, key=distances.get)
        for node, distance in graph[current].items():  # Change this line
            if distance + distances[current] < distances[node]:
                distances[node] = distance + distances[current]
                if paths[node] and paths[node][-1] == node:
                    paths[node] = paths[current][:]
                else:
                    paths[node].extend(paths[current])
                paths[node].append(node)
        unvisited.remove(current)

    targets_to_print = [target] if target else graph
    for node in targets_to_print:
        if node == start:
            continue
        # print(f'\n{start}-{node} distance: {distances[node]}\nPath: {" -> ".join(paths[node])}')

    return distances, paths

# Call the function with the correct variable
# shortest_path(graph, 'O', 'G')
def shortest_path_through_nodes(graph, nodes):
    total_distance = 0
    total_path = []
    for i in range(len(nodes) - 1):
        distances, paths = shortest_path(graph, nodes[i], nodes[i+1])
        total_distance += distances[nodes[i+1]]
        total_path.extend(paths[nodes[i+1]][:-1])  # Don't include the last node as it will be included in the next path
    total_path.append(nodes[-1])  # Add the last node
    return total_distance, total_path

# Call the function with the correct variable
distance, path = shortest_path_through_nodes(graph, ['Z', 'I', 'P', 'K'])
print(f"Total distance: {distance}\nPath: {' -> '.join(path)}")