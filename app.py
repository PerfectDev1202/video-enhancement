import cv2
import numpy as np
import matplotlib.pyplot as plt
import tqdm  # Import tqdm for progress bar
import pandas as pd
from insert import draw_semi_transparent_rectangle, draw_semi_transparent_text

# Load the video
video_path = '1.mp4'
cap = cv2.VideoCapture(video_path)

#frame per second and time per frame
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Frames per second: {fps}")
f_time=1/fps


# Load data from edit.csv
data_csv = pd.read_csv('edit.csv', delimiter='\t')
print(data_csv)

# Get total number of frames for progress tracking
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frames)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

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
    img_mod = denoised_img_enhanced
    for index, row in data_csv.iterrows():
        start_time = pd.to_timedelta(row['start'])
        end_time = pd.to_timedelta(row['end'])
        text = row['text']
        score = row['score']
        # Calculate the frame range for the current text
        start_frame = int(start_time.total_seconds() * fps)
        end_frame = int(end_time.total_seconds() * fps)

        # Check if the current frame is within the range to display the text
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if start_frame < current_frame <= end_frame:
            # print(text,score)
            if not pd.isna(text):
                img_mod = draw_semi_transparent_rectangle(denoised_img_enhanced,(0,-100),-1,100,(255,0,0),0.2)
                img_mod = draw_semi_transparent_text(img_mod, text, (0, -100), cv2.FONT_HERSHEY_TRIPLEX, font_scale=2, color=(255, 255, 255), alpha=0.7,width=-1, height=100)
            if not pd.isna(score):
                img_mod = draw_semi_transparent_rectangle(denoised_img_enhanced,(-400,100),300,80,(255,0,0),0.5,thickness=5)
                img_mod = draw_semi_transparent_text(img_mod, f"Score: {int(score)}", (-400,100), cv2.FONT_HERSHEY_TRIPLEX, font_scale=1.5, color=(255, 30, 120), width=300, height=80 ,alpha=0.7)


    # Write the processed frame to the output video
    out.write(img_mod)

    # Convert images from BGR to RGB for matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_mod = cv2.cvtColor(img_mod, cv2.COLOR_BGR2RGB)

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
    progress_bar.update(1/total_frames*100)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
progress_bar.close()  # Close the progress bar