import mysql.connector as mysql
def dbConnect_new(sqlCommand,params1):
    db = mysql.connect(
    host = 'your host ip',
    user = "mysql user",
    passwd = "mysql password",
    database = "DoorSecurity_demo",#Database Name
    port = "13306"
    )
    ConnectDB = db.cursor()
    ConnectDB.execute(sqlCommand,params1)
    ConnectDB_result = ConnectDB.fetchall()
    return ConnectDB_result
