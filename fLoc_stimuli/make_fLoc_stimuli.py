import os
import random
from PIL import Image, ImageDraw, ImageFont

join = os.path.join

def get_image_files(directory):
    """List all image files in the votcloc/stimuli/scrambled."""
    supported_formats = ['.jpeg', '.jpg', '.png', '.bmp', '.gif']  # Add or remove formats as needed
    image_files = []
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in supported_formats):
            image_files.append(os.path.join(directory, file))
    return image_files

def create_word_images(category_of_your_stimuli, word_list, 
                       backgrounds_directory, output_dir, 
                       fonts_directory, font_size=150, doSC, doCB):

    # Get all image files for backgrounds
    background_paths = get_image_files(backgrounds_directory)

    # Get all .ttf fonts from the specified directory
    fnt = ImageFont.truetype(fonts_directory, font_size)

    for idx in range(len(word_list)):
        # Select a random background
        word = word_list[idx]
        bg_path = random.choice(background_paths)
        background = Image.open(bg_path)

        pic_width, pic_height = background.width, background.height

        with Image.open(bg_path).convert("RGBA") as base:
        # make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", base.size, (255, 255, 255,0))

            # get a drawing context
            d = ImageDraw.Draw(txt)

            # draw text, half opacity, center the image
            _, _, w, h = d.textbbox((0, 0), word, font = fnt)
            d.text(((pic_width-w)/2, (pic_height-h)/2), word, font=fnt, fill=255,
                                        stroke_width = 10, stroke_fill = "white")
            d.textlength(word, font=fnt)        
        
            # draw text, full opacity
            out = Image.alpha_composite(base, txt)

            # if you want to test, you can use out.show()
            # out.show()
            # Save the image
            out = out.convert("RGB")
            output_path = os.path.join(output_dir, f"{category_of_your_stimuli}-{idx}.jpeg")
            out.save(output_path)
            
            if doCB:
                top_image = Image.new('RGB', [w, h], (255, 255, 255))
                draw = ImageDraw.Draw(top_image)
                
                # Set the colors
                number_of_square_across = 10

                # Set the colors
                color_one = (0, 0, 0)
                color_two = (0, 0, 255)

                length_of_square = h/number_of_square_across
                length_of_two_squares = h/number_of_square_across*2
                pixels = top_image.load()  # create the pixel map

                for i in range(h):
                    # for every 100 pixels out of the total 500 
                    # if its the first 50 pixels
                    if (i % length_of_two_squares) >= length_of_square:
                        for j in range(w):
                            if (j % length_of_two_squares) < length_of_square:
                                pixels[i,j] = color_one
                            else:
                                pixels[i,j] = color_two

                    # else its the second 50 pixels         
                    else:
                        for j in range(w):
                            if (j % length_of_two_squares) >= length_of_square:
                                pixels[i,j] = color_one
                            else:
                                pixels[i,j] = color_two

                top_image.show()
                
                
                
                
                
                
                
                
            if doSC:    

def get_ttf_fonts(fonts_directory):
    """List all .ttf font files in the specified directory."""
    font_paths = []
    for file in os.listdir(fonts_directory):
        if file.endswith('.ttf'):
            font_paths.append(os.path.join(fonts_directory, file))
    return font_paths


# FOLDERS
homedir = os.getenv('HOME')
word_dir = join(homedir,'toolboxes/votc-langorth/DATA/output')
backgrounds_directory = join(homedir,"soft/fLoc/stimuli/scrambled")
base_output_dir = join(homedir,"soft/SHINEtoolbox/SHINE_INPUT/")
fonts_directory = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

# VARIABLES
font_size = 150
doSC = True
doCB = True

# These are the lists of words we need to generate, this comes from fLoc
#         stim_set1 = {'body' 'JP_word1' 'adult' 'ff' 'cb'};
#         stim_set2 = {'limb' 'JP_word2' 'child' 'cs' 'sc'};

languages = ['ES','EU','JP','ZH','DE']

categories_textfiles_dict = {
    "ES_word1":'RW_ES_CB1_80_justwords.txt',
    # "ES_word2":'RW_ES_CB2_80_justwords.txt',
    # "EU_word1":'RW_EU_CB1_80_justwords.txt',
    # "EU_word2":'RW_EU_CB2_80_justwords.txt',
    # "JP_word1":'RW_JP_CB1_72_justwords.txt',
    # "JP_word2":'RW_JP_CB2_72_justwords.txt',
    # "ZH_word1":'RW_ZH_CB1_80_justwords.txt',
    # "ZH_word2":'RW_ZH_CB2_80_justwords.txt',
    # "DE_word1":'RW_DE_CB1_80_justwords.txt',
    # "DE_word2":'RW_DE_CB2_80_justwords.txt',
}

for category_of_your_stimuli in categories_textfiles_dict.keys(): 
    word_listn = open(
        join(word_dir,categories_textfiles_dict[category_of_your_stimuli]),
        'r').readlines()
    word_list = [w.strip('\n') for w in word_listn]

    output_dir = join(base_output_dir, category_of_your_stimuli)
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    create_word_images(category_of_your_stimuli, word_list, backgrounds_directory, 
                       output_dir, fonts_directory, font_size, doSC, doCB)

