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
from greedy_hillclimber import hillclimber
from simulated_annealing import simulated_annealing
from smartgrid import SmartGrid
import visualiser as vis



if __name__ == "__main__":


    # Ask user to choose a neighborhood
    '''print(f"Hello! Welcome at the application of team Smartgrid10\n\
    Choose a neighborhood for the smartgrid problem\n")

    while True:
        neighbourhood = int(input("Type 1, 2 or 3\n"))
        if neighbourhood == 1 or neighbourhood == 2 or neighbourhood == 3:
            break

    # Ask user for fixed or moveable batteries
    fixed = None
    print(f"Should the neighbourhood have fixed or moveable batteries?")

    while True:
        answer = str(input("Type A for fixed batteries and B for moveable batteries\n"))
        if answer == 'A':
            position_batteries = "Fixed_batteries"
            fixed = True
            break
        if answer == 'B':
            position_batteries = "Moveable_batteries"
            fixed = False
            break'''

    # Load data


    # Calculate bounds
    #smartgrid.bound()

    # Ask user for algorithm
    '''print(f"Which algoritm would you like to use?\n\
        Type A for a brute force algorithm\n\
        Type B for a random algorithm that will run 10.000 times and saves the best result\n\
        Type C for a greedy algorithm followed by a hillclimber\n\
        Type D for a simulated annealing algorithm on a random solution")

    while True:
        answer = str(input())
        if answer == 'A':
            results = brute_force(smartgrid)
            algorithm = "brute_force"
            break
        if answer == 'B':
            results = random_solution(smartgrid)
            algorithm = "random"
            break
        if answer == 'C':
            results = greedy(smartgrid)
            results = add_missing_houses(smartgrid, results)
            results = hillclimber(smartgrid, results)
            algorithm = "greedy_hillclimber"
            break
        if answer == 'D':
            results = random_solution(smartgrid)
            results = simulated_annealing(smartgrid, results)
            algorithm = "simulated_annealing"
            break '''

    # RUNT smartgrid en pakt laagste bound etc
    bound = 10
    for i in range(1):
        smartgrid = SmartGrid(2, True)
        boundje = smartgrid.bound()
        results = greedy(smartgrid)
        results = random_solution(smartgrid)
        results = simulated_annealing(smartgrid, results)

        if bound > boundje:
            bound = boundje
            best_positions = []
            for battery in smartgrid.batteries:
                xypos = []
                xypos.append(smartgrid.batteries[battery].xpos)
                xypos.append(smartgrid.batteries[battery].ypos)
                best_positions.append(xypos)

    print("GRIDJE3 - bound:", bound)

    total_distance = results[0]
    connections = results[1]

    #Visualiser
    # data = vis.load_results_runs('results_random_distance.csv')
    # vis.plot_line(data)
    data = vis.load_results_runs('results_random_distance.csv')
    vis.plot_line(data)

    # test
    '''houses_list = []
    print(len(connections))
    print(total_distance)
    for battery in smartgrid.batteries:
        print(smartgrid.batteries[battery])
    for connection in connections:
        houses_list.append(connection['house'])

    missing_houses = [value for value in range(1, 150) if value not in houses_list]
    print(missing_houses)'''

    print(f"Total distance: {total_distance}")

    # # Calculate total costs
    # price_grid = 9
    # costs_grid = price_grid * total_distance
    # costs_batteries = 5 * 5000
    # total_costs = costs_batteries + costs_grid
    # #print(f"Total costs: {total_costs}")

    # Write results to csv
    # smartgrid.write_to_csv(position_batteries, algorithm, neighbourhood, connections, total_distance, costs_grid, costs_batteries, total_costs)
