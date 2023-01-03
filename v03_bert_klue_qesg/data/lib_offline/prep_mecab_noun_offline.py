

import pandas as pd
from konlpy.tag import Mecab
from tqdm import tqdm_notebook as tqdm

def content2noun_mecab(series_content, save_path = None):
    df_com = pd.DataFrame()
    try:
        tokenizer = Mecab() 
    except:
        tokenizer = Mecab('C:\mecab\mecab-ko-dic') 


    res_list = []
    for row in tqdm(series_content):

        try:
            res = ' '.join(tokenizer.nouns(row))
            res_list.append(res)
        except:
            res_list.append('')

    df_com['contents_nouns'] = res_list
    df_com = df_com.reset_index(inplace=False, drop=True)
    if save_path != None:
        df_com.to_feather(save_path)
        print('save df_com (contents_nouns) : {}'.format(save_path))
    return df_com