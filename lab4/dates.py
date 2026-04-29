# Write a Python program to subtract five days from current date.

import datetime
print(datetime.date.today() - datetime.timedelta(5))


# Write a Python program to print yesterday, today, tomorrow.

import datetime
print(datetime.date.today() - datetime.timedelta(1), datetime.date.today(), datetime.date.today()+ datetime.timedelta(1), end=" ")


# Write a Python program to drop microseconds from datetime.

from datetime import datetime
print(datetime.now().replace(microsecond=0))


# Write a Python program to calculate two date difference in seconds.

import datetime

d1= input()
d2= input()

d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
diff = (d2 - d1).total_seconds()
print(diff)

