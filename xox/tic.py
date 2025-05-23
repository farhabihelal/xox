from enum import Enum
from pydantic import BaseModel


class PlayerType(Enum):
    AI = 0
    HUMAN = 1


class Player(BaseModel):
    name: str
    symbol: str
    type: PlayerType


class Board:
    def __init__(self, config: dict):
        self.configure(config)

    def configure(self, config: dict):
        self.grid = [[" " for _ in range(3)] for _ in range(3)]

    def display(self):
        print("\n  0   1   2")
        for idx, row in enumerate(self.grid):
            print(f"{idx} " + " | ".join(row))
            if idx < 2:
                print("  " + "-" * 9)

    def update_cell(self, row, col, symbol):
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


class Game:
    def __init__(self, player1_name: str, player2_name: str):
        self.board = Board()
        self.players = [Player(player1_name, "X"), Player(player2_name, "O")]
        self.current_player_idx = 0

    def switch_player(self):
        self.current_player_idx = 1 - self.current_player_idx

    def play(self):
        print("Welcome to Tic Tac Toe!")
        self.board.display()

        while True:
            player = self.players[self.current_player_idx]
            print(f"\n{player.name}'s turn ({player.symbol})")
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
            except ValueError:
                print("Invalid input. Please enter numbers only.")
                continue

            if not (0 <= row < 3 and 0 <= col < 3):
                print("Invalid position. Try again.")
                continue

            if not self.board.update_cell(row, col, player.symbol):
                print("Cell already taken. Try a different move.")
                continue

            self.board.display()

            if self.board.check_winner(player.symbol):
                print(f"\n🎉 {player.name} wins!")
                break
            elif self.board.is_full():
                print("\nIt's a draw!")
                break

            self.switch_player()


class GameConfig(BaseModel):
    board_rows: int
    board_cols: int
    total_player_count: int
    human_player_count: int


def game_prep():
    pass


if __name__ == "__main__":
    board_rows = input("Enter board rows (3): ")
    board_cols = input("Enter board cols (3): ")

    player_count = input("Enter player number: ")

    for i in range(player_count):
        pass

    name1 = input("Enter name for Player 1 (X): ")
    name2 = input("Enter name for Player 2 (O): ")
    game = Game(name1, name2)
    game.play()
