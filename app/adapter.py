# Adapter 함수
def content_adapter(df):
    columns_to_use = ['id','category_id','club_nm', 'brief_description', 'recruit_description', 
                      'target_people_description', 'target_cycle_description', 
                      'apply_description', 'act_day_description', 
                      'location_description', 'cost_description', 
                      'spec_description']
    return df[columns_to_use].copy()

def favorite_adapter(df):
    columns_to_use = ['user_id','club_id']
    return df[columns_to_use].copy()

def click_adapter(df):
    columns_to_use = ['user_id', 'event_properties']
    return df[columns_to_use].copy()
