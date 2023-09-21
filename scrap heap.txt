# Cut from real code, research, examples, etc.  
# Not runnable or anything.

#################
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

################
# subrecords...
# NESTED already...
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
    # elif  j == 'subrecords':  # It's a list of dicts.
    #   for n in i[j]:  # For each dict in the list.
    #     for p in n:  # For each key in the dict.
    #       s += p + fd  # The key
    #       t = re.sub(crlf, nl, n.get(p))
    #       s += t + fd  # The value
    elif j != 'raw':  # Exclude raw. All others are lists:
      s += j + fd  # The key
      t = re.sub(crlf, nl, i[j])
      s += t + fd  # The value
  s+='\n'

  ###################
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

# Accumulate output into a string, field-delimited with character, Alt-0165
# Replace embedded carriage-returns and line-feeds with ' '
# One row per job, really, really wide, with no column headings, column names will prefix values for now:
print(f'\n### {getframeinfo(currentframe()).lineno}:')
s=''           # Initialize tring to accumulate result.
fd='¥'         # Field delimiter in output.
crlf='[\r\n]'  # Carriage-return and line-feed pattern to replace.
nl=' '         # Replacement text for embedded CR & LF.

# Header contents in the first columns:
for i in d.properties.get('header'):
  s += i + fd  # The key
  t = re.sub(crlf, nl, d.properties.get('header').get(i))
  s += t + fd  # The value

# ...followed by job and subrecord columns.
for i in d.properties.get('jobs'):
  for j in i:
    # if j != 'raw' and j != 'subrecords' and j != 'description' and j != 'fulldescription' and j != 'jobcontrolcode' and j != 'orchestratecode':
    if j != 'raw' and j != 'subrecords':
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
print(f'\n### {getframeinfo(currentframe()).lineno}:')
with open(parsed_file, 'wb') as out:
  out.write(s.encode('utf-8'))

##################
9/5/2023 10:22:58 AM

d.properties['header']['toolinstanceid']
'EDW_DW1_PROD'

d.properties['jobs'][0]
to
d.properties['jobs'][2880]
(2881 items)

Records:
d.properties['jobs'][0]['records'][0]

Job name:
The first record has identifier=ROOT:
d.properties['jobs'][0]['records'][0]['identifier']
'ROOT'
and oletype=CJobDefn:
d.properties['jobs'][0]['records'][0]['oletype']
'CJobDefn'
Here is the Job Name:
d.properties['jobs'][0]['records'][0]['name']
'AAP_HISTY_FastLoadINS'
And a pair of descriptions, second one appears to be the work log:
d.properties['jobs'][0]['records'][0]['description']
"=+=+=+=EDWSTGPromoFrntln_Prc                                     Wrk Stg processing.                                                  Uses active plans are (stat_cd =  25).   + main frontline table will have prcssd_flg = 'N' \nand RM_Frontline.Prop_Beg_Eff_Dt is null.                                          \n=+=+=+=\n"
d.properties['jobs'][0]['records'][0]['fulldescription']
"=+=+=+=* VC LOGS *\n^1_1 08/14/07 14:15:49 Batch  14471_51358 PROMOTE stldv105 EDW_DW1_PROD zmm2897 migrate to prod\n^1_1 08/14/07 14:14:43 Batch  14471_51290 INIT stlts105 EDW_DW1_TEST zmm2897 move to prod\n^1_1 07/19/07 16:24:09 Batch  14445_59058 PROMOTE stldv105 EDW_DW1_TEST zmm2897 move to test\n^1_1 07/19/07 16:21:07 Batch  14445_58873 INIT stldv105 EDW_DW1_DEV zmm2897 move to test \n^1_5 04/26/07 09:28:04 Batch  14361_34104 INIT stldv105 EDW_DW1_DEV zmm2897 changed PRC_PKG_GRP to Varchar from Char \n^1_4 03/23/07 10:21:41 Batch  14327_37327 INIT stldv105 EDW_DW1_DEV zmm2897 fixed rmr.rm_brand_vers  selection -- using stat_cd = 'A'\n^1_4 03/08/07 17:01:04 Batch  14312_61308 INIT stldv105 EDW_DW1_DEV z900329 Move to Test and then to PROD after making changes to frntln prc for brand vers and new job to handle upserts for frntln prc alchl.\n^1_3 03/08/07 14:39:35 Batch  14312_52779 PROMOTE stldv105 EDW_DW1_DEV z900329 Move to Dev to change the code to join to rm brand vers table.\n^1_3 03/08/07 14:38:27 Batch  14312_52724 INIT stlpr105 EDW_DW1_PROD z900329 Move to Dev to change the code to join to rm brand vers table.\n^1_2 02/28/07 09:35:06 Batch  14304_34509 PROMOTE stldv105 EDW_DW1_PROD z900329 Move to PROD\n^1_2 02/28/07 09:34:27 Batch  14304_34470 INIT stlts105 EDW_DW1_TEST z900329 Move to PROD\n^1_1 02/26/07 10:45:22 Batch  14302_38767 PROMOTE stldv105 EDW_DW1_TEST z900329 Move to TEST after making change to code to prevent getting wrong brand cd's.\n^1_1 02/26/07 10:43:55 Batch  14302_38643 INIT stldv105 EDW_DW1_DEV z900329 Move to TEST.\n^1_3 01/05/07 11:01:30 Batch  14250_39704 INIT stldv105 EDW_DW1_DEV zmm2897 changed the brand_ctgy_id RI  constraint.\n^1_2 12/06/06 08:03:37 Batch  14220_29030 INIT stldv105 EDW_DW1_DEV zm93046 RMR jobs to test\n^1_1 11/14/06 10:24:01 Batch  14198_37477 INIT stldv105 EDW_DW1_DEV z900329 Move to Version Control\n^1_1 05/22/06 11:06:46 Batch  14022_40055 INIT stldv105 EDW_DW1_DEV zm93046 migrate Work Stage jobs for E2 \n^1_12 02/21/06 17:05:58 Batch  13932_61584 INIT stldv105 EDW_DW1_DEV zv96407 02/21/2006 VI Change File Structure\n^1_11 01/10/06 14:05:26 Batch  13890_50783 INIT stldv105 EDW_DW1_DEV zm93046 Changes for Error files BrwyCust  PkgGrp, new PromProv Sync jobs\n^1_10 12/21/05 15:31:02 Batch  13870_55880 INIT stldv105 EDW_DW1_DEV zm93046 Future TSP to all SQL\n^1_9 12/21/05 15:20:07 Batch  13870_55227 INIT stldv105 EDW_DW1_DEV zm93046 added future TSP to all SQL for work stage\n^1_7 12/15/05 17:11:57 Batch  13864_61946 INIT stldv105 EDW_DW1_DEV zm93046 changes for model change - combine qty_lv into Sls_Prd\n^1_5 12/07/05 09:23:26 Batch  13856_33815 INIT stldv105 EDW_DW1_DEV zm93046 migrate to test\n^1_3 12/06/05 08:13:25 Batch  13855_29623 INIT stldv105 EDW_DW1_DEV zm93046 2nd migration to test\n^1_2 12/02/05 16:22:58 Batch  13851_58989 INIT stldv105 EDW_DW1_DEV zm93046 migrate all work stage to test\n^1_1 11/28/05 16:36:01 Batch  13847_59782 INIT stldv105 EDW_DW1_DEV zm93046 Promote to TEST  \n\n\n#Description\n#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\nRelevant Spec\t\t: TSD -  PRICING ELAB\nPupose\t                                : This Job Inserts Data into the Teradata Wrk Stg table Promotions_s.AAP_PROMO_QTY_LVL \nSources\t\t                : TOTAL.PROM,  Promotions.AAP_PROMO_SLS_PRD,  (base) Promotions.AAP_Promo_Qty_Lvl \nTarget Tables\t\t: Promotions_s.AAP_PROMO_QTY_LVL\nReusables\t\t: NA\nAuthor\t\t\t: M.Moore\nDate MM/DD/CCYY)\t: 10/19/2005\n#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\nModification History\nModified by\t\t: Name of Developer\nDate MM/DD/CCYY)\t: 0 \nModification Details\t                :  \nChange Log \t\t: NA\nReference \t\t: NA\n#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n=+=+=+=\n"


Sub records:
d.properties['jobs'][0]['records'][0]['subrecords'][0]
d.properties['jobs'][0]['records'][0]['subrecords'][8]['name']
'EDW_USER'
d.properties['jobs'][0]['records'][0]['subrecords'][8]['default']
'firecall_331926'
d.properties['jobs'][0]['records'][0]['subrecords'][12]['name']
'ETL_DSN'
d.properties['jobs'][0]['records'][0]['subrecords'][12]['prompt']
'Oracle DataSource'
d.properties['jobs'][0]['records'][0]['subrecords'][13]['name']
'ETL_USER'
d.properties['jobs'][0]['records'][0]['subrecords'][13]['prompt']
'Oracle UserName'
d.properties['jobs'][0]['records'][0]['subrecords'][13]['default']
'edw_ro'

Next record, start of "real" steps:
d.properties['jobs'][0]['records'][1]['identifier']
'V0'
d.properties['jobs'][0]['records'][1]['oletype']
'CContainerView'


