import tsp_parser
import ga
import csv
import argparse
import matplotlib.pyplot as plt
from tqdm import tqdm


def main():
    city_list = tsp_parser.parser("rl11849.tsp")
    print(city_list)

    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default=100, help="population size")
    parser.add_argument('-f', type=int, default=10, help="total number of fitness evaluations")
    parser.add_argument('-plot', type=str, default='n', choices=['n', 'y'], help="Plot the distance-generation graph (y)es/(n)o")
    args = parser.parse_args()

    pop_size = args.p
    generations = args.f
    is_plot = args.plot

    print("population size: "+str(pop_size))
    print("total generations: "+str(generations))

    # declare model
    model = ga.GA(cityList=city_list, popSize=pop_size, eliteSize=20, mutationRate=0.01, generations=generations)
    progress = []
    progress.append(1/model.rank_routes(model.population)[0][1])

    for i in tqdm(range(0, model.generations), desc="Evolving now..."):
        model.nextGeneration()
        progress.append(1 / model.rank_routes(model.population)[0][1])

    best_route = model.population[model.rank_routes(model.population)[0][0]]
    print(best_route)
    print("Final distance: " + str(1 / model.rank_routes(model.population)[0][1]))

    # plot the progress graph if argument plot is 'y'
    if is_plot == "y":
        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.show()

    # write solution file with best_route
    f = open('solution.csv', 'w', newline='')
    wr = csv.writer(f)
    for i in range(len(best_route)):
        wr.writerow([best_route[i]])

    f.close()

if __name__ == "__main__":
    main()