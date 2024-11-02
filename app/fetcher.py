def fetcher():
    df = pd.DataFrame({
        'clubNm': ['Club A', 'Club B', 'Club C'],
        'briefDescription': ['Sports club focusing on soccer', 'Tech club for coding', 'Art club for painting lovers'],
        'recruitDescription': ['Open for all interested', 'Only for university students', 'Open for beginners'],
        'targetPeopleDescription': ['People aged 18-25', 'Coding enthusiasts', 'All ages welcome'],
        'targetCycleDescription': ['Weekly', 'Bi-weekly', 'Monthly'],
        'applyDescription': ['Fill out form online', 'Contact via email', 'Apply through website'],
        'actDayDescription': ['Saturdays', 'Wednesdays', 'Fridays'],
        'locationDescription': ['Community center', 'University campus', 'Art studio'],
        'costDescription': ['Free', 'Membership fee', 'Material cost'],
        'specDescription': ['No experience required', 'Basic coding skills', 'Interest in painting']
    })
    return df
