from itertools import count


for attempt in count(1, 2):
    print(attempt)
    if attempt > 10:
        break
