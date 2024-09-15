import numpy as np
from copy import copy

def check_divide(a, b, c):
    if b != 0:
        if a / b == c:
            return True
    if a != 0:
        if b / a == c:
            return True
    return False

def check_equation(a, b, c, plus_constraint = False, minus_constraint = False, multiply_constraint = False, divide_constraint = False):


    a = int(copy(a))
    b = int(copy(b))
    c = int(copy(c))

    if plus_constraint:
        return a + b == c
    elif minus_constraint:
        return any([a - b == c, b-a == c])
    elif multiply_constraint:
        return a * b == c
    elif divide_constraint:
        return check_divide(a, b, c)
    else:
        return any([a + b == c, a - b == c, b - a == c, a * b == c, check_divide(a, b, c)])




def calculate_points(diff_matrix, current_matrix):

    x3_points = [(0, 0), (0, 13), (13, 0), (13, 13), 
                 (0, 6), (0, 7), (13, 6), (13, 7), 
                 (6, 0), (7, 0), (6, 13), (7, 13)]
    x2_points = [(1, 1), (2, 2), (3, 3), (4, 4), 
                 (9, 9), (10, 10), (11, 11), (12, 12), 
                 (1, 12), (2, 11), (3, 10), (4, 9), 
                 (9, 4), (10, 3), (11, 2), (12, 1)]
    plus_constraint = [(3, 6), (4, 7), 
                       (6, 4), (7, 3), 
                       (6, 10), (7, 9), 
                       (9, 6), (10, 7)]
    minus_constraint = [(2, 5), (2, 8),
                        (5, 2), (8, 2),
                        (5, 11), (8, 11),
                        (11, 5), (11, 8)]
    multiply_constraint = [(7, 4), (6, 3),
                           (3, 7), (4, 6),
                           (6, 9), (7, 10),
                           (9, 7), (10, 6)]
    divide_constraint = [(1, 4), (1, 9),
                         (4, 1), (9, 1),
                         (4, 12), (9, 12),
                         (12, 4), (12, 9)]
    

    score = 0
    plus_c = False
    minus_c = False
    multiply_c = False
    divide_c = False
    bonus = 1

    x_coords, y_coords = np.where(np.array(diff_matrix) != "-")

    current_matrix[6][6] = 1
    current_matrix[6][7] = 2
    current_matrix[7][6] = 3
    current_matrix[7][7] = 4

    for x, y in zip(x_coords, y_coords):

        score_power = 0

        if (x, y) in plus_constraint:
            plus_c = True
        elif (x, y) in minus_constraint:
            minus_c = True
        elif (x, y) in multiply_constraint:
            multiply_c = True
        elif (x, y) in divide_constraint:
            divide_c = True
        elif (x, y) in x3_points:
            bonus = 3
        elif (x, y) in x2_points:
            bonus = 2

        if x >= 2:  # Ensure there are two points above
            if current_matrix[x-1][y] != '-' and current_matrix[x-2][y] != '-':
                if check_equation(current_matrix[x-1][y], current_matrix[x-2][y], diff_matrix[x][y], plus_c, minus_c, multiply_c, divide_c):
                    score_power += 1

        if x <= 11:  # Ensure there are two points below
            if current_matrix[x+1][y] != '-' and current_matrix[x+2][y] != '-':
                if check_equation(current_matrix[x+1][y], current_matrix[x+2][y], diff_matrix[x][y], plus_c, minus_c, multiply_c, divide_c):
                    score_power += 1

        if y >= 2:  # Ensure there are two points to the left
            if current_matrix[x][y-1] != '-' and current_matrix[x][y-2] != '-':
                if check_equation(current_matrix[x][y-1], current_matrix[x][y-2], diff_matrix[x][y], plus_c, minus_c, multiply_c, divide_c):
                    score_power += 1

        if y <= 11:  # Ensure there are two points to the right
            if current_matrix[x][y+1] != '-' and current_matrix[x][y+2] != '-':
                if check_equation(current_matrix[x][y+1], current_matrix[x][y+2], diff_matrix[x][y], plus_c, minus_c, multiply_c, divide_c):
                    score_power += 1

        score += int(diff_matrix[x][y]) * score_power * bonus

    return score
