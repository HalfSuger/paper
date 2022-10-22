import time
from datetime import datetime
time1 = datetime.now()
print(time.strftime('%H:%M', time.localtime()))
print(type(time.strftime('%H:%M', time.localtime())))

