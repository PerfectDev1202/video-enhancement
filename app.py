import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = 'Frames/frame_0005.jpg'
img = cv2.imread(image_path, cv2.IMREAD_COLOR)

# Parameters: h is the filter strength, hForColorComponents is usually same as h, templateWindowSize, searchWindowSize
denoised_img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

# Convert images from BGR to RGB for matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
denoised_img_rgb = cv2.cvtColor(denoised_img, cv2.COLOR_BGR2RGB)

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Display the original image
ax1.imshow(img_rgb)
ax1.set_title('Original Image')
ax1.axis('off')

# Display the denoised image
ax2.imshow(denoised_img_rgb)
ax2.set_title('Denoised Image')
ax2.axis('off')

# Adjust the layout and display the plot
plt.tight_layout()
plt.show()