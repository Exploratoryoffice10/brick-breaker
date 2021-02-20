
from colorama import Fore, Back
import numpy as np
import random


class Board:
    def __init__(self, rows, cols):
        self.__rows = rows
        self.__cols = cols
        self.grid = [[' ' for j in range(self.__cols)] for i in range(self.__rows)]
        self.gridlayout = np.empty([self.__rows, self.__cols], dtype='str')
        self.bricks = []
        # constructing wall
        for i in range(self.__rows):
            for j in range(self.__cols):
                self.gridlayout = ' '
        for i in range(self.__rows):
            self.grid[i][0] = Back.WHITE + Fore.WHITE + 'W' + Fore.RESET + Back.RESET   # W for wall
            self.grid[i][self.__cols - 1] = Back.WHITE + Fore.WHITE + 'W' + Fore.RESET + Back.RESET
            self.gridlayout[i][0] = 'W'
            self.gridlayout[i][self.__cols - 1] = 'W'
        for i in range(self.__cols):
            self.grid[0][i] = Back.WHITE + Fore.WHITE + 'W' + Fore.RESET + Back.RESET
            self.grid[self.__rows - 1][i] = Back.WHITE + Fore.WHITE + 'W' + Fore.RESET + Back.RESET
            self.gridlayout[0][i] = 'W'
            self.gridlayout[self.__rows - 1][i] = 'W'

    def add_brick(self, brk):
        self.bricks.append(brk)

    def draw_all_bricks(self):
        for brk in self.bricks:
            self.draw_brick(brk)

    def print_board(self):
        for i in range(self.__rows):
            print("    ")
            for j in range(self.__cols):
                print(self.grid[i][j], end='')
            print()

    def get_no_of_rows(self):
        return self.__rows

    def get_no_of_cols(self):
        return self.__cols

    def draw_brick(self, br):
        if not br.did_it_die():
            for i in range(br.get_len()):
                self.gridlayout[br.get_y()][br.get_x() + i] = 'B'
                self.gridlayout[br.get_y()+1][br.get_x() + i] = 'B'
                if br.get_level() == 1:
                    self.grid[br.get_y()][br.get_x()+i] = Back.GREEN + Fore.GREEN + 'B' + Fore.RESET + Back.RESET
                    self.grid[br.get_y()+1][br.get_x()+i] = Back.GREEN + Fore.GREEN + 'B' + Fore.RESET + Back.RESET
                elif br.get_level() == 2:
                    self.grid[br.get_y()][br.get_x()+i] = Back.YELLOW + Fore.YELLOW + 'B' + Fore.RESET + Back.RESET
                    self.grid[br.get_y()+1][br.get_x()+i] = Back.YELLOW + Fore.YELLOW + 'B' + Fore.RESET + Back.RESET
                elif br.get_level() == 3:
                    self.grid[br.get_y()][br.get_x()+i] = Back.RED + Fore.RED + 'B' + Fore.RESET + Back.RESET
                    self.grid[br.get_y()+1][i + br.get_x()] = Back.RED + Fore.RED + 'B' + Fore.RESET + Back.RESET
                else:
                    self.grid[br.get_y()][br.get_x()+i] = Back.BLUE + Fore.BLUE + 'B' + Fore.RESET + Back.RESET
                    self.grid[br.get_y() + 1][br.get_x()+i] = Back.BLUE + Fore.BLUE + 'B' + Fore.RESET + Back.RESET
        else:
            for i in range(br.get_len()):
                self.gridlayout[br.get_y()][br.get_x() + i] = ' '
                self.gridlayout[br.get_y()+1][br.get_x() + i] = ' '
                self.grid[br.get_y()][br.get_x() + i] = ' '
                self.grid[br.get_y()+1][br.get_x()+i] = ' '

    def draw_paddle(self, pd):
        ad = pd.get_length()//2
        for i in range(pd.get_x()-ad, pd.get_x()+ad+1):
            self.grid[pd.get_y()][i] = Back.WHITE + Fore.WHITE + 'P' + Fore.RESET + Back.RESET   # P for paddle
            self.gridlayout[pd.get_y()][i] = 'P'

    def draw_ball(self, b):
        self.grid[b.get_x()][b.get_y()] = 'o'
        self.gridlayout[b.get_x()][b.get_y()] = 'o'

    def draw_ball_with_paddle(self, b, val):
        self.grid[b.get_x()][b.get_y()] = ' '
        self.gridlayout[b.get_x()][b.get_y()] = ' '
        b.move_with_paddle(val)
        self.draw_ball(b)

    def clear_ball(self, b):
        self.grid[b.get_y()][b.get_x()] = ' '
        self.gridlayout[b.get_y()][b.get_x()] = ' '

    def move_draw_paddle(self, pd, b, val):
        ad = pd.get_length()//2
        for i in range(pd.get_x() - ad, pd.get_x() + ad + 1):
            self.grid[pd.get_y()][i] = ' '
            self.gridlayout[pd.get_y()][i] = ' '
        pd.move(val)
        """
        for i in range(pd.get_x() - ad, pd.get_x +ad + 1):
            self.grid[pd.get_y()][i] = Back.WHITE + Fore.WHITE + 'P' + Fore.RESET + Back.RESET  # P for paddle
            self.gridlayout[pd.get_y()][i] = 'P'
        """
        self.draw_paddle(pd)
        if pd.is_attached():
            self.draw_ball_with_paddle(b, val)

    def find_brick(self, x1, y1):
        for i in range(len(self.bricks)):
            if self.bricks[i].is_it_in(x1, y1):
                return self.bricks[i]

    def collision_check(self, bl, pd, pl):  # and move ball and change velocities accordingly
        if pd.is_attached():
            return
        x1, y1 = bl.get_x(), bl.get_y()
        x2, y2 = x1 + bl.get_vx, y1 + bl.get_vy()
        self.clear_ball(bl)
        if x2 == x1:
            if y1 < y2:  # going down
                sd = 0  # something detected
                for i in range(y1 + 1, y2 + 1):
                    if self.gridlayout[i][x1] == pd.chr:
                        sd = 1
                        bl.invert_vy()
                        bl.set_y(i-1)
                        bl.set_vx(bl.get_vx() - pd.get_x() + x1)
                        break
                    elif i == (self.__rows - 2):
                        sd = 1
                        pl.die()
                        pd.change_attached()    # false to true
                        # add additional functions to reinstate the structure
                        # bl.set_xy(i-1, x1)
                        new_x1, aaa2 = pd.get_x(), pd.get_length()
                        new_x1 = random.randint(new_x1 - aaa2 // 2, new_x1 + (aaa2 // 2) + 1)
                        bl.set_xy(new_x1, pd.get_y() - 1)
                        break
                if sd == 0:
                    bl.set_xy(x2, y2)
                self.draw_ball(bl)
                return  # done
            if y1 > y2:  # going up
                sd = 0
                for i in range(y2+1, y1+1):
                    if self.gridlayout[i][x1] == 'W':   # hit wall
                        bl.invert_vy()
                        bl.set_xy(i-1, x1)
                        # dude
                        break
                    if self.gridlayout[i][y1] == 'B':
                        cb = self.find_brick(i, x1)   # collided block
                        cb.collided()
                        self.draw_brick(cb)
                        bl.invert_vy()
                        bl.set_xy(x1, i-1)
                        pl.inc_score(cb)
                        break
                if sd == 0:
                    bl.set_xy(x2, y2)
                self.draw_ball(bl)
                return  # done

        if x2 > x1:
            if y2 > y1:  # right downwards
                sd = 0
                x_lis = list(range(x1+1, x2+1))
                y_lis = list(range(y1, y2+1))
                if self.gridlayout[y1+1][x1] == 'B':
                    sd = 1
                    cb = self.find_brick(y1+1, x1)
                    cb.collided()
                    self.draw_brick(cb)
                    bl.invert_vy()
                    pl.inc_score(cb)
                    bl.set_xy(x1,y1)
                    # break
                elif self.gridlayout[y1+1][x1+1] == 'B':
                    if self.gridlayout[y1][x1+1] == ' ':
                        sd = 1
                        cb = self.find_brick(y1+1, x1+1)
                        cb.collided()
                        self.draw_brick(cb)
                        bl.invert_vy()
                        pl.inc_score(cb)
                        bl.set_xy(x1+1,y1)
                if self.gridlayout[y1+1][x1] == 'P':
                    sd = 1
                    bl.invert_vy()
                    bl.set_vx(bl.get_vx() - pd.get_x() + x1)
                    bl.set_xy(x1, y1)
                # if self.gridlayout[y1+1][x1] == 'W'
                if sd == 0:
                    for i in x_lis:
                        chk1 = 0
                        if i == self.__rows - 2:
                            pl.die()
                            pl.change_attached()
                            new_x1, aaa2 = pd.get_x(), pd.get_length()
                            new_x1 = random.randint(new_x1 - aaa2 // 2, new_x1 + (aaa2 // 2) + 1)
                            bl.set_xy(new_x1, pd.get_y() - 1)
                            break
                        for j in y_lis:
                            if self.gridlayout[j][i] == 'B':
                                chk1 = 1
                                sd = 1 
                                cb = self.find_brick(j, i)
                                cb.collided()
                                self.draw_brick(cb)
                                if cb.get_y() == y1:
                                    bl.invert_vx()
                                if (x1+x2+1)/2 > i:
                                    bl.set_xy(i-1, y2)
                                else:
                                    bl.set_xy(i-1, y1)
                                pl.inc_score(cb)
                            if self.gridlayout[j][i] == 'P':
                                sd = 1
                                chk1= 1
                                if y1 == pd.get_y():
                                    bl.invert_vy()
                                    bl.set_xy(i, j-1)
                                    bl.set_vx(bl.get_vx() - pd.get_x() + x1)
                                else:
                                    bl.invert_vx()
                                    bl.set_xy(i-1,j+1)
                            if self.gridlayout[j][i] == 'W':
                                sd = 1
                                chk1 = 1
                                bl.invert_vx()
                                if (x2+x1+1)/2 < i:
                                    bl.set_xy(i-1, y2)
                                else:
                                    bl.set_xy(i-1, y1)
                                #bl.set_xy(j, i-1)
                        if chk1 == 1:
                            break
                if sd == 0:
                    bl.set_y(x2, y2)
                self.draw_ball(bl)
                return
            else:   # y1 > y2   x2 > x1 # right upwards
                sd = 0  
                x_lis = list(range(x1+1, x2+1))
                y_lis = list(range(y2, y1+1))
                y_lis.reverse()
                if self.gridlayout[y1-1][x1] == 'B':
                    sd = 1
                    cb = self.find_brick(y1-1, x1)
                    cb.collided()
                    self.draw_brick(cb)
                    bl.invert_vy()
                    pl.inc_score(cb)
                    bl.set_xy(x1, y1)
                elif self.gridlayout[y1-1][x1+1] == 'B':
                    if self.gridlayout[y1][x1+1] == ' ':
                        sd = 1
                        cb = self.find_brick(y1-1, x1+1)
                        cb.collided()
                        self.draw_brick(cb)
                        bl.invert_vy()
                        pl.inc_score(cb)
                        bl.set_xy(x1+1,y1)

                 #paddle going upward left no chance of hitting paddle
                if sd==0:
                    for i in x_lis:
                        chk1 = 0
                        for j in y_lis:
                            if self.gridlayout[j][i] == 'B':
                                chk1 = 1
                                sd = 1
                                cb = self.find_brick(j, i)
                                cb.collided()
                                self.draw_brick(cb)
                                bl.invert_vx()
                                pl.inc_score(cb)
                                if (x1+x2+1)/2 > i:
                                    bl.set_xy(i-1,y1)
                                else:
                                    bl.set_xy(i-1,y2)
                            if self.gridlayout[j][i] == 'W':
                                sd = 1
                                chk1 = 1
                                if j==0:
                                    bl.invert_vx()
                                elif i == (self.__cols-1):
                                    bl.invert_vy()
                                bl.set_xy(i-1, y1)
                        if chk1 == 1:
                            break
                        # going upward right not possible to hit the bottom
                    if sd == 0:
                        bl.set_y(x2, y2)
                    self.draw_ball(bl)
                    return
        if x1 > x2 :            
            if y2 < y1: # left upwards
                sd = 0  
                x_lis = list(range(x2+1, x1+1))
                y_lis = list(range(y2, y1+1))
                x_lis.reverse()
                y_lis.reverse()
                if self.gridlayout[y1-1][x1] == 'B':
                    sd = 1
                    cb = self.find_brick(y1-1, x1)
                    cb.collided()
                    self.draw_brick(cb)
                    bl.invert_vy()
                    pl.inc_score(cb)
                    bl.set_xy(x1, y1)
                elif self.gridlayout[y1-1][x1-1] == 'B':
                    if self.gridlayout[y1-1][x1] == ' ':
                        sd = 1
                        cb = self.find_brick(y1-1, x1-1)
                        cb.collided()
                        self.draw_brick(cb)
                        bl.invert_vy()
                        pl.inc_score(cb)
                        bl.set_xy(x1+1,y1)

                 #paddle going upward left no chance of hitting paddle
                if sd == 0:
                    for i in x_lis:
                        chk1 = 0
                        for j in y_lis:
                            if self.gridlayout[j][i] == 'B':
                                chk1 = 1
                                sd = 1
                                cb = self.find_brick(j, i)
                                cb.collided()
                                self.draw_brick(cb)
                                bl.invert_vx()
                                pl.inc_score(cb)
                                if (x1+x2+1)/2 > i:
                                    bl.set_xy(i-1,y2)
                                else:
                                    bl.set_xy(i-1,y1)
                            if self.gridlayout[j][i] == 'W':
                                sd = 1
                                chk1 = 1
                                if j==0:
                                    bl.invert_vx()
                                elif i == 0:
                                    bl.invert_vy()
                                bl.set_xy(i+1, y1)
                        if chk1 == 1:
                            break
                    # going upward right not possible to hit the bottom
                if sd == 0:
                    bl.set_y(x2, y2)
                self.draw_ball(bl)
                return
                #    going upward right not possible to hit the bottom
            else:   # left downwards
                sd = 0
                x_lis = list(range(x2+1, x1+1))
                y_lis = list(range(y1, y2+1))
                x_lis.reverse()
                if self.gridlayout[y1+1][x1] == 'B':
                    sd = 1
                    cb = self.find_brick(y1, x1+1)
                    cb.collided()
                    self.draw_brick(cb)
                    bl.invert_vy()
                    pl.inc_score(cb)
                    bl.set_xy(x1,y1)
                    # break
                elif self.gridlayout[y1+1][x1-1] == 'B':
                    if self.gridlayout[y1][x1-1] == ' ':
                        sd = 1
                        cb = self.find_brick(y1+1, x1-1)
                        cb.collided()
                        self.draw_brick(cb)
                        bl.invert_vy()
                        pl.inc_score(cb)
                        bl.set_xy(x1-1,y1)
                if self.gridlayout[y1+1][x1] == 'P':
                    sd = 1
                    bl.invert_vy()
                    bl.set_vx(bl.get_vx() - pd.get_x() + x1)
                    bl.set_xy(x1, y1)
                # if self.gridlayout[y1+1][x1] == 'W'
                if sd == 0:
                    for i in x_lis:
                        chk1 = 0
                        if i == self.__rows - 2:
                            pl.die()
                            pl.change_attached()
                            new_x1, aaa2 = pd.get_x(), pd.get_length()
                            new_x1 = random.randint(new_x1 - aaa2 // 2, new_x1 + (aaa2 // 2) + 1)
                            bl.set_xy(new_x1, pd.get_y() - 1)
                            break
                        for j in y_lis:
                            if self.gridlayout[j][i] == 'B':
                                chk1 = 1
                                sd = 1 
                                cb = self.find_brick(j, i)
                                cb.collided()
                                self.draw_brick(cb)
                                if cb.get_y() == y1:
                                    bl.invert_vx()
                                if (x1+x2+1)/2 > i:
                                    bl.set_xy(i-1, y2)
                                else:
                                    bl.set_xy(i-1, y1)
                                pl.inc_score(cb)
                            if self.gridlayout[j][i] == 'P':
                                sd = 1
                                chk1= 1
                                if y1 == pd.get_y():
                                    bl.invert_vy()
                                    bl.set_xy(i, j-1)
                                    bl.set_vx(bl.get_vx() - pd.get_x() + x1)
                                else:
                                    bl.invert_vx()
                                    bl.set_xy(i+1,j+1)
                            if self.gridlayout[j][i] == 'W':
                                sd = 1
                                chk1 = 1
                                bl.invert_vx()
                                if (x2+x1+1)/2 < i:
                                    bl.set_xy(i-1, y1)
                                else:
                                    bl.set_xy(i-1, y2)
                                #bl.set_xy(j, i-1)
                        if chk1 == 1:
                            break
                if sd == 0:
                    bl.set_y(x2, y2)
                self.draw_ball(bl)
                return
