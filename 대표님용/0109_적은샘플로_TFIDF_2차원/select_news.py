import pandas as pd
from konlpy.tag import Mecab
from functools import *
from collections import Counter
import numpy as np
import re

def cleaning_korean(content):
    content = content.replace('\n\n','')
    content = content.replace('”','')
    content = ' '.join(content.split(' '))
    #클리닝1
    content = re.sub(r'... 기자', '', content)
    content = re.sub(r'...기자', '', content)

    #괄호안 제거 
    ''' 괄호안 내용 제거하기 '''
    pattern_bracket1 = r'\([^)]*\)'
    pattern_bracket2 = r'\{[^)]*\}'
    pattern_bracket3 = r'\<[^)]*\>'
    pattern_bracket4 = r'\[[^)]*\]'
    x = '이건 {괄호 안의 불필요한 정보를} 삭제하는 코드다.'
    content = re.sub(pattern=pattern_bracket1, repl='', string= content)
    content = ' '.join(content.split())
    content = re.sub(pattern=pattern_bracket2, repl='', string= content)
    content = ' '.join(content.split())
    content = re.sub(pattern=pattern_bracket3, repl='', string= content)
    content = ' '.join(content.split())
    content = re.sub(pattern=pattern_bracket4, repl='', string= content)
    content = ' '.join(content.split())

    #클리닝
    content = content.lower() #lower case
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    content = re.sub(pattern=pattern, repl='', string=content)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    content = re.sub(pattern=pattern, repl='', string=content)

    # 특수기호 특수
    content = re.sub('[-=+#/\?:^$@*\"※~%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》Δ△·“=◎<>▷]', '', content)
    content = re.sub('[一-龥]', '',content)

    #pattern = '[^\w\s]'         # 특수기호제거
    #content = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\:\;\!\-\,\_\~\$\'\"]', '',str(content)) #removepunctuation
    content = re.sub(r"[^a-zA-Z0-9가-힣\.\s]","",content)
    content = re.sub(pattern=pattern, repl='', string=content)
    content = re.sub(r'\s+', ' ', content) #remove extra space
    content = re.sub(r'<[^>]+>','',content) #remove Html tags
    content = re.sub(r'\s+', ' ', content) #remove spaces
    content = re.sub(r"^\s+", '', content) #remove space from start
    content = re.sub(r'\s+$', '', content) #remove space from the end
    return content



def load_data():
    df_temp = pd.read_parquet('df_temp.pq')

    # 기간 지정 및 제외 기타 제거 
    df = df_temp
    df_sm = df.loc[df.contents_clean != '']\
        .loc[df.y != '제외']\
        .loc[df.y != '기타']\
        .loc[df.time < '2021-04-28']\
        .loc[df.time > '2020-01-01']

    df_sm.title = df_sm.title.apply(lambda x : cleaning_korean(x))
    return df_sm

def filter_list_in_title(df_trg, cate , keywords):
    trg = cate
    df_trg = df_trg.loc[df_trg.y == trg]
    
    rows = []
    for k,item in df_trg.iterrows():
        row = item.title
        
        FLAG_OUT= False
        for keyword in keywords:
            if keyword not in row:
                FLAG_OUT = True
                break
                
        if FLAG_OUT:
            continue
        else:
            rows.append(item)
    df_in = pd.DataFrame(rows)
    return df_in

def filter_list_out_title(df_trg, trg , keyword_list ):
    print('find words is not in title')

    df_trg = df_trg.loc[df_trg.y == trg]
    
    rows = []
    for k,item in df_trg.iterrows():
        row = item.title
        FLAG_IN= False
        for keys in keyword_list:
            for key in keys:
                if key in row:
                    FLAG_IN = True
                    break
        if FLAG_IN:
            continue
        else:
            rows.append(item)
            continue
    df_out = pd.DataFrame(rows)
    df_out['from'] = 'x'
    print(f'size : {len(df_out)}')
    return df_out

def filter_list_out_content(df_trg, trg , keyword_list ):
    print('find words is not in content')

    df_trg = df_trg.loc[df_trg.y == trg]
    
    rows = []
    for k,item in df_trg.iterrows():
        row = item.contents_clean	
        FLAG_IN= False
        for keys in keyword_list:
            for key in keys:
                if key in row:
                    FLAG_IN = True
                    break
        if FLAG_IN:
            continue
        else:
            rows.append(item)
            continue
    df_out = pd.DataFrame(rows)
    df_out['from'] = 'x'
    print(f'size : {len(df_out)}')
    return df_out

def get_in_df( df , trg , keyword_list):
    print('find words is in title')
    # 키워드는 list of list 이다. 
    df_trg = df.loc[df.y == trg]
    df_inlist = []
    for keys in keyword_list:
        dfres = filter_list_in_title(df_trg , trg , keys)
        if len(dfres) != 0:
            dfres['from'] = ','.join(keys)
            df_inlist.append(dfres)
            print( trg,keys, dfres.shape)
    return df_inlist

if __name__ =='__main__':
    df = load_data()
    # 키워드 넣으면 제목에 그 키워드가 들어가 있는 뉴스를 선별해준다. 
    trg = '인적자원관리'
    keyword_list = [['사망'] , ['임금' , '협상'] , ['파업'] , ['채용','비리']]
    
    df_out_title  = filter_list_out_title( df , trg , keyword_list)
