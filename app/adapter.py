# Adapter 함수
def adapter(df):
    columns_to_use = ['ID','clubNm', 'briefDescription', 'recruitDescription', 
                      'targetPeopleDescription', 'targetCycleDescription', 
                      'applyDescription', 'actDayDescription', 
                      'locationDescription', 'costDescription', 
                      'specDescription']
    return df[columns_to_use].copy()
