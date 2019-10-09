import numpy as np
import random
import operator
import pandas as pd
from tqdm import tqdm

class City:
    def __init__(self, x, y, index):
        # Index represents the column number of the city
        self.index = index
        self.x = x
        self.y = y

    # Calculate Euclidean distance
    def distance(self, city):
        return np.sqrt((self.x-city.x)**2+(self.y-city.y)**2)

    # Each city is represented as their index
    def __repr__(self):
        return str(self.index)


def create_route(city_list):
    route = random.sample(city_list, len(city_list))
    return route

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    # Calculate the total distance of the route
    def total_distance(self):
        if self.distance == 0:
            route_distance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i+1 < len(self.route):
                    toCity = self.route[i+1]
                else:
                    toCity = self.route[0]
                route_distance += fromCity.distance(toCity)
            self.distance = route_distance
        return self.distance

    def get_fitness(self):
        if self.fitness == 0:
            self.fitness = 1/float(self.total_distance())
        return self.fitness

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

class GA:
    def __init__(self, cityList, popSize, eliteSize, mutationRate, generations):
        self.cityList = cityList
        self.popSize = popSize
        population = []
        for i in range(0, self.popSize):
            population.append(create_route(self.cityList))
        self.population = population
        self.population = population
        self.eliteSize = eliteSize
        self.mutationRate = mutationRate
        self.generations = generations

    def rank_routes(self, pop):
        fitness_results = {}
        for i in range(0, len(pop)):
            fitness_results[i] = Fitness(pop[i]).get_fitness()
        return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)

    def selection(self, ranked_pop):
        selection_results = []
        df = pd.DataFrame(np.array(ranked_pop), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(0, self.eliteSize):
            selection_results.append(ranked_pop[i][0])
        for i in range(0, len(ranked_pop) - self.eliteSize):
            pick = 100 * random.random()
            for i in range(0, len(ranked_pop)):
                if pick <= df.iat[i, 3]:
                    selection_results.append(ranked_pop[i][0])
                    break
        return selection_results

    def matingPool(self, pop, selectionResults):
        matingpool = []
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matingpool.append(pop[index])
        return matingpool


    def breedPopulation(self, matingpool):
        children = []
        length = len(matingpool) - self.eliteSize
        pool = random.sample(matingpool, len(matingpool))

        for i in range(0, self.eliteSize):
            children.append(matingpool[i])

        for i in range(0, length):
            child = breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children


    def mutate(self, individual):
        for swapped in range(len(individual)):
            if (random.random() < self.mutationRate):
                swapWith = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swapWith]

                individual[swapped] = city2
                individual[swapWith] = city1
        return individual


    def mutatePopulation(self, pop):
        mutatedPop = []

        for ind in range(0, len(pop)):
            mutatedInd = self.mutate(pop[ind])
            mutatedPop.append(mutatedInd)

        return mutatedPop


    def nextGeneration(self):
        ranked_pop = self.rank_routes(self.population)
        selection_results = self.selection(ranked_pop)
        matingpool = self.matingPool(self.population, selection_results)
        children = self.breedPopulation(matingpool)
        nextGeneration = self.mutatePopulation(children)
        self.population = nextGeneration

