import random
import turtle
import math
import copy

def student_details():
    
    # add variables to store student ID and username to be returned

    student_id = 17062941
    student_username = "eg18aba"
    
    return student_id, student_username


def generate_map(x_range, y_range, locations):

    # add code to create a list then use a for loop to create a random population for this list

    #create an empty lists
    generated_map = []
    single_point = []

    #create negative limits for x and y range
    x_range_neg = -x_range
    y_range_neg = -y_range

    #loop until reach location amount, we generate 2 random int and store them
    for x in range(locations):
        single_point.append(random.randint(x_range_neg, x_range))
        single_point.append(random.randint(y_range_neg, y_range))
        generated_map.append(copy.deepcopy(single_point))
        #add this single_point list to generated_map list as [X, Y]
        single_point = []
        #empty that list again

    return generated_map

def print_map(speed, color, thickness, selected_map):

    # add code to use the turtle to draw the path between all destinations
    # the turtle should make use of the parameters provided: speed. color, etc...
    # you will need to use a loop in order to draw the path to all locations
    #print("printing map")

    turtle.speed(speed)
    turtle.pencolor(color)
    turtle.pensize(thickness)

    #turtle goes to start point with pen up
    turtle.penup()
    turtle.goto(selected_map[0][0], selected_map[0][1])
    turtle.pendown()

    #print(selected_map)

    #outer loop, looping x coordinate count
    for x in range(len(selected_map)):
        #print("starting new loop", x)
        for i in range(1):
            turtle.goto(selected_map[x][i], selected_map[x][i+1])

    #go back to the first location/city
    turtle.goto(selected_map[0][0], selected_map[0][1])
    #freeze frame
    turtle.done()

#MANUALLY PRINT MAP
#print_map(1, "blue", 2, generate_map(50, 50, 20))
    
def calculate_distance(starting_x, starting_y, destination_x, destination_y):
    
    distance = math.hypot(destination_x - starting_x, destination_y - starting_y) 
    # calculates Euclidean distance (straight-line) distance between two points

    return distance


def calculate_path(selected_map):

    # you will need to setup a variable to store the total path distance
    # you will need to use a loop in order to calculate the distance of the locations individually
    # it would be wise to use make use of the calculate_distance function as you can reuse this
    # remember your need to calculate the path of all locations returning to the original location

    #variable setup for total distance
    distance = 0

    #add to distance variable each distance calculated
    for x in range(len(selected_map)-1):
        distance += calculate_distance(selected_map[x][0], selected_map[x][1], selected_map[x+1][0], selected_map[x+1][1])

    #add the last distance from last location to start
    distance += calculate_distance(selected_map[-1][0], selected_map[-1][1], selected_map[0][0], selected_map[0][1])

    return distance

#FOR MANUAL CHECKING ONLY
#print(calculate_path(generate_map(50, 50, 20)))

#################################################################################################

def nearest_neighbour_algorithm(selected_map):

    temp_map = copy.deepcopy(selected_map)
    optermised_map = []

    #sorting this is useful since the algorithm finds a quicker shortest path
    #by starting with the lowest value (grabbing from the end using pop)
    temp_map.sort()

    optermised_map.append(temp_map.pop())

    # you need to create an empty list for your optimised map 
    for x in range(len(temp_map)):

        # you need to add some variables to store establish the closest location
        nearest_value = 1000
        nearest_index = 0

        for i in range(len(temp_map)):

            current_value = abs(calculate_distance(optermised_map[x][0], optermised_map[x][1], temp_map[i][0], temp_map[i][1]))

            if nearest_value > current_value:
                #set neareast to current value and index
                nearest_value = current_value
                nearest_index = i

        optermised_map.append(temp_map[nearest_index])

        del temp_map[nearest_index]
        
    return optermised_map

#################################################################################################

def genetic_algorithm(selected_map, population, iterations, mutation_rate, elite_threshold):

    # this is the main genetic algorithm function and should make use of the inputs and call the sub functions in order to run
    # you will need to call the create_population function and store this in a list
    # you will then need to use the iterator function and store the returned solution to best_solution
    gene_pool = create_population(population, generate_map(50, 50, 20))
    iterator(gene_pool, 100, 0.05, 0.1)

    return best_solution

def create_population(population, selected_map):

    # you need to create an empty list called gene_pool for the population
    gene_pool = []
    # use a for loop and the provided inputs to create the population 
    for x in range(population):
        gene_pool.append(copy.deepcopy(selected_map))
    # you will also need to randomise the individuals within the population
        random.shuffle(gene_pool[x])

    return gene_pool

#MANUAL CHECKING ONLY
#print(create_population(15, generate_map(50, 50, 20)))

def fitness_function(gene_pool, best_solution):

    # you need to find a way to rank the fitness of your population. one way you may consider doing this is with a ranked list
    best_arrangement = best_solution
    best_arrangement_score = 0

    ranked = []

    # you will need to have correctly implemented the calculate_path function in order to rank the fitness of the population
    score = 0
    for x in range(len(gene_pool)):
        score += calculate_path(gene_pool[x])
    ranked.append(score)

    if score > best_arrangement_score:

        best_arrangement = x
        best_arrangement_score = score

    best_solution = best_arrangement

    sorted_gene_pool = gene_pool
    
    return sorted_gene_pool, best_solution


def iterator(gene_pool, iterations, mutation_rate, elite_threshold):


    for i in range(iterations):
        mating_function()
    # you need to use the provided inputs to iterate (run) the algorithm for the specified iterations
    # you will need to use a for loop in order to achieve this
    # in order for this function to work all over parts of the algorithm must be complete
    # the function must return the best individual (best_solution) in the population

    return best_solution

def mating_function(gene_pool, best_solution, mutation_rate, elite_threshold):

    new_gene_pool = []
    
    for x in len(gene_pool):
        new_gene_pool.extend(mutate(breed(copy.deepcopy(gene_pool[random.randint(0, int(len(gene_pool)*elite_threshold))])), (copy.deepcopy(x)), mutation_rate)) 

    new_gene_pool[len(new_gene_pool)-1] = best_solution

    return new_gene_pool

def breed(parent_1, parent_2):

    # you need to select random points in which to cut the genes of the parents and put them into the child
    cut_points = []
    cut_points.extend([random.randint(0, len(parent_1)), random.randint(0, len(parent_1))])
    cut_points.sort()

    # because the individual must contain all of the locations (this is a unique issue to the TSP) the gene selection is slightly more difficult
    # one suggested way is to selected portions of genetic data from one parent then fill in the remainder of locations from the other parent

    child = []
    dna_1 = []
    dna_2 = []

    # the portion of genes selected should be random and you may want to use some for loops to achieve this

    for g in range(cut_points[0], cut_points[1]):
        dna_1.append(parent_1[g])
    dna_2 = [item for item in parent_2 if item not in dna_1]
    child = dna_1 + dna_2

    # the function must return a child of the 2 parents containing all the locations in the original map

    return child

def mutate(child, mutation_rate):

    #mutate genes of child
    #switch represents the position within the search of the child
    for switch in range(len(child)):

        #mutation rate if random number generated is less than
        #mutation rate: if its lower that 5%
        if(random.random() < mutation_rate):

            #perform genetic switch
            switchwith = random.randint(0, len(child)-1)
            gene_1 = child[switch]
            gene_2 = child[switchwith]
            child[switch] = gene_2
            child[switchwith] = gene_1
            #print("mutation performed, gene_1", gene_1, "switched with gene_2", gene_2)

    mutated_child = child

    return mutated_child
