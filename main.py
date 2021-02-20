
import os
import time
from board import Board
from paddle import Paddle
from player import Player
from brick import Brick
from input import input_to, Get
from entity import quit_exit
from ball import Ball
import random

board1 = Board(29, 83)
pad1 = Paddle(board1.get_no_of_cols()//2, board1.get_no_of_rows()-3, board1)
aaa1, aaa2 = pad1.get_x(), pad1.get_length()
aaa1 = random.randint(aaa1 - aaa2//2, aaa1 + (aaa2//2) + 1)
ball1 = Ball(aaa1, pad1.get_y()-1)
player1 = Player()

# total 7 rows of bricks starting from row 4. 0 is wall
brik_1 = Brick(4, 10)
b_len = brik_1.get_len()

for j in range(4, 18, 2):   # filling the bricks row wise
    for i in range(10, 70, b_len):
        if j == 4 and i == 10:
            board1.add_brick(brik_1)
        else:
            board1.add_brick(Board(i, j))
board1.draw_all_bricks()

os.system('clear')
# draw paddle, other bricks first
board1.draw_paddle(pad1)

start_time = time.time()
while True:
    rch = Get()
    fch = input_to(rch)
    if fch == 'q':
        quit_exit()
    if fch == 'a':
        board1.move_draw_paddle(pad1, ball1, -1)
        if pad1.is_attached():
            ball1.move_with_paddle(-1)
    if fch == 'd':
        board1.move_draw_paddle(pad1, ball1, 1)
        if pad1.is_attached():
            ball1.move_with_paddle(1)
    if fch == ' ':
        pad1.change_attached()
    board1.collision_check(ball1, pad1, player1)
    os.system('clear')
    ct = time.time() - start_time
    player1.set_time(int(ct))
    player1.print_details()
    board1.print_board()
