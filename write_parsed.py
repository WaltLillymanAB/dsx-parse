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
interest_items='interest_items'

# Load the dictionary from a .pkl file created by dsx-parse.py
print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Loading pickle file into a dictionary.')
with open(pickle_file, 'rb') as f:
  d = pickle.load(f)

crlf='[\r\n]'  # Carriage-return and line-feed pattern to replace.
nl=' '         # Replacement text for embedded CR+LF.

# StageTypes of interest:
stage_types_desired=['CODBCSTAGE','ODBCCONNECTOR','ODBCCONNECTORPX','ORACLECONNECTOR','ORACLECONNECTORPX','ORAOCI9','PXODBC','PXORACLE']

# Counters:
j_cnt=0; r_cnt=0; s_cnt=0

# Keep track of current position:
job=''; record=''; subrecord=''

file_name = strftime("%Y%m%d_%H%M%S")+'_'+parsed_file

# Capture items of interest to a file:
with open(interest_items+'_'+strftime("%Y%m%d_%H%M%S")+'.txt', mode='w', encoding="utf-8") as f:
  # Print header record:
  f.write('DSX Project\tJob #\tJob name\tRecord #\tOLEType\tRecord Name\tRecord Category\tInputPins\tStageType\tSubrecord #\tSubrecord Name\tSubrecord Value\n')

  # Reset vars that will save contents of items of interest for writing each line to a file per record/subrecord.:
  identifier=''; rec_oletype=''; rec_name=''; rec_category=''; rec_inputpins=''; rec_stagetype=''; subrec_name=''; subrec_value=''; is_usersql=False; wrote_record=False

  print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Parsing dictionary contents.')
  # There's one header per DSX project file. Get the header attribute for this DSX project name:
  i = d.properties.get('header')
  for j in ['toolinstanceid']:
    t = re.sub(crlf, nl, i.get(j))  # Replace cr+lf
    project = t

  # There's many "job" records per project file. Get some "job" attributes:
  for i in d.properties.get('jobs'):
    j_cnt += 1
    print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Job {j_cnt}...')
    job = str(j_cnt)
    for j in ['identifier']: 
      t = re.sub(crlf, nl, i[j]) 
      identifier = t

    # There's many "records" per job. Get some "records" attributes:
    for j in i.get('records'): 
      r_cnt += 1
      record = r_cnt
      # print(f'{strftime("%Y-%m-%d %H:%M:%S")}  #{getframeinfo(currentframe()).lineno}: Job {j_cnt}, record {r_cnt}...')
      for k in ['oletype','name','category','inputpins','stagetype']:
        if j.get(k) is not None:  # j.get('oletype')
          t = re.sub(crlf, nl, j.get(k))
          if k=='oletype': rec_oletype=t
          if k=='name': rec_name=t
          if k=='category': rec_category=t
          if k=='inputpins': rec_inputpins=t
          if k=='stagetype': rec_stagetype=t
      # Keep inputpins & stagetype only for desired stagetypes:
      if rec_stagetype not in stage_types_desired:
        rec_inputpins=''
        rec_stagetype=''
      
      # There's many "subrecords" per record.
      for m in j.get('subrecords'):  # For each dict in the list.
        s_cnt += 1
        subrecord = s_cnt
        for p in m:  # For each key in the dict.
          t = re.sub(crlf, nl, m.get(p))
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
          f.write(project+'\t'+str(job)+'\t'+identifier+'\t'+str(record)+'\t'+rec_oletype+'\t'+rec_name+'\t'+rec_category+'\t'+rec_inputpins+'\t'+rec_stagetype+'\t'+str(subrecord)+'\t'+subrec_name+'\t'+subrec_value+'\n')  # Header record
          wrote_record=True
          subrec_name=''; subrec_value=''
      s_cnt=0

    # At the end of each job record:
    if not wrote_record:
      f.write(project+'\t'+str(job)+'\t'+identifier+'\t'+str(record)+'\t'+rec_oletype+'\t'+rec_name+'\t'+rec_category+'\t'+rec_inputpins+'\t'+rec_stagetype+'\t'+str(subrecord)+'\t'+subrec_name+'\t'+subrec_value+'\n')  # Header record
      wrote_record=False
    # Reset vars:
    identifier=''; rec_oletype=''; rec_name=''; rec_category=''; rec_inputpins=''; rec_stagetype=''; subrec_name=''; subrec_value=''; is_usersql=False; wrote_record=False
    r_cnt=0

    # While debugging, use many fewer rows:
    if j_cnt==5:
      break