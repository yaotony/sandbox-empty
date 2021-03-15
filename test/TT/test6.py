from datetime import date, timedelta

start_date = date(2019, 1, 1)
end_date = date(2020, 1, 1)
delta = timedelta(days=1)
while start_date <= end_date:
    print (start_date.strftime("%Y-%m-%d"))
    start_date += delta