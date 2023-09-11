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

# Load the dictionary from a .pkl file created by dsx-parse.py
print(f'\n### {getframeinfo(currentframe()).lineno}: Loading pickle file into a dictionary.')
with open(pickle_file, 'rb') as f:
  d = pickle.load(f)

''' 
d's type is '__main__.DSX', it's a class, containing jobs, properties, header, 
  search_types, which is a list of ["JOB", "STAGE", "LINK", "STRING", "PARAMETER"]
  See in dsx-parse's code, jobs gets an appendsion of each BEGIN_DSJOB, #687
  records gets an appendsion of each BEGIN_DSRECORD, #711
  subrecords gets an appendsion of each BEGIN DSSUBRECORD, #755

d.header is a dict, 11 keys: 'begin', 'characterset', 'exportingtool', 'toolversion', 'servername', 'toolinstanceid', 'mdisversion', 'date', 'time', 'serverversion', 'end'
d.jobs is a map, 25 items: A list of 25 "__" methods, nothing of interest? d.jobs has only special variables, no function variables, no properties. Maybe jobs are in d.properties.jobs?
d.properties is a dict, 2 keys: 'jobs', 'header'

d.properties['header'] is a dict: d.properties['header']['servername'], d.properties['header']['toolinstanceid']
d.properties['jobs'] is a list. 2881 items, same as the count of BEGIN DSJOB in the DSX file.
d.properties['jobs'][0] is a dict. 48 keys. The key, raw, has all the text. The other keys break out the stuff in raw.

There are 2881 DSJOBs represented in d.properties['jobs']). 
In the first DSJOB, there are 48 keys, including raw, (so maybe 47 things from the dsx file.)
The keys of interest include identifier, oletype, name, description, jobtype. Maybe others are complex, like subrecords ?

Job oletype and job name:
print(d.properties['jobs'][0]['identifier'], d.properties['jobs'][0]['oletype'], d.properties['jobs'][0]['name'])
print(d.properties['jobs'][1]['identifier'], d.properties['jobs'][1]['oletype'], d.properties['jobs'][1]['name'])

d.properties['jobs'][0]['subrecords'] is a list, all of subrecord's neighbors are just strings.
len(d.properties['jobs'][0]['subrecords']) has 23 items. Every item in the subrecords list is a dict. Each key's value is a string, no more nested dicts or lists.

'''
print(f'\n### {getframeinfo(currentframe()).lineno}: Parsing dictionary contents.')
print(type(d.properties.get('jobs')), len(d.properties.get('jobs'))) # is a list, 2881 items long.
# for d in d.properties.get('jobs'): # jobs contains a list of dicts. The first dict in the list is records.
#     # print(d.keys())  # 'records', 'raw', 'identifier', 'datemodified', 'timemodified'  These are the keys for this dict.
#     for i in d:
#         print(i, type(i))


exit(0)

# Accumulate output into a string, field-delimited with character, Alt-0165
# Replace embedded carriage-returns and line-feeds with ' '
# One row per job, really, really wide, with no column headings, column names will prefix values for now:
s=''           # Initialize tring to accumulate result.
fd='¥'         # Field delimiter in output.
crlf='[\r\n]'  # Carriage-return and line-feed pattern to replace.
nl=' '         # Replacement text for embedded CR+LF.

print(f'\n### {getframeinfo(currentframe()).lineno}: Parsing dictionary contents.')
# Header contents in the first columns:
for i in d.properties.get('header'):
  s += i + fd  # The key
  t = re.sub(crlf, nl, d.properties.get('header').get(i))
  s += t + fd  # The value

# ...followed by job and subrecord columns.
for i in d.properties.get('jobs'):
  for j in i:
    if j == 'records':   # It's a list of dicts, incl. subrecords.
        # There are subrecords in records. 
        # So move subrecords saving down to inside here.
        # And save the other stuff in records that isn't already being saved.
      for n in i[j]:  # For each dict in the list.
        for p in n:  # For each key in the dict.
          print(p, type(p))
          if p=='subrecords':
            for q in n:  # For each key in the dict.
                s += q + fd  # The key
                t = re.sub(crlf, nl, n.get(q))   # EXAMINE THIS , this isn't right.
                s += t + fd  # The value
          else:
            s += p + fd  # The key
            t = re.sub(crlf, nl, n.get(p))  # n.get(p) produced a list of dicts to iterate thru...
            s += t + fd  # The value
    elif  j == 'subrecords':  # It's a list of dicts.
      for n in i[j]:  # For each dict in the list.
        for p in n:  # For each key in the dict.
          s += p + fd  # The key
          t = re.sub(crlf, nl, n.get(p))
          s += t + fd  # The value
    elif j != 'raw':  # Exclude raw. All others are lists:
      s += j + fd  # The key
      t = re.sub(crlf, nl, i[j])
      s += t + fd  # The value
  s+='\n'

# Write that string to a file.
print(f'\n### {getframeinfo(currentframe()).lineno}: Writing parsed text to file.')
with open(parsed_file, 'wb') as out:
  out.write(s.encode('utf-8'))