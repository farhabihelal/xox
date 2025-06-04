import random
import tkinter as tk
from tkinter import messagebox

from xox import Board, Game, Player


class XoxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XOX")

        self.game: Game = None
        self.buttons = []

        self.home()

    def create_game(self, players):
        config = Game.Config(players=players)
        self.game = Game(config)

    def home(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        lbl_title = tk.Label(self.root, text="XOX Game", font=("Helvetica", 20))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Game mode selection
        self.game_mode = tk.StringVar(value="human_vs_human")
        rb_human_vs_human = tk.Radiobutton(
            self.root,
            text="Human vs Human",
            variable=self.game_mode,
            value="human_vs_human",
            font=("Helvetica", 14),
        )
        rb_human_vs_ai = tk.Radiobutton(
            self.root,
            text="Human vs AI",
            variable=self.game_mode,
            value="human_vs_ai",
            font=("Helvetica", 14),
        )
        rb_human_vs_human.grid(row=1, column=0, sticky="w", padx=10)
        rb_human_vs_ai.grid(row=1, column=1, sticky="w", padx=10)

        # Player name inputs
        lbl_player1 = tk.Label(self.root, text="Player 1 Name:", font=("Helvetica", 12))
        lbl_player1.grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.entry_player1 = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_player1.grid(row=2, column=1, pady=5, padx=5)

        lbl_player2 = tk.Label(self.root, text="Player 2 Name:", font=("Helvetica", 12))
        lbl_player2.grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.entry_player2 = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_player2.grid(row=3, column=1, pady=5, padx=5)

        def on_mode_change(*args):
            if self.game_mode.get() == "human_vs_ai":
                self.entry_player2.delete(0, tk.END)
                self.entry_player2.insert(0, "AI")
                self.entry_player2.config(state="disabled")
            else:
                self.entry_player2.config(state="normal")
                self.entry_player2.delete(0, tk.END)

        self.game_mode.trace_add("write", on_mode_change)
        on_mode_change()

        def on_start():
            player1_name = self.entry_player1.get().strip() or "Player 1"
            player2_name = self.entry_player2.get().strip() or (
                "AI" if self.game_mode.get() == "human_vs_ai" else "Player 2"
            )
            players = [Player(name=player1_name, type=Player.Type.HUMAN, symbol="X")]
            if self.game_mode.get() == "human_vs_ai":
                players.append(
                    Player(name=player2_name, type=Player.Type.AI, symbol="O")
                )
            else:
                players.append(
                    Player(name=player2_name, type=Player.Type.HUMAN, symbol="O")
                )
            self.create_game(players)
            # Clear home screen and show game board
            for widget in self.root.winfo_children():
                widget.destroy()
            self.create_widgets()
            self.make_ai_move()

        btn_start = tk.Button(
            self.root, text="Start", font=("Helvetica", 14), command=on_start
        )
        btn_start.grid(row=4, column=0, columnspan=2, pady=15)

    def create_widgets(self):
        for i in range(9):
            btn = tk.Button(
                self.root,
                text="",
                font=("Helvetica", 32),
                width=5,
                height=2,
                command=lambda i=i: self.make_move(i),
            )
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

        self.reset_button = tk.Button(
            self.root, text="Reset", font=("Helvetica", 14), command=self.reset_game
        )
        self.reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

    def make_move(self, index: int):
        row, col = index // 3, index % 3
        if self.game.board.is_empty(row, col):
            self.game.board.update_cell(row, col, self.game.current_player.symbol)
            self.buttons[index].config(text=self.game.current_player.symbol)

            if self.game.board.check_winner(self.game.current_player.symbol):
                messagebox.showinfo(
                    "Game Over", f"Player {self.game.current_player.name} wins!"
                )
                self.disable_buttons()
            elif self.game.board.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()
            else:
                self.game.switch_player()

                self.make_ai_move()

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def reset_game(self):
        self.game.reset()
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL)

        self.make_ai_move()

    def make_ai_move(self):
        if self.game.current_player.type == Player.Type.AI:
            row, col = self.game.get_ai_move()
            index = row * 3 + col
            self.make_move(index)


if __name__ == "__main__":
    root = tk.Tk()
    game = XoxGUI(root)
    root.mainloop()
