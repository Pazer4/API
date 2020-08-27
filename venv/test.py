import sqlite3
class batch():
    barcode=None
    batchNumber=None
    theoreticalQty=None
    sortMethod=None

data_batch=batch()
data_batch.barcode="12343"
data_batch.batchNumber="art3534"
data_batch.theoreticalQty="2"
data_batch.sortMethod="1"


for i in data_batch:
    print(i)
"""conn = sqlite3.connect('DB.db')
cursor = conn.cursor()
cursor.execute(f"insert into Save values ({data_batch})")
conn.commit()"""