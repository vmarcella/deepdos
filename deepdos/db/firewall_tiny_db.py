from deepdos.conf import ETC_DIR
from tinydb import TinyDB, database

# Create the database/connection to it
db = TinyDB("{ETC_DIR}/db/firewall.json")

# Create all necessary tables
offenders: database.Table = db.table("Offenders")
banned_output: database.Table = db.table("BannedOutput")
banned_input: database.Table = db.table("BannedInput")
