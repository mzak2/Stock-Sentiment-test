import streamlit as st
import numpy as np
import requests
import json
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
from itables.streamlit import interactive_table


#set pandas options for better mobile viewing
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

current_date = datetime.today()
yesterday = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")

def get_stonk_data():
    url = f'https://tradestie.com/api/v1/apps/reddit?date={yesterday}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

stonks = get_stonk_data()

if stonks:
    df = json_normalize(stonks)

    #swaps the first and last columns for readability
    cols = list(df.columns)
    if len(cols) > 1:
        cols[0], cols[-1] = cols[-1], cols[0]  # Swap the first and last columns
        df = df[cols]
    
    df.iloc[:, 2] = (df.iloc[:, 2] * 100).round(2).astype(str) + "%"
    
    #function to apply alternating row colors
    def highlight_rows(row):
        return ['background-color: #f2f2f2' if row.name % 2 == 0 else '' for _ in row]

    interactive_table(df)

    
else:
    st.write("No data available")
