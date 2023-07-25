import json
import pandas as pd
import numpy as np

from allocator import MeaningfulGapsSolver
from globals import minizinc_dir
from misc_plots import plot_gantt_chart

# heart_surgeries_set = {
#     "605,1742",
#     "57.49",
#     "81.51",
#     "81.54",
#     "Z8108",
#     "Z283",
#     "Z286 0",
#     "44.38",
#     "44.97",
#     "Z5631",
#     "62.19",
#     "28.6",
#     "21.69",
#     "Z2769",
#     "82.21",
#     "7286",
#     "82.01",
#     "3540",
#     "81.65",
#     "78.60"
# }

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
# print("Tasks task_list:")
# print(task_list)
print("\nBlocks Dictionary:")
print(blocks_dict)
# Create an empty DataFrame with specified column names
# db_all_tasks = pd.DataFrame(index=range(0, len(task_list)), columns=['parent_block_id', 'start', 'end', 'movable'])
#
# # Fill the DataFrame with data from task_list and blocks_dict
# for i, (parent_block_id, procedure_icd) in enumerate(task_list):
#     db_all_tasks.loc[i, 'parent_block_id'] = parent_block_id
#     db_all_tasks.loc[i, 'start'] = blocks_dict[parent_block_id]['start']
#     db_all_tasks.loc[i, 'end'] = blocks_dict[parent_block_id]['end']
#     db_all_tasks.loc[i, 'movable'] = 1 if procedure_icd not in heart_surgeries_set else 0
#
# # Print the DataFrame
# # Convert 'start' and 'end' columns to datetime
# db_all_tasks['start'] = pd.to_datetime(db_all_tasks['start'])
# db_all_tasks['end'] = pd.to_datetime(db_all_tasks['end'])
#
# # Convert other columns to integers
# db_all_tasks[['parent_block_id', 'movable']] = db_all_tasks[['parent_block_id', 'movable']].astype(int)
#
# # Calculate the minimum value in the 'start' column
# min_start = db_all_tasks['start'].min()
# # Check if the minimum time in the 'start' column is '07:00:00'
# assert min_start.time() == pd.to_datetime('07:00:00').time(), "Minimum 'start' time is not '07:00:00'."
#
# # Calculate the time differences in minutes from the minimum start value
# db_all_tasks['start15'] = (db_all_tasks['start'] - min_start).dt.total_seconds() // 900
# db_all_tasks['end15'] = (db_all_tasks['end'] - min_start).dt.total_seconds() // 900
#
# # Convert the 'start15' and 'end15' columns to integers
# db_all_tasks[['start15', 'end15']] = db_all_tasks[['start15', 'end15']].astype(int)

## block db
# Convert 'blocks_dict' to a DataFrame
blocks_df = pd.DataFrame.from_dict(blocks_dict, orient='index')
print(blocks_df)

# Print the DataFrame
# Convert 'start' and 'end' columns to datetime
blocks_df['start'] = pd.to_datetime(blocks_df['start'])
blocks_df['end'] = pd.to_datetime(blocks_df['end'])
blocks_df['movable'] = 1

# Convert other columns to integers
blocks_df[['movable']] = blocks_df[['movable']].astype(int)

# Calculate the minimum value in the 'start' column
min_start = blocks_df['start'].min()
# Check if the minimum time in the 'start' column is '07:00:00'
assert min_start.time() == pd.to_datetime('07:00:00').time(), "Minimum 'start' time is not '07:00:00'."

# Calculate the time differences in minutes from the minimum start value
blocks_df['start15'] = (blocks_df['start'] - min_start).dt.total_seconds() // 900
blocks_df['end15'] = (blocks_df['end'] - min_start).dt.total_seconds() // 900

# Convert the 'start15' and 'end15' columns to integers
blocks_df[['start15', 'end15']] = blocks_df[['start15', 'end15']].astype(int)
blocks_df.loc['2153529', 'movable'] = 0
print(blocks_df)
# print(len(blocks_dict))
# print(len(blocks_df))
assert np.all((blocks_df['end15'] - blocks_df['start15']).values > 0)

intervals_lo = blocks_df['start15'].values.tolist()
intervals_hi = blocks_df['end15'].values.tolist()
movable = blocks_df['movable'].values.tolist()
print('%d blocks' % len(intervals_lo))
print(intervals_lo)
print(intervals_hi)
print(movable)

solver = MeaningfulGapsSolver(minizinc_dir)


block_2_room, shift, gaps = solver.calc(np.array(intervals_lo), np.array(intervals_hi), np.array(movable))
print(block_2_room, shift)
blocks_df['room_id'] = -1
blocks_df['comment'] = ''
blocks_df['start_o'] = blocks_df['start']
blocks_df['end_o'] = blocks_df['end']

i = 0
for block_id in blocks_df.index.tolist():
    room_id = block_2_room[i]
    print(room_id)
    blocks_df.loc[block_id, 'room_id'] = room_id
    blocks_df.loc[block_id, 'comment'] = str(block_id)
    blocks_df.loc[block_id, 'start_o'] += pd.Timedelta(minutes=15) * shift[i]
    blocks_df.loc[block_id, 'end_o'] += pd.Timedelta(minutes=15) * shift[i]
    i += 1

print(blocks_df.dtypes)
print(blocks_df)
print(gaps)

all_rooms = set(blocks_df['room_id'].values.tolist())

for room_id in all_rooms:
    sorted_intervals = blocks_df.loc[blocks_df['room_id'] == room_id, ['start_o', 'end_o']].sort_values(
        by='start_o').index.tolist()
    print('room_id: %d' % room_id)
    for index in range(1, len(sorted_intervals)):
        dT = blocks_df.loc[sorted_intervals[index], 'start_o'] - blocks_df.loc[sorted_intervals[index - 1], 'end_o']
        print(dT)
plot_gantt_chart(blocks_df)
