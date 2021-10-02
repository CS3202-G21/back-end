from datetime import  datetime

time_now = datetime.now().time()

breakfast_begin = time_now.replace(hour=6, minute=0, second=0, microsecond=0)
breakfast_end = time_now.replace(hour=10, minute=30, second=0, microsecond=0)
lunch_begin = time_now.replace(hour=12, minute=0, second=0, microsecond=0)
lunch_end = time_now.replace(hour=15, minute=30, second=0, microsecond=0)
dinner_begin = time_now.replace(hour=19, minute=30, second=0, microsecond=0)
dinner_end = time_now.replace(hour=22, minute=30, second=0, microsecond=0)

current_times = [breakfast_begin, breakfast_end, lunch_begin, lunch_end, dinner_begin, dinner_end]