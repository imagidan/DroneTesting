from dbInteract import *

cur, conn = start_conn()

g = input()

add_plate(cur, conn, "P19 SND", 4.32, 32.3, 32.44, 0)
add_plate(cur, conn, "H9J 3P3", 5.32, 32.33, 45, 1)

g = input()

update_plate(cur, conn, "P19 SND", "isVisible", 1)

g = input()

delete_plate(cur, conn, "P19 SND")

g = input()

clear_table(cur, conn)

g = input()

ret = check_plate(cur, conn, "H9J 3P3")
print(ret)
close(conn)