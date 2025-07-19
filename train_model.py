import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

# Load data
X = np.load("X.npy")
y = np.load("y.npy")

# Build model
model = Sequential([
    Dense(64, activation='relu', input_shape=(5,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(3, activation='softmax')
])

# Compile
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train
model.fit(X, y, epochs=50, batch_size=32, validation_split=0.1,
          callbacks=[EarlyStopping(patience=5, restore_best_weights=True)])

# Save model
model.save("smart_dodge_model.h5")
print("✅ Trained and saved smart_dodge_model.h5")
