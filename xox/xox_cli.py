import os
import sys
import logging
from typing import List, Optional
import random

from rich.console import Console
from rich.table import Table
from rich.text import Text

from pydantic import BaseModel


from xox import Game, Player, Board

console = Console()


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

        human_move_count = 0
        ai_move_count = 0

        while True:

            player: Player = self.players[self.current_player_idx]
            print(f"\n{player.name}'s turn ({player.symbol})")

            if player.type == Player.Type.HUMAN:
                try:
                    row = int(input("Enter row (0-2): "))
                    col = int(input("Enter column (0-2): "))
                    human_move_count += 1
                except ValueError:
                    print("Invalid input. Please enter numbers only.")
                    continue
            elif player.type == Player.Type.AI:
                row, col = (
                    self.get_ai_move()
                    if ai_move_count > 0
                    else random.choice(
                        [
                            (i, j)
                            for i, _ in enumerate(self.board.grid)
                            for j, _ in enumerate(self.board.grid[i])
                            if self.board.is_empty(i, j)
                        ]
                    )
                )
                ai_move_count += 1
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

    # def display_board(self):
    #     print("\n  0   1   2")
    #     for idx, row in enumerate(self.board.grid):
    #         print(f"{idx} " + " | ".join(row))
    #         if idx < 2:
    #             print("  " + "-" * 9)

    # def display_board(self):
    #     table = Table(show_header=False, show_lines=True, border_style="grey50")
    #     for _ in range(3):
    #         table.add_column(justify="center", width=3)
    #     for row in self.board.grid:
    #         rich_row = []
    #         for cell in row:
    #             if cell == "X":
    #                 token = Text("X", style="bold red", justify="center")
    #             elif cell == "O":
    #                 token = Text("O", style="bold blue", justify="center")
    #             else:
    #                 token = Text(" " * 3, justify="center")
    #             # Stretch the token based on cell_size
    #             content = "\n".join([token.plain])
    #             rich_row.append(Text(content, style=token.style))
    #         table.add_row(*rich_row)
    #     console.print(table)

    def display_board(self):
        table = Table(show_header=True, show_lines=True, border_style="grey50")

        # column for row indices
        table.add_column(" ", justify="center", width=3)
        # column headers (0, 1, 2)
        for col in range(3):
            table.add_column(str(col), justify="center", width=3)

        for row_idx, row in enumerate(self.board.grid):
            rich_row = [Text(str(row_idx), style="bold grey50")]
            for cell in row:
                if cell == "X":
                    token = Text("X", style="bold red", justify="center")
                elif cell == "O":
                    token = Text("O", style="bold blue", justify="center")
                else:
                    token = Text(" ", justify="center")
                rich_row.append(token)
            table.add_row(*rich_row)

        console.print(table)


if __name__ == "__main__":
    players = [
        Player(name="Farhabi", symbol="X", type=Player.Type.HUMAN),
        Player(name="AI", symbol="O", type=Player.Type.AI),
    ]
    config = XoxCLI.Config(players=players)
    xox_cli = XoxCLI(config)
    xox_cli.play()
