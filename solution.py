assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def diagonal_sudoku(boolean):
    """
    Function to output unitlist, units, and peers
    """
    if boolean:
        unitlist = row_units + column_units + square_units + diagonal_units
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    else:
        unitlist = row_units + column_units + square_units
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    return (unitlist, units, peers)

def naked_twins(values, diagonal=True):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Include the diagonal units if we're solving diagonal sudoku
    unitlist, units, peers = diagonal_sudoku(diagonal)
    
    # Find all instances of naked twins
    # Search through each unit, collect all boxes with 2 numbers, then see if any of them contain the same numbers.
    twins_list = []
    for unit in unitlist:
        box_2num = [key for key in unit if len(values[key])==2]
        n = len(box_2num)
        if n>1:
            twins_list = twins_list + [(box_2num[i],box_2num[j]) for i in range(n) for j in range(i+1,n) if values[box_2num[i]]==values[box_2num[j]]]
    # Eliminate the naked twins as possibilities for their peers
    # Go through each twin pairs found, then remove the digits assigned to those pairs from all other boxes in their shared peers
    for twins in twins_list:
        twin_digits = values[twins[0]]
        for digit in twin_digits:
            for box in (peers[twins[0]]&peers[twins[1]]):
                values = assign_value(values, box, values[box].replace(digit,''))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '123456789' for empties."
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values, diagonal=True):
    # Write a function that will take as an input, the sudoku in dictionary form,
    # run through all the boxes, applying the eliminate technique,
    # and return the resulting sudoku in dictionary form.
    
    # Include the diagonal units if we're solving diagonal sudoku
    unitlist, units, peers = diagonal_sudoku(diagonal)
    
    for square in values.keys():
        digit = values[square]
        if len(digit) == 1:
            for peer in peers[square]:
                values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values, diagonal=True):
    # Write a function that will take as an input, the sudoku in dictionary form,
    # run through all the units, applying the only choice technique,
    # and return the resulting sudoku in dictionary form.
    
    # Include the diagonal units if we're solving diagonal sudoku
    unitlist, units, peers = diagonal_sudoku(diagonal)
    
    for unit in unitlist:
        for digit in '123456789':
            boxes_with_digit = [square for square in unit if digit in values[square]]
            if len(boxes_with_digit) == 1:
                values[boxes_with_digit[0]] = digit
    return values

def reduce_puzzle(values, diagonal=True):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values, diagonal)

        # Use the Naked Twin Strategy
        values = naked_twins(values, diagonal)

        # Use the Only Choice Strategy
        values = only_choice(values, diagonal)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid, diagonal=True):
    
    return search(grid_values(grid), diagonal)

def search(values, diagonal = True):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values, diagonal)
    if values is False:
        return False
    if max([len(choices) for choices in values.values()]) == 1:
        return values
    
    # Chose one of the unfilled square s with the fewest possibilities
    square = min([box for box in values.keys() if len(values[box])>1])
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for choice in values[square]:
        new_values = values.copy()
        new_values[square] = choice
        new_values = search(new_values, diagonal)
        if new_values:
            return new_values

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows,cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[(rows[i]+cols[i]) for i in range(9)],[(rows[i]+cols[8-i]) for i in range(9)]]

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')