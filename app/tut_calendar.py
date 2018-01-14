from calendar import Calendar, TextCalendar, HTMLCalendar, calendar

cal = Calendar()
iter = cal.iterweekdays()
for i in iter:
	print(i)

#cal.TextCalendar()
html_cal = HTMLCalendar()
code =  html_cal.formatmonth(2017, 12, False) 
code =  html_cal.formatyear(2017, 6)   # in HTML Format!
code =  html_cal.formatyearpage(2017,encoding='UTF-8')
code = calendar(2017)   # In text !
print(code)