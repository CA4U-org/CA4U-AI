# Preprocess �Լ�
def preprocess(data):
    stopwords = ['�߾Ӵ�', '�߾Ӵ��б�', '���Ƹ�', 'PM', '��', '���', '����', '�����ο�', '����', '���Ժο�', '1�б�', '00', '�������', '����', '��', '2024', '�ο�', '��']
    
    def preprocess_text(text):
        text = str(text)
        for stopword in stopwords:
            text = text.replace(stopword, '')
        return text
    
    for col in data.columns[1:]:
        data[col] = data[col].apply(preprocess_text)
    
    return data

