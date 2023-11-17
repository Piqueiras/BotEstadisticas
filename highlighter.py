import calendar
from typing import List,Dict

def month_highlight(year:int,month:int,highlights:List[int],pre_char='__**',post_char='**__') -> str:
    
    month_str = calendar.month(year, month)
    
    #Iterate days to highlight
    for day in highlights:
        #Format the day string
        colored_day = pre_char + str(day) + post_char

        #Find occurrences of the digits inside the year string
        count_day_in_year = str(year).count(str(day))

        #Changes digits color only in the right place
        if str(day) in str(year):
            #Paint day within year (first occurrence(s)) and one more occurrence (the curr. day)
            month_str = month_str.replace(str(day), colored_day, count_day_in_year + 1)
            #Remove color of the first occurrence(s) in the year
            month_str = month_str.replace(pre_char, '', count_day_in_year)
            month_str = month_str.replace(post_char, '', count_day_in_year)
        else:
            month_str = month_str.replace(str(day), colored_day, 1)
            
    return month_str

def year_highlight(year:int,highlights:Dict[int,List[int]],pre_char='__**',post_char='**__'):
    result : List[str] = []
    
    #Just use the function on every month
    for month in range(1,13):
        if month in highlights:
            result.append(month_highlight(year,month,highlights[month],pre_char,post_char))
        else:
            result.append(calendar.month(year, month))
            
    return "\n".join(result)