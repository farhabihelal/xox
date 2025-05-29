import os
import sys
import logging
import rich

from pydantic import BaseModel

from xox import Game, Player, Board


class XoxCLI(Game):
    class Config(Game.Config):
        pass

    def __init__(self, config: Config):
        super().__init__(config)

    def configure(self, config: Config):
        super().configure(config)

    def play_round(self):
        super().play()
        self.display_board()

        while True:

            player: Player = self.players[self.current_player_idx]
            print(f"\n{player.name}'s turn ({player.symbol})")

            if player.type == Player.Type.HUMAN:
                try:
                    row = int(input("Enter row (0-2): "))
                    col = int(input("Enter column (0-2): "))
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
                    continue
            elif player.type == Player.Type.AI:
                row, col = self.get_ai_move()
            else:
                raise ValueError("Invalid player type found!")

            if not (0 <= row < 3 and 0 <= col < 3):
                print("Invalid position. Try again.")
                continue

            if not self.board.update_cell(row, col, player.symbol):
                print("Cell already taken. Try a different move.")
                continue

            self.display_board()

            if self.board.check_winner(player.symbol):
                print(f"\n🎉 {player.name} wins!")
                break
            elif self.board.is_full():
                print("\nIt's a draw!")
                break

            self.switch_player()

    def play(self):
        while True:
            self.play_round()
            try:
                should_continue = input("Want to play again? (Y/n): ")
                should_continue = should_continue.strip().lower()
                if should_continue not in ["y", "n"]:
                    raise ValueError("Invalid input.")
                if should_continue == "n":
                    break
            except Exception as e:
                pass
        print("Thanks for playing!")

    def display_board(self):
        print("\n  0   1   2")
        for idx, row in enumerate(self.board.grid):
            print(f"{idx} " + " | ".join(row))
            if idx < 2:
                print("  " + "-" * 9)


if __name__ == "__main__":
    players = [
        Player(name="Farhabi", symbol="X", type=Player.Type.HUMAN),
        Player(name="AI", symbol="O", type=Player.Type.AI),
    ]
    config = XoxCLI.Config(players=players)
    xox_cli = XoxCLI(config)
    xox_cli.play()
