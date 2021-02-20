
import os
import emoji


class Player:
    def __init__(self):
        self.__score = 0
        self.__time = 0
        self.lives = 3

    def get_score(self):
        return self.__score

    def get_time(self):
        return self.__time

    def inc_score(self, brk):
        self.__score += brk.get_score

    def set_time(self, time):
        self.__time = time

    def show_time(self):
        return self.__time

    def show_score(self):
        return self.__score

    def lose(self):
        os.system('clear')
        al = list()
        with open("./text/yl.txt") as f:
            for aix in f:
                al.append(aix.rstrip())
        for ix in al:
            print(ix)
        print()
        print("your score is", self.__score)
        al = list()
        print()
        with open("./text/go.txt") as f:
            for aix in f:
                al.append(aix.rstrip())
        for ix in al:
            print(ix)
        exit()

    def win(self):
        os.system('clear')
        al = list()
        with open("./text/yw.txt") as f:
            for aix in f:
                al.append(aix.rstrip())
        for ixb in al:
            print(ixb)
        print()
        print("your score is", self.__score)
        al = list()
        print()
        with open("./text/go.txt") as f:
            for aix in f:
                al.append(aix.rstrip())
        for ix in al:
            print(ix)
        exit()

    def die(self):
        self.lives -= 1
        if self.lives == 0:
            self.lose()

    def print_details(self):
        print('    Lives: ', end='')
        heart = emoji.emojize(':red_heart')
        print(heart*self.lives, end='')
        print('                score:', self.__score)
