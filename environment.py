import random
LANES = [175, 275, 375, 475, 575]

class Environment:
    def __init__(self):
        self.traffic = []
        for _ in range(6):
            self.spawn_traffic()

    def spawn_traffic(self):
        lane = random.choice(LANES)
        y = random.randint(-800, -50)
        speed = random.uniform(2, 7)  # more variation in speed
        self.traffic.append({"x": lane, "y": y, "speed": speed, "width": 20, "height": 40})

    def update(self):
        for t in self.traffic:
            t["y"] += t["speed"]
        self.traffic = [t for t in self.traffic if t["y"] < 700]
        while len(self.traffic) < 6:
            self.spawn_traffic()

    def get_traffic(self):
        return self.traffic