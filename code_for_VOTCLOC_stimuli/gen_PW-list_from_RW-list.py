from wuggy import WuggyGenerator
import random
import pandas as pd
import os
import time

def gen_PW(df_RWH, df_RWL, df_word_col_name ,lang):
    '''
    code for generating PW list from word

    need to input RWH list and RWL list

    It will take half of the RWH and half of the RWL to form the final PW
    
    lang: valid options: english, italian, french, german
    '''
    g = WuggyGenerator()
    g.load(f"orthographic_{lang}")
    mixed_df, word_list=gen_rand_word_list(df_RWH, df_RWL,df_word_col_name)
    rw_pw_pair_lst=[]
    t=time.time()
    for word in word_list:
        try:    
            pw_lst=[]
            for match in g.generate_classic([word]):
                pw_lst.append(match["pseudoword"])
            num_ps=len(pw_lst)
            rand_idx= random.sample(range(0,num_ps),1)
            ps_word= pw_lst[rand_idx[0]]
            rw_pw_pair_lst.append((match['word'],ps_word))
        except Exception:
            print(f"One {word} in the MIXED list is wrong, but we excluded it into the final list")
        
    elapsed = time.time() - t
    print(f'Time take to get the PW df is {elapsed}')   
    rw_pw_df,pw_df=gen_output(rw_pw_pair_lst)

    return mixed_df, rw_pw_df, pw_df

def gen_AT_PW(AT_RW_path):
    '''
    code for generating PW list from word

    need to input RWH list and RWL list

    It will take half of the RWH and half of the RWL to form the final PW
    
    lang: valid options: english, italian, french, german
    '''
    g = WuggyGenerator()
    g.load(f"orthographic_german")
    word_list=pd.read_csv(AT_RW_path, header=None).iloc[:,0].tolist()
    rw_pw_pair_lst=[]
    t=time.time()
    for word in word_list:
        try:    
            pw_lst=[]
            for match in g.generate_classic([word]):
                pw_lst.append(match["pseudoword"])
            num_ps=len(pw_lst)
            rand_idx= random.sample(range(0,num_ps),1)
            ps_word= pw_lst[rand_idx[0]]
            rw_pw_pair_lst.append((match['word'],ps_word))
        except Exception:
            print(f"One {word} in the MIXED list is wrong, but we excluded it into the final list")
        
    elapsed = time.time() - t
    print(f'Time take to get the PW df is {elapsed}')   
    rw_pw_df,pw_df=gen_output(rw_pw_pair_lst)

    return rw_pw_df, pw_df
def gen_rand_word_list(df_RWH, df_RWL, word_col_name):
    
    # randomize gen index of 50 RWH and 50 RHL
    rand_high_idx=random.sample(range(0, df_RWH.shape[0]),50)
    rand_low_idx=random.sample(range(0, df_RWL.shape[0]),50)
    rand_high_df=df_RWH.iloc[rand_high_idx]
    rand_low_df=df_RWL.iloc[rand_low_idx]

    mixed_df=pd.concat([rand_high_df,rand_low_df],axis=0)
    word_list=mixed_df[word_col_name].tolist()
    return mixed_df,word_list

def gen_output(rw_pw_tuple_list):
    '''
    '''
    rw_pw_df=pd.DataFrame(rw_pw_tuple_list,columns=['RW','PW'])
    pw_df=rw_pw_df['PW']
    return rw_pw_df,pw_df

def main():
    basedir='/media/tlei/data/toolboxes/votc-langorth/DATA/IT_material'
    RWH_fname='IT_RWH.txt' 
    RWL_fname='IT_RWL.txt'

    df_RWH=pd.read_csv(os.path.join(basedir,RWH_fname))
    df_RWL=pd.read_csv(os.path.join(basedir,RWL_fname))

    ref_rw_df, rw_pw_df, pw_df=gen_PW(df_RWH,df_RWL,"LEMMA",'italian')
    # then save both dataframe 
    ref_df_fname=os.path.join(basedir,'IT_mixed_RWHL.txt')
    rw_pw_list_fname=os.path.join(basedir,'IT_RW_PW_match.txt')
    pw_txt_fname=os.path.join(basedir,'IT_PW.txt')

    ref_rw_df.to_csv(ref_df_fname,sep='\t', index=False)
    rw_pw_df.to_csv(rw_pw_list_fname, sep='\t',index=False)
    pw_df.to_csv(pw_txt_fname,sep='\t', index=False)
    print(f'Length of the PW list is {pw_df.shape[0]}')
    
    ### a small note to filter RW_PW df with PW df
    #df_filtered = df1[df1['PW'].isin(df2['PW'])]

    # for IT, there are first 2 raw lists: RWH RWL
    # then those two lists were hadn filtered by NK, to drop the weired meaning and weired word
    # the I have a new IT_RWH and IT_RWL, I create IT_PW, IT_RW_PW_match from it 
    # I filtered the PW with the pseudohomophones and then get the filnal list: IT_PW,
    # then using this code:
    '''
    basedir='/media/tlei/data/toolboxes/votc-langorth/DATA/IT_material'
    rw_pw_list_fname=os.path.join(basedir,'IT_RW_PW_match.txt')
    df_rw_pw=pd.read_csv(rw_pw_list_fname,sep='\t')
    df_pw=pd.read_csv(os.path.join(basedir,'IT_PW.txt'),sep='\t')
    df_filtered = df_rw_pw[df_rw_pw['PW'].isin(df_pw['PW'])]
    df_filtered.to_csv(rw_pw_list_fname, sep='\t',index=False)
    df_filtered['RW'].to_csv(os.path.join(basedir,'IT_RW.txt'), index=False, sep='\t')
    '''
    # the above code gives me: IT_PW.txt and IT_RW.txt with 80 words inside of it


    ## for FR
    # I first run this raw code to get a RW-PW match list
    # then SV helped to manually check the list, mainly drop the pseudo-homophones and orthotatic 
    # illegal word
    # then I manually edit the RW_PW_match list to make it have 80 words only
    # then I use this code to create the 2 final list: FR_RW and FR_PW
    '''
    rw_pw_list_fname=os.path.join('/media/tlei/data/toolboxes/votc-langorth/DATA/FR_material','FR_RW_PW_match.txt')
    df_rw_pw=pd.read_csv(rw_pw_list_fname,sep='\t')    
    basedir='/media/tlei/data/toolboxes/votc-langorth/DATA/FR_material'
    df_rw_pw=pd.read_csv(rw_pw_list_fname,sep='\t')
    df_rw_pw['RW'].to_csv(os.path.join(basedir,'FR_RW.txt'), index=False, sep='\t')
    df_rw_pw['PW'].to_csv(os.path.join(basedir,'FR_PW.txt'), index=False, sep='\t')
    '''
def main_AT():
    basedir='/media/tlei/data/toolboxes/votc-langorth/DATA/AT_material'
    AT_df_path= join(basedir,'AT_RW_80.txt')

    rw_pw_df, pw_df=gen_AT_PW(AT_df_path)
    
    # then save both dataframe 
    rw_pw_list_fname=os.path.join(basedir,'AT_RW_PW_match.txt')
    pw_txt_fname=os.path.join(basedir,'AT_PW.txt')

    rw_pw_df.to_csv(rw_pw_list_fname, sep='\t',index=False)
    pw_df.to_csv(pw_txt_fname,sep='\t', index=False)
    print(f'Length of the PW list is {pw_df.shape[0]}')

    ### then I did a manually operation to lower case all the words
    # df_lowercase=AT_list_16.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    # df_lowercase.to_csv('/media/tlei/data/toolboxes/votc-langorth/DATA/AT_material/AT_RW_list_160.txt', header=None, index=False)
def create_PW_from_old():
    basedir='/media/tlei/data/toolboxes/votc-langorth/DATA/wordlist_for_VOTCLOC/wordlist_for_old_design'
    lang=['EN','ES','EU']
    input_output_file = {f"PW_{code}_CB1_80_justwords.txt": f"{code}_PW_80.txt" for code in lang}
    for ip in input_output_file.keys():
        print(ip)
        df=pd.read_csv(os.path.join(basedir, ip),header=0, sep='\t')
        print(df.head(5))
        out_path=os.path.join(basedir,input_output_file[ip])
        df_PW=df['Match']
        df_PW.to_csv(out_path, header=None, index=False)
if __name__ =='__main__':
    #main()
    #main_AT()
    create_PW_from_old()