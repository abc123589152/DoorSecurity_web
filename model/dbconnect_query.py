import mysql.connector as mysql
def dbConnect_query(sqlCommand,params1):
    db = mysql.connect(
    host = '172.16.1.186',
    user = "root",
    passwd = "1qaz@WSX",
    database = "DoorSecurity",
    port = "13306"
    )
    ConnectDB = db.cursor()
    ConnectDB.execute(sqlCommand,params1)
    db.commit()
    