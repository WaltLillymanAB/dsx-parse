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

# Examine value of key, d.properties['jobs'] :
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(type(d.properties['jobs'])) # d.properties is a dict, d.properties['jobs'] is a list.
# How many items are in the list?
print(len(d.properties['jobs'])) # 2881, same as the count of BEGIN DSJOB.

# What is the type of the first item in the list?
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(type(d.properties['jobs'][0])) # d.properties is a dict, d.properties['jobs'] is a list, and d.properties['jobs'][0] is a dict.

# How many keys are in the dict, and what are their names?
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(len(d.properties['jobs'][0])) # 48 keys. 
print(d.properties['jobs'][0].keys())
# The key, raw, has all the text. The other keys break out the stuff in raw, I think.
# There are 2881 DSJOBs represented in d.properties['jobs']). 
# In the first DSJOB, there are 48 keys, including raw, (so maybe 47 things from the dsx file.)
# The keys of interest include identifier, oletype, name, description, jobtype. Maybe others are complex, like subrecords ?

# From the first and second items in the list, get these keys' string values:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.properties['jobs'][0]['identifier'], d.properties['jobs'][0]['oletype'], d.properties['jobs'][0]['name'])
print(d.properties['jobs'][1]['identifier'], d.properties['jobs'][1]['oletype'], d.properties['jobs'][1]['name'])

# What's the type of subrecords?
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(type(d.properties['jobs'][0]['subrecords'])) # List

# Get the type of each thing in the 48 things:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
for i in d.properties['jobs'][0]:
  print(i, type(d.properties['jobs'][0][i])) # subrecords is a list, all others are str.

# Get the count of items in the subrecords list:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(len(d.properties['jobs'][0]['subrecords'])) # 23 items in the subrecords list.

# Dump that list:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.properties['jobs'][0]['subrecords']) # Looks like dicts are in that list.

# Get the type of each item in the list:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
for i in d.properties['jobs'][0]['subrecords']:
  print(type(i)) # Every item in the list is a dict.

# Get the key & value for each item in the dict:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
for i in d.properties['jobs'][0]['subrecords']:
  print()
  for j in i:
    print(f'{j}={i[j]}')
