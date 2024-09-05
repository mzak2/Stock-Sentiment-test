import streamlit as st
import numpy as np
import requests
import json
import pandas as pd
from pandas import json_normalize
from datetime import datetime, timedelta
from itables.streamlit import interactive_table

# Set pandas options for better mobile viewing
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

# Initialize session state for date if not already present
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.today()

# Ensure current_date is not in the future
if st.session_state.current_date > datetime.today():
    st.session_state.current_date = datetime.today()

def get_stonk_data(date):
    if date > datetime.today():
        date = datetime.today()
    
    url = f'https://tradestie.com/api/v1/apps/reddit?date={date.strftime("%Y-%m-%d")}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def display_table(stonks):
    st.header(f"Stock Data for: {st.session_state.current_date.strftime('%Y-%m-%d')}")
    df = json_normalize(stonks)

    # Swaps the first and last columns for readability
    cols = list(df.columns)
    if len(cols) > 1:
        cols[0], cols[-1] = cols[-1], cols[0]  # Swap the first and last columns
        df = df[cols]
    
    df.iloc[:, 2] = (df.iloc[:, 2] * 100).round(2).astype(str) + "%"
    
    interactive_table(df)

# Function to go to the previous day
def prev_day_button():
    if st.button("Previous Day"):
        st.session_state.current_date -= timedelta(days=1)
        st.experimental_rerun()

# Function to reset date to yesterday
def reset_button():
    if st.button("Reset Date"):
        st.session_state.current_date = datetime.today() - timedelta(days=1)
        st.experimental_rerun()

# Function to go to the next day
def next_day_button():
    if st.button("Next Day"):
        if st.session_state.current_date >= datetime.today():
            st.session_state.current_date = datetime.today()  # Fix assignment
        else:
            st.session_state.current_date += timedelta(days=1)
        st.experimental_rerun()

# Get the stock data for the current date in session state
stonks = get_stonk_data(st.session_state.current_date)

if stonks:
    display_table(stonks)
else:
    st.error("No stock data available for this date.")

# Display buttons
prev_day_button()
reset_button()
next_day_button()
