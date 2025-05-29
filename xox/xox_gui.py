import tkinter as tk
from tkinter import messagebox


class XoxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XOX")

        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        self.create_widgets()

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

    def make_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.disable_buttons()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # rows
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # columns
            [0, 4, 8],
            [2, 4, 6],  # diagonals
        ]
        return any(
            all(self.board[i] == player for i in cond) for cond in win_conditions
        )

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    game = XoxGUI(root)
    root.mainloop()
