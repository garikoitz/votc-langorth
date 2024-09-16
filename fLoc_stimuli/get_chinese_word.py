# Tiger 2024 Feb 20
# this script is used for getting the Chinese characters from the grey background picture
# the output will be transparent background characters
from PIL import Image
import numpy as np
import os


input_CN_dir='/User/Users/tiger/Packages/toolbox/votc-langorth/DATA/output'
# get all the files into a list for iteration 
def get_image_files(directory):
    """List all image files in the votcloc/stimuli/scrambled."""
    supported_formats = ['.jpeg', '.jpg', '.png', '.bmp', '.gif']  # Add or remove formats as needed
    image_files = []
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in supported_formats):
            image_files.append(os.path.join(directory, file))
    return image_files

CN_image_files= get_image_files(input_CN_dir)


def get_CN_character(image_path, outputcolor='black' ):
    '''
    Get CN character from a grey background file
    input file size 308*308

    Output
    CN character in transparent background
    color can be set, default black
    '''
    
    image = Image.open(image_path).convert("RGBA")
    
    
    # Convert the image to numpy array and split the channels
    data = np.array(image)
    red, green, blue, alpha = data.T
    
    # Replace white and grey background with a transparent background
    # Adjust the threshold according to your image's background color
    threshold = 127  # You might need to adjust this threshold
    transparent_areas = (red > threshold) & (green > threshold) & (blue > threshold)
    data[..., :-1][transparent_areas.T] = (0, 0, 0)  # Set the color to black (can be adjusted)
    data[..., -1][transparent_areas.T] = 0  # Set the alpha channel to 0 (transparent)

    # Customize the character color
    # options: white, black
    '''
    RGB color code
    
    '''
    if outputcolor == "black":


        # Convert back to an Image and save
        result_image = Image.fromarray(data)
    elif outputcolor == "white":
        result_image = Image.fromarray(data)

    return result_image




def make_CN_stim (result_image, I ):
    return

def visual_degree_and_stim_size(visual_degree, projector_measurement, background_size ):
    stimulus_size=0
    return stimulus_size


result_image= 