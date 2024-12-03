import argparse
import time

class KnapsackProblem:
    def __init__(self, profits=None, weights=None, capacity=None, file_path=None):
        if file_path:
            self.read_from_file(file_path)
        else:
            self.profits = profits
            self.weights = weights
            assert len(profits) == len(weights), "Profits and weights must have the same length"
            self.n = len(profits)
            self.capacity = capacity
            self.x = [0] * self.n
            self.z = 0
    
    def read_from_file(self, file_path):
        with open(file_path, "r") as file:
            first_line = file.readline().split()
            self.n = int(first_line[0])
            self.capacity = int(first_line[1])
            self.profits = []
            self.weights = []
            
            for _ in range(self.n):
                profit, weight = map(int, file.readline().split())
                self.profits.append(profit)
                self.weights.append(weight)
        
        assert len(self.profits) == len(self.weights) == self.n, "The number of profits and weights must match the specified number of items"
        self.x = [0] * self.n
        self.z = 0

    def solve_problem(self):
        # initialize a n*capacity table
        d = [[0 for _ in range(self.capacity + 1)] for _ in range(self.n + 1)]
        
        # fill the table
        for i in range(1, self.n + 1):
            for j in range(self.capacity + 1):
                # includes item if it fits
                if self.weights[i-1] <= j:
                    d[i][j] = max(d[i-1][j], self.profits[i-1] + d[i-1][j - self.weights[i-1]])
                # excludes item
                else:
                    d[i][j] = d[i-1][j]
        
        # store the decision variables
        current_weight = self.capacity
        for i in range(self.n, 0, -1):
            if d[i][current_weight] != d[i-1][current_weight]:  # item i-1 is included
                self.x[i-1] = 1
                current_weight -= self.weights[i-1]  # reduce current weight by the weight of item i-1
        
        # store the solution
        self.z = d[self.n][self.capacity]

# command-line argument parsing
parser = argparse.ArgumentParser(description='Solve the knapsack problem.')
parser.add_argument('file_path', type=str, help='Path to the file containing profits, weights, and capacity.')
args = parser.parse_args()

# define the knapsack problem
kp = KnapsackProblem(file_path=args.file_path)

# start measuring execution time
start_time = time.perf_counter()

# solve using the network simplex method
kp.solve_problem()

# stop measuring execution time
end_time = time.perf_counter()
execution_time = end_time - start_time

# Solve the knapsack problem and print the result
print(f'x = {kp.x}')
print(f'z = {kp.z}')
print(f'Execution time: {execution_time} seconds')
