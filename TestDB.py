import db 
import sqlite3 as sql

connection = sql.connect("database.db")
cursor = connection.cursor()
db.createTables(cursor)

# Insert data into the tbl_Accounts table
data = (2, "adminn", "adminn")
db.insertToAccountsTable(connection, cursor, data)

allRows = db.getAllRows(cursor, "tbl_Accounts")
print(allRows)
