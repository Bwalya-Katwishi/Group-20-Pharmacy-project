import os
import cv2
import numpy as np

# Paths
yes_path = "../data/brain_mri/yes"
no_path = "../data/brain_mri/no"

# Image size (important for ML)
IMG_SIZE = 128

# Data containers
X = []
y = []

# Function to load images
def load_images(folder, label):
    for img_name in os.listdir(folder):
        img_path = os.path.join(folder, img_name)

        try:
            img = cv2.imread(img_path)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            X.append(img)
            y.append(label)

        except:
            pass

# Load both classes
load_images(yes_path, 1)  # Tumor
load_images(no_path, 0)   # No Tumor

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

print("Images shape:", X.shape)
print("Labels shape:", y.shape)

import matplotlib.pyplot as plt

plt.imshow(X[0])
plt.title("Label: " + str(y[0]))
plt.show()