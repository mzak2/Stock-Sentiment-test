import streamlit as st
import numpy as np
import requests
import json
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta

current_date = datetime.today()
yesterday = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")

def get_stonk_data():
    #url = 'https://tradestie.com/api/v1/apps/reddit?date=2022-04-03'
    url = f'https://tradestie.com/api/v1/apps/reddit?date={yesterday}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

stonks = get_stonk_data()

df = json_normalize(stonks)

#print(df)

st.table(df)
