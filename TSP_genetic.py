from collections import namedtuple
from typing import List, Callable, Tuple
from random import choices, sample, randint, random
import math
import time
from capitals import things
#from TSP_plot import draw_frame

#Thing = namedtuple('Thing', ['name', 'coords'])
#
## create list of cities
#things = [             #  Lat      Lon
#    Thing('Toronto'  , (43.650, -79.380)),
#    Thing('Montreal' , (45.520, -73.570)),
#    Thing('Vancouver', (49.280, -123.130)),
#    Thing('Calgary'  , (51.050, -114.060)),
#    Thing('Ottawa'   , (45.420, -75.710)),
#    Thing('Edmonton' , (53.570, -113.540)),
#    Thing('Hamilton' , (43.260, -79.850)),
#    Thing('Quebec'   , (46.820, -71.230)),
#    Thing('Winnipeg' , (49.880, -97.170)),
#]

Genome = List[int]
Population = List[Genome]

def generate_genome(length: int) -> Genome:
    return sample(range(length), k=length)

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def calculate_dist(coord1: tuple, coord2: tuple) -> int:
    # This uses the ‘haversine’ formula to calculate the great-circle distance between two points

    R = 6371 # radius earth in km
    dLat = deg2rad(coord1[0]-coord2[0])
    dLon = deg2rad(coord1[1]-coord2[1])

    a = math.sin(dLat/2) * math.sin(dLat/2) + \
    math.cos(deg2rad(coord1[0])) * math.cos(deg2rad(coord2[0])) * \
    math.sin(dLon/2) * math.sin(dLon/2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(round(R * c))
    
def deg2rad(deg):
  return deg * (math.pi/180)

def fitness(genome: Genome, things: things) -> int:
    if len(genome) != len(things):
        raise ValueError("genome and things MUST be of the same length")

    #Initialize fitness to ZERO
    value = 0
    #Calculate return to start
    value += calculate_dist(things[genome[0]][1],things[genome[-1]][1])  
    
    #Calculate sequence fitness
    for i in range(len(genome)-1):
        value += calculate_dist(things[genome[i]][1], things[genome[i+1]][1])

    #print(str(genome) + str(value))    
    return value

def select_parents(population: Population) -> Population:
    #can add joisting of two random pairs to become parents, instead of two random strong parents
    return choices(
        population=population,
        weights=[(1 / (fitness(genome, things))) for genome in population],
        k=2
    )

def single_point_crossover(a: Genome, b: Genome) -> tuple:
    if len(a) != len(b):
        raise ValueError("Genomes MUST be of the same length")

    p = randint(1, len(a) - 1)

    #In order to prevent duplicity from the crossover, 
    # child(a) will inherit genes from parent(a) until the cut point(p) and inherit non repeating genes from the begining of parent(b)
    # child(b) will inherit genes from parent(b) until the cut point(p) and inherit non repeating genes from the begining of parent(a)
    child_a = a[0:p]
    child_b = b[0:p]

    for i in range(len(a)):
        if b[i] not in child_a:
            child_a.append(b[i])
        if a[i] not in child_b:
            child_b.append(a[i])

    return (child_a, child_b)

def swap_random(genome: Genome) -> Genome:
    idx = range(len(genome))
    i1, i2 = sample(idx, 2)
    genome[i1], genome[i2] = genome[i2], genome[i1]
    return genome

def mutation(genome: Genome, probability: float=0.3) -> Genome:
    if random() < probability:
        genome = swap_random(genome) 
    return genome

def evolution(generation_limit: int = 1000, fitness_limit: int = 7000):
    population = generate_population(size = 50, genome_length=len(things))

    for gen in range(generation_limit):
        #rearange in order of fitness score
        population = sorted(
            population,
            key=lambda genome:fitness(genome, things),
            reverse=False
        )

        #check generation alpha fitness
        if fitness(population[0], things) <= fitness_limit:
            break

        #carry the two strongest genomes to the next generation
        next_generation = population[0:2]

        #fill the population with children from dominant parents
        while len(next_generation) < len(population):
            parents = select_parents(population)
            child_a, child_b = single_point_crossover(parents[0], parents[1])
            child_a = mutation(child_a)
            child_b = mutation(child_b)
            next_generation += child_a, child_b

        population = next_generation

        population = sorted(
            population,
            key=lambda genome:fitness(genome, things),
            reverse=False
        )
        yield population[0], fitness(population[0], things), gen

    return population[0]
    #return population[0], fitness(population[0], things), (i+1) 


# TEST BENCH_______________________________________________________________
#Population = generate_population(10, len(things))
#print('Genomes : Fitness')
#for geno in Population:
#    print(str(geno) + " " + str(fitness(geno, things)))
#print('Weighted Random parents: ')
#pair = select_parents(Population)
#print(pair)
#print('Crossover Children: ')
#cross_pair = single_point_crossover(pair[0], pair[1])
#print(cross_pair)
#print('Potentially Mutated Children: ')
#mute_1 = mutation(cross_pair[0])
#mute_2 = mutation(cross_pair[1])
#print(' ' +str(mute_1) + '  ' + str(mute_2))
#for sequence, fit, gen in evolution():
    #print(fit)
#_________________________________________________________________________