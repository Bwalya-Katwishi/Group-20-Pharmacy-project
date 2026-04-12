import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Path to dataset
data_path = "../data/brain_mri/yes"

# Get list of images
images = os.listdir(data_path)

# Pick first image
img_path = os.path.join(data_path, images[0])

# Load image
img = mpimg.imread(img_path)

# Display image
plt.imshow(img)
plt.title("MRI Scan (Tumor)")
plt.axis('off')
plt.show()