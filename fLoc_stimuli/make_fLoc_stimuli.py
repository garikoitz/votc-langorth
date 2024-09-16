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

def create_checkboard(background_path, output_path, word, fnt):
    # Load the background image
    background = Image.open(background_path)

    draw = ImageDraw.Draw(background)

    # draw text, half opacity, center the image
    _, _, w, h = draw.textbbox((0, 0), word, font = fnt)
    canvas_width, canvas_height= background.size

    # Define the location of the checkerboard (randomly)
    cheker_center_x=  canvas_width//2
    cheker_center_y=  canvas_height//2


    x0,y0=cheker_center_x-w//2, cheker_center_y-h//2
    x1,y1=cheker_center_x+w//2, cheker_center_y+h//2

    # Draw a random shape (in this case, a rectangle)
    draw.rectangle([x0,y0, x1,y1], fill=0)

    # Draw the checkerboard pattern inside the shape
    square_size = 20
    for row in range(y0,y1, square_size):
        for col in range(x0, x1, square_size):
            if (row // square_size + col // square_size) % 2 == 0:
                draw.rectangle([col, row, col + square_size, row + square_size], fill=255)
            else:
                 draw.rectangle([col, row, col + square_size, row + square_size], fill=0)

    background.save(output_path)

def create_word(background_path, output_path, word, fnt):
    background = Image.open(background_path)

    pic_width, pic_height = background.width, background.height

    draw = ImageDraw.Draw(background)

    # draw text, half opacity, center the image
    _, _, w, h = draw.textbbox((0, 0), word, font=fnt)

    draw.text(((pic_width - w) / 2, (pic_height - h) / 2), word, font=fnt, fill=255,
              stroke_width=2, stroke_fill="white")

    # draw text, full opacity
    background.save(output_path)

def create_scambled(background_path, output_path, word, fnt):
    background= Image.open(background_path)
    pic_width, pic_height = background.width, background.height
    txt = Image.new("RGBA", background.size, (255, 255, 255, 0))

    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity, center the image
    _, _, w, h = d.textbbox((0, 0), word, font=fnt)
    d.text(((pic_width - w) / 2, (pic_height - h) / 2), word, font=fnt, fill=(255,255,255),
           stroke_width=2, stroke_fill="white")



    # Calculate the number of tiles in each dimension
    num_tiles_x = w // 10
    num_tiles_y = h // 10
    # crop the text box for scramble
    txtbox = txt.crop(d.textbbox(((pic_width - w) / 2, (pic_height - h) / 2), word, font=fnt))
    # Create a list to store the tiles
    tiles = []

    # Extract 10x10 pixel tiles from the image
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            left = x * 10
            upper = y * 10
            right = left + 10
            lower = upper + 10
            tile = txtbox.crop((left, upper, right, lower))
            tiles.append(tile)

    # Randomly shuffle the tiles
    random.shuffle(tiles)

    # Create a new image to reconstruct the scrambled image
    scrambled_image = Image.new("RGBA", (w, h), (255, 255, 255, 0))

    # Paste the shuffled tiles back into the image
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            index = y * num_tiles_x + x
            left = x * 10
            upper = y * 10
            scrambled_image.paste(tiles[index], (left, upper))

    background.paste(scrambled_image, ((pic_width - w) // 2, (pic_height - h) // 2), scrambled_image)

    background.save(output_path)


def main(backgrounds_directory, base_output_dir, word_list, category_of_your_stimuli, doWORD, doSC, doCB, fnt, one_folder):
    background_paths = get_image_files(backgrounds_directory)

    for idx in range(len(word_list)):
        # Select a random background
        word = word_list[idx]
        background_path = random.choice(background_paths)

        if doWORD:
            if one_folder:
                output_dir = join(base_output_dir, 
                                  f"{category_of_your_stimuli[0:2]}_ALL")
            else:
                output_dir = join(base_output_dir, category_of_your_stimuli)
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f"{category_of_your_stimuli}-{idx+1}.jpg")
            create_word(background_path, output_path, word, fnt)
            # print(f"the image of word {word} and index {idx} created to {output_path}")
            
        if doSC:
            if one_folder:
                output_dir = join(base_output_dir, 
                                  f"{category_of_your_stimuli[0:2]}_ALL")
            else:            
                output_dir = join(base_output_dir, category_of_your_stimuli.replace('word','SC'))
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f"{category_of_your_stimuli.replace('word','SC')}-{idx+1}.jpg")
            create_scambled(background_path, output_path, word, fnt)
            # print(f"the image of scrabled word {word} and index {idx} created to {output_path}")

        if doCB:
            if one_folder:
                output_dir = join(base_output_dir, 
                                  f"{category_of_your_stimuli[0:2]}_ALL")
            else:
                output_dir = join(base_output_dir, category_of_your_stimuli.replace('word','CB'))
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f"{category_of_your_stimuli.replace('word','CB')}-{idx+1}.jpg")
            create_checkboard(background_path, output_path, word, fnt)
            # print(f"the image of checkboards based on length of {word} and index {idx} created to {output_path}")




            
            
### Section below is for excuting
###
# FOLDERS
homedir = os.getenv('HOME')
word_dir = join(homedir,'toolboxes/votc-langorth/DATA/output')
backgrounds_directory = join(homedir,"toolboxes/fLoc/stimuli/scrambled")
base_output_dir = join(homedir,"Desktop")
fonts_directory = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

# VARIABLES
font_size = 150
doWORD = True
fnt = ImageFont.truetype(fonts_directory, font_size)
# These are the lists of words we need to generate, this comes from fLoc
#         stim_set1 = {'body' 'JP_word1' 'adult' 'ff' 'cb'};
#         stim_set2 = {'limb' 'JP_word2' 'child' 'cs' 'sc'};

languages = ['ES','EU','JP','ZH','DE']

# Web page to translate to Georgian, just copy and paste lists
# https://translit.cc/ge/

categories_textfiles_dict = {
     "ES_word1":'RW_ES_CB1_80_justwords.txt',
     "ES_word2":'RW_ES_CB2_80_justwords.txt',
     "ES_CS1":'CS_ES_CB1_80_csonly.txt',
     "ES_CS2":'CS_ES_CB2_80_csonly.txt',
    
    #"EU_word1":'RW_EU_CB1_80_justwords.txt',
    #"EU_word2":'RW_EU_CB2_80_justwords.txt',
    #"EU_CS1":'CS_EU_CB1_80_justwords.txt',
    #"EU_CS2":'CS_EU_CB2_80_justwords.txt',
    #"EU_FF1":'FF_EU_CB1_80_justwords.txt',
    #"EU_FF2":'FF_EU_CB2_80_justwords.txt',    
    # "JP_word1":'RW_JP_CB1_72_justwords.txt',
    # "JP_word2":'RW_JP_CB2_72_justwords.txt',
    # "JP_CS1":'CS_JP_CB1_134_justwords.txt',
    # "JP_FF1":'FF_JP_CB1_72_justwords.txt',
    # "JP_FF2":'FF_JP_CB2_72_justwords.txt',
    # "ZH_word1":'RW_ZH_CB1_80_justwords.txt',
    # "ZH_word2":'RW_ZH_CB2_80_justwords.txt',
    # "DE_word1":'RW_DE_CB1_80_justwords.txt',
    # "DE_word2":'RW_DE_CB2_80_justwords.txt',
}

for category_of_your_stimuli in categories_textfiles_dict.keys():
    word_listn = open(
        join(word_dir, categories_textfiles_dict[category_of_your_stimuli]),
        'r').readlines()
    word_list = [w.strip('\n') for w in word_listn]
  
    if 'word' in category_of_your_stimuli:
        main(backgrounds_directory, base_output_dir, word_list, category_of_your_stimuli, 
             True, True, True, fnt, False)
    else:
        main(backgrounds_directory, base_output_dir, word_list, category_of_your_stimuli, 
             True, False, False, fnt, False)