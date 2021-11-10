from datetime import  datetime

time_now = datetime.now().time()

breakfast_begin = time_now.replace(hour=0, minute=1, second=0, microsecond=0)
breakfast_end = time_now.replace(hour=13, minute=0, second=0, microsecond=0)
lunch_begin = time_now.replace(hour=13, minute=0, second=0, microsecond=0)
lunch_end = time_now.replace(hour=17, minute=30, second=0, microsecond=0)
dinner_begin = time_now.replace(hour=17, minute=30, second=0, microsecond=0)
dinner_end = time_now.replace(hour=23, minute=59, second=0, microsecond=0)

current_times = [breakfast_begin, breakfast_end, lunch_begin, lunch_end, dinner_begin, dinner_end]
