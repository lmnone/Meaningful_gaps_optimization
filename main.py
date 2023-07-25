import json
import pandas as pd
import numpy as np

heart_surgeries_set = {
    "605,1742",
    "57.49",
    "81.51",
    "81.54",
    "Z8108",
    "Z283",
    "Z286 0",
    "44.38",
    "44.97",
    "Z5631",
    "62.19",
    "28.6",
    "21.69",
    "Z2769",
    "82.21",
    "7286",
    "82.01",
    "3540",
    "81.65",
    "78.60"
}

# Replace 'path/to/your/json_file.json' with the actual path to your JSON file
file_path = 'schedule.json'

# Read JSON data from the file
with open(file_path, 'r') as file:
    json_data = file.read()

# Parse the JSON data into a Python dictionary
data_dict = json.loads(json_data)

# Create dictionaries for tasks and blocks
task_list = []
blocks_dict = {}

# Iterate over the "tasks" list and group tasks based on "parent_block_id"
for task in data_dict['tasks']:
    parent_block_id = task['parent_block_id']
    procedure_icd = task['procedure_icd']
    task_list.append((parent_block_id, procedure_icd))

# Iterate over the "blocks" list and create a dictionary with block IDs as keys
for block in data_dict['blocks']:
    block_id = block['id']

    assert block_id not in blocks_dict.keys()
    blocks_dict[block_id] = {
        'start': block['start'],
        'end': block['end']
    }

# Print the resulting dictionaries
print("Tasks task_list:")
print(task_list)
print("\nBlocks Dictionary:")
print(blocks_dict)
# Create an empty DataFrame with specified column names
db = pd.DataFrame(index=range(0, len(task_list)), columns=['parent_block_id', 'start', 'end', 'movable'])

# Fill the DataFrame with data from task_list and blocks_dict
for i, (parent_block_id, procedure_icd) in enumerate(task_list):
    db.loc[i, 'parent_block_id'] = parent_block_id
    db.loc[i, 'start'] = blocks_dict[parent_block_id]['start']
    db.loc[i, 'end'] = blocks_dict[parent_block_id]['end']
    db.loc[i, 'movable'] = 1 if procedure_icd not in heart_surgeries_set else 0

# Print the DataFrame
# Convert 'start' and 'end' columns to datetime
db['start'] = pd.to_datetime(db['start'])
db['end'] = pd.to_datetime(db['end'])

# Convert other columns to integers
db[['parent_block_id', 'movable']] = db[['parent_block_id', 'movable']].astype(int)

# Calculate the minimum value in the 'start' column
min_start = db['start'].min()
# Check if the minimum time in the 'start' column is '07:00:00'
assert min_start.time() == pd.to_datetime('07:00:00').time(), "Minimum 'start' time is not '07:00:00'."

# Calculate the time differences in minutes from the minimum start value
db['start15'] = (db['start'] - min_start).dt.total_seconds() // 900
db['end15'] = (db['end'] - min_start).dt.total_seconds() // 900

# Convert the 'start15' and 'end15' columns to integers
db[['start15', 'end15']] = db[['start15', 'end15']].astype(int)

print(db.columns)
print(db.dtypes)
print(db)

task_db = np.array(db[['start15', 'end15', 'movable']].values)
print(task_db)
print(task_db.shape)
