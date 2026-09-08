import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load saved data (IMPORTANT: we reuse from previous step)
from prepare_data import X, y

# Flatten images (convert 2D image → 1D array)
X = X.reshape(len(X), -1)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

import matplotlib.pyplot as plt

# Show one test image
plt.imshow(X_test[0].reshape(128,128,3))
plt.title("Actual: " + str(y_test[0]) + " | Predicted: " + str(predictions[0]))
plt.show()