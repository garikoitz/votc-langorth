import matplotlib.pyplot as plt
import os
join=os.path.join
from PIL import Image
import numpy as np
from pathlib import Path
import dask
from dask import delayed, compute

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
from PIL import Image
import os

def flip_image(input_file_path: Path, output_dir: Path, force: bool = False):
    """
    Flip an image left-to-right and then up-down.

    Parameters:
    - input_file_path (Path): Path to the input image file.
    - output_file_path (Path): Path to save the flipped image.
    - force (bool): If True, overwrite the output file if it exists. Default is False.
    """
    imagename=input_file_path.name
    output_name=imagename.replace('CN_CS','CN_FF')
    output_file_path=output_dir / output_name
    
    if input_file_path.suffix.lower() != ".png":
        raise ValueError("Input file must be a .png file")

    
    if output_file_path.exists() and not force:
        raise FileExistsError(f"File {output_file_path} already exists. Use force=True to overwrite.")

    try:
        with Image.open(input_file_path) as img:
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)  # Left to right flip first
            flipped_img = flipped_img.transpose(Image.FLIP_TOP_BOTTOM)  # Then up-down flip
            flipped_img.save(output_file_path, format='PNG')
            print(f'successfully created image {output_file_path}')
    except Exception as e:
        print(f"Error processing image: {e}")



def process_images_dask(input_dir: str, output_dir: str, force: bool = False):
    """
    Process all .png images in a folder using Dask for parallel execution.

    Parameters:
    - input_dir (str): Path to the folder containing input images.
    - output_dir (str): Path to the folder to save processed images.
    - force (bool): If True, overwrite the output files if they exist.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_files = list(input_dir.glob("*.png"))  # Get all PNG files
    tasks = [delayed(flip_image)(input_dir / img.name, output_dir, force) for img in image_files]

    compute(*tasks)  # Execute tasks in parallel

if __name__ == "__main__":

    homedir = os.getenv('HOME')
    input_dir=join(homedir,'toolboxes/votc-langorth/DATA/CN_material/Transbg_CN_CS')

    output_dir=join(homedir,'toolboxes/votc-langorth/DATA/CN_material/Transbg_CN_FF')


    process_images_dask(input_dir,output_dir, force=True)