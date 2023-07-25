import json

# Replace 'path/to/your/json_file.json' with the actual path to your JSON file
file_path = 'schedule.json'

# Read JSON data from the file
with open(file_path, 'r') as file:
    json_data = file.read()

# Parse the JSON data into a Python dictionary
data_dict = json.loads(json_data)

# Create dictionaries for tasks and blocks
tasks_dict = {}
blocks_dict = {}

# Iterate over the "tasks" list and group tasks based on "parent_block_id"
for task in data_dict['tasks']:
    parent_block_id = task['parent_block_id']
    procedure_icd = task['procedure_icd']

    if parent_block_id in tasks_dict:
        tasks_dict[parent_block_id].append(procedure_icd)
    else:
        tasks_dict[parent_block_id] = [procedure_icd]

# Iterate over the "blocks" list and create a dictionary with block IDs as keys
for block in data_dict['blocks']:
    block_id = block['id']

    assert block_id not in blocks_dict.keys()
    blocks_dict[block_id] = {
        'start': block['start'],
        'end': block['end']
    }

# Print the resulting dictionaries
print("Tasks Dictionary:")
print(tasks_dict)
print("\nBlocks Dictionary:")
print(blocks_dict)

icd_set = set()

# Loop through the tasks dictionary and add ICD codes to the set
for icd_list in tasks_dict.values():
    if icd_list:
        icd_set.update(icd_list)

# Print the set of unique ICD codes
print("Set of unique ICD codes:[%d]" % len(icd_set))
print(icd_set)
