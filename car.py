# === Fully Updated car.py with Smart Logging for Training ===
import math
import numpy as np
from model_loader import DodgeModel

LANES = [175, 275, 375, 475, 575]

class Car:
    def __init__(self):
        self.lane_index = 2
        self.x = LANES[self.lane_index]
        self.y = 300
        self.target_x = self.x
        self.speed = 0.8
        self.model = DodgeModel()
        self.is_alive = True

    def update(self, traffic):
        if not self.is_alive:
            return

        distances = [1.0 for _ in range(5)]
        for i, lx in enumerate(LANES):
            buffer_ahead = 120  # invisible buffer zone in front
            front_cars = [abs(t["y"] - (self.y - buffer_ahead)) for t in traffic
              if abs(t["x"] - lx) < 30 and t["y"] > (self.y - buffer_ahead) and (t["y"] - self.y) < 300]

            if front_cars:
                distances[i] = min(front_cars) / 300  # earlier reaction

        lane_inputs = [1.0, 1.0, 1.0]
        if self.lane_index > 0:
            lane_inputs[0] = distances[self.lane_index - 1]
        lane_inputs[1] = distances[self.lane_index]
        if self.lane_index < len(LANES) - 1:
            lane_inputs[2] = distances[self.lane_index + 1]

        # Closest car speed in current lane
        closest_speed = min([t["speed"] for t in traffic if abs(t["x"] - self.x) < 30 and t["y"] > self.y] + [0])

        # Input features for training/logging
        observation = [
            lane_inputs[0], lane_inputs[1], lane_inputs[2],
            closest_speed, self.lane_index
        ]

        # Predict action using model
        # TEMP RULE-BASED LOGIC for data generation
# Updated TEMP RULE-BASED LOGIC for logging
        if lane_inputs[1] < 0.7:  # center is somewhat blocked
            if lane_inputs[0] > 0.9 and self.lane_index > 0:
                action = 0  # go left
            elif lane_inputs[2] > 0.9 and self.lane_index < len(LANES) - 1:
                action = 2  # go right
            else:
                action = 1  # stay
        else:
            action = 1  # stay




        # Apply action
        if action == 0 and self.lane_index > 0:
            self.lane_index -= 1
        elif action == 2 and self.lane_index < len(LANES) - 1:
            self.lane_index += 1

        self.target_x = LANES[self.lane_index]
        self.x += (self.target_x - self.x) * 0.45

    def to_dict(self):
        return {"x": self.x, "y": self.y}
