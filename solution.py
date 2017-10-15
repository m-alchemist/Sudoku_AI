import itertools;
assignments = [];
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[i] + cols[i] for i in range(9)], [rows[::-1][i] + cols[i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """


    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for unit in unitlist:
        peer_boxes=[];
        # there have to be at least two boxes with a value of length 2 to have naked twins

        for box in unit:
            #finding all boxes with two digits

            if len(values[box])==2:
                peer_boxes.append((values[box], box))
        """
        if two boxes have the same two digits eliminate from the two digits from the rest
        of the unit
        """
        if len(peer_boxes) == 2:
            box1= peer_boxes[0];
            box2= peer_boxes[1];
            if box1[0] == box2[0]:
                #removing digits from the rest of the units
                for i in unit:
                    if len(values[i]) > 2:

                        digit1, digit2 = box1[0][0], box1[0][1]
                        assign_value(values, i, values[i].replace(digit1, ''))
                        assign_value(values, i, values[i].replace(digit2, ''))
    return values

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    # Nine by nine grid
    assert len(chars) == 81
    return dict(zip(boxes, chars));

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        # Remove solved digit from the list of possible values for each peer
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    numbers="123456789"
    for unit in unitlist:

        for digit in numbers:
            occurences=[];
            for box in unit:
                if digit in values[box] :
                  occurences.append(box);
            if len(occurences)==1:
                values[occurences[0]]=digit;
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values=eliminate(values);
        # Your code here: Use the Only Choice Strategy
        values=only_choice(values);
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values=reduce_puzzle(values);
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values;
    # Choose one of the unfilled squares with the fewest possibilities

    shortest="";

    for box in values.keys():
        if len(values[box])>1:
            if shortest=="":
                shortest=box;

            elif len(values[box])<  len(values[shortest])  :
               shortest=box;
    if len(shortest)>0:
        for value in values[shortest]:
            pending_values=values.copy();
            pending_values[shortest]=value;
            attempt=search(pending_values);
            if attempt:
                return attempt;

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
