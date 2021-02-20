import random
from entity import Entity
from colorama import Fore, Back


class Paddle(Entity):
    def __init__(self, x, y, b):
        super().__init__(x, y)
        self.__length = 7
        self.xcbound = ((self.__length//2) + 1, b.get_no_of_cols() - (self.__length//2) - 2)
        self.__attached = True
        self.chr = 'P'

    def move(self, d):  # d is 1 or -1
        if self.x + d >= self.xcbound[1]:
            self.x = self.xcbound[1]
        elif self.x + d <= self.xcbound[0]:
            self.x = self.xcbound[0]
        else:
            self.x += d

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def is_attached(self):
        return self.__attached

    def get_length(self):
        return self.__length

    def change_attached(self):
        if self.is_attached():
            self.__attached = False
        else:
            self.__attached = True