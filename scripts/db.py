import mysql.connector as mariadb
import sys

class DroneDB:
    
    def __init__(self):
        self.start_conn()

    def start_conn(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="dandan",
                host="127.0.0.1",
                port=3306,
                database="dronedb"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit()

        self.cur = self.conn.cursor()

    def add_plate(self, number, horizontalAngle, verticalAngle, distance, isVisible):
        self.cur.execute(f"INSERT INTO targets (number,horizontalAngle,verticalAngle,distance,isVisible) VALUES ('{number}', {horizontalAngle}, {verticalAngle}, {distance}, {isVisible});")

    def check_plate(self, number):
        self.cur.execute(f"SELECT * FROM targets WHERE number='{number}';")
        rows = self.cur.fetchall()
        return rows

    def delete_plate(self, number):
        self.cur.execute(f"DELETE FROM targets WHERE number='{number}';")

    def update_plate(self, number, column, value):
        self.cur.execute(f"UPDATE targets SET {column}={value} WHERE number='{number}';")

    def update_plates(self, column, value):
        self.cur.execute(f"UPDATE targets SET {column}={value};")

    def clear_table(self):
        self.cur.execute("DELETE FROM targets;")
        self.cur.execute("ALTER TABLE targets AUTO_INCREMENT = 1")

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()