import os
import random
from PIL import Image, ImageDraw, ImageFont
join = os.path.join
import numpy as np
from pathlib import Path
import random
import math
from scipy.io import savemat

'''
This script is used for generate the fLoc stimuli
    1. for the fMRI: CN RW, CN FF, CN CS, and CN SC
        it's gonna be scrambled background
        color is white
    2. for the LDT: CN RW, CN CS and CN PW
        it's gonna be grey background
        color of word is black
    3. create 1024x1024x100
        need PNGs for that
        it's gonna be 25 50 100 letsize
        black word and white background


'''
def images_to_mat_uint8_4d(
    input_dir: Path, 
    output_mat: Path,
    force: bool = False
):
    """
    Loads 100 PNG RGB images of shape 1024x1024, stacks into a 4D uint8 array 
    (1024, 1024, 3, 100), and saves it inside a 1x1 struct with field 'images' 
    that contains a 1x1 cell array holding the 4D array.

    Result in MATLAB:
        struct with fields:
            images: {[1024×1024×3×100 uint8]}
    """
    
    if output_mat.exists() and not force:
        raise FileExistsError(
            f"'{output_mat}' already exists. Use force=True to overwrite."
        )
    
    output_mat.parent.mkdir(parents=True, exist_ok=True)

    img_paths = sorted(input_dir.glob("*.png"))
    if len(img_paths) != 100:
        raise ValueError(f"Expected exactly 100 images, but found {len(img_paths)}.")

    stacked = np.zeros((100, 1024, 1024, 3), dtype=np.uint8)
    for i, path in enumerate(img_paths):
        img = Image.open(path).convert("RGB")
        arr = np.array(img, dtype=np.uint8)
        if arr.shape != (1024, 1024, 3):
            raise ValueError(
                f"Image '{path.name}' has shape {arr.shape}, expected (1024, 1024, 3)."
            )
        stacked[i] = arr

    # Transpose to (1024, 1024, 3, 100)
    stacked_4d = np.transpose(stacked, (1, 2, 3, 0))

    # Create a 1x1 cell array containing the 4D array
    cell_array = np.empty((1, 1), dtype=object)
    cell_array[0, 0] = stacked_4d

    # Create a struct with one field 'images', containing that cell
    struct = {'images': cell_array}

    savemat(output_mat, struct)
    print(f"Saved .mat file with struct->cell->4D array to '{output_mat}'")

def get_image_files(directory):
    """List all image files in the votcloc/stimuli/scrambled."""
    supported_formats = ['.jpeg', '.jpg', '.png', '.bmp', '.gif']  # Add or remove formats as needed
    image_files = []
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in supported_formats):
            image_files.append(os.path.join(directory, file))
    return image_files

def count_black_white_pixels(image_path: Path):
    """
    Counts how many black and white pixels an image has (assuming it's strictly black text 
    on a white background) and computes the ratio (black_count / white_count).
    
    Args:
        image_path (Path): The path to the input image.

    Returns:
        dict: A dictionary containing:
            - black_count (int): Number of black pixels.
            - white_count (int): Number of white pixels.
            - ratio (float or None): black_count / white_count. 
              If white_count == 0, ratio will be None.
    """
    
    # Open and ensure it's in RGB mode
    with Image.open(image_path).convert("RGB") as img:
        # Get all pixel values in one go
        pixels = img.getdata()
        
        black_count = 0
        white_count = 0
        
        for r, g, b in pixels:
            if (r, g, b) == (0, 0, 0):
                black_count += 1
            elif (r, g, b) == (255, 255, 255):
                white_count += 1
        
        # Compute the ratio of black to white pixels
        ratio = black_count / white_count if white_count != 0 else None
        
        return {
            "black_count": black_count,
            "white_count": white_count,
            "ratio": ratio
        }

'''
if __name__ == "__main__":
    # Example usage:
    img_path = Path("word.png")
    results = count_black_white_pixels(img_path)
    print(f"Black pixels: {results['black_count']}")
    print(f"White pixels: {results['white_count']}")
    print(f"Ratio (black/white): {results['ratio']}")
'''

def crop_word(img_path:Path, output_dir:Path, reference:str, force:bool ):
    '''
    This function should be able to get the word out of the picture, so that we could adjust the size for ret
    img_path: 
        the Path object of the image file path
    output_dir:
        the directory to output
    reference:
        is if from ret or for floc
        if it is ret, then we are choosing from black word and white bg
        if it is floc, we are choosing from white word and transparent bg

        img_path="/home/irakeinu/toolboxes/fLoc/stimuli/intermediate_files/CH_words_img"
        output_dir="/home/irakeinu/toolboxes/fLoc/stimuli/CH_RW"
        reference="fLoc"
        force=True
    '''
    imagename=img_path.name
    output_name=imagename.replace('.png','_crop.png')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_path=output_dir / output_name
    
    if img_path.suffix.lower() != ".png":
        raise ValueError("Input file must be a .png file")

    
    if output_file_path.exists() and not force:
        raise FileExistsError(f"File {output_file_path} already exists. Use force=True to overwrite.")  
      
    img = Image.open(img_path).convert('RGBA')
    image_data = np.array(img)

    if reference=='floc':
        # it is a 308x308x4, so we get the Alpha info
        alpha_channel = image_data[:, :, 3]
        # white mask is the T/F table for the white 
        # white_mask = (image_data[:, :, 0] == 255) & (image_data[:, :, 1] == 255) & (image_data[:, :, 2] == 255) & (alpha_channel > 0)
        # for chinese chars is black text
        white_mask = (image_data[:, :, 0] == 0) & (image_data[:, :, 1] == 0) & (image_data[:, :, 2] == 0) & (alpha_channel > 0)
        # Then get the coordinates of the white part
        white_coords = np.argwhere(white_mask)
        # get x y limit
        (y_min, x_min), (y_max, x_max) = white_coords.min(axis=0), white_coords.max(axis=0)
    elif reference=='ret':
        # white mask is the T/F table for the white 
        black_mask = (image_data[:, :, 0] == 0) & (image_data[:, :, 1] == 0) & (image_data[:, :, 2] == 0) 
        # Then get the coordication of the white part
        black_coords = np.argwhere(black_mask)
        # get x y limit
        (y_min, x_min), (y_max, x_max) = black_coords.min(axis=0), black_coords.max(axis=0)
    cropped_image = img.crop((x_min, y_min, x_max, y_max))
    cropped_image.save(output_file_path)

    x=cropped_image.size[0]
    y=cropped_image.size[1]

    # return the size of the cropped image
    return x,y
src_dir=Path('/home/irakeinu/toolboxes/fLoc/stimuli/intermediate_files/CH_words_img')
images=[f'CH_RW-{i+1}.png' for i in range(80)]
output_dir=Path(src_dir) / "CH_words_img_crop"

size=[]
for image in images:
    img_path=Path(src_dir) / image
    reference='floc'
    force=True
    x,y=crop_word(img_path, output_dir, reference, force)
    #size is the x y for letsize 25
    size.append((x,y))

# need to find a way to calculate the ratio of the Chinese word


def resize_image_by_ratio(
    image_path: Path,
    output_dir: Path,
    letsize: int,
    ratio: float,
    force: bool = False
) -> Path:
    """
    Resizes the given image by the specified ratio and saves it to output_dir.
    
    Args:
        image_path (Path): The path to the source image file.
        output_dir (Path): The directory where the resized image will be saved.
        ratio (float): The ratio by which the image is resized. 
                       For example, 0.5 will make the image half its size, 
                       2.0 will double it.
        force (bool): If True, overwrite the output image if it already exists.
                      If False, raise an exception if the output file exists.

    Returns:
        Path: The full path to the resized image.
    """
    
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Construct the output image path output_name=imagename.replace('.png','_crop.png')
    output_image_path = output_dir / image_path.name.replace('.png',f'_letsize-{letsize}.png')
    
    # If the file exists and force=False, raise an exception
    if output_image_path.exists() and not force:
        raise FileExistsError(f"Output file '{output_image_path}' already exists.")
    
    # Open the image
    with Image.open(image_path) as img:
        original_width, original_height = img.size
        
        # Calculate new dimensions
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Resize (use LANCZOS for high-quality results)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save the resized image
        resized_img.save(output_image_path)
    
    return output_image_path




def convert_white_text_to_black_variants(
    image_path: Path,
    output_dir: Path,
    force: bool = False
) -> None:
    """
    Convert an image of white text on a transparent background into two variants:
      1) black text on a white background
      2) black text on a gray background

    The images will be saved in the given output_dir.
    
    Args:
        image_path (Path): The path to the source image (white text on transparent bg).
        output_dir (Path): The directory where output images will be saved.
        force (bool): If True, overwrite output files if they already exist.
                      If False, raise an exception if output files exist.
    """

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    dir_name=image_path.parent.parent.name
    output_black_white=output_dir / dir_name.replace('cropped_Transbg','ret') / image_path.parent.name
    output_black_grey=output_dir / dir_name.replace('cropped_Transbg','beh') / image_path.parent.name

    output_black_white.mkdir(parents=True, exist_ok=True)
    output_black_grey.mkdir(parents=True, exist_ok=True)
    # Derive output file paths (PNG extension)
    white_bg_output = output_black_white / image_path.name.replace('TransBG-', '')
    grey_bg_output = output_black_grey / image_path.name.replace('TransBG-', '')

    # Check if output files exist and handle the 'force' logic
    for out_path in [white_bg_output, grey_bg_output]:
        if out_path.exists() and not force:
            raise FileExistsError(f"Output file '{out_path}' already exists.")

    # --- Open the original image in RGBA mode ---
    with Image.open(image_path).convert("RGBA") as img:

        # Extract pixel data
        pixels = img.getdata()

        # Create a new RGBA image for black text on transparent background
        new_data = []
        for (r, g, b, a) in pixels:
            # If alpha > 0, we assume it's white text; convert to black text
            if a > 0:
                new_data.append((0, 0, 0, 255))  # black
            else:
                new_data.append((0, 0, 0, 0))    # remain transparent

        black_text_img = Image.new("RGBA", img.size)
        black_text_img.putdata(new_data)

        # 1) Composite onto a WHITE background
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        white_bg.alpha_composite(black_text_img)
        white_bg_final = white_bg.convert("RGB")
        white_bg_final.save(white_bg_output)

        # 2) Composite onto a GRAY background
        grey_bg = Image.new("RGBA", img.size, (128, 128, 128, 255))
        grey_bg.alpha_composite(black_text_img)
        grey_bg_final = grey_bg.convert("RGB")
        grey_bg_final.save(grey_bg_output)

    print(f"Successfully created:\n  - {white_bg_output}\n  - {grey_bg_output}")

def create_1024x1024_paragraph(
    words_dir: Path,
    output_path: Path,
    force: bool = False,
    canvas_size=(1024, 1024),
    padding=20,
    horizontal_spacing=15,
    vertical_spacing=25
):
    """
    Creates a 1024x1024 image with a grid of word images from words_dir,
    ensuring each row has the same number of images (columns).
    
    Steps:
      1) Collect & measure all images; find max width & height.
      2) Compute how many columns and rows can fit within the canvas_size,
         given the padding and spacing.
      3) Determine how many words we can place fully (rows * columns).
      4) Place them in a centered grid so that no row is partially filled.
    
    Args:
        words_dir (Path): Directory containing single-word images (e.g. ~95x95).
        output_path (Path): Where to save the final 1024x1024 PNG.
        force (bool): Overwrite output if True, else raise error if file exists.
        canvas_size (tuple): (width, height), default is (1024, 1024).
        padding (int): Space around the edges of the canvas.
        horizontal_spacing (int): Horizontal gap between images in a row.
        vertical_spacing (int): Vertical gap between rows.
    """

    # 1) File check & gather images
    if output_path.exists() and not force:
        raise FileExistsError(f"Output file '{output_path}' already exists. "
                              "Use force=True to overwrite.")

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect .png images (add more patterns if you have other formats)
    word_paths = list(words_dir.glob("*.png"))
    if not word_paths:
        raise ValueError(f"No .png images found in directory: {words_dir}")

    # Shuffle if you want a random arrangement
    random.shuffle(word_paths)

    # 2) Create a blank canvas (white background)
    canvas_w, canvas_h = canvas_size

    # Measure all images to find the maximum width/height
    max_w = 0
    max_h = 0
    for img_path in word_paths:
        with Image.open(img_path) as im:
            w, h = im.size
            if w > max_w:
                max_w = w
            if h > max_h:
                max_h = h

    # Compute how many images (columns) can fit in one row
    # Each column is max_w wide, plus horizontal_spacing (except maybe after the last column)
    # Available horizontal space = canvas_w - 2*padding
    # We'll assume we add spacing between columns, so effectively each column needs (max_w + horizontal_spacing),
    # but the last column doesn't *require* spacing on its right. 
    # A simple approach is to treat each column as (max_w + horizontal_spacing) except for the last,
    # so effectively:
    #   columns = floor( (AvailableWidth + horizontal_spacing) / (max_w + horizontal_spacing) )
    # so that if one column fits, we can place it. 
    import math

    available_w = canvas_w - 2*padding
    columns = (available_w + horizontal_spacing) // (max_w + horizontal_spacing)
    columns = int(columns)  # ensure integer

    if columns < 1:
        raise ValueError("Not enough horizontal space to fit even one image with the given padding/spacings.")

    # Compute how many rows fit
    available_h = canvas_h - 2*padding
    rows = (available_h + vertical_spacing) // (max_h + vertical_spacing)
    rows = int(rows)

    if rows < 1:
        raise ValueError("Not enough vertical space to fit even one row with the given padding/spacings.")

    # The total capacity in full rows:
    capacity = rows * columns

    # We only place a multiple of columns so that every row is full.
    # So the actual number of images we can place is the largest multiple of columns <= len(word_paths).
    # e.g., if we have 37 images and columns=5, we can only place 35 in full rows.
    # However, typically you might do:
    #   num_words_to_place = min(capacity, len(word_paths))
    # which ensures we fill up to capacity or the number we have.
    # That means if we have fewer than capacity, we might end up with the last row not completely filled.
    # But you specifically want each row to have the same number of words. 
    # => We must discard any leftover beyond multiples of columns.
    total_images = len(word_paths)
    if total_images >= capacity:
        # We can fill up to 'capacity' words fully
        num_words_to_place = capacity
    else:
        # If we don't have enough words to fill all rows,
        # we can figure out how many full rows we can do:
        full_rows_possible = total_images // columns
        num_words_to_place = full_rows_possible * columns

    if num_words_to_place == 0:
        raise ValueError("Not enough images to fill even one full row. "
                         f"Needed {columns} images, but only {total_images} available.")

    # Now slice the word_paths to the chosen number
    final_word_paths = word_paths[:num_words_to_place]

    # 3) Build a new white canvas to draw on
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))

    # 4) Calculate the "grid" bounding box 
    # We have 'columns' columns, 'rows_needed' = num_words_to_place//columns rows
    rows_needed = num_words_to_place // columns

    grid_width = columns * max_w + (columns - 1) * horizontal_spacing
    grid_height = rows_needed * max_h + (rows_needed - 1) * vertical_spacing

    # We'll center this grid in the canvas
    start_x = (canvas_w - grid_width) // 2
    start_y = (canvas_h - grid_height) // 2

    # 5) Place the images row by row
    idx = 0
    for r in range(rows_needed):
        for c in range(columns):
            # Each cell's top-left
            x = start_x + c * (max_w + horizontal_spacing)
            y = start_y + r * (max_h + vertical_spacing)

            img_path = final_word_paths[idx]
            idx += 1

            word_img = Image.open(img_path).convert("RGBA")
            # Optionally center the image within the "cell" if it's smaller than max_w
            # For perfect alignment, compute offsets:
            offset_x = (max_w - word_img.width) // 2
            offset_y = (max_h - word_img.height) // 2

            # Now place it so it's centered in that cell
            canvas.paste(word_img, (x + offset_x, y + offset_y), mask=word_img)

    # 6) Save the result
    canvas.save(output_path)
    print(f"Saved grid layout (same number of images per row) to: {output_path}")

def preproc():
    # get all the images:
    homedir = Path(os.getenv('HOME'))
    word_dir = homedir / 'toolboxes/votc-langorth/DATA/CN_material'
    types=['RW','FF'] #['RW','FF']
    output_dir=word_dir / 'derivatives' 
    force=True
    # crop everything
    for type in types:
        image_dir= word_dir / f'Transbg_CN_{type}'
        image_lst= get_image_files(image_dir)
        for img in image_lst:    
            img_path=Path(img)
            force=True
            reference='floc'
            output_dir_tbg_crop=output_dir/ 'cropped_Transbg' / f'CN_{type}'
            crop_word(img_path, output_dir_tbg_crop, reference, force)
    
    # after crop, make it to black/white and black/grey
    for type in types:
        cropped_image_dir=output_dir/ 'cropped_Transbg' / f'CN_{type}'
        cropped_image_lst= get_image_files(cropped_image_dir)
        for img in cropped_image_lst:
            image_path=Path(img)
            convert_white_text_to_black_variants(
                            image_path,
                            output_dir,
                            force)

    # change the ret-letsize-25 image background to grey
    for type in types:
        letsize_25_image_dir=output_dir/ 'ret' / f'CN_{type}_letsize-25_ratio-0.3'
        image_lst= get_image_files(letsize_25_image_dir)
        for img in image_lst:
            image_path=Path(img)
            change_bg(image_path,
                      force)            
    # the ratio I checked, it's gonna be 0.3 for letsize-25
    #   
    # then for ret, I need to resize it to letsize25 50 100, today is only 25
    # before resize, get some stats about the size of CN word and then Italian word
    # desktop=Path('/home/tlei/Desktop')
    # Italian_img_list=[desktop / f'IT_word{i+1}_letsize25.png' for i in range(4)]
    # for img in Italian_img_list:
    #     results=count_black_white_pixels(img)
    #     print(f"Black pixels: {results['black_count']}")
    #     print(f"White pixels: {results['white_count']}")
    #     print(f"Ratio (black/white): {results['ratio']}")

    # ret_CN_list=[Path(i) for i in get_image_files(output_dir / 'ret_crop_CN_RW')]
    # for img in ret_CN_list[8:12]:
    #     results=count_black_white_pixels(img)
    #     print(f"Black pixels: {results['black_count']}")
    #     print(f"White pixels: {results['white_count']}")
    #     print(f"Ratio (black/white): {results['ratio']}")
    for type in types:
        ret_CN_list=get_image_files(output_dir /'ret'/f'CN_{type}')
        img_path=[Path(i) for i in ret_CN_list]
        output_letsize25_dir= output_dir / 'ret' /f'CN_{type}_letsize-{letsize}_ratio-{ratio}'
        letsize=25
        ratio=0.3
        force=True
        for img in img_path:
            resize_image_by_ratio(
                img,
                output_letsize25_dir,
                letsize,
                ratio,
                force
            )

    # now create 100 ramdon images with size 1024x1024
    for type in types:
        word_img_dir=output_dir / 'ret' /f'CN_{type}_letsize-{letsize}_ratio-{ratio}'

        output_1024_dir= output_dir/'ret'/ f'CN_{type}_1024x1024_letsize-{letsize}_PNGs'
        for i in range(100):
            output_filename= output_1024_dir /  f'CN_{type}_1024x1024_{i+1}_letsize-{letsize}.png'
            create_1024x1024_paragraph(
                    word_img_dir,
                    output_filename,
                    force,
                    canvas_size=(1024, 1024),
                    padding=20,
                    horizontal_spacing=15,
                    vertical_spacing=25
                )
    ##########################################
    ##########################################
    # store things into a mat
    for type in types:
        input_dir= output_dir/'ret'/ f'CN_{type}_1024x1024_letsize-{letsize}_PNGs'
        output_mat=output_dir/'ret'/f'CN_{type}_1024x1024x100_letsize-{letsize}.mat'
        convert_mode = "RGB"
        images_to_mat_uint8_4d(
                input_dir, 
                output_mat,
                force
            )

def create_CN_fig_overlay(background_path, figure_path, output_path, convert_to_white=False):
    background = Image.open(background_path)
    figure = Image.open(figure_path).convert("RGBA")

    if convert_to_white:
        pixels = figure.getdata()
        new_pixels = [
            (255, 255, 255, a) if (r, g, b) == (0, 0, 0) else (r, g, b, a)
            for (r, g, b, a) in pixels
        ]
        figure.putdata(new_pixels)

    # Get the dimensions of the figure and background
    fig_width, fig_height = figure.width, figure.height
    pic_width, pic_height = background.width, background.height

    background.paste(figure, ((pic_width - fig_width) // 2, (pic_height - fig_height) // 2), figure)

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



def resize_to_make_50_100():
    # get all the images:
    homedir = Path(os.getenv('HOME'))
    word_dir = homedir / 'toolboxes/votc-langorth/DATA/CN_material'
    types=['RW','FF'] #['RW','FF']
    output_dir=word_dir / 'derivatives'

    for type in types:
        ret_CN_list=get_image_files(output_dir /'ret'/f'CN_{type}')
        img_path=[Path(i) for i in ret_CN_list]
        letsize=100
        ratio=0.9
        output_letsize25_dir= output_dir / 'ret' /f'CN_{type}_letsize-{letsize}_ratio-{ratio}'
        
        force=True
        for img in img_path:
            resize_image_by_ratio(
                img,
                output_letsize25_dir,
                letsize,
                ratio,
                force
            )

    # now create 100 random images with size 1024x1024
    for type in types:
        word_img_dir=output_dir / 'ret' /f'CN_{type}_letsize-{letsize}_ratio-{ratio}'

        output_1024_dir= output_dir/'ret'/ f'CN_{type}_1024x1024_letsize-{letsize}_PNGs'
        for i in range(100):
            output_filename= output_1024_dir /  f'CN_{type}_1024x1024_{i+1}_letsize-{letsize}.png'
            create_1024x1024_paragraph(
                    word_img_dir,
                    output_filename,
                    force,
                    canvas_size=(1024, 1024),
                    padding=20,
                    horizontal_spacing=15,
                    vertical_spacing=25
                )
    ##########################################
    ##########################################
    # store things into a mat
    for type in types:
        input_dir= output_dir/'ret'/ f'CN_{type}_1024x1024_letsize-{letsize}_PNGs'
        output_mat=output_dir/'ret'/f'CN_{type}_1024x1024x100_letsize-{letsize}.mat'
        convert_mode = "RGB"
        images_to_mat_uint8_4d(
                input_dir, 
                output_mat,
                force
            )

# the change BG function is used to make fixRW and fixFF
def change_bg(
    image_path: Path,
    force: bool = False
) -> None:
    """
    Convert an image of white text on a transparent background into two variants:
      1) black text on a white background
      2) black text on a gray background

    The images will be saved in the given output_dir.
    
    Args:
        image_path (Path): The path to the source image (white text on transparent bg).
        output_dir (Path): The directory where output images will be saved.
        force (bool): If True, overwrite output files if they already exist.
                      If False, raise an exception if output files exist.
    """
    image_path=Path(image_path)
    output_dir=image_path.parent.parent  / 'ret_fix' 

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    grey_bg_output=output_dir / image_path.name

    # --- Open the original image in RGBA mode ---
    with Image.open(image_path).convert("RGBA") as img:

        # Extract pixel data
        pixels = img.getdata()

        # Create a new RGBA image for black text on transparent background
        new_data = []
        for (r, g, b, a) in pixels:
            # If it is black, we maintain it 
            if r>130 :
                new_data.append((0, 0, 0, 0))    # remain transparent
            else:
                new_data.append((r,g,b,a))
        black_text_img = Image.new("RGBA", img.size)
        black_text_img.putdata(new_data)


        # 2) Composite onto a GRAY background
        grey_bg = Image.new("RGBA", img.size, (128, 128, 128, 255))
        grey_bg.alpha_composite(black_text_img)
        grey_bg_final = grey_bg.convert("RGB")
        grey_bg_final.save(grey_bg_output)

    print(f"Successfully created: \n  - {grey_bg_output}")

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
word_dir = join(homedir,'toolboxes/votc-langorth/DATA/CN_stim')
backgrounds_directory = join(homedir,"toolboxes/fLoc/stimuli/scrambled")
base_output_dir = join(homedir,"Desktop")

# Overlay all cropped word images onto scrambled backgrounds
cropped_dir  = Path(homedir) / 'toolboxes/fLoc/stimuli/intermediate_files/CH_words_img/CH_words_img_crop'
scrambled_dir = Path(backgrounds_directory)
output_overlay_dir = Path(base_output_dir) / 'CN_RW_overlay'
output_overlay_dir.mkdir(parents=True, exist_ok=True)

figure_paths     = sorted(cropped_dir.glob('*.png'))
background_paths = sorted(scrambled_dir.glob('*.jpg'))

# Randomly sample one background per figure (without replacement if possible)
sampled_backgrounds = random.sample(background_paths, len(figure_paths)) \
    if len(background_paths) >= len(figure_paths) \
    else [background_paths[random.randint(0, len(background_paths) - 1)] for _ in figure_paths]

for i, (figure_path, background_path) in enumerate(zip(figure_paths, sampled_backgrounds)):
    output_filename = figure_path.stem.replace('_crop', '') + '_overlay.png'
    output_path = output_overlay_dir / output_filename
    create_CN_fig_overlay(background_path, figure_path, output_path, convert_to_white=True)
    print(f'[{i+1}/{len(figure_paths)}] {figure_path.name} -> {output_path.name}')

print(f'\nDone! {len(figure_paths)} overlays saved to: {output_overlay_dir}')

