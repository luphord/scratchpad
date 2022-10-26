from datetime import datetime
import time
import sqlite3
import json

c = sqlite3.connect("database.db")
with open("database_setup.sql", "r") as f:
    c.executescript(f.read())
c.commit()

def save(object_id, view, data):
    c.execute("insert into objects values (?, ?, ?, ?);", (object_id, int(time.time() * 1000), view, json.dumps(data)))

def get_latest(object_id):
    return c.execute("select * from objects where object_id=? order by version desc;", (object_id,)).fetchone()

if __name__ == "__main__":
    print(get_latest(3))

    for i in range(10):
        save(i, "test_view", dict(a=i, b=str(datetime.now())))

    print(get_latest(3))

    c.commit()