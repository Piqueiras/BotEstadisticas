from typing import Dict
from datetime import date
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
        
def increase_value(file_path:str, usr:str, value:int) -> None:
    db : UserData = read_json_file(file_path)
    today = date.today().isoformat()
    if usr not in db:
        db[usr] = {}  #If user is new, create new dict
    if today not in db[usr]:
        db[usr][today] = value  #If user had no entry for today, create one
    else:
        db[usr][today] += value
    write_json_file(file_path,db)
        
def total_value(file_path:str, usr:str) -> int:
    db : UserData = read_json_file(file_path)
    total = 0
    for key in db[usr].keys():
        total += db[usr][key]
    return total

def day_value(file_path:str, usr: str, day: date) -> int:
    db : UserData = read_json_file(file_path)
    if usr not in db:
        raise ValueError(f"User '{usr}' not in database.")
    if day not in db[usr]:
        raise ValueError(f"No info for '{usr}' at '{day}'.")
    return db[usr][day.isoformat()]

def month_info(file_path:str, usr: str, year: int, month: int) -> str:
    db : UserData = read_json_file(file_path)
    res = ""
    for day in range(1, 32):
        fecha = date(year, month, day).isoformat()
        if fecha in db[usr]:
            res += f"{fecha}: {db[usr][fecha]}\n"
    return res

def user_stats(file_path:str,usr:str) -> str:
    db : UserData = read_json_file(file_path)
    res = ""
    for key, value in db[usr].items():
        res += f"{key}: {value}\n"
    return res.strip()

def delete_user(file_path:str, usr:str) -> None:
    db : UserData = read_json_file(file_path)
    db[usr] = {}
    write_json_file(file_path,db)
    
def delete_day(file_path:str, usr:str) -> None:
    db : UserData = read_json_file(file_path)
    today = date.today().isoformat()
    db[usr].pop(today,None)
    write_json_file(file_path,db)