# This reads the string into a dataframe, which I abandoned, currently, in favor of writing directly to the final dest., a csv file.
import pandas as pd

with open('20230912_090504_EDW_DW1_PROD_parsed.txt') as f:
    num_cols = max(len(line.split('¥')) for line in f)  # ;  f.seek(0);  df = pd.read_csv(f, names=range(num_cols)) 

print(num_cols)

df = pd.read_csv('20230912_090504_EDW_DW1_PROD_parsed.txt', sep="¥", names=range(num_cols))

# Creates a massive dataframe which is really slow. Go back and whittle it down to items of interest.  
# display DataFrame
print(df)
