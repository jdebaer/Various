import pandas as pd

# Note on chained indexing:
# Don't do: df[df.C <= df.B].loc[:,'B':'E'] -> this is not guaranteed to work, instead do:
# df.loc[df.C <= df.B, 'B':'E'] -> this is faster and will always work. SettingWithCopyWarning is an indication you *might* be doing chained indexing.

# Creating a Series can be done from a list:
school = pd.Series(	['UoU', 'USU'    , 'UvU'  , 'ASU' , 'UoA'  , 'NAU'  , 'UoN' , 'NSU'  , 'UoC'   , 'CSU'])
state_code = pd.Series(	['Uta((', 'Uta))', '((Uta', 'Ari+', 'Ari))', '**Ari', 'Nev-', '*Nev*', '+Col--', '*Col*'])
classes = pd.Series([
    'math chemistry',
    'history math chemistry',
    'chemistry',
    'english math chemistry history',
    'chemistry english math',
    'math',
    'chemistry english math history',
    'english math history',
    'history math chemistry',
    'math english history'
])

# Now put these Series in a List or in a Dict. Dict is nice because you can provide the column names:
series_dict = {'school': school,
                'state_code': state_code,
                'classes': classes}

df = pd.DataFrame(series_dict)

print(df)

# 1) Remove all colleges that have less than 3 classes:

# df['classes'].str.count('\w+') >= 3 -> this becomes a Series object with only the matching rows (and a column containing 'True' for those rows).
df = df[df['classes'].str.count('\w+') >= 3]

print(df)

# 2) Remove all non alphanumeric characters from the state codes:

# Notes on copy vs. view:
# You can test if something is a view with print(df._is_view)

# df = df['state_code']									-> df is a view
# df = df['state_code'].str.replace('[^0-9a-zA-Z]', '', regex = True)			-> df is a copy
# df = df.loc[:, ['state_code']]							-> df is a copy

df['state_code'] = df['state_code'].str.replace('[^0-9a-zA-Z]', '', regex = True)       # This uses a view to create a copy of the column that is then copied in.

print(df)

# 3) Now group on state code and count how many instances of each class there are in the state, with each count having its own column: 

df.drop('school', axis = 1, inplace = True)


df['classes'] = df.groupby(['state_code'])['classes'].transform(lambda x : ' '.join(x))
df = df.drop_duplicates() 

print(df)

df['math'] = df['classes'].str.count('math')
df['history'] = df['classes'].str.count('history')
df['chemistry'] = df['classes'].str.count('chemistry')
df['english'] = df['classes'].str.count('english')

print(df)

df.drop('classes', axis = 1, inplace = True)
df.sort_values(by=['state_code'], inplace = True)

print(df)








