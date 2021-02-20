import os


class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def quit_exit():
    al = list()
    with open("./text/dq.txt") as fh:
        for i in fh:
            al.append(i.rstrip())
    os.system('clear')
    for i in al:
        print(i)
    print("\nX---------------------------Bye Bye---------------------------X")
    exit()
