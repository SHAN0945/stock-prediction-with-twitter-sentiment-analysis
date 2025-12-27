import numpy as np
import tensorflow as tf
from joblib import load
import matplotlib.pyplot as plt

# Load trained generator model
generator = tf.keras.models.load_model('generator_model.h5')

# Load scalers
X_scaler = load('X_scaler.pkl')
y_scaler = load('y_scaler.pkl')

# Start from the last 5 known days of data
# Assumes 'X_scale_dataset' is still in memory or load it if saved
last_sequence = X_scale_dataset[-5:]  # shape: (5, feature_size)
sequence = last_sequence.reshape(1, 5, last_sequence.shape[1])  # reshape to (1, 5, features)

predictions_scaled = []

for _ in range(30):
    next_scaled = generator.predict(sequence, verbose=0)
    predictions_scaled.append(next_scaled[0][0])

    # Create next sequence by appending prediction and removing oldest timestep
    next_features = sequence[0][1:]  # Drop first timestep
    next_input = np.append(next_features, [[next_scaled[0]] * sequence.shape[2]], axis=0)
    sequence = next_input.reshape(1, 5, sequence.shape[2])

# Inverse transform predictions to get actual stock prices
predictions_scaled = np.array(predictions_scaled).reshape(-1, 1)
predicted_prices = y_scaler.inverse_transform(predictions_scaled)

# Plot predictions
plt.figure(figsize=(10, 5))
plt.plot(predicted_prices, marker='o', label='Predicted Stock Prices (Next 30 Days)')
plt.title("30-Day Future Stock Price Prediction")
plt.xlabel("Days Ahead")
plt.ylabel("Predicted Price")
plt.legend()
plt.grid(True)
plt.show()
