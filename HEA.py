import random


# Define necessary functions and classes
class Item:
    def __init__(self, id, weight, position):
        self.id = id
        self.weight = weight
        self.position = position


class Request:
    def __init__(self, id, items, deadline):
        self.id = id
        self.items = items
        self.deadline = deadline


class Batch:
    def __init__(self):
        self.items = []
        self.total_weight = 0


class Chromosome:
    def __init__(self, genome1, genome2):
        self.genome1 = genome1
        self.genome2 = genome2
        self.fitness = 0


def evaluate_fitness(chromosome):
    # Evaluate the fitness of the chromosome
    # For demonstration, a simple fitness calculation
    fitness = sum(chromosome.genome1) + sum(chromosome.genome2)
    return fitness


def initialize_population(size, items, requests):
    population = []
    for _ in range(size):
        genome1 = [random.randint(1, 3) for _ in items]
        genome2 = [random.randint(1, len(requests)) for _ in items]
        chromosome = Chromosome(genome1, genome2)
        chromosome.fitness = evaluate_fitness(chromosome)
        population.append(chromosome)
    return population


def selection(population):
    # Select the best individuals for crossover
    selected = random.choices(population, k=len(population) // 2)
    if len(selected) % 2 != 0:  # Ensure the number of selected individuals is even
        selected.append(random.choice(population))
    return selected


def crossover(parent1, parent2):
    # Perform crossover between two parents to generate offspring
    crossover_point = random.randint(0, len(parent1.genome1) - 1)
    child1_genome1 = parent1.genome1[:crossover_point] + parent2.genome1[crossover_point:]
    child2_genome1 = parent2.genome1[:crossover_point] + parent1.genome1[crossover_point:]

    child1_genome2 = parent1.genome2[:crossover_point] + parent2.genome2[crossover_point:]
    child2_genome2 = parent2.genome2[:crossover_point] + parent1.genome2[crossover_point:]

    child1 = Chromosome(child1_genome1, child1_genome2)
    child2 = Chromosome(child2_genome1, child2_genome2)

    return child1, child2


def mutation(chromosome):
    # Mutate a chromosome
    if len(chromosome.genome1) > 1:  # Ensure there is a valid range
        mutation_point = random.randint(0, len(chromosome.genome1) - 1)
        chromosome.genome1[mutation_point] = random.randint(1, 3)
        chromosome.genome2[mutation_point] = random.randint(1, len(chromosome.genome2))
        chromosome.fitness = evaluate_fitness(chromosome)


def hybrid_evolutionary_algorithm(items, requests, max_generations, population_size):
    population = initialize_population(population_size, items, requests)
    for generation in range(max_generations):
        selected = selection(population)
        next_generation = []
        for i in range(0, len(selected), 2):
            parent1 = selected[i]
            parent2 = selected[i + 1]
            child1, child2 = crossover(parent1, parent2)
            mutation(child1)
            mutation(child2)
            next_generation.append(child1)
            next_generation.append(child2)
        population = sorted(next_generation + population, key=lambda x: x.fitness)[:population_size]
        print(f'Generation {generation}: Best Fitness: {population[0].fitness}')
    return population[0]


# Generate sample items and requests
items = [Item(i, random.randint(1, 10), (random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))) for i in
         range(10)]
requests = [Request(i, random.sample(items, random.randint(1, 5)), random.randint(36000, 64800)) for i in range(5)]

# Run the algorithm with the generated sample data
best_solution = hybrid_evolutionary_algorithm(items, requests, max_generations=100, population_size=50)
best_solution.genome1, best_solution.genome2