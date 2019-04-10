from PIL import Image
from random import random as rand
from random import choice
import math

genes = list(range(256))  # [0,255] -> will represent values for each channel of a pixel


def pixel_distance(pixel1: object, pixel2: object) -> object:
    """
    :param pixel1: first pixel
    :param pixel2: second pixel
    :return: euclidian distance between the pixels, as in 3d space
    """
    a = math.pow((pixel1[0] - pixel2[0]), 2)
    b = math.pow((pixel1[1] - pixel2[1]), 2)
    c = math.pow((pixel1[2] - pixel2[2]), 2)

    return math.sqrt(a + b + c)


class Individual:
    def __init__(self, data, target):
        self.data = data # an Image object
        self.pixels = list(data.getdata()) # a list of pixels from image
        self.fitscore = 0 # fitscore of individual
        self.target = target

    def get_fitscore(self, target):
        """
        calculates the pixel-distance between individual and target
        :param target: the image which to compare the individual to
        :return: fitscore
        """
        pixels = list(self.data.getdata())
        tg_px = list(target.getdata())
        s = 0
        for p1, p2 in zip(pixels, tg_px):
            s += pixel_distance(p1, p2)
        self.fitscore = int(math.sqrt(math.exp(math.sqrt(s))))

    def mutate(self,mutation_rate):
        """
        Will change a random pixel with a random value from [0,255]
        :param mutation_rate: the chance of each pixel getting mutated
        :return:  mutated individual
        """
        for i in range(len(self.pixels)):
            u = rand()
            if u < mutation_rate:
                # generating random values of each of the R, G and B channels
                self.pixels[i] = (choice(genes), choice(genes), choice(genes))

        return self

    def crossover(self, partner):
        child_data = []
        '''
            randomly picks genes from one parent or the other
        '''
        for gp1, gp2 in zip(self.pixels, partner.pixels):
            prob = rand()
            if prob < 0.45:
                child_data.append(gp1)
            else:
                child_data.append(gp2)

        child = Image.new(self.target.mode,self.target.size)
        child.putdata(child_data)
        new_child = Individual(child, self.target)
        # mutation
        '''
            0.05 is the mutation rate. should be a hyperparameter
        '''
        if rand() < 0.05:
            new_child = new_child.mutate(0.15)

        return new_child

    @classmethod
    def new_individual(cls, target):
        size = len(list(target.getdata()))
        new_genome = []
        '''
            picks a random value from [0,255] for each channel (R,G,B). alpha is for now 0 by default
        '''
        for _ in range(size):
            R = choice(genes)
            G = choice(genes)
            B = choice(genes)
            px = (R, G, B)
            new_genome.append(px)
        child = Image.new(target.mode, target.size)
        child.putdata(new_genome)
        child_new = Individual(child, target)

        return child_new

