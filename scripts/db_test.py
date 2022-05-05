from db import DroneDB

db = DroneDB()
db.update_plate("P19 SND", "isVisible", 1)

g = input()

db.delete_plate("P19 SND")

g = input()

db.clear_table()

g = input()

ret = db.check_plate("H9J 3P3")
print(ret)
db.close()