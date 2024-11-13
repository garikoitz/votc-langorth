import os
import random
from PIL import Image, ImageDraw, ImageFont
join = os.path.join

'''
This script is used for generate the fLoc stimuli,
it will create RW, SC, FF
We also need use CS

'''
def get_image_files(directory):
    """List all image files in the votcloc/stimuli/scrambled."""
    supported_formats = ['.jpeg', '.jpg', '.png', '.bmp', '.gif']  # Add or remove formats as needed
    image_files = []
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in supported_formats):
            image_files.append(os.path.join(directory, file))
    return image_files


def get_word_bounding_box(img_path,output_dir_name):
    img = Image.open(os.path.join(img_path)).convert('RGBA')
    image_data = np.array(img)
    # it is a 308x308x4, so we get the Alpha info
    alpha_channel = image_data[:, :, 3]
    # white mask is the T/F table for the white 
    white_mask = (image_data[:, :, 0] == 255) & (image_data[:, :, 1] == 255) & (image_data[:, :, 2] == 255) & (alpha_channel > 0)
    # Then get the coordication of the white part
    white_coords = np.argwhere(white_mask)
    # get x y limit
    (y_min, x_min), (y_max, x_max) = white_coords.min(axis=0), white_coords.max(axis=0)
    cropped_image = img.crop((x_min, y_min, x_max, y_max))
    cropped_image.save(output_dir_name)
    return

def create_CN_fig_overlay(background_path, figure_path, output_path):
    background = Image.open(background_path)
    figure = Image.open(figure_path).convert("RGBA") 
    pic_width, pic_height = background.width, background.height
    # Get the dimensions of the figure and background
    fig_width, fig_height = figure.width, figure.height
    pic_width, pic_height = background.width, background.height

    background.paste(figure, ((pic_width - fig_width) // 2, (pic_height - fig_height) // 2), figure)

    # draw text, full opacity
    background.save(output_path)
    return
def creat_CN_FF(background_path, figure_path, output_path):
    background = Image.open(background_path)
    figure = Image.open(figure_path).convert("RGBA") 
    mirrored_image = figure.transpose(Image.FLIP_LEFT_RIGHT)

    fig_width, fig_height = mirrored_image.width, mirrored_image.height
    pic_width, pic_height = background.width, background.height

    background.paste(mirrored_image, ((pic_width - fig_width) // 2, (pic_height - fig_height) // 2), mirrored_image)
    # draw text, full opacity
    background.save(output_path)
    return
def create_CN_SC(background_path, figure_path, output_path, tile_size=10):
    # Load the background and figure images
    background = Image.open(background_path)
    figure = Image.open(figure_path).convert("RGBA")  # Ensure figure is in RGBA mode

    # Get the dimensions of the figure and background
    fig_width, fig_height = figure.width, figure.height
    pic_width, pic_height = background.width, background.height

    # Calculate the number of tiles in each dimension based on tile_size
    num_tiles_x = fig_width // tile_size
    num_tiles_y = fig_height // tile_size

    # Create a list to store the tiles
    tiles = []

    # Extract tiles from the figure image
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            left = x * tile_size
            upper = y * tile_size
            right = left + tile_size
            lower = upper + tile_size
            tile = figure.crop((left, upper, right, lower))
            tiles.append(tile)

    # Randomly shuffle the tiles
    random.shuffle(tiles)

    # Create a new image to reconstruct the scrambled image
    scrambled_image = Image.new("RGBA", (fig_width, fig_height), (255, 255, 255, 0))

    # Paste the shuffled tiles back into the scrambled image
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            index = y * num_tiles_x + x
            left = x * tile_size
            upper = y * tile_size
            scrambled_image.paste(tiles[index], (left, upper))

    # Paste the scrambled figure onto the background image
    background.paste(scrambled_image, ((pic_width - fig_width) // 2, (pic_height - fig_height) // 2), scrambled_image)

    # Save the result
    background.save(output_path)


def main ():
    # 1. get the image from output folder

    # 2. crop the image and have secondary output

    # 3. For RW, plot RW and save

    # 4. For SC, based on the crop image doing scamble

    # 5. For FF, need to manually cut, then save as L and R, and then flip the left and right 
        # here aslo based on the crop box, crop only by x not y 
    return
            
### Section below is for excuting
###
# FOLDERS
homedir = os.getenv('HOME')
word_dir = join(homedir,'tlei/toolboxes/votc-langorth/DATA/CN_stim')
backgrounds_directory = join(homedir,"tlei/toolboxes/fLoc/stimuli/scrambled")
base_output_dir = join(homedir,"Desktop")
