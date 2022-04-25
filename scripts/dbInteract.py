import mysql.connector as mariadb
import sys
import os


username = os.environ.get("username")
password = os.environ.get("password")

def start_conn():

    try:
        conn = mariadb.connect(
            user="root",
            password="dandan",
            host="127.0.0.1",
            port=3306,
            database="dronedb"
        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit()

    cur = conn.cursor()
    return cur, conn

def add_plate(cur, number, horizontalAngle, verticalAngle, distance, isVisible):
    cur.execute(f"INSERT INTO targets (number,horizontalAngle,verticalAngle,distance,isVisible) VALUES ('{number}', {horizontalAngle}, {verticalAngle}, {distance}, {isVisible});")

def check_plate(cur, number):
    cur.execute(f"SELECT * FROM targets WHERE number='{number}';")
    rows = cur.fetchall()
    return rows

def delete_plate(cur, number):
    cur.execute(f"DELETE FROM targets WHERE number='{number}';")

def update_plate(cur, number, column, value):
    cur.execute(f"UPDATE targets SET {column}={value} WHERE number='{number}';")

def update_plates(cur, column, value):
    cur.execute(f"UPDATE targets SET {column}={value};")

def clear_table(cur):
    cur.execute("DELETE FROM targets;")
    cur.execute("ALTER TABLE targets AUTO_INCREMENT = 1")

def commit(conn):
    conn.commit()

def close(conn):
    conn.close()