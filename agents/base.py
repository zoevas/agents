class Agent:
    def __init__(self, name: str):
        self.name = name

    def run(self, input_data: dict) -> dict:
        raise NotImplementedError