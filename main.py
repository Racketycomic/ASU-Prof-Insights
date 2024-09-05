from helpers.selenium_helper import get_driver, validate_links,extract_asu_profile,close_windows
from helpers.mongo_helper import insert_profs,get_connection
import pandas as pd

df = pd.read_csv('merged.csv')
driver = get_driver()
client = get_connection()
i = 0
profile_not_found = []
for index,row in df.iterrows():
    links = validate_links(driver,row['Full Name'])
    if 'asu_profile' in links.keys():
        print(f"{row['Full Name']} found")
        profile = extract_asu_profile(driver,links['asu_profile'])
        if profile is not None:
            insert_profs(client,profile)
        else:
            print(f"{row['Full Name']} not found")
            profile_not_found.append(row['Full Name'])
    else:
        print(f"{row['Full Name']} not found")
        profile_not_found.append(row['Full Name'])
        
    close_windows(driver)
    
with open('Profile Not Found.txt','a+') as f:
    for profile in profile_not_found:
        f.write(f'{profile}\n')
        
client.close()
driver.quit()

