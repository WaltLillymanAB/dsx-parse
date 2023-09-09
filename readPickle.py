import dill as pickle
from inspect import currentframe, getframeinfo
import pprint
pp = pprint.PrettyPrinter(indent=4)

project_file='EDW_DW1_PROD'
pickle_file=project_file + '.pkl'
pretty_file=project_file + '_pp.txt'

# Now to access objects' properties:
# Load the dictionary from a .pkl file created by dsx-parse.py
with open(pickle_file, 'rb') as f:
  d = pickle.load(f)

# Print the contents of a node.
print(f'\n### {getframeinfo(currentframe()).lineno}:')
pp.pprint(f"d.properties['header']['toolinstanceid'] = {d.properties['header']['toolinstanceid']}") # EDW_DW1_PROD
# pp.pprint(d.properties['jobs']) # Prints ALL the jobs & details, too much.

'''
d: DSX object instance
 properties: dict
  jobs: list
   0, 1, 2: dict
    name: str
'''

# for prop in d.properties:
  # pprint(prop) # TypeError: 'module' object is not callable

# for key,val in d.properties:
#   for i in val:
#     pp.pprint(f"{key} : {i}")  # ValueError: too many values to unpack (expected 2)

# print(d.properties['jobs']) # 1
# print(d.get('header', 'unknown'))
# d is a DSX object, which doesn't have "get()"
# DSX object is a list.

# print(f'print_node(head) at Line {getframeinfo(currentframe()).lineno}') # 
# pp.pprint(d.properties['jobs'][0]['records'][0]['subrecords'][0]) # KeyError: 'records'
# pp.pprint(d.properties['jobs'][0]['records'][0]['subrecords'][8])
# print(d.properties['jobs'][0]['subrecords'][0]) # KeyError: 'records'
# print(d.properties['jobs'][0]['subrecords'][0]['identifier']) # KeyError: 'records'
# print(d.properties['jobs'][0][0][0]['identifier']) # KeyError: 'records'
# print(d.properties['jobs'][3]['records'][3]['fulldescription']) # KeyError: 'records'
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.properties['jobs'][3]['subrecords'][2]['default']) # /etl/dev/mss/budnet/data/vip/hash
print()
pp.pprint(d.properties['jobs'][3]['subrecords'][2]) # all elements which appears to be a dict.
print()
for i in d.properties['jobs'][3]['subrecords'][2]:
  pp.pprint(i)
print()

# Write to file in pretty format:
# with open(pretty_file, 'w') as out:
#     PP = pprint.PrettyPrinter(indent=4, width=254, sort_dicts=False, stream=out)
#     PP.pprint(d.properties['jobs'])

# Get type of object, d:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(type(d)) # '__main__.DSX'
# It's a class. Get directory of items in d:
pp.pprint(d.__dir__()) # A list of items, incl. jobs, properties, header, 
  # search_types, which is a list of ["JOB", "STAGE", "LINK", "STRING", "PARAMETER"]
  # See in code, jobs gets an appendsion of each BEGIN_DSJOB, # 687
  # records gets an appendsion of each BEGIN_DSRECORD, # 711
  # subrecords gets an appendsion of each BEGIN DSSUBRECORD, #755
# Get types of items of interest in object:
print(type(d.jobs)) # 'map'
print(type(d.properties)) # 'dict'
print(type(d.header)) # 'dict'

print() # Get counts:
print(len(d.jobs.__dir__())) # 25
print(len(d.properties)) # 2
print(len(d.header)) # 11

# Get names of top-level things:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.jobs.__dir__()) # A list of 25 "__" methods, nothing of interest? d.jobs has only special variables, no function variables, no properties. Maybe jobs are in d.properties.jobs?
print(d.properties.keys()) # ['jobs', 'header']
print(d.header.keys()) # ['begin', 'characterset', 'exportingtool', 'toolversion', 'servername', 'toolinstanceid', 'mdisversion', 'date', 'time', 'serverversion', 'end']

print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(type(d.properties['header'])) # d.properties is a dict, d.properties['header'] is a dict
print(d.properties['header']) # Returns the whole dict.
print(d.properties['header']['servername'], d.properties['header']['toolinstanceid']) # Returns the string values of the keys, servername & toolinstanceid, from the dict, d.properties['header'].

print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(type(d.properties['jobs'])) # d.properties is a dict, d.properties['jobs'] is a list
# How many items are in the list?
print(len(d.properties['jobs'])) # 2881, same as the count of BEGIN DSJOB.

print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.properties['jobs'][0]) # The zeroeth (first) item in the list
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.properties['jobs'][1]) # The second item in the list




print(f'\n### {getframeinfo(currentframe()).lineno}:')
# print(d.properties['jobs'])

# Print things of interest from the header:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.header['servername'], d.header['toolinstanceid'])

# Print things of interest from jobs:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
# print(d.jobs[])

print(type(d.properties['jobs'])) # List


# Get items of interest for this project file:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
# print(d.properties) # A dict with key=jobs, value=one job name with records & subrecords. 
# print()
# print(d.properties['jobs'])
# print()

# parse_dsx() returns a dict that looks like, {"jobs":[]}


# print(f'{len(d.properties[0])}') # Key error
# print(f'{len(d)}') # no len() for DSX
# print(f'{len(d.properties.jobs)}') # 'dict' object has no attribute 'jobs'
# print(d.properties.get('jobs', 'bad')) # Worked. Returns a list of one or more dicts. key='raw'. Name: AAP_HISTY_FastLoadINS
# print(d.properties.jobs.get(0, 'bad')) # 'dict' object has no attribute 'jobs'

