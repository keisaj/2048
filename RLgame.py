from game import Game2048

class AIGame2048(Game2048):

    def __init__(self, screen_size: int = 800, board_size: int = 4, win_num: int = 2048) -> None:
        super().__init__(screen_size, board_size, win_num)



    def run(self, display: bool = True) -> None:
        while True:
            if self.game_over:
                return
            self.handle_ai_events()

            if display:
                self.draw_board(self.board)
                self.cap_frame_rate()

