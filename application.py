# voeg de huidige structuur toe aan path
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))

# importeer de gebruikte structuur
from brute_force import brute_force
from random_algorithm import random_solution
from greedy_hillclimber import greedy
from greedy_hillclimber import add_missing_houses
from greedy_hillclimber import hillclimber_determined
from hillclimber import hillclimber
from simulated_annealing import simulated_annealing
from smartgrid import SmartGrid
import visualiser as vis



if __name__ == "__main__":


    # Ask user to choose a neighborhood
    print(f"Hello! Welcome at the application of team Smartgrid10\n\
    Choose a neighbourhood for the smartgrid problem\n")

    while True:
        neighbourhood = int(input("Type 1, 2 or 3\n"))
        if neighbourhood == 1 or neighbourhood == 2 or neighbourhood == 3:
            break

    # Ask user for fixed or moveable batteries
    type = ''
    fixed = None
    pos = ''
    different = False
    algorithm = None
    print(f"\nShould the neighbourhood have fixed or moveable batteries?")

    while True:
        answer = str(input("\nType A for fixed batteries and B for moveable batteries\n"))
        if answer == 'A':
            position_batteries = "Fixed_batteries"
            fixed = True
            break
        if answer == 'B':
            position_batteries = "Moveable_batteries"
            fixed = False

            # Ask user if they want different types of batteries and how to define their positions
            print(f"\nDo you want one type of battery or different types?")
            while True:
                answer = str(input("Type A for one type and type B for different types\n"))
                if answer == 'A':
                    type = 'regular'
                    break
                if answer == 'B':
                    different = True
                    type = 'different'
                    break
            print(f"\nDo want random positions for the batteries or define their position with K-means clustering?")
            while True:
                answer = str(input("Type A for random positions and B for K-means clustering\n"))
                if answer == 'A':
                    pos = "random_position"
                    break
                if answer == 'B':
                    pos = "cluster_position"
                    break
            break

    # Load data
    smartgrid = SmartGrid(neighbourhood, fixed, pos, different)

    # Show user batteries
    count = 0
    print("\nThese are your batteries:")
    for battery in smartgrid.batteries:
        print(smartgrid.batteries[battery])
        count += 1

    # Calculate bounds
    minim, maxim = smartgrid.bound()
    print(f"\nMinimum bound neigbourhood: {minim}\n"f"Maximum bound neigbourhood: {maxim}")

    # Ask user for algorithm
    print(f"Which algoritm would you like to use?\n\
        Type A for a brute force algorithm\n\
        Type B for a random algorithm that will run 1.000 times and saves the best result\n\
        Type C for a greedy algorithm followed by a hillclimber\n\
        Type D for a hillclimber algorithm on a random solution\n\
        Type E or a simulated annealing algorithm on a random solution")

    while True:
        answer = str(input())
        if answer == 'A':
            results = brute_force(smartgrid)
            algorithm = "brute_force"
            break
        if answer == 'B':
            results = random_solution(smartgrid, count)
            algorithm = "random"
            break
        if answer == 'C':
            results = greedy(smartgrid)
            results = add_missing_houses(smartgrid, results)
            results = hillclimber_determined(smartgrid, results)
            algorithm = "greedy_hillclimber"
            break
        if answer == 'D':
            results = random_solution(smartgrid, count)
            results = hillclimber(smartgrid, results)
            algorithm = "hillclimber"
            break
        if answer == 'E':
            results = random_solution(smartgrid, count)
            results = simulated_annealing(smartgrid, results)
            algorithm = "simulated_annealing"
            break


    # Visualiser --> TO DO: SEPERATE LOADER FOR DIFFERENT ALGORITHMS

    # Plots a linechart of a single neighbourhood
    # data = vis.load_results_runs('results_SA1_distance.csv')
    # vis.plot_line(data)

    # Plots a comparison for the different neighbourhoods
    '''data = vis.load_results_runs('results_random_distance.csv')
    data1 = vis.load_results_runs('results_GH1_distance.csv')
    # data2 = vis.load_results_runs('results_SA3_distance.csv')
    vis.plot_comparison(data, data1, data2)'''


    total_distance = results[0]
    connections = results[1]
    print(f"Total distance: {total_distance}")

    # Calculate total costs
    price_grid = 9
    costs_grid = price_grid * total_distance
    costs_batteries = 0
    for battery in smartgrid.batteries:
        costs_batteries += smartgrid.batteries[battery].price
    total_costs = costs_batteries + costs_grid
    print(f"Total costs: {total_costs}")

    # Write results to csv
    smartgrid.write_to_csv(position_batteries, type, pos, algorithm, neighbourhood, connections, total_distance, costs_grid, costs_batteries, total_costs)
