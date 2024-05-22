# Meaningful gaps 



Each task consists of a procedure and its parent block - procedure_icd (icd9) and parent_block_id accordingly. Blocks consist of id, and duration defined by start and end times.

Tasks are executed inside their parent blocks and blocks are assigned to operating rooms.

The goal is to maximize potential revenue by assigning blocks to rooms. This metric is defined by the sum of all <u>meaningful gaps</u> - at least 60 minutes in the schedule of the operating rooms. In order to achieve that, we have a pool of 9 rooms that can host the blocks. There is a constraint on the assignment though, blocks that contain heart surgeries (by procedure_icds of tasks in them) must be assigned to operating room 4. Gaps could also be achieved between the start and end of primetime hours and the first or last block that is assigned to a room. Primetime hours start at 7am and end at 11pm. If the first block in a room starts at 8am then there is a 60 minutes potentiel time value.

Additionally, it is allowed to delay or move ahead of schedule each block by up to 60 minutes.

