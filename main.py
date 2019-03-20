from Individual import *
from PIL import Image

# globals
target_image = Image.open('if_Radiation_132691.png')
target = list(target_image.getdata())
max_pop = 1000
max_gen = 2000


def create_population(population_number):

    '''
    :param population_number: the number of individuals in the population
    :return: the list of randomly generated images (aka individuals)
    '''

    population = []
    for _ in range(population_number):
        individual = Individual.new_individual(target_image)
        population.append(individual)

    return population


def main():
    population = create_population(max_pop)
    generation = 0
    while generation < max_gen:
        for ind in population:
            ind.get_fitscore(target_image)
        print("Generation: ", generation, "\t Fitscore: ", population[0].fitscore)

        population = sorted(population, key=lambda x: x.fitscore)
        if population[0].fitscore == 0:
            print("Target ")
            break
        new_generation = []
        s = int((10*max_pop)/100)
        new_generation.extend(population[:s])
        for _ in range(s):
            parent1 = choice(population[:int(max_pop/2)])
            parent2 = choice(population[:int(max_pop/2)])
            child = parent1.crossover(parent2)
            new_generation.append(child)

        population = new_generation
        generation += 1

        # saving the best individual from each generation
        child_im = Image.new(target_image.mode, target_image.size)
        child_im.putdata(population[0].pixels)
        name = "out" + str(generation) + ".bmp"
        child_im.save("out/" + name)

    child = Image.new(target_image.mode, target_image.size)
    child.putdata(population[0].pixels)
    child.show()


if __name__ == '__main__':
    main()
