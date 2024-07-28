import mysql.connector as mysql
def dbConnect_noparams(sqlCommand):
    db = mysql.connect(
    host = 'your host ip',
    user = "mysql user",
    passwd = "mysql password",
    database = "DoorSecurity_demo",#DataBase Name
    port = "13306"
    )
    ConnectDB = db.cursor()
    ConnectDB.execute(sqlCommand)
    ConnectDB_result = ConnectDB.fetchall()
    return ConnectDB_result
