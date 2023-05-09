import sqlite3
import time as timemodule

def createtable(cur):
    query = "CREATE TABLE IF NOT EXISTS reminders(id INTEGER PRIMARY KEY, eventdesc VARCHAR, eventtime DATETIME, recurring BOOL, frequency INTEGER)"
    cur.execute(query)

def createreminder(cur, desc, time):
    if time == 0:
        print("Error! Can't insert 0 into time")
        return
    query = f"INSERT INTO reminders (eventdesc, eventtime, recurring, frequency) VALUES ('{desc}', datetime({time}, 'unixepoch', false, 0))"
    cur.execute(query)

def parsetime(time):
    time = time.lower()
    parsedtime = timemodule.time()
    # relative date parsing using heuristics
    # TODO: support fractional hours/days and round to nearest minute for safety
    if "later" in time or "from now" in time:
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

desc = input("Enter event details: ")
print("Enter when to remind you")
time = input("(Hint- write 4 hours later or just a date like 13/4/23): ")

con = sqlite3.connect("reminders.db")
cur = con.cursor()

createtable(cur)
parsedtime = parsetime(time)
createreminder(cur, desc, parsedtime)
con.commit()

res = cur.execute("SELECT * FROM reminders ORDER BY eventtime").fetchall()
for i in res:
    print(i)
