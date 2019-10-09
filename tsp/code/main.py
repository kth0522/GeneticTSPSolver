import tsp_parser
import ga
import random
import csv
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


def main():
    # city_list = tsp_parser.parser("rl11849.tsp")
    # print(city_list)
    # x = []
    # y = []
    # for i in tqdm(range(len(city_list)), desc="parsing now..."):
    #     x.append(city_list[i].x)
    #     y.append(city_list[i].y)

    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=100, help="population size")
    parser.add_argument('-f', type=int, default=10, help="total number of fitness evaluations")
    args = parser.parse_args()

    pop_size = args.p
    generations = args.f

    print("population size: "+str(pop_size))
    print("total generations: "+str(generations))

    city_list = []
    for i in range(0, 25):
        city_list.append(ga.City(x=int(random.random() * 200), y=int(random.random() * 200), index = i))

    model = ga.GA(cityList=city_list, popSize=pop_size, eliteSize=20, mutationRate=0.01, generations=generations)
    progress = []
    progress.append(1/model.rank_routes(model.population)[0][1])

    for i in tqdm(range(0, model.generations), desc="Evolving now..."):
        model.nextGeneration()
        progress.append(1 / model.rank_routes(model.population)[0][1])

    best_route = model.population[model.rank_routes(model.population)[0][0]]
    print(best_route)
    print("Final distance: " + str(1 / model.rank_routes(model.population)[0][1]))

    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()


    f = open('solution.csv', 'w', newline='')
    wr = csv.writer(f)
    for i in range(len(best_route)):
        wr.writerow([best_route[i]])

    f.close()

if __name__ == "__main__":
    main()