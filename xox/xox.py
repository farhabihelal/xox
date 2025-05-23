class Xox:

    def __init__(self, config: dict):
        self.configure(config)
        pass

    def configure(self, config: dict):
        self.config = config


if __name__ == "__main__":

    import xox_ai

    score = xox_ai.get_best_move([0 for x in range(9)])
    print(score)

    config = {}
    xox = Xox(config)
