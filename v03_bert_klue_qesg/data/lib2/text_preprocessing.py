import re

## 재목 필터링
def remove_title_by_keyword(df_src, col_trg ='title'):
    # 타이플에서 제거 키워드 
    remove_regex = re.compile(
    r"""
    증시|증시|시황|펀드|자산|상승|실적|어닝|호재|거래소|급락|
    급등|코스피|특징주|시총|폭락|폭등|종목|농구|축구|골프|
    스포츠|탁구|레슬링|환율|개장|코스닥|매수|매도|
    추경|와인|주가|불펜|株|투수|총선|금리|주식|리뷰|
    이 시각|證|재방송|에이스|영화|공천|실점|득점|개막전|
    팔자|하락|프로|경기|국민|박근혜|공천|민주당|통합당|한국당|
    정의당|입국금지|이낙연|연인|후보|감염|박원순|선발진|
    정봉주|대통령|확진|부고|입주물량|별세|강세 토픽|인터뷰|
    포토|인사|소방방재신문|성금내역|러시아|낙태|만루|감독|
    초대석|체고|포토|스포츠|영상|그림책|여행|공감|컬럼|
    주요일정|게임노트|가요|연예|굿모닝|소상공인|케이에스피뉴스|
    러시아|날씨|퍼포먼스|육아|외식|KOTRA|유학생|르포|♥|케미|
    이효리|법문|시평|녹색|도서관|다문화|정봉주|대통령|확진|결혼식|팔짱|
    """)

    isleave_list = []
    for title in df_src[col_trg]:
         #반드시 제외할 키워드가 있다면 추가
        if remove_regex.search(title):
            isleave_list.append(False)
        else:
            isleave_list.append(True)
    return df_src[isleave_list]


## 본문 다운로드 클리닝

def cleaning_korean(content):
    content = content.replace('\n\n','')
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

def manual_remove(content):
    trgs = ['무단 전재 및 재배포금지','연합뉴스','copyrights','viewer',
            '기사내용 요약','입력','수정','이데일리','무단전재재배포 금지','공감언론','뉴시스',
            '저작권자','의 다른기사보기','키워드copyright it chosun','전자부품 전문 미디어 디일렉','무단전재 및 재배포 금지'
           ,'기사문의 및 제보 카톡라인','제보는','카카오톡','기호일보 아침을 여는 신문 kihoilbo','okjebo']
    for trg in trgs:
        content = content.replace(trg,'')
    return content
