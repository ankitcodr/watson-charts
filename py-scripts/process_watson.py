import csv
from datetime import datetime
with open('data/watson.csv', newline='') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')
    tasks = {}

    for row in csvreader:
        date = datetime.fromisoformat(row["start"]).date().strftime("%Y-%m-%d")
        starttime = datetime.fromisoformat(row["start"]).timestamp()
        stoptime = datetime.fromisoformat(row["stop"]).timestamp()
        tasknameLabels = [row["project"], row["tags"]]
        taskname = '-'.join(tasknameLabels)
        diff = stoptime-starttime
        if date in tasks:
            date_tasks = tasks[date]
            if taskname in date_tasks:
                date_tasks[taskname] += diff
            else:
                date_tasks[taskname] = diff
        else:
            tasks[date] = {taskname: diff, "date": date}

    headerSet = {'A'}
    data = []
    for records in tasks.values():
        data.append(records)
        for key in records.keys():
            headerSet.add(key)
    headerSet.remove("A")
    headerSet.remove("date")
    csv_columns = ["date"]
    headers = sorted(headerSet)
    for header in headers:
        csv_columns.append(header)


csv_file = "data/timesheet.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, restval='0.0')
        writer.writeheader()
        for row in data:
            writer.writerow(row)
except IOError:
    print("I/O error")
