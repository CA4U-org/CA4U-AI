# Preprocess 함수
def preprocess(data):
    stopwords = ['중앙대', '중앙대학교', '동아리', 'PM', '명', '기수','1학기', '00', '0', '정기모임', '기준', '약', '2024', '부원', '여',
        '활동', '중앙', '모집', '학기', '학회', '대학교', '합니다', '입니다', '및','있습니다', '지원', '기간', ',', '.', '-', '!', ':','?','~']
    
    import os
    import re
    def preprocess_stopwords_file():
        # 현재 파일 위치를 기준으로 stopword.txt 파일 경로 설정
        base_dir = os.path.dirname(__file__)
        stopword_path = os.path.join(base_dir, '../dataSource/stopword.txt')
        
        with open(stopword_path, 'r', encoding='utf-8') as file:
            additional_stopwords = file.read().splitlines()
        return additional_stopwords
    
    stopwords += preprocess_stopwords_file()
     
    data = data.fillna(0) #결측치 제거
    
    def preprocess_text(text):
        text = str(text)
        text = text.replace("\n", " ").replace("\n\n", " ")  # 줄바꿈 제거
        text = ' '.join(text.split())  # 중복 공백 제거
        # 단어 단위로 stopwords 제거
        pattern = r'\b(' + '|'.join(map(re.escape, stopwords)) + r')\b'
        text = re.sub(pattern, '', text)
        return text
    
    for col in data.columns[1:]:
        data[col] = data[col].apply(preprocess_text)
    
    return data
