import numpy as np, random, operator
import pandas as pd
import matplotlib.pyplot as plt

# Create necessary classes and functions
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, node):
        from math import sin, cos, sqrt, atan2, radians
        R = 6373.0  # approximate radius of earth in km
        lat1 = radians(self.x)
        lng1 = radians(self.y)
        lat2 = radians(node.x)
        lng2 = radians(node.y)

        lat_d = lat2 - lat1
        lng_d = lng2 - lng1

        a = sin(lat_d / 2)**2 + cos(lat1) * cos(lat2) * sin(lng_d / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a)) 

        distance = R * c

        return distance
    
    # turn Node to list
    def tolist(self):
        l = []
        l.append(self.x)
        l.append(self.y)
        return l

    # turn Node to list    
    def totuple(self):
        return (self.x, self.y)
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromNode = self.route[i]
                toNode = None
                if i + 1 < len(self.route):
                    toNode = self.route[i + 1]
                else:
                    toNode = self.route[0]
                pathDistance += fromNode.distance(toNode)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

# Create our initial population
# Route generator
def createRoute(nodeList):
    route = random.sample(nodeList, len(nodeList))
    return route

# Create first "population" (list of routes)
def initialPopulation(popSize, nodeList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(nodeList))
    return population

# Create the genetic algorithm
# Rank individuals
def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

# Create a selection function that will be used to make the list of parent routes
def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

# Create mating pool
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

# Create a crossover function for two parents to create one child
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

# Create function to run crossover over full mating pool
def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

# Create function to mutate a single route
def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            node1 = individual[swapped]
            node2 = individual[swapWith]
            
            individual[swapped] = node2
            individual[swapWith] = node1
    return individual

# Create function to run mutation over entire population
def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

# Put all steps together to create the next generation
def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

# Final step: create the genetic algorithm
def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("\nInitial distance: " + str(1 / rankRoutes(pop)[0][1]) + " km")
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        # print(str(i) + "'s generation distance: " + str(1 / rankRoutes(pop)[0][1]))    
    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]) + " km")
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]

    # conver Node to Tuple
    for i in range(len(bestRoute)):
        bestRoute[i] = bestRoute[i].totuple()

    return bestRoute

# Plot the progress
def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])
    # print("\nInitial distance: " + str(1 / rankRoutes(pop)[0][1]) + " km")

    initialRouteIndex = rankRoutes(pop)[0][0]
    initialRoute = pop[initialRouteIndex]    

    lat = []
    lng = []
    for l in initialRoute:
        lat.append(l.tolist()[0])
        lng.append(l.tolist()[1])

    plt.ion()

    figure1, ax = plt.subplots(figsize=(16,9), num='Route')
    plt.title("  Generation: " + str(0), fontsize=28, loc='left', color='#515070')
    # plt.title("Total Distance: " + str(round(progress[-1], 4)) + " km", fontsize=16, loc='right')
    line1, = ax.plot(lng, lat, color='#515070', linewidth=2)    
    # ax.scatter(lng, lat, facecolors='none', edgecolors='#ff8e6e', s=200, marker='o')
    ax.scatter(lng, lat, color='#ff8e6e', s=200, marker='o')
    plt.xlabel("Longitude", fontsize=24, color='#515070')
    plt.ylabel("Latitude", fontsize=24, color='#515070')  
    ax.spines['left'].set_color('#515070')
    ax.spines['bottom'].set_color('#515070')
    ax.spines['right'].set_color('#515070')
    ax.spines['top'].set_color('#515070')
    ax.tick_params(axis='x', color='#515070') 
    ax.tick_params(axis='y', color='#515070') 


    plt.savefig("01_generation_begin.jpg")

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])
       
        currentRouteIndex =  rankRoutes(pop)[0][0]
        currentRoute = pop[currentRouteIndex]
        lat.clear()
        lng.clear()
        for l in currentRoute:
            lat.append(l.tolist()[0])
            lng.append(l.tolist()[1])

        plt.title("  Generation: " + str(i + 1), fontsize=28, loc='left', color='#515070')
        # plt.title("Total Distance: " + str(round(progress[-1], 4)) + " km", fontsize=16, loc='right')
        line1.set_xdata(lng)
        line1.set_ydata(lat)
        # ax.scatter(lng, lat, facecolors='none', edgecolors='#ff8e6e', s=200, marker='o')
        ax.scatter(lng, lat, color='#ff8e6e', s=200, marker='o')

        if (i == generations - 1):
            plt.ioff()
            plt.savefig("02_generation_end.jpg")

        figure1.canvas.draw()
        figure1.canvas.flush_events()

    # figure2 = plt.figure('Progress', figsize=(16,9))
    figure2, ax2 = plt.subplots(figsize=(16,9), num='Progress')
    plt.ion()

    # plt.plot(progress)
    # plt.ylabel('Distance', fontsize=24)
    # plt.xlabel('Generation', fontsize=24)

    # plt.plot(progress, color='#ff8e6e', linewidth=2)
    # plt.ylabel('Distance', fontsize=24, color='#ff8e6e')
    # plt.xlabel('Generation', fontsize=24, color='#ff8e6e')
    # ax2.spines['left'].set_color('#ff8e6e')
    # ax2.spines['bottom'].set_color('#ff8e6e')
    # ax2.tick_params(axis='x', colors='#ff8e6e') 
    # ax2.tick_params(axis='y', colors='#ff8e6e') 
    # ax2.spines['right'].set_visible(False)
    # ax2.spines['top'].set_visible(False)
    # # ax2.set_facecolor('#515070')

    plt.plot(progress, color='#515070', linewidth=2)
    plt.ylabel('Distance', fontsize=24, color='#515070')
    plt.xlabel('Generation', fontsize=24, color='#515070')
    ax2.spines['left'].set_color('#515070')
    ax2.spines['bottom'].set_color('#515070')
    ax2.tick_params(axis='x', colors='#515070') 
    ax2.tick_params(axis='y', colors='#515070') 
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    plt.ioff()
    plt.savefig("03_progress.jpg")
    # plt.savefig("03_progress.png", transparent = True)
    plt.show()
    plt.close()

    # print("Final distance: " + str(1 / rankRoutes(pop)[0][1]) + " km")

    percentage = (progress[0] - progress[-1]) / progress[0] * 100

    # print("Total distance reduced: " + str(percentage) + " %\n")

    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]

    # conver Node to Tuple
    for i in range(len(bestRoute)):
        bestRoute[i] = bestRoute[i].totuple()

    return bestRoute