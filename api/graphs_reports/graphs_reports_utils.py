from config.config import Config
import fdb

def get_db_connection(line):
    if line in (1, 2, 3, 4):
        db_info = Config.DB_LINE_1_4
    elif line == 5:
        db_info = Config.DB_LINE_5
    elif line == 6:
        db_info = Config.DB_LINE_6
    elif line == 7:
        db_info = Config.DB_LINE_7
    else:
        raise ValueError(f"Unknown line: {line}")

    return fdb.connect(
        dsn=f"{db_info['host']}/3050:{db_info['database']}",
        user=db_info['user'],
        password=db_info['password']
    )



COLOR_PALETTE = [
    "#f87171", "#fdba74", "#bef264", "#86efac", "#93c5fd",
    "#a5b4fc", "#c4b5fd", "#fda4af", "#7c3aed", "#be185d"
]

