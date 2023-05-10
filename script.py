import sqlite3
import time as timemodule

def create_table_if_needed(cur):
    query = "CREATE TABLE IF NOT EXISTS reminders(id INTEGER PRIMARY KEY, eventdesc VARCHAR, eventtime DATETIME, recurring BOOL, frequency INTEGER)"
    cur.execute(query)

def add_reminder(cur, desc, time):
    if time == 0:
        print("Error! Can't insert 0 into time")
        return
    query = f"INSERT INTO reminders (eventdesc, eventtime, recurring, frequency) VALUES ('{desc}', datetime({time}, 'unixepoch'), false, 0)"
    cur.execute(query)

def parse_time_from_str(time):
    time = time.lower()
    parsedtime = timemodule.time()
    # relative date parsing using heuristics
    # TODO: support fractional hours/days and round to nearest minute for safety
    #if "later" in time or "from now" in time:
    if True:
        amt = 0
        if "day" in time:
            amt = int(time.split("day")[0]) * 86400
        elif "hour" in time:
            amt = int(time.split("hour")[0]) * 3600
        elif "minute" in time:
            amt = int(time.split("minute")[0]) * 60
        parsedtime += amt
    # absolute date, we must parse raw date given
    # TODO: actually implement this
    else:
        datetuple = timemodule.strptime(time, "%d/%m/%y")
        unixtimestamp = int(timemodule.mktime(datetuple))
        isfuture = unixtimestamp > parsedtime
        if isfuture:
            parsedtime = unixtimestamp
        else:
            print("Past value entered!")
            parsedtime = 0
    return parsedtime

def print_time_from_seconds(relativetime):
    days = 0
    hours = 0
    minutes = 0
    if relativetime > 86400:
        days += (relativetime // 86400)
        relativetime = relativetime % 86400
    if relativetime > 3600:
        hours += (relativetime // 3600)
        relativetime = relativetime % 3600
    if relativetime > 60:
        minutes += (relativetime // 60)
    pretty_time = ""
    if days:
        pretty_time += f"{days} day(s), "
    if hours:
        pretty_time += f"{hours} hour(s), "
    if minutes:
        pretty_time += f"{minutes} minute(s)"
    return pretty_time

def print_upcoming_events(cur):
    res = cur.execute("SELECT eventdesc, strftime('%s', eventtime) FROM reminders ORDER BY eventtime").fetchall()
    for i in res:
        unixtime = int(i[1])
        relativetime = unixtime - timemodule.time()
        pretty_time = print_time_from_seconds(relativetime)
        print(f"Event: {i[0]}, to be triggered within {pretty_time}")

desc = input("Enter event details: ")
time = input("Enter when to remind you:")

con = sqlite3.connect("reminders.db")
cur = con.cursor()

create_table_if_needed(cur)
if desc and time:
    parsedtime = parse_time_from_str(time)
    add_reminder(cur, desc, parsedtime)
    con.commit()

print_upcoming_events(cur)
