import xox_ai


class XoxAI:
    class Config:
        pass

    def __init__(self, config: Config):
        pass

    def configure(self, config: Config):
        self.config = config

    def _to_1d(self, board_2d: list[list]) -> list:
        return [cell for row in board_2d for cell in row]

    def _from_idx_to_2d(self, idx: int, col_count: int) -> tuple:
        row = idx // col_count
        col = idx % col_count
        return row, col

    def get_move(self, board_2d: list[list]) -> tuple:
        idx = xox_ai.get_best_move(self._to_1d(board_2d))
        return self._from_idx_to_2d(idx, col_count=len(board_2d[0]))


if __name__ == "__main__":

    board_2d = [
        [" ", " ", "O"],
        [" ", "X", " "],
        ["X", " ", " "],
    ]

    config = {}
    ai = XoxAI({})

    board_1d = ai._to_1d(board_2d)
    print(board_1d)

    print(ai._from_idx_to_2d(7, col_count=3))
