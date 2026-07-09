#datatime module classes and its operation
from datetime import datetime
print("Current time with date: ",datetime.now()) #class.method.parameter(year,month,day,hrs,min,sec,microsec)
""" from datetime import date
today=date.today() #class_name.method_name.parameters(year,month,day)
print(today) #year-month-day(yyyy-mm-dd)
print("Current day:", today.day) """
import time
t=time.localtime()
print("Current time without date: ",time.strftime("%H:%M:%S",t))

#number of days calculation use timedelta class
from datetime import datetime,timedelta
""" today=datetime.now()
yesterday=today-timedelta(days=1)
tommorow=today+timedelta(days=1)
after_10=today+timedelta(days=10)
days_diff=str(after_10-(today))
print(yesterday)
print(tommorow)
print(after_10)
print(days_diff) """

#to convert date string format to date object vice versa strptime(string_variable,format)
""" date_string= "15 December 2025"
date_object = datetime.strptime(date_string, "%d %B %Y")
print(date_object) """

#
dates = ['2024/12/2', '2023/2/12', '2025/1/24']
format1 = '%Y/%m/%d'

for i in dates:
    dt = datetime.strptime(i, format1)
    print("strptime:", dt)
    print("date only:", dt.date())
    print("strftime:", dt.strftime("%d-%m-%Y"))