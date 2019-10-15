from tinydb import Table, TinyDB

from conf import ETC_DIR

db = TinyDB("{ETC_DIR}/db/firewall")

offenders: Table = db.table("Offenders")
banned_output: Table = db.table("BannedOutput")
banned_input: Table = db.table("BannedInput")
offenders.insert()
