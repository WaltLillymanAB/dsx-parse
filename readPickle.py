import sys
import re
import dill as pickle
from inspect import currentframe, getframeinfo
import pprint
pp = pprint.PrettyPrinter(indent=4)

project_file='EDW_DW1_PROD'
pickle_file=project_file + '.pkl'
pretty_file=project_file + '_pp.txt'
parsed_file=project_file + '_parsed.txt'

# Now to access objects' properties:
# Load the dictionary from a .pkl file created by dsx-parse.py
with open(pickle_file, 'rb') as f:
  d = pickle.load(f)

# Write to file in pretty format for comparison:
# with open(pretty_file, 'w') as out:
#     PP = pprint.PrettyPrinter(indent=4, width=254, sort_dicts=False, stream=out)
#     PP.pprint(d.properties['jobs'])

# From the top, get the type of each thing, and the types of the thing's nested things, etc., till no more unknown nested things.
# Get type of object, d:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(type(d)) # '__main__.DSX'
# It's a class. Get directory of items in d:
pp.pprint(d.__dir__()) # A list of items, incl. jobs, properties, header, 
  # search_types, which is a list of ["JOB", "STAGE", "LINK", "STRING", "PARAMETER"]
  # See in dsx-parse's code, jobs gets an appendsion of each BEGIN_DSJOB, #687
  # records gets an appendsion of each BEGIN_DSRECORD, #711
  # subrecords gets an appendsion of each BEGIN DSSUBRECORD, #755

# Get types of items of interest in object:
print(type(d.jobs)) # 'map'
print(type(d.properties)) # 'dict'
print(type(d.header)) # 'dict'

print() # Get counts:
print(len(d.jobs.__dir__())) # 25  # jobs is a map
print(len(d.properties)) # 2  # d.properties is a dict containing 2 keys.
print(len(d.header)) # 11  # header is a dict containing 11 keys.

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
  print(type(i)) # Every item in the subrecords list is a dict.

# Get the type for every value in the dict:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
for i in d.properties['jobs'][0]['subrecords']:
  print()
  for j in i:
    print(f'{j} type is {type(i[j])}')  # Each key's value is a string, no nested.

# Get the key & value for each item in the dict:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
for i in d.properties['jobs'][0]['subrecords']:
  print()
  for j in i:
    print(f'{j}={i[j]}')

# An example of the lowest level thing:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.properties['jobs'][0]['subrecords'][0]['default']) # $PROJDEF
print(d.properties['jobs'][0]['subrecords'][8]['default']) # firecall_331926

# Dictionaries: Use "get()" to prevent raising KeyError:  dict.get(key, default)
print(f'\n### {getframeinfo(currentframe()).lineno}:')
print(d.properties.get('jobs','Nada')[0].get('subrecords','Nada')[8].get('default','Nada')) # firecall_331926

# Dynamically get each dicts keys' names:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
for i in d.properties.get('jobs')[0].get('subrecords'):
  print()
  for j in i:
    print(f'{j}={i[j]}')

# Accumulate output into a string, field-delimited with tie fighter: |-O-|
# Replace embedded carriage-returns and line-feeds with '#nl '
# One row per job, really, really wide, with no column headings, column names will prefix values for now:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
s=''           # String to accumulate result.
fd='|-O-|'     # Field delimiter in output.
crlf='[\r\n]'  # Carriage-return and line-feed pattern to replce.
nl='#nl '      # Replacement text for embedded CR & LF.

# Header contents in the first columns:
for i in d.properties.get('header'):
  s += i + fd  # The key
  t = re.sub(crlf, nl, d.properties.get('header').get(i))
  s += t + fd  # The value

# Job records will be next set of columns.
# Exclude the keys, raw and subrecords. Raw will not be parsed. Subrecords is a list so it will be parsed, below.
# Exclude verbose multi-line fields, for now. To include them, will need to replace \n.
for i in d.properties.get('jobs'):
  for j in i:
    if j != 'raw' and j != 'subrecords' and j != 'description' and j != 'fulldescription' and j != 'jobcontrolcode' and j != 'orchestratecode':
      s += j + fd
      i[j] = re.sub(crlf, nl, i[j])
      s += i[j] + fd
    elif j == 'subrecords':  # It's a list of dicts.
      for n in i[j]:  # For each dict in the list.
        for p in n:  # For each key in the dict.
          s += p + fd  # The key
          t = re.sub(crlf, nl, n.get(p))
          s += t + fd  # The value
  s+='\n'

# Write that string to a file.
with open(parsed_file, 'wb') as out:
  out.write(s.encode('ascii'))


# 2023-09-09 16:59:12
# To do:
# Get rid of newlines in output.
# Desired stage types aren't showing up, but are in pretty print.
# whittle down the unneeded columns.