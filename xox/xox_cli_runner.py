from xox_cli import Game, Board, Player


class XoxCLIRunner:

    def __init__(self):
        self.game = None

    def prepare_game(self):
        while True:
            try:
                print(
                    """
Welcome to Tic Tac Toe!

Game modes:
1) Human vs. AI
2) Human vs. Human

"""
                )
                mode_str = input("Choose mode (1): ")
                mode_str = mode_str.strip()
                mode_str = mode_str if mode_str else "1"

                max_player_count = 2
                try:
                    human_player_count = int(mode_str)
                except Exception as e:
                    print("Invalid input. Please enter either `1` or `2`.")
                    raise e

                players = []
                player_symbols = {"X", "O"}
                for i in range(human_player_count):
                    name = input(f"Enter name for Player {i+1}: ")
                    symbol = player_symbols.pop()
                    players.append(
                        Player(name=name, symbol=symbol, type=Player.Type.HUMAN)
                    )

                for i in range(human_player_count, max_player_count):
                    name = f"Player {i+1} (AI)"
                    symbol = player_symbols.pop()
                    players.append(
                        Player(name=name, symbol=symbol, type=Player.Type.HUMAN)
                    )

                game_config = Game.Config(
                    max_player_count=max_player_count, players=players
                )
                game = Game(game_config)
                game.play()

                play_again = input("Want to play again? (Y/n): ", end="")

            except Exception as e:
                print(e)
