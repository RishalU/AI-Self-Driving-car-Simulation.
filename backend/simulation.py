from environment import Environment
from car import Car

class Simulation:
    def __init__(self):
        self.env = Environment()
        self.car = Car()

    def step(self):
        self.env.update()
        self.car.update(self.env.get_traffic())

    def get_state(self):
        return {
            "car": self.car.to_dict(),
            "traffic": self.env.get_traffic()
        }