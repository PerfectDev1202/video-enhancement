import cv2
import numpy as np

def draw_semi_transparent_rectangle(image, top_left, width, height, color, alpha=0.5, thickness=-1):
    # Create a new list for modified top_left
    top_left_x = top_left[0] + (image.shape[1] if top_left[0] < 0 else 0)
    top_left_y = top_left[1] + (image.shape[0] if top_left[1] < 0 else 0)
    # Create a copy of the image to draw on
    overlay = image.copy()
    if width == -1:
        right = image.shape[1]-1
    else:
        right = top_left_x + width
    if height == -1:
        bottom = image.shape[0] - 1
    else:
        bottom = top_left_y + height

    
    # if thickness is 0:
    overlay = cv2.rectangle(overlay, (top_left_x, top_left_y), (right,bottom), color, thickness)

    # Blend the overlay with the original image
    overlay = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    return overlay
    
# Example usage
# image = cv2.imread('path_to_image.jpg')
# draw_semi_transparent_rectangle(image, (50, 50), (200, 200), (0, 255, 0))  # Green rectangle
# cv2.imshow('Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
def draw_semi_transparent_text(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), alpha=0.5, width = None, height = None):
    # Create a copy of the image to draw on
    position = list(position)  # {{ edit_1 }}
    position[0] = position[0] + (image.shape[1] if position[0] < 0 else 0)
    position[1] = position[1] + (image.shape[0] if position[1] < 0 else 0)
    overlay = image.copy()
    
    # Get the text size
    text_size = cv2.getTextSize(str(text), font, font_scale, 2)[0]
    
    # Calculate the text position
    if not width is None:
        if width<0:
            text_x=(width+image.shape[1]+position[0]-text_size[0])/2
        else:
            text_x=(width-text_size[0])/2+position[0]
    else:
        text_x=position[0]
    if not height is None:
        if height<0:
            text_y=(height+image.shape[0]+position[1]-text_size[1])/2+ text_size[1]
        else:
            text_y=(height-text_size[1])/2+position[1]+ text_size[1]
    else:
        text_y = position[1] + text_size[1]
    
    # Draw the text on the overlay
    text_x = int(text_x)  # {{ edit_1 }}
    text_y = int(text_y)  # {{ edit_2 }}
    overlay = cv2.putText(overlay, str(text), (text_x, text_y), font, font_scale, color, 2, cv2.LINE_AA)
    
    # Blend the overlay with the original image
    overlay = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    return overlay
# Example usage
# image = cv2.imread('path_to_image.jpg')
# draw_semi_transparent_text(image, 'Hello, World!', (50, 50), color=(0, 255, 0))  # Green text
# cv2.imshow('Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
