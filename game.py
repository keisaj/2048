import pygame
import numpy as np
import random
import sys
from math import log
from colour import Color

# TODO add requirements.txt, implement optional arguments passing via terminal, optional, add menu/ start new game, set win num
class Game2048:

    def __init__(self, screen_size: int = 800, board_size: int = 4, win_num: int = 2048) -> None:
        self.screen_size = screen_size
        self.board_size = board_size
        self.cell_size = self.screen_size / self.board_size
        self.win_num = win_num
        self.game_over = False

        self.check_if_win_num_correct()

        # colors
        self.line_color = (0, 0, 0)
        self.background_color = (194, 184, 178)

        self.colors = self.init_colors()
        self.check_if_win_num_in_colors()

        # fps
        self.fps = 30
        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / self.fps) * 1000.0

        pygame.init()
        pygame.display.set_caption('2048')

        self.screen = pygame.display.set_mode(
            (self.screen_size, self.screen_size))

        self.board = self.init_board()
        self.screen.fill(self.background_color)

    def init_board(self) -> np.array:
        """
        Initiates a board
        """
        board = np.zeros((self.board_size, self.board_size))
        self.print_instruction()
        board = self.add_new_2(board)
        return board

    def init_colors(self) -> dict:
        """
        Generates color table
        """
        colors = {0: self.background_color}

        red = Color("yellow")
        gradient = list(red.range_to(
            Color("red"), int(log(self.win_num, 2))+1))

        for idx, colour in enumerate(gradient):
            if idx != 0:
                rgb = tuple(x*255 for x in colour.get_rgb())
                colors[2**idx] = rgb

        return colors

    def check_if_win_num_correct(self) -> None:
        """
        Check if winning number is a power of 2
        """
        if not log(self.win_num, 2).is_integer():
            raise ValueError("Winning number has to be a power of 2")

    def check_if_win_num_in_colors(self) -> None:
        """
        Check if winning number is allowed
        """
        if self.win_num not in self.colors:
            raise ValueError("Winning number is to high")

    def print_instruction(self) -> None:
        print(f"Score {self.win_num} to win")
        print("Commands are as follows : ")
        print("'w' or arrow_UP : Move Up")
        print("'s' or arrow_DOWN: Move Down")
        print("'a' or arrow_LEFT: Move Left")
        print("'d' or arrow_RIGHT: Move Right")
        print("'q' : Quit")

    def add_new_2(self, board: np.array) -> np.array:
        """
        # function to add a new 2 in
        # grid at any random empty cell
        """
        # choosing a random index for
        # row and column.
        r = random.randint(0, self.board_size - 1)
        c = random.randint(0, self.board_size - 1)
        # while loop will break as the
        # random cell chosen will be empty
        # (or contains zero)
        while(board[r][c] != 0):
            r = random.randint(0, self.board_size - 1)
            c = random.randint(0, self.board_size - 1)

        # we will place a 2 at that empty
        # random cell.
        board[r][c] = 2
        return board

    def get_current_state(self, board: np.array) -> str:
        """
        # function to get the current
        # state of game
        """
        # if any cell contains
        # 2048 we have won
        if self.win_num in board:  # TODO fixed winning number, it should be changable
            return 'WON'  # TODO maybe change it to bool
        if 0 in board:
            return 'GAME NOT OVER'

        # or if no cell is empty now
        # but if after any move left, right,
        # up or down, if any two cells
        # gets merged and create an empty
        # cell then also game is not yet over
        for i in range(self.board_size - 1):
            for j in range(self.board_size - 1):
                if(board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1]):
                    return 'GAME NOT OVER'

        for j in range(self.board_size - 1):
            if(board[self.board_size - 1][j] == board[self.board_size - 1][j + 1]):
                return 'GAME NOT OVER'

        for i in range(self.board_size - 1):
            if(board[i][self.board_size - 1] == board[i + 1][self.board_size - 1]):
                return 'GAME NOT OVER'

        # else we have lost the game
        return 'LOST'

    def compress(self, board: np.array) -> np.array:
        """
        function to compress the grid after every step before and after merging cells.
        """
        # bool variable to determine
        # any change happened or not
        changed = False

        # empty grid
        new_board = np.zeros((self.board_size, self.board_size))

        # here we will shift entries
        # of each cell to it's extreme
        # left row by row
        # loop to traverse rows
        for i in range(self.board_size):
            pos = 0

            # loop to traverse each column
            # in respective row
            for j in range(self.board_size):
                if(board[i][j] != 0):

                    # if cell is non empty then
                    # we will shift it's number to
                    # previous empty cell in that row
                    # denoted by pos variable
                    new_board[i][pos] = board[i][j]

                    if(j != pos):
                        changed = True
                    pos += 1

        # returning new compressed matrix
        # and the flag variable.
        return new_board, changed

    def merge(self, board: np.array) -> np.array:
        """
        function to merge the cells in matrix after compressing
        """

        changed = False

        for i in range(self.board_size):
            for j in range(self.board_size - 1):

                # if current cell has same value as
                # next cell in the row and they
                # are non empty then
                if(board[i][j] == board[i][j + 1] and board[i][j] != 0):

                    # double current cell value and
                    # empty the next cell
                    board[i][j] = board[i][j] * 2
                    board[i][j + 1] = 0

                    # make bool variable True indicating
                    # the new grid after merging is
                    # different.
                    changed = True

        return board, changed

    def reverse(self, board: np.array) -> np.array:
        """
        function to reverse the matrix means reversing the content of each row (reversing the sequence)
        """
        new_board = []
        for i in range(self.board_size):
            new_board.append([])
            for j in range(self.board_size):
                new_board[i].append(board[i][self.board_size - 1 - j])
        return np.array(new_board).reshape(self.board_size, self.board_size)

    def move_left(self, board: np.array) -> np.array:
        """
        function to update the matrix if we move / swipe left
        """
        # first compress the grid
        new_board, changed1 = self.compress(board)

        # then merge the cells.
        new_board, changed2 = self.merge(new_board)

        changed = changed1 or changed2

        # again compress after merging.
        new_board, temp = self.compress(new_board)

        # return new matrix and bool changed
        # telling whether the grid is same
        # or different
        return new_board, changed

    def move_right(self, board: np.array) -> np.array:
        """
        function to update the matrix if we move / swipe right
        """
        # to move right we just reverse
        # the matrix
        new_board = np.flip(board)

        # then move left
        new_board, changed = self.move_left(new_board)

        # then again reverse matrix will
        # give us desired result
        new_board = np.flip(new_board)
        return new_board, changed

    def move_up(self, board: np.array) -> np.array:
        """
        function to update the matrix if we move / swipe up
        """
        # to move up we just take
        # transpose of matrix
        new_board = np.transpose(board)

        # then move left (calling all
        # included functions) then
        new_board, changed = self.move_left(new_board)

        # again take transpose will give
        # desired results
        new_board = np.transpose(new_board)
        return new_board, changed

    def move_down(self, board: np.array) -> np.array:
        """
        function to update the matrix if we move / swipe down
        """
        # to move down we take transpose
        new_board = np.transpose(board)

        # move right and then again
        new_board, changed = self.move_right(new_board)

        # take transpose will give desired
        # results.
        new_board = np.transpose(new_board)
        return new_board, changed

    def draw_board(self, board: np.array) -> None:
        """
        Draws a board using pygame
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                # draw a cell for a number
                rect = pygame.Rect(
                    i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.line_color, rect, width=2)

                rectangle_surface = pygame.Surface(
                    (self.cell_size, self.cell_size))
                rectangle_surface.set_alpha(128)
                # fill cell with color coresponding with its value
                rectangle_surface.fill(self.colors[board[j][i]])

                self.screen.blit(rectangle_surface,
                                 (i*self.cell_size, j*self.cell_size))

                if board[j][i] != 0:
                    font = pygame.font.SysFont(None, int(self.cell_size/2))
                    img = font.render(
                        str(int(board[j][i])), True, self.line_color)
                    self.screen.blit(img, (i*self.cell_size+self.cell_size*0.5-int(img.get_size()[0]*0.5),
                                           j*self.cell_size+self.cell_size*0.5-int(img.get_size()[1]*0.5)))  # text is centered in the rect

                pygame.display.flip()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'w' or event.key == pygame.K_UP:
                    # call the move_up function
                    self.board, flag = self.move_up(self.board)

                    # get the current state and print it
                    status = self.get_current_state(self.board)
                    # print(status)

                    # if game not ove then continue
                    # and add a new two
                    if(status == 'GAME NOT OVER'):
                        self.board = self.add_new_2(self.board)

                    # else break the loop
                    else:
                        self.game_over = True
                if event.unicode == 's' or event.key == pygame.K_DOWN:
                    self.board, flag = self.move_down(self.board)
                    status = self.get_current_state(self.board)
                    # print(status)
                    if(status == 'GAME NOT OVER'):
                        self.board = self.add_new_2(self.board)
                    else:
                        self.game_over = True
                if event.unicode == 'a' or event.key == pygame.K_LEFT:
                    self.board, flag = self.move_left(self.board)
                    status = self.get_current_state(self.board)
                    # print(status)
                    if(status == 'GAME NOT OVER'):
                        self.board = self.add_new_2(self.board)
                    else:
                        self.game_over = True
                if event.unicode == 'd' or event.key == pygame.K_RIGHT:
                    self.board, flag = self.move_right(self.board)
                    status = self.get_current_state(self.board)
                    # print(status)
                    if(status == 'GAME NOT OVER'):
                        self.board = self.add_new_2(self.board)
                    else:
                        self.game_over = True
                if event.unicode == 'q':
                    print("quitting......")
                    pygame.quit()
                    sys.exit()

    def cap_frame_rate(self) -> None:
        # cap framerate at 60fps if time since the last frame draw < 1/60th of a second, sleep for remaining time
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - \
            milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now

    def run(self) -> None:
        while True:
            if self.game_over:
                return
            self.handle_events()
            self.draw_board(self.board)
            self.cap_frame_rate()


if __name__ == '__main__':
    """
    Lunch a 2048 Game
    """
    game = Game2048(board_size=4, win_num=2048)
    game.run()
