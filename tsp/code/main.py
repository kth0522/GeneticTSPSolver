import tsp_parser
import ga
import csv
import argparse
import matplotlib.pyplot as plt
from tqdm import tqdm


def main():
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('data', type=str, default="rl11849.tsp", help="Data file name  ex)rl11849.tsp")
    parser.add_argument('-p', type=int, default=200, help="Population size")
    parser.add_argument('-f', type=int, default=250, help="Total number of fitness evaluations")
    parser.add_argument('-e', type=int, default=50, help="The size of the elite population")
    parser.add_argument('-m', type=float, default=0.01, help="Probability of the mutation")
    parser.add_argument('-plot', type=str, default='n', choices=['n', 'y'], help="Plot the distance-generation graph (y)es/(n)o")
    args = parser.parse_args()

    data_name = args.data
    pop_size = args.p
    generations = args.f
    elite_size = args.e
    mutation_rate = args.m
    is_plot = args.plot

    city_list = tsp_parser.parser(data_name)

    print("data: "+data_name)
    print("population size: "+str(pop_size))
    print("total generations: "+str(generations))
    print("elite size: "+str(elite_size))
    print("mutation_rate: "+str(mutation_rate))


    # declare model
    model = ga.GA(cityList=city_list, popSize=pop_size, eliteSize=elite_size, mutationRate=mutation_rate, generations=generations)
    progress = []
    progress.append(1/model.rank_routes(model.population)[0][1])

    for i in tqdm(range(0, model.generations), desc="Evolving now..."):
        model.nextGeneration()
        progress.append(1 / model.rank_routes(model.population)[0][1])

    best_route = model.population[model.rank_routes(model.population)[0][0]]

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