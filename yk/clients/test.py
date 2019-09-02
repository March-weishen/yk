# s = "nihao    免费"
# s.rsplit(" ")
import time
r1 = time.time()
r2 = time.localtime(r1)
r4 = time.strftime("%Y-%m-%d %H:%M:%S",r2)
r3 = time.strftime("%Y-%m-%d %H:%M:%S")
print(type(r3))


