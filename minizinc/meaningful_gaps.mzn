


include "alldifferent.mzn";
include "globals.mzn";

int: n_blocks = 22;

int: max_n_rooms = 9;
int: max_time_line = 64;


int: primetime_start = 0;
int: primetime_end = 64;


array [1..n_blocks] of 0..max_time_line: intervals_lo = [28, 0, 0, 31, 0, 0, 0, 32, 36, 32, 38, 0, 32, 36, 52, 28, 20, 0, 12, 32, 0, 24];
array [1..n_blocks] of 0..max_time_line: intervals_hi = [52, 24, 32, 63, 32, 32, 24, 60, 64, 60, 60, 28, 61, 64, 64, 36, 36, 12, 20, 60, 36, 32];
array [1..n_blocks] of 0..1: movable = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1];


array [1..n_blocks] of var -4..4: shift;
array [1..n_blocks] of var 1..max_n_rooms: block_2_room;

% selected rooms
set of int: Selected_Rooms = 1..max_n_rooms;



% optimization vars
array [1..max_n_rooms] of var 0..max_time_line: gaps;

%var int: primetime_start_end_gaps;


predicate interval_intersects(var int: start1, var int: end1, var int: start2, var int: end2) =
  (start1 <= end2 /\ start2 <= end1);
  


% seems to be all rooms will be selected
constraint
    Selected_Rooms = { block_2_room[i] | i in 1..n_blocks }
;


constraint
    forall(i in 1..n_blocks, j in 1..n_blocks where i < j)
    (
         block_2_room[i] == block_2_room[j] -> 
                                        not interval_intersects( intervals_lo[i] + shift[i], intervals_hi[i] + shift[i], intervals_lo[j] + shift[j], intervals_hi[j] + shift[j] )
    );

    
% primetime
constraint
    forall(i in 1..n_blocks)
    (
      ((intervals_lo[i] + shift[i]) >= primetime_start)
      /\
      ((intervals_hi[i] + shift[i]) <= primetime_end)
    );

    
            
function var int: interval_gap(var int: start1, var int: end1, var int: start2, var int: end2) =
  if end1 < start2 then
    ((start2 - end1) div 4)
  elseif start1 > end2 then
    ((start1 - end2) div 4)
  else
    0  % Intervals overlap or touch
  endif;
    
    

          
function var bool: is_between(int: start1, int: end1, int: start2, int: end2, int: r, int: p, int: q) =

  exists(k in 1..n_blocks where (block_2_room[k] == r /\ (k != p) /\ (k != q))) (
    ((intervals_lo[k] >= start1 /\ intervals_hi[k] <= end2)  ) \/
    ((intervals_lo[k] >= start2 /\ intervals_hi[k] <= end1)  )
  );


  
       
          
constraint     forall(r in Selected_Rooms)
    (
    gaps[r] = sum([ interval_gap( intervals_lo[i] + shift[i], intervals_hi[i] + shift[i], intervals_lo[j] + shift[j], intervals_hi[j] + shift[j]) 
                | i in 1..n_blocks, j in 1..n_blocks 
                
                where ( 
                i < j /\ 
                (not is_between(intervals_lo[i], intervals_hi[i], intervals_lo[j], intervals_hi[j], r, i, j))
                 /\ block_2_room[i] == r /\ block_2_room[j] == r)   ])
    
    )
;


 


     
solve maximize sum([gaps[r] | r in Selected_Rooms]);


output [  show(block_2_room), "," , show(shift), ",", show(Selected_Rooms), ",", show(gaps) ]




