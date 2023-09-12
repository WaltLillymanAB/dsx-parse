from time import strftime
from inspect import currentframe, getframeinfo

print(f'\n{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Loading pickle file into a dictionary.')


print(strftime("%Y-%m-%d %H:%M:%S"))