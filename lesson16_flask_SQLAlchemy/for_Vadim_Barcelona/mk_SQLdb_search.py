from flask import Flask
import sqlite3

with open ('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/calendar.csv') as file:
    calendar_dict = {}
    calendar_list = []
    for row in file:
        calendar_list.append(row.replace('\n', ''))
        
    for i in range (0, len(calendar_list)):
        if i == 0:
            column_list = calendar_list[0].split(',')
            for num in range (0,len(column_list)):
                calendar_dict [column_list[num]] = ''
                
        else:
            inner_list = calendar_list[i].split(',')
            for num in range (7):
                calendar_dict [column_list[num]] += f", {calendar_list[num]}"

    print (calendar_dict)
    

        