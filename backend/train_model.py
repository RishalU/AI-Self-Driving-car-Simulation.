import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import random

# 1. Generate synthetic data using rule-based logic
def simulate_training_data(num_samples=3000):
    X = []
    y = []
    for _ in range(num_samples):
        d_left = random.uniform(0, 1)
        d_center = random.uniform(0, 1)
        d_right = random.uniform(0, 1)

        # Rule-based decision logic
        if d_center < 0.3:
            if d_left > d_right and d_left > 0.3:
                action = 0  # go left
            elif d_right > 0.3:
                action = 2  # go right
            else:
                action = 1  # forced to stay
        else:
            action = 1  # path is clear

        X.append([d_left, d_center, d_right])
        y.append(action)

    return np.array(X), to_categorical(y, num_classes=3)

# 2. Train a simple feedforward neural network
def train():
    X, y = simulate_training_data()

    model = Sequential([
        Dense(16, activation='relu', input_shape=(3,)),
        Dense(16, activation='relu'),
        Dense(3, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=30, batch_size=32)

    model.save("traffic_dodge_model.h5")
    print("✅ Model saved as traffic_dodge_model.h5")

if __name__ == "__main__":
    train()
