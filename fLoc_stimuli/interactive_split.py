import matplotlib.pyplot as plt
import os
join=os.path.join
from PIL import Image
import numpy as np

def flip_image(image, split_point, image_name, output_dir):
    # Convert the image to RGBA and get its size
    width, height = image.size
    
    # Split the image into left and right halves at the selected split point
    left_half = image.crop((0, 0, split_point, height))
    right_half = image.crop((split_point, 0, width, height))
    
    # Create a new image where the left and right halves will be swapped
    flipped_image = Image.new("RGBA", (width, height))
    
    # Paste the right half on the left and the left half on the right
    flipped_image.paste(right_half, (0, 0))
    flipped_image.paste(left_half, (width - split_point, 0))
    
    flipped_image.save(join(output_dir,image_name.replace('.png','_flip.png')))
    return flipped_image

def onclick(event, image):
    # This function gets triggered when the user clicks on the image
    x_click = int(event.xdata)  # The x-coordinate of the click
    
    # Call the flip_image function to flip the image based on the click position
    flipped_image = flip_image(image, x_click)
    
    # Display the flipped image using matplotlib
    plt.imshow(np.array(flipped_image))
    plt.axis('off')  # Hide axes
    plt.show()

def interactive_image_split(image_path):
    # Load the image
    image = Image.open(image_path).convert("RGBA")
    
    # Display the image using matplotlib
    fig, ax = plt.subplots()
    ax.imshow(np.array(image))
    ax.set_title('Click to choose the split point')
    
    # Set up the event listener for mouse click
    cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, image))
    
    plt.axis('off')  # Hide axes
    plt.show()
homedir = os.getenv('HOME')
output_dir=join(homedir,'tlei/toolboxes/votc-langorth/DATA/CN_stim')
tp_img_dir=output_dir
image_path=os.path.join(tp_img_dir,'TransBG-CS_001_SHEN-01.png')
interactive_image_split(image_path)