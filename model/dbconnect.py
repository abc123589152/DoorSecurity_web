import mysql.connector
#資料庫連接
def get_db_connection():
    return mysql.connector.connect(
        host="172.16.1.186",
        user="root",
        password="1qaz@WSX",
        database="DoorSecurity",
        port="13306"
    )