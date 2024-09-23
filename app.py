import cv2
import numpy as np
import matplotlib.pyplot as plt
import tqdm  # Import tqdm for progress bar

# Load the video
video_path = '1.mp4'
cap = cv2.VideoCapture(video_path)

# Get total number of frames for progress tracking
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output_video.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

# Create a figure for displaying the processed frames
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Initialize progress bar
progress_bar = tqdm.tqdm(total=total_frames, desc="Processing Video", unit="frame")

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = np.array(255*(img/255)**2.5, dtype='uint8')
    img = cv2.bilateralFilter(img, 21, 10, 20)
    img = np.array(255*(img/255)**0.4, dtype='uint8')

    # Adjust brightness and contrast
    # Enhance color and saturation
    # Convert image to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Increase saturation by 50%
    hsv_img[:,:,1] = hsv_img[:,:,1] * 1.4  # Increase saturation by 50%
    # Ensure values are within 0-255 range
    hsv_img[:,:,1] = np.clip(hsv_img[:,:,1], 0, 255)
    # Convert back to BGR color space
    denoised_img_enhanced = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

    # Adjust brightness
    denoised_img_enhanced = cv2.convertScaleAbs(denoised_img_enhanced, alpha=1.2, beta=30)

    # Write the processed frame to the output video
    out.write(denoised_img_enhanced)

    # Convert images from BGR to RGB for matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    denoised_img_enhanced_rgb = cv2.cvtColor(denoised_img_enhanced, cv2.COLOR_BGR2RGB)

    # Display the original and denoised images
    # ax1.imshow(img_rgb)
    # ax1.set_title('Original Image')
    # ax1.axis('off')

    # ax2.imshow(denoised_img_enhanced_rgb)
    # ax2.set_title('Denoised Image')
    # ax2.axis('off')

    # # Adjust the layout and display the plot
    # plt.tight_layout()
    # plt.pause(0.01)  # Pause to update the plot

    # Update progress bar
    progress_bar.update(1)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
progress_bar.close()  # Close the progress bar