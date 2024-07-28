import mysql.connector as mysql
def dbConnect_query(sqlCommand,params1):
    db = mysql.connect(
    host = 'your host ip',
    user = "mysql user",
    passwd = "mysql password",
    database = "DoorSecurity_demo",#Database Name
    port = "13306"
    )
    ConnectDB = db.cursor()
    ConnectDB.execute(sqlCommand,params1)
    db.commit()
    db.close()
    
