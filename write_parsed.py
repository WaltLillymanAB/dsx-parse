from time import strftime
import re
import dill as pickle
from inspect import currentframe, getframeinfo
# import pprint
# pp = pprint.PrettyPrinter(indent=4)

project_file='EDW_DW1_PROD'
pickle_file=project_file + '.pkl'
pretty_file=project_file + '_pp.txt'
parsed_file=project_file + '_parsed.txt'

# Load the dictionary from a .pkl file created by dsx-parse.py
print(f'\n{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Loading pickle file into a dictionary.')
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
print(type(d.properties.get('jobs')), len(d.properties.get('jobs'))) # is a list, 2881 items long.

In the first DSJOB, there are 48 keys, including raw, (so maybe 47 things from the dsx file.)
The keys of interest include identifier, oletype, name, description, jobtype. Maybe others are complex, like subrecords ?

Job oletype and job name:
print(d.properties['jobs'][0]['identifier'], d.properties['jobs'][0]['oletype'], d.properties['jobs'][0]['name'])
print(d.properties['jobs'][1]['identifier'], d.properties['jobs'][1]['oletype'], d.properties['jobs'][1]['name'])

d.properties['jobs'][0]['subrecords'] is a list, all of subrecord's neighbors are just strings.
len(d.properties['jobs'][0]['subrecords']) has 23 items. Every item in the subrecords list is a dict. Each key's value is a string, no more nested dicts or lists.

'''
# d->properties->jobs->records->subrecords

# for d in d.properties.get('jobs'): # jobs contains a list of dicts. The first dict in the list is records.
#   print(d.keys())  # 'records', 'raw', 'identifier', 'datemodified', 'timemodified'  These are the keys for this dict.
#   for i in d.keys():

# print(d.properties.get('jobs')[0]('records')[0])
# print(d.properties.get('jobs')[0].get('records')[0]) # WORKS.
# pp.pprint(d.properties.get('jobs')[0].get('records')[0]) # WORKS.
# pp.pprint(d.properties.get('jobs')[0].get('records')[0].get('subrecords')[0]) # WORKS.
# pp.pprint(d.properties.get('jobs')[0].get('records')[0].get('subrecords')[0]) # WORKS
# pp.pprint(d.properties.get('jobs')[0].get('records')[0].get('subrecords')) # WORKS
# pp.pprint(d.properties.get('jobs')[0].get('records')[0].get('subrecords')[4].get('prompt')) # WORKS

# Accumulate output into a string, field-delimited with character, Alt-0165
# Replace embedded carriage-returns and line-feeds with ' '
# One row per job, really, really wide, with no column headings, column names will prefix values for now:

s=''           # Initialize tring to accumulate result.
fd='¥'         # Field delimiter in output, Alt-0165
crlf='[\r\n]'  # Carriage-return and line-feed pattern to replace.
nl=' '         # Replacement text for embedded CR+LF.

print(f'\n{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Parsing dictionary contents.')
# There's one header per DSX project file. Get some "header" attributes:
# i = d.properties.get('header')
# for j in ['servername','toolinstanceid']:
#   s += j + fd  # The key
#   t = re.sub(crlf, nl, i.get(j))  # Replace cr+lf
#   s += t + fd  # The value

# Counters:
j_cnt=0
r_cnt=0
s_cnt=0

# There's many "job" records per project file. Get some "job" attributes:
for i in d.properties.get('jobs'):
  j_cnt += 1
  print(f'\n{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Job {j_cnt}...')
  for j in ['identifier','datemodified']: 
    s += j + fd  # The key
    t = re.sub(crlf, nl, i[j])  # Replace cr+lf
    s += t + fd  # The value

  # There's many "records" per job. Get some "records" attributes:
  for j in i.get('records'): 
    r_cnt += 1
    print(f'\t{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Job {j_cnt}, record {r_cnt}...')
    for k in ['identifier', 'name','oletype','category','parameters']:
      if j.get(k) is not None:
        s += k + fd
        t = re.sub(crlf, nl, j.get(k))
        s += t + fd
    
    # There's many "subrecords" per record.
    for m in j.get('subrecords'):  # For each dict in the list.
      s_cnt += 1
      print(f'\t\t{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Job {j_cnt}, record {r_cnt}, subrecord {s_cnt}...')
      for p in m:  # For each key in the dict.
        s += p + fd
        t = re.sub(crlf, nl, m.get(p))
        s += t + fd

  # At the end of each job record:
  s+='\n'

# Write that string to a file.
print(f'\n{strftime("%Y-%m-%d %H:%M:%S")}  line {getframeinfo(currentframe()).lineno}: Writing parsed text to file.')
with open(parsed_file, 'wb') as out:
  out.write(s.encode('utf-8'))