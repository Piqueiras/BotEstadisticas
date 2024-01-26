import database
from typing import Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
from datetime import datetime

def generate_leaderboard(file_path:str,image_path:str):
    db:database.UserData = database.read_json_file(file_path)
    # Create a dictionary to store the total study time for each user and month
    monthly_user_times = defaultdict(lambda: defaultdict(int))

    # Iterate through the nested dictionary to aggregate study times by user and month
    for username, date_data in db.items():
        for date, time in date_data.items():
            month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
            monthly_user_times[username][month] += time

    # Create a list of dictionaries for Plotly
    data_list = []

    # Sort
    while monthly_user_times.__len__()>0:
        max = list(monthly_user_times.keys())[0]
        for username in monthly_user_times.keys():
            if sum(monthly_user_times[username].values()) > sum(monthly_user_times[max].values()):
                max = username
        data_list.append({'Username': max, **monthly_user_times[max]})
        del monthly_user_times[max]
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # Create a stacked bar plot using Plotly Express
    fig = px.bar(df, x='Username', y=list(df.columns[1:]), title='Monthly Study Hours Leaderboard', labels={'value': 'Study Hours'}, barmode='relative')
    fig.write_image(image_path,width=1200)

def user_graph(usr:str,file_path:str,image_path:str):
    db:database.UserData = database.read_json_file(file_path)
    
    df = pd.DataFrame(zip(db[usr].keys(), db[usr].values()), columns=["LABEL", "VALUE"])
    
    fig = px.bar(df, x="LABEL", y="VALUE", title="Dias", orientation="v")
    fig.write_image(image_path,width=1200)