import mysql.connector
#資料庫連接
def get_db_connection():
    return mysql.connector.connect(
        host="your host ip",
        user="mysql user",
        password="your mysql password",
        database="DoorSecurity_demo",#Database name
        port="13306"
    )
