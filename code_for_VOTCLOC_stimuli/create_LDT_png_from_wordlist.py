import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
join = os.path.join

'''
This script is used for generate the VOTCLOC LDT stimuli,
it will create RW, PW, CS images PNG to one folder

'''
def create_word(output_path, word, fnt):
    image = Image.new("RGB", (1, 1), 'grey')
    draw = ImageDraw.Draw(image)
    # Calculate word size
    _,_,text_width, text_height = draw.textbbox((0, 0),word, font=fnt)

    pic_width=text_width
    pic_height=text_height+20
    # Create the final image with the proper dimensions
    image = Image.new("RGB", (pic_width, pic_height), 'grey')
    draw = ImageDraw.Draw(image)

    # Draw the word in the center
    draw.text((0,0), word, font=fnt,fill='black')


    # Save or display the image
    # 
    # image.show()
    image.save(output_path)

def main(rw_list,base_output_dir, word_list, category_of_your_stimuli, fnt, one_folder):

    for idx in range(len(word_list)):
        # Select a random background
        word = word_list[idx]
        rw = rw_list[idx]
        if one_folder:
            output_dir = join(base_output_dir, 
                                f"{category_of_your_stimuli[0:2]}")
        else:
            output_dir = join(base_output_dir, category_of_your_stimuli)
        if not os.path.exists(output_dir): 
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, f"{category_of_your_stimuli}_{idx+1}.png")
        create_word(output_path, word, fnt)
        # print(f"the image of word {word} and index {idx} created to {output_path}")
            

            
### Section below is for excuting
###
# FOLDERS
homedir = os.getenv('HOME')
# if in linux, need to add one tlei
base_output_dir = join(homedir,"soft",'Behav_LDT')
# for Ubuntu is "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"
# for mac is "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
fonts_directory = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
# VARIABLES
font_size = 100
fnt = ImageFont.truetype(fonts_directory, font_size)
word_dir = join(homedir,'toolboxes/votc-langorth/DATA/wordlist_for_VOTCLOC') 
langs=['AT','EN','ES','EU','FR','IT']
cats=['RW','CS','PW']

categories_textfiles_dict = {f"{code}_{cat}": f"{code}_{cat}_80.txt" for code in langs for cat in cats}

for category_of_your_stimuli in categories_textfiles_dict.keys():
    word_listn = open(
        join(word_dir, categories_textfiles_dict[category_of_your_stimuli]),
        'r').readlines()
    word_list = [w.strip('\n') for w in word_listn]
    
    rw_listn  =  open(
        join(word_dir, categories_textfiles_dict[f'{category_of_your_stimuli.split('_')[0]}_RW']),
        'r').readlines()
    rw_list = [w.strip('\n') for w in rw_listn]


    main(rw_list, base_output_dir, word_list, category_of_your_stimuli,fnt, True)


        

#doWORD, doSC, doCB,