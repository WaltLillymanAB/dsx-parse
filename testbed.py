from time import strftime
from inspect import currentframe, getframeinfo

# print(f'\n{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Loading pickle file into a dictionary.')
# print(strftime("%Y-%m-%d %H:%M:%S"))

interest_items='interest_items.txt'
with open(interest_items, mode='w', encoding="utf-8") as f:
  f.write('Project\tJob\tRecord\tSubrecord\n')
  f.write('testproj\ttestob\ttestrecord\ttestsubrecord\n')
