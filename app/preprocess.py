# Preprocess 함수
def preprocess(data):
    stopwords = ['중앙대', '중앙대학교', '동아리', 'PM', '명', '기수', '기존', '기존부원', '신입', '신입부원', '1학기', '00', '정기모임', '기준', '약', '2024', '부원', '여']
    
    def preprocess_text(text):
        text = str(text)
        for stopword in stopwords:
            text = text.replace(stopword, '')
        return text
    
    for col in data.columns[1:]:
        data[col] = data[col].apply(preprocess_text)
    
    return data

