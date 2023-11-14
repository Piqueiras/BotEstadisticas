import database
from typing import Dict

import pandas as pd
import plotly.express as px
from collections import defaultdict
from datetime import datetime

def generate_leaderboard(db:database.UserData,image_path:str):
    # Create a dictionary to store the total study time for each user and month
    monthly_user_times = defaultdict(lambda: defaultdict(int))

    # Iterate through the nested dictionary to aggregate study times by user and month
    for username, date_data in db.items():
        for date, time in date_data.items():
            month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
            monthly_user_times[username][month] += time

    # Create a list of dictionaries for Plotly
    data_list = []
    for username, month_data in monthly_user_times.items():
        data_list.append({'Username': username, **month_data})

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # Create a stacked bar plot using Plotly Express
    fig = px.bar(df, x='Username', y=list(df.columns[1:]), title='Monthly Study Hours Leaderboard', labels={'value': 'Study Hours'}, barmode='relative')
    fig.write_image("imagen.png",width=1200)
