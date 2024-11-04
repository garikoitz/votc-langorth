import nltk
import pandas as pd
import os
import random

basedir='/Users/tiger/italian_stim/corpus'  
IT_lemma_freq=pd.read_csv(os.path.join(basedir,'lemma-WITHOUTnumberssymbols-frequencies-paisa.txt'), sep=",", header=1, names=["lemma","occurrence"])

total_lemma_counts=IT_lemma_freq['occurrence'].sum()
IT_lemma_freq["LEMMA"]=IT_lemma_freq.lemma.astype(str)
IT_lemma_freq["freq"]=IT_lemma_freq.occurrence.apply(lambda x: round(10e6*x/total_lemma_counts,2)).astype(int)

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
IT_word_list=IT_lemma_freq[word_length & (high_freq | low_freq)]
# the size of it are
print(f"The total number of words are: {IT_word_list.shape[0]}")

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

annotated_lemma_path=os.path.join(basedir,'paisa.annotated.CoNLL.utf8')
annotated_whole_list= parse_paisa_corpus(annotated_lemma_path)

#IT_word_list=IT_word_list.rename(columns={'lemma':'LEMMA'})
annoted_list=pd.merge(IT_word_list, annotated_whole_list, on='LEMMA', how='left')

final_annoted_list=annoted_list.filter(items=['LEMMA','freq','POSTAG']).reset_index(drop=True).drop_duplicates(keep='first',inplace=False)
# store it first
#final_annoted_list.to_csv(os.path.join(basedir,'derivatives_final_annoted_list.txt'))
POS_list=['A','B','DD','E','S','V']
linguistic_filter=final_annoted_list['POSTAG'].apply(lambda x: x in POS_list)
filtered_final=final_annoted_list[linguistic_filter]
# remains the items that are only be here once
only_one_filtered=filtered_final[filtered_final['LEMMA'].map(filtered_final['LEMMA'].value_counts())==1]

high_frequency_list=only_one_filtered[only_one_filtered['freq'].apply(lambda x: x>1000)]
low_frequency_list=only_one_filtered[only_one_filtered['freq'].apply(lambda x: x<39 and x>1)]

# random choose 100 from high frequency and low frequency list

rand_high= random.sample(range(0,high_frequency_list.shape[0]-1), 100)
final_high_freq_list=high_frequency_list.iloc[rand_high]

rand_low= random.sample(range(0,low_frequency_list.shape[0]-1), 100)
final_low_freq_list=low_frequency_list.iloc[rand_low]


# final_high_freq_list.to_csv(os.path.join(basedir,'derivatives_final_high_frequency_list.txt'),index=False)
# final_low_freq_list.to_csv(os.path.join(basedir,'derivatives_final_low_frequency_list.txt'),index=False)

# then choose 80 RWH and choose 80RWL to have the final RW list

# then choose 50% of the high and 50% of the low to form the PW list

# then choose 50% of the high and 50% of the low to form the CS list