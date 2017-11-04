import time

Old_time = time.time()
#print Old_time
for i in range(1, 1000):
    continue

New_time = time.time()
#print New_time
total = New_time - Old_time
print total
