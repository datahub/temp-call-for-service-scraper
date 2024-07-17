import pandas as pd
from io import StringIO
import requests
from bs4 import BeautifulSoup
import datetime as dt

def get_calllog(date):
    response = requests.get(f"https://mke-police.herokuapp.com/?date={date}")
    while response.status_code != 200:
        print(f"could not get to page {response}")
        response = requests.get(f"https://mke-police.herokuapp.com/?date={date}")
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    df_date = pd.read_html(StringIO(str(soup)))[0]
    df_date["date"] = date
    return df_date

df_23 = pd.DataFrame()
start_date = "2023-06-01"
end_date = "2023-07-31"
date_range = pd.date_range(start = start_date, end = end_date)

for single_date in date_range:
    date = single_date.strftime("%Y-%m-%d")
    print(f"in date {date}")
    df_date = get_calllog(date)
    df_23 = pd.concat([df_23, df_date], ignore_index=True)

df_23 = df_23.drop_duplicates(subset=['Time', 'Location', 'Nature', 'date'])


print("Exporting to CSV:")
df_23.to_csv("2023-calls.csv", index = False)