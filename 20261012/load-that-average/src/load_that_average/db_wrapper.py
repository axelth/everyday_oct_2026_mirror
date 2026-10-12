import sqlite3
import time

class DbWriter:
    mode_str = "mode=rwc"
    uri = ""
    db = None

    def __init__(self, db_path):
        self.uri = f"file:{db_path}?{self.mode_str}"
        self.db = sqlite3.connect(self.uri, uri=True)
        self.ensure_db_initialized()
        
    def ensure_db_initialized(self):
        load_averages_exists = self.db.execute(
            "SELECT EXISTS(SELECT 1 FROM sqlite_schema WHERE type='table' AND name='load_averagesb')"
        ).fetchone()[0]
        if load_averages_exists == 0:
            self.create_load_averages_table()
    
    def create_load_averages_table(self):
        self.db.execute("""CREATE TABLE load_averages(
  id INTEGER PRIMARY KEY,
  timestamp INTEGER NOT NULL,
  one_min REAL NOT NULL,
  five_min REAL NOT NULL,
  fifteen_min REAL NOT NULL
);
""")

    def store_load_average(self, one_min: float, five_min: float, fifteen_min: float):
        timestamp = int(time.time())

        self.db.execute("""INSERT INTO load_averages
                        (timestamp, one_min, five_min, fifteen_min)
                        VALUES (:timestamp, :one, :five, :fifteen)""",
                   {"timestamp": timestamp, "one": one_min,
                    "five": five_min, "fifteen": fifteen_min})
        self.db.commit()



class DbReader:
    mode_str = "mode=ro"
    uri = ""
    db = None

    def __init__(self, db_path):
        self.uri = f"file:{db_path}?{self.mode_str}"
        self.db = sqlite3.connect(self.uri, uri=True)

    def get_latest_load_averages(self, limit: int = 30) -> tuple[tuple[int, float, float, float]]:
        return (self.db.execute("SELECT timestamp, one_min, five_min, fifteen_min from load_averages LIMIT :limit", {"limit": limit})
                .fetchall())
                  

        
        
        
