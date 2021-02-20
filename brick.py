from colorama import Fore, Back
from entity import Entity
import random


class Brick(Entity):            # x to x+l-1 where y lies in y and y+1
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__flag = True
        self.__length = 6
        self.score = 10
        self.chr = 'B'
        rv = random.randint(1, 11)
        if rv <= 5:
            self.__level = 1
        elif rv <= 8:
            self.__level = 2
        elif rv <= 9:
            self.__level = 3
        else:
            self.__level = 4

    def did_it_die(self):
        return not self.__flag

    def collided(self):
        if not self.__level == 4:
            self.__level -= 1
        if self.__level == 0:
            self.__flag = False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_len(self):
        return self.__length

    def get_level(self):
        return self.__level

    def is_it_in(self, x1, y1):
        x_list = range(self.x, self.x+self.__length)
        y_list = [self.y, self.y + 1]
        if (x1 in x_list) and (y1 in y_list):
            return self
        else:
            return None

    def get_score(self):
        return self.score