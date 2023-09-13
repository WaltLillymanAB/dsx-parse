# Read the dictionary from the pkl file.
# Store its contents into a very wide string.
# Also parse some items of interest from it and write them to a text file.:
from time import strftime
import re
import dill as pickle
from inspect import currentframe, getframeinfo

project_file='EDW_DW1_PROD'
pickle_file=project_file + '.pkl'
pretty_file=project_file + '_pp.txt'
parsed_file=project_file + '_parsed.txt'
interest_items='interest_items.txt'

# Load the dictionary from a .pkl file created by dsx-parse.py
print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Loading pickle file into a dictionary.')
with open(pickle_file, 'rb') as f:
  d = pickle.load(f)

s=''           # Initialize tring to accumulate result.
fd='¥'         # Field delimiter in output, Alt-0165
crlf='[\r\n]'  # Carriage-return and line-feed pattern to replace.
nl=' '         # Replacement text for embedded CR+LF.

# Counters:
j_cnt=0
r_cnt=0
s_cnt=0

# Keep track of current position:
job=''
record=''
subrecord=''

# Capture items of interest to a file:
with open(interest_items, mode='w', encoding="utf-8") as f:
  # Print output file header record:
  f.write('DSX Project\tJob #\tJob name\tRecord #\tOLEType\tRecord Name\tRecord Category\tSubrecord #\tSubrecord Name\tSubrecord Value\n')

  # Reset vars that will save contents of items of interest for writing each line to a file per record/subrecord.:
  identifier=''; rec_oletype=''; rec_name=''; rec_category=''; subrec_name=''; subrec_value=''; is_usersql=False; wrote_record=False

  print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Parsing dictionary contents.')
  # There's one header per DSX project file. Get some "header" attributes:
  i = d.properties.get('header')
  # for j in ['servername','toolinstanceid']:
  for j in ['toolinstanceid']:
    s += j + fd  # The key
    t = re.sub(crlf, nl, i.get(j))  # Replace cr+lf
    s += t + fd  # The value
    project = t

  # There's many "job" records per project file. Get some "job" attributes:
  for i in d.properties.get('jobs'):
    j_cnt += 1
    print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Job {j_cnt}...')
    job = str(j_cnt)
    s += f'Job' + fd + job + fd
    for j in ['identifier']: 
      s += j + fd  # The key
      t = re.sub(crlf, nl, i[j])  # Replace cr+lf
      s += t + fd  # The value
      identifier = t

    # There's many "records" per job. Get some "records" attributes:
    for j in i.get('records'): 
      r_cnt += 1
      record = r_cnt
      # print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Job {j_cnt}, record {r_cnt}...')
      s += f'Record' + fd + str(r_cnt) + fd 
      for k in ['oletype','name','category']:
        if j.get(k) is not None:  # j.get('oletype')
          s += k + fd
          t = re.sub(crlf, nl, j.get(k))
          s += t + fd
          if k=='oletype': rec_oletype=t
          if k=='name': rec_name=t
          if k=='category': rec_category=t
      
      # There's many "subrecords" per record.
      for m in j.get('subrecords'):  # For each dict in the list.
        s_cnt += 1
        subrecord = s_cnt
        s += f'Subrecord' + fd + str(s_cnt) + fd
        for p in m:  # For each key in the dict.
          s += p + fd
          t = re.sub(crlf, nl, m.get(p))
          s += t + fd
          if p=='tabledef': 
            subrec_name=p
            subrec_value=t
          # Grab SQL:
          if p=='name':
            if t=='USERSQL':
              is_usersql=True
              subrec_name=t
          if p=='value':
              if is_usersql:
                subrec_value=t
                is_usersql=False
        # At the end of each subrecord, if subrec_name was populated, print the row to the file:
        if subrec_name != '':
          f.write(project+'\t'+str(job)+'\t'+identifier+'\t'+str(record)+'\t'+rec_oletype+'\t'+rec_name+'\t'+rec_category+'\t'+str(subrecord)+'\t'+subrec_name+'\t'+subrec_value+'\n')  # Header record
          wrote_record=True
          subrec_name=''; subrec_value=''
      s_cnt=0

    # At the end of each job record:
    if not wrote_record:
      f.write(project+'\t'+str(job)+'\t'+identifier+'\t'+str(record)+'\t'+rec_oletype+'\t'+rec_name+'\t'+rec_category+'\t'+str(subrecord)+'\t'+subrec_name+'\t'+subrec_value+'\n')  # Header record
      wrote_record=False
    # Reset vars:
    identifier=''; rec_oletype=''; rec_name=''; rec_category=''; subrec_name=''; subrec_value=''; is_usersql=False; wrote_record=False
    r_cnt=0
    s+='\n'

    # While debugging, use many fewer rows:
    # if j_cnt==5:
    #   break

exit(0)

# Write the delimited string to a file.
print(f'\n{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Writing parsed text to file.')
file_name = strftime("%Y%m%d_%H%M%S")+'_'+parsed_file
with open(file_name, 'wb') as out:
  out.write(s.encode('utf-8'))