import numpy as np
from tensorflow.keras.models import load_model

class DodgeModel:
    def __init__(self, model_path="C:/Users/Rishal Usman/Desktop/autonomous-car-sim/backend/traffic_dodge_model.h5"):
        self.model = load_model(model_path)

    def predict_action(self, distances):
        # distances = [d_left, d_center, d_right], values from 0 to 1
        input_vector = np.array([distances], dtype=np.float32)
        prediction = self.model.predict(input_vector, verbose=0)[0]
        return int(np.argmax(prediction))  # 0=left, 1=stay, 2=right
