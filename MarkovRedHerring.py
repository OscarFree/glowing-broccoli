# Problem statement: given an mxn array g, find the number of possible states p that could have generated g where g[x][y] is determined by
# p[x:x+2] + p[y:y+2] subject to the rule "if the sum of the 2x2 box is 1, g is 1 else 0"
# Great problem! Initially I thought about using a Markov Chain since the state g is solely determined by the previous state p. 
# I thought about defining the starting state as the end state of g and the final state as one a possible state p. However, I couldn't come up with appropriate transition matrices
# So, I went with a more brute force approach.

# 1. Generate all possible values for the first two columns of the previous state. I've chosen columns instead of rows because the max height is 9 so there are fewer possible column pairs than row pairs.
# 2. Check which column pairs evolve into the first column of g at the next timestep.
# 3. Store all valid second columns and their number of occurrences. For example, if 10 first columns and a particular second column form a valid pair, store the number 10.
# 4. Generate all possible values for the next column.
# 5. Check which column pairs (all possible combinations of the previous and next column) evolve into the next column of g at the next timestep and store all valid pairs.
# 6. For each last column in column pairs, count its number of occurrences and add that to the previous number of occurrences in the associated first column
# 7. Repeat steps 4-6 until no columns remain in g.
# 8. Return the sum of the number of occurrences

g = [[True, False, False, True, False, True, False, True], 
     [True, False, False, False, False, False, True, True], 
     [True, True, False, False, False, False, False, False],
     [True, True, False, True, False, False, False, False],
     [True, True, False, False, False, False, False, False],
     [False, False, False, False, False, False, False, False],
     [True, True, True, True, True, True, True, True],
     [True, True, False, True, False, False, False, False], 
     [False, True, False, False, False, False, True, True]]
# ans 1181730

def solution(g):
  import itertools
  from collections import Counter

  def generate_combinations(length): # generate all possible True False lists
    return list(itertools.product([True, False], repeat = length))

  def check_candidates_smart(columns, g_column): # uses lazy evaluation so we don't need to check all the elements of g_column
    for i in range(height):
      if (columns[0][i] + columns[1][i] + columns[0][i+1] + columns[1][i+1] == 1) != g_column[i]:
        return False
    return True

  height, width = len(g), len(g[0])
  column = generate_combinations(height+1) 
  column_candidates = list(itertools.product(column, repeat=2))
  g_column = [row[0] for row in g]
  valid_columns = Counter([columns[1] for columns in column_candidates if check_candidates_smart(columns, g_column)]) # second columns which satisfy check_candidates and their number of occurrences

  for i in range(1, width):
    column_candidates = list(itertools.product([columns for columns in valid_columns], column))
    g_column = [row[i] for row in g] # associated column in g
    valid_column_pairs = [columns for columns in column_candidates if check_candidates_smart(columns, g_column)] # list of column pairs which satisfy check_candidates
    # valid_column_pairs = filter(func, (1,2,3,4))
    new_column_candidates = {}

    for column1, column2 in valid_column_pairs:
      new_column_candidates[column2] = new_column_candidates.get(column2, 0) + valid_columns[column1] # Keys are the second column, values are the sum of all previously accumulated occurences which match the second column

    valid_columns = new_column_candidates

    print(sum(valid_columns.values()))
  return sum(valid_columns.values())

solution(g)
