from game import Game2048

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


class AIGame2048(Game2048):

    def __init__(self, screen_size: int = 800, board_size: int = 4, win_num: int = 2048) -> None:
        super().__init__(screen_size, board_size, win_num)

    def reset(self):
        """ resets state of the environment """
        pass

    def is_terminal(self, state) -> bool:
        """
        return true if state is terminal or false otherwise
        state is terminal when there is no valid moves
        """
        pass

    def get_possible_actions(self, state: object) -> tuple:
        """ return a tuple of possible actions in a given state """
        pass

    def get_next_states(self, state, action):
        """
        return a set of possible next states and probabilities of moving into them
        """
        pass

    def get_reward(self, state, action, next_state):
        pass

    def step(self, action):

        if action == UP:
            self.board, flag = self.move_up(self.board)
            status = self.is_game_over(self.board)
            self.manage_status(status)
            reward = self.manage_reward(status)
            self.draw_board(self.board)
            return self.__get_state(), reward, self.game_over, self.score

        if action == DOWN:
            self.board, flag = self.move_down(self.board)
            status = self.is_game_over(self.board)
            self.manage_status(status)
            reward = self.manage_reward(status)
            self.draw_board(self.board)
            return self.__get_state(), reward, self.game_over, self.score

        if action == LEFT:
            self.board, flag = self.move_left(self.board)
            status = self.is_game_over(self.board)
            self.manage_status(status)
            reward = self.manage_reward(status)
            self.draw_board(self.board)
            return self.__get_state(), reward, self.game_over, self.score

        if action == RIGHT:
            self.board, flag = self.move_right(self.board)
            status = self.is_game_over(self.board)
            self.manage_status(status)
            reward = self.manage_reward(status)
            self.draw_board(self.board)
            return self.__get_state(), reward, self.game_over, self.score

    def manage_reward(self, status: bool) -> int:
        pass

    def __get_state(self):
        '''
        Function returns current state of the game
        :return: state
        '''
        pass

    def turn_off_display(self):
        pass

    def turn_on_display(self):
        pass


if __name__ == '__main__':
    game = AIGame2048()
    game.run()
