import mysql.connector as mysql
def dbConnect_noparams(sqlCommand):
    db = mysql.connect(
    host = '172.16.1.186',
    user = "root",
    passwd = "1qaz@WSX",
    database = "DoorSecurity_demo",
    port = "13306"
    )
    ConnectDB = db.cursor()
    ConnectDB.execute(sqlCommand)
    ConnectDB_result = ConnectDB.fetchall()
    return ConnectDB_result