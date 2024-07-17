import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime as dt

# date should be in format 2024-07-15
def get_calllog(date):
    response = requests.get(f"https://mke-police.herokuapp.com/?date={date}")
    while response.status_code != 200:
        print(f"could not get to page {response}")
        response = requests.get(f"https://mke-police.herokuapp.com/?date={date}")
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    df_date = pd.read_html(str(soup))[0]
    df_date["date"] = date
    return df_date

df_24 = pd.DataFrame()
start_date = "2024-06-01"
end_date = dt.date.today()
date_range = pd.date_range(start = start_date, end = end_date)

for single_date in date_range:
    date = single_date.strftime("%Y-%m-%d")
    print(f"in date {date}")
    df_date = get_calllog(date)
    df_24 = pd.concat([df_24, df_date], ignore_index=True)

df_24 = df_24.drop_duplicates(subset=['Time', 'Location', 'Nature', 'date'])

print("Exporting to CSV:")
df_24.to_csv("rnc-calls.csv", index = False)
