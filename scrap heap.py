# Cut from real code, probably ignore.

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