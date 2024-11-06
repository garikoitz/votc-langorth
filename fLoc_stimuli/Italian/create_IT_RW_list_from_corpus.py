
import pandas as pd
import os
import random
from wuggy import WuggyGenerator
import time   
'''
The Italian corpus is from this source: https://www.corpusitaliano.it/en/contents/description.html

It is the corpus that contains 220 million words from online material. 

They provide: 
1. the corpus
2. the annotated corpus
3. the occurrence counts for all the element
4. the occurrence counts for the elements without numbers etc
'''


## Input the basedir
basedir='/Users/tiger/italian_stim/corpus'  
# Load the lemma freq txt
IT_lemma_freq=pd.read_csv(os.path.join(basedir,'lemma-WITHOUTnumberssymbols-frequencies-paisa.txt'), sep=",", header=1, names=["lemma","occurrence"])
# Format the Lemma_freq txt
total_lemma_counts=IT_lemma_freq['occurrence'].sum()
IT_lemma_freq["LEMMA"]=IT_lemma_freq.lemma.astype(str)
IT_lemma_freq["freq"]=IT_lemma_freq.occurrence.apply(lambda x: round(10e6*x/total_lemma_counts,2)).astype(int)

###### 
# Input 1:
# draft_IT_word_list df, this one we can preselect the word that are having the length we want and the frequency we want
# Then we will merged the annotated info to this list and we do the further selection
######

# apply the criteria to the words to get the lists
# word length 4,5,6
word_length=IT_lemma_freq['LEMMA'].apply(lambda x: (len(x) >= 4) and len(x)<=6)
# filter the high and low frequency word from the list
# Used from one paper, I stored it in the paper pile
# standard high freq > 1000 
high_freq=IT_lemma_freq['freq'].apply(lambda x: x>1000)
# standard low freq  > 1   <39
low_freq=IT_lemma_freq['freq'].apply(lambda x: x<39 and x>1)

# get the IT_high-low freq big df
draft_IT_word_list=IT_lemma_freq[word_length & (high_freq | low_freq)]
# the size of it are
print(f"The total number of words in draft IT list: {draft_IT_word_list.shape[0]}")

# Read the corpus annotated, get the linguistic info
# now get the information of the notation
def parse_paisa_corpus(file_path):
    # Define the columns based on the provided description
    columns = [
        'ID', 'FORM', 'LEMMA', 'CPOSTAG', 'POSTAG', 
        'FEATS', 'HEAD', 'DEPREL', 'unused_1', 'unused_2'
    ]
    
    # Initialize an empty list to store rows of the DataFrame
    data = []
    
    # Read the file and parse it
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Skip comment lines or empty lines
            if line.startswith('#') or line.strip() == "":
                continue
                
            # Split the line into fields based on whitespace
            fields = line.split('\t')
            
            # Make sure the line has 10 fields (to match the structure)
            if len(fields) == 10:
                # Append only relevant columns and drop 'unused_1' and 'unused_2'
                data.append(fields[:8])  # We take only the first 8 fields
                
    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data, columns=columns[:8])  # Use only relevant column names

    return df

t=time.time()
annotated_lemma_path=os.path.join(basedir,'paisa.annotated.CoNLL.utf8')
annotated_whole_list= parse_paisa_corpus(annotated_lemma_path)

# Merge the linguistic to the draft IT list
annoted_list=pd.merge(draft_IT_word_list, annotated_whole_list, on='LEMMA', how='left')
####
# second DF, the annted list of the preselect IT list with freq and length filtered
####
annoted_list=annoted_list.filter(items=['LEMMA','freq','FORM','POSTAG','DEPREL']).reset_index(drop=True).drop_duplicates(keep='first',inplace=False)
# Here we want to save it
#annoted_list.to_csv(os.path.join(basedir,'IT_annoted_list_short.txt'))
elapsed = time.time() - t
print(f"Time to get the annoted and store the final one takes {elapsed}")

######
###### Below, start the filtering based on the linguistic properties
######
# 1. clean the annoted list using wuggy,
# wuggy can detect if a word is Italian or not, and due to the fact that this corpus is a online Italian corpus, there are a lot of English or Acronyms 


from wuggy import WuggyGenerator
import swifter
t=time.time()
# Filter the non-Italian word using wuggy
# Initialize the Wuggy generator for Italian
g = WuggyGenerator()
g.load("orthographic_italian")  # Load Italian configuration

# Function to check if a word is Italian
def is_italian(word):
    try:
        # Generate matches for the word to check its language
        matches = g.generate_classic([word])
        return any(match['word'] == word for match in matches)
    except:
        return False  # In case of errors, treat it as non-Italian

# Apply the function and filter the dataframe
print ('start doing apply')
lemma_freq_list=annoted_list.filter(items=['LEMMA','freq']).reset_index(drop=True).drop_duplicates(keep='first',inplace=False)
lemma_freq_list.to_csv(os.path.join(basedir,'IT_RW_list_length_freq_filtered.txt'))
is_italian = lemma_freq_list['LEMMA'].swifter.apply(is_italian)  # Mark Italian words
filtered_final = annoted_list[is_italian]

# store it first
filtered_final.to_csv(os.path.join(basedir,'IT_RW_list_wuggy_filtered.txt'))

print(f"The total number of words in final IT list: {filtered_final.shape[0]}")
elapsed = time.time() - t
print(f"Time to get the wuggy preprocessed one takes: {elapsed}")

#####
# last step, ramdom choose 100 words of high frequency and 100 words of low frequency.
# Go to Nicola or Simona, as them help to get the final list of 80H+80L
#####


high_frequency_list=filtered_final[filtered_final['freq'].apply(lambda x: x>1000)]
low_frequency_list=filtered_final[filtered_final['freq'].apply(lambda x: x<39 and x>1)]

# random choose 100 from high frequency and low frequency list
rand_high= random.sample(range(0,high_frequency_list.shape[0]), 100)
final_high_freq_list=high_frequency_list.iloc[rand_high]

rand_low= random.sample(range(0,low_frequency_list.shape[0]), 100)
final_low_freq_list=low_frequency_list.iloc[rand_low]


final_high_freq_list.to_csv(os.path.join(basedir,'IT_RWH.txt'),index=False)
final_low_freq_list.to_csv(os.path.join(basedir,'IT_RWL.txt'),index=False)

# then choose 80 RWH and choose 80RWL to have the final RW list

# then choose 50% of the high and 50% of the low to form the PW list

# then choose 50% of the high and 50% of the low to form the CS list