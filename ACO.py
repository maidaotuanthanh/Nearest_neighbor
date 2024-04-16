import numpy as np


class AntColony:
    def __init__(self, num_ants, num_iterations, decay_rate, alpha=1, beta=1):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay_rate = decay_rate
        self.alpha = alpha
        self.beta = beta

    def _update_pheromone(self, delta_pheromone):
        self.pheromone *= (1 - self.decay_rate)
        self.pheromone += delta_pheromone

    def _calculate_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += np.linalg.norm(self.points[path[i]] - self.points[path[i + 1]])
        distance += np.linalg.norm(self.points[path[-1]] - self.points[path[0]])
        return distance

    def fit(self, points):
        self.points = points
        num_points = len(points)
        self.pheromone = np.ones((num_points, num_points))

        best_path = None
        best_distance = np.inf

        for iteration in range(self.num_iterations):
            all_paths = []
            all_distances = []
            for _ in range(self.num_ants):
                start_point = np.random.randint(num_points)
                current_point = start_point
                visited = [False] * num_points
                visited[current_point] = True
                path = [current_point]
                total_distance = 0

                while False in visited:
                    probabilities = ((self.pheromone[current_point] ** self.alpha) *
                                     ((1 / (1e-10 + np.linalg.norm(self.points[current_point] - self.points,
                                                                   axis=1))) ** self.beta))
                    visited = np.array(visited)
                    probabilities = probabilities * (1 - visited)
                    probabilities = np.divide(probabilities, np.sum(probabilities))  # Normalize the probabilities
                    next_point = np.random.choice(np.arange(num_points), p=probabilities)
                    visited[next_point] = True
                    path.append(next_point)
                    total_distance += np.linalg.norm(self.points[current_point] - self.points[next_point])
                    current_point = next_point

                total_distance += np.linalg.norm(self.points[path[-1]] - self.points[path[0]])
                all_paths.append(path)
                all_distances.append(total_distance)

            # Update pheromone
            delta_pheromone = np.zeros((num_points, num_points))
            for path, distance in zip(all_paths, all_distances):
                for i in range(len(path) - 1):
                    delta_pheromone[path[i], path[i + 1]] += 1 / distance
                delta_pheromone[path[-1], path[0]] += 1 / distance
            self._update_pheromone(delta_pheromone)

            # Update best path
            if min(all_distances) < best_distance:
                best_distance = min(all_distances)
                best_path = all_paths[np.argmin(all_distances)]

        self.best_path = best_path
        self.best_distance = best_distance

    def print_best_path(self):
        print("Best path:", self.best_path)
        print("Minimum distance:", self.best_distance)


# # Example usage:
# if __name__ == "__main__":
#     # Đầu vào là tọa độ các điểm trong kho
#     # points = np.array([[0, 0], [1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
#     #
#     # # Tạo một đối tượng ACO và fit với các điểm trong kho
#     # aco = AntColony(num_ants=5, num_iterations=100, decay_rate=0.5)
#     # aco.fit(points)
#     #
#     # # In ra tuyến đường tối ưu và quãng đường ngắn nhất
#     # aco.print_best_path()
#     #
#     # # Giả sử có một lượng đơn hàng cần lấy hàng
#     # orders = [2, 4, 1, 3]
#     #
#     # # Xây dựng tuyến đường tối ưu cho việc lấy các đơn hàng này
#     # optimal_order_path = [0]  # Điểm bắt đầu
#     # for order in orders:
#     #     optimal_order_path += [order]
#     # optimal_order_path += [0]  # Quay về điểm bắt đầu
#     #
#     # print("Optimal order picking path:", optimal_order_path)
#     # print("Distance for optimal order picking path:", aco._calculate_distance(optimal_order_path))
#
#     # Tạo ma trận thể hiện vị trí các sản phẩm
#     products = np.array([[0, 0], [1, 2], [3, 4], [5, 6], [7, 8]])
#
#     # Định nghĩa các đơn hàng
#     orders = [[0, 1], [2, 3, 4]]  # Mỗi đơn hàng là một danh sách các chỉ số sản phẩm
#
#     # Khởi tạo đối tượng AntColony
#     aco = AntColony(num_ants=50, num_iterations=100, decay_rate=0.5)
#
#     # Tìm đường đi ngắn nhất cho mỗi đơn hàng
#     for order in orders:
#         # Lấy tọa độ của các sản phẩm trong đơn hàng
#         points = products[order]
#
#         # Sử dụng ACO để tìm đường đi ngắn nhất
#         aco.fit(points)
#
#         # In ra lộ trình và khoảng cách
#         aco.print_best_path()
