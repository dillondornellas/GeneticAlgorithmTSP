from collections import namedtuple
from typing import List
from random import choices, sample, randint, random
import math
from capitals import things
import pandas as pd

#______________ 
pop_size = 50
gen_limit = 2000
#______________

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

    champions = []

    # SELECT 4 COMBATANTS (WEIGHTED BY FITNESS) TO JOUST FOR PARENTHOOD
    competitors = choices(
        population=population,
        weights=[(1 / (fitness(genome, things))) for genome in population],
        k=4
    )

    # JOUSTING
    for i in range(0, 4, 2):
        if fitness(competitors[i], things) < fitness(competitors[i+1], things):
            champions.append(competitors[i]) 
        else: champions.append(competitors[i+1])

    # RETURN THE TWO PARENTS
    return champions

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

def evolution(generation_limit: int = gen_limit, fitness_limit: int = 7000):
    population = generate_population(size = pop_size, genome_length=len(things))

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

# TEST BENCH FOR GENETIC ALGORITHM
#fitness_count = []
#for sequence, fit, gen in evolution():
#    title = "Generation : " + str(gen+1) + " | Fitness : " + str(fit)
#    print(title)
#    fitness_count.append(fit)
#
## APPEND TO CSV
#column = str(pop_size)
## read in CSV
##df = pd.DataFrame(fitness_count, columns = [column])
#df = pd.read_csv("datav2.csv")
## add new column to DF
#df[column] = fitness_count
## save new DF
#df.to_csv("datav2.csv", index=False)