import cv2
import numpy as np
import matplotlib.pyplot as plt
from insert import draw_semi_transparent_rectangle, draw_semi_transparent_text

# Load the video
img_rgb = cv2.imread("Frames/frame_0003.jpg")
# Parameters: h is the filter strength, hForColorComponents is usually same as h, templateWindowSize, searchWindowSize
img = img_rgb

img = np.array(255*(img/255)**2.5, dtype='uint8')
img = cv2.bilateralFilter(img, 21, 10, 20)
img = np.array(255*(img/255)**0.4, dtype='uint8')
# img = cv2.bilateralFilter(img, 10, 30, 5)
# Adjust brightness and contrast
# Enhance color and saturation
# Convert image to HSV color space
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# Increase saturation by 50%
hsv_img[:,:,1] = hsv_img[:,:,1] * 1.4  # Increase saturation by 50%
# Ensure values are within 0-255 range
hsv_img[:,:,1] = np.clip(hsv_img[:,:,1], 0, 255)
# Convert back to BGR color space
img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

# Adjust brightness
img = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
img = draw_semi_transparent_rectangle(img,(0,-100),-1,100,(58,78,78),0.5)
img = draw_semi_transparent_text(img, "text", (0, -100), cv2.FONT_HERSHEY_TRIPLEX, font_scale=2, color=(255, 255, 255), alpha=0.7,width=-1, height=100)
img = draw_semi_transparent_rectangle(img,(-400,100),300,80,(0,55,55),0.8,thickness=5)
img = draw_semi_transparent_text(img, "SCORE : 5", (-400,100), cv2.FONT_HERSHEY_TRIPLEX, font_scale=1, color=(205, 72,63 ), width=300, height=80 ,alpha=1)

# Display the original and denoised images
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
ax1.imshow(cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB))
ax1.set_title('Original Image')
ax1.axis('off')

# ax2.imshow(denoised_img_enhanced_rgb)
ax2.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax2.set_title('Denoised Image')
ax2.axis('off')

# Adjust the layout and display the plot
plt.tight_layout()
plt.show()

# Release everything if job is finished
# cap.release()
cv2.destroyAllWindows()