import dill as pickle
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Now to access objects' properties:
# Load the dictionary from a .pkl file created by dsx-parse.py
with open('EDW_DW1_PROD.pkl', 'rb') as f:
  d = pickle.load(f)

# Print the contents of a node.
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
# pp.pprint(d.properties['jobs'][0]['records'][0]['subrecords'][8])
# print(d.properties['jobs'][0]['subrecords'][0]) # KeyError: 'records'
# print(d.properties['jobs'][0]['subrecords'][0]['identifier']) # KeyError: 'records'
# print(d.properties['jobs'][0][0][0]['identifier']) # KeyError: 'records'
# print(d.properties['jobs'][3]['records'][3]['fulldescription']) # KeyError: 'records'
print(d.properties['jobs'][3]['subrecords'][2]['default']) # /etl/dev/mss/budnet/data/vip/hash
print()
pp.pprint(d.properties['jobs'][3]['subrecords'][2]) # all elements which appears to be a dict.
print()
for i in d.properties['jobs'][3]['subrecords'][2]:
  pp.pprint(i)
print()

# Write to file in pretty format:
# with open('pickle.txt', 'w+') as out:
#     PP = pprint.PrettyPrinter(indent=4,stream=out)
#     PP.pprint(d.properties['jobs'])