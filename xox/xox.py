from abc import ABC
from enum import Enum
from pydantic import BaseModel

from xox_ai_utils import XoxAI


class Player(BaseModel):
    class Type(Enum):
        AI = 0
        HUMAN = 1

    name: str
    symbol: str
    type: Type

    def get_move(self) -> tuple:
        pass


class Board:
    class Config(BaseModel):
        pass

    def __init__(self, config: Config):
        self.configure(config)

    def configure(self, config: Config):
        self.grid = [[" " for _ in range(3)] for _ in range(3)]

    # def display(self):
    #     print("\n  0   1   2")
    #     for idx, row in enumerate(self.grid):
    #         print(f"{idx} " + " | ".join(row))
    #         if idx < 2:
    #             print("  " + "-" * 9)

    def update_cell(self, row: int, col: int, symbol: str):
        if self.grid[row][col] == " ":
            self.grid[row][col] = symbol
            return True
        return False

    def is_full(self):
        return all(cell != " " for row in self.grid for cell in row)

    def check_winner(self, symbol):
        # Check rows and columns
        for i in range(3):
            if all(self.grid[i][j] == symbol for j in range(3)) or all(
                self.grid[j][i] == symbol for j in range(3)
            ):
                return True
        # Check diagonals
        if all(self.grid[i][i] == symbol for i in range(3)) or all(
            self.grid[i][2 - i] == symbol for i in range(3)
        ):
            return True
        return False

    def is_empty(self, row: int, col: int) -> bool:
        return self.grid[row][col] == " "


class Game(ABC):
    class Config(BaseModel):
        board_rows: int = 3
        board_cols: int = 3
        max_player_count: int = 2
        players: list

    def __init__(self, config: Config):
        self.configure(config)

        self.board: Board = None
        self.ai: XoxAI = None
        self.current_player_idx: int = None

    def configure(self, config: Config):
        self.config = config
        self.players = config.players

    def switch_player(self):
        self.current_player_idx = 1 - self.current_player_idx

    def play(self):
        self.reset_game()

    def reset_game(self):
        self.board = Board(Board.Config())
        self.ai = XoxAI(XoxAI.Config())
        self.current_player_idx = 0

    def get_ai_move(self) -> tuple:
        board = [
            [
                1 if self.is_human(symbol) else 2 if self.is_ai(symbol) else 0
                for symbol in row
            ]
            for row in self.board.grid
        ]
        return self.ai.get_move(board)

    def is_human(self, symbol: str) -> bool:
        return any(
            [
                player.type == Player.Type.HUMAN
                for player in self.players
                if player.symbol == symbol
            ]
        )

    def is_ai(self, symbol: str) -> bool:
        return not (self.is_human(symbol) or self.is_empty(symbol))

    def is_empty(self, symbol: str) -> bool:
        return symbol == " "


if __name__ == "__main__":

    players = [
        Player(name="Farhabi", symbol="X", type=Player.Type.HUMAN),
        Player(name="AI", symbol="O", type=Player.Type.AI),
    ]

    config = Game.Config(players=players)
    game = Game(config)

    game.reset_game()

    game.board.grid = [
        ["O", " ", "O"],
        [" ", " ", " "],
        ["X", " ", "X"],
    ]
    row, col = game.get_ai_move()
    print(f"AI move is {row}, {col}")
