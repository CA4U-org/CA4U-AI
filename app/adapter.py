# Adapter ÇÔ¼ö
def adapter(df):
    columns_to_use = ['clubNm', 'briefDescription', 'recruitDescription', 
                      'targetPeopleDescription', 'targetCycleDescription', 
                      'applyDescription', 'actDayDescription', 
                      'locationDescription', 'costDescription', 
                      'specDescription']
    return df[columns_to_use].copy()