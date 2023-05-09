import sqlite3


def createtable(cur):
    query = "CREATE TABLE IF NOT EXISTS reminders(id INTEGER PRIMARY KEY, eventdesc VARCHAR, eventtime DATETIME)"
    cur.execute(query)

def createreminder(cur, desc, time):
    query = f"INSERT INTO reminders (eventdesc, eventtime) VALUES ('{desc}', datetime(strftime('%s', 'now') + {time}, 'unixepoch'))"
    cur.execute(query)

def parsetime(time):
    time = time.lower()
    amt = 0
    # relative date parsing
    # TODO: support fractional hours/days and round to nearest minute for safety
    if "day" in time:
        amt = int(time.split("day")[0]) * 86400
    elif "hour" in time:
        amt = int(time.split("hour")[0]) * 3600
    elif "minute" in time:
        amt = int(time.split("minute")[0]) * 60
    return amt

desc = input("Enter event details: ")
time = input("Enter when to remind you: ")

con = sqlite3.connect("reminders.db")
cur = con.cursor()

createtable(cur)
reltime = parsetime(time)
createreminder(cur, desc, reltime)
con.commit()

res = cur.execute("SELECT * FROM reminders").fetchall()
for i in res:
    print(i)
