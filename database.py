from typing import Dict, Tuple
from datetime import date, timedelta
import json

UserData = Dict[str,Dict[date,int]]

def read_json_file(file_path:str) -> UserData:
    try:
        with open(file_path, 'r') as file:
            db = json.load(file)
        return db
    except FileNotFoundError:
        return {}

def write_json_file(file_path:str, db:UserData) -> None:
    with open(file_path, 'w') as file:
        json.dump(db, file, indent=4)
        
def increase_value(db:UserData, usr:str, value:int) -> None:
    today = date.today().isoformat()
    if usr not in db:
        db[usr] = {}  #If user is new, create new dict
    if today not in db[usr]:
        db[usr][today] = value  #If user had no entry for today, create one
    else:
        db[usr][today] += value
        
def total_value(db:UserData, usr:str) -> int:
    total = 0
    for key in db[usr].keys():
        total += db[usr][key]
    return total

def day_value(db:UserData, usr: str, day: date) -> int:
    if usr not in db:
        raise ValueError(f"User '{usr}' not in database.")
    if day not in db[usr]:
        raise ValueError(f"No info for '{usr}' at '{day}'.")
    return db[usr][day.isoformat()]

def month_info(db:UserData, usr: str, year: int, month: int) -> str:
    res = ""
    for day in range(1, 32):
        fecha = date(year, month, day).isoformat()
        if fecha in db[usr]:
            res += f"{fecha}: {db[usr][fecha]}\n"
    return res

def user_stats(db:UserData,usr:str) -> str:
    res = ""
    for key, value in db[usr].items():
        res += f"{key}: {value}\n"
    return res.strip()

def delete_user(db:UserData, usr:str) -> None:
    db[usr] = {}
    
def delete_day(db:UserData, usr:str) -> None:
    today = date.today().isoformat()
    db[usr].pop(today,None)
    
def consecutive_days(db:UserData, usr:str) -> Tuple[int,str]:
    if usr not in db:
        return None, None
    
    #If user has no data for today, return a streak of 0
    
    today = date.today()
    if today.isoformat() not in db[usr] or db[usr][today.isoformat()]<1:
        return 0, None
    
    streak = 1
    #Now just iterate backwards until we find a date the user has no data on
    prev_date=today-timedelta(days=1)
    
    while prev_date.isoformat() in db[usr] and db[usr][prev_date.isoformat()]>0:
        prev_date=prev_date-timedelta(days=1)
        streak+=1
        
    return streak,prev_date.isoformat()
    