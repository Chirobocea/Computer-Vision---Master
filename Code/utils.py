import cv2 as cv
import numpy as np
from visualisation import *

def get_mask(image, lower_bound:tuple[int, int], upper_bound:tuple[int, int], dilate_kernel_size:int = None, erode_kernel_size:int = None):

    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv, lower_bound, upper_bound)
    if dilate_kernel_size is not None:
        mask = cv.dilate(mask, np.ones((dilate_kernel_size, dilate_kernel_size), np.uint8), iterations=1)
    if erode_kernel_size is not None:
        mask = cv.erode(mask, np.ones((erode_kernel_size, erode_kernel_size), np.uint8), iterations=1) 
    return mask


def make_lines(n, k):
    
    def frange(start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    lines_horizontal = []
    for i in frange(0, n+1, k):
        x = round(i)
        lines_horizontal.append([(0, x), (n, x)])

    lines_vertical = []
    for i in frange(0, n+1, k):
        x = round(i)
        lines_vertical.append([(x, 0), (x, n)])

    return lines_horizontal, lines_vertical


def cut_patch(image, lines_horizontal, lines_vertical, i, j, err_horizontal, err_vertical):
    y_min = lines_vertical[j][0][0] + err_vertical
    y_max = lines_vertical[j + 1][1][0] - err_vertical
    x_min = lines_horizontal[i][0][1] + err_horizontal
    x_max = lines_horizontal[i + 1][1][1] - err_horizontal
    patch = image[x_min:x_max, y_min:y_max].copy()
    return patch


def pad_image_random(image, top, bottom, left, right, values):
    padded_image = cv.copyMakeBorder(image, top, bottom, left, right, cv.BORDER_CONSTANT, value=values[0])

    rows, cols, _ = padded_image.shape

    for i in range(rows):
        for j in range(cols):
            if ((i < top or i >= rows - bottom) or (j < left or j >= cols - right)) and (i + j) % 2 == 1:
                padded_image[i, j] = [values[1], values[1], values[1]] 

    return padded_image


def find_new_changes(last_matrix, current_matrix):

    if last_matrix is None:
        return current_matrix.copy()
    else:
        diff = np.empty_like(last_matrix)
        for i in range(diff.shape[0]):
            for j in range(diff.shape[1]):
                if last_matrix[i][j] == '-' and current_matrix[i][j] != '-':
                    diff[i][j] = current_matrix[i][j]
                else:
                    diff[i][j] = '-'
        return diff
    

def combine(last_matrix, current_matrix):
    if last_matrix is None:
        return current_matrix.copy()
    else:
        comb = current_matrix.copy()
        for i in range(len(last_matrix)):
            for j in range(len(last_matrix[0])):
                if last_matrix[i][j] != '-':
                    comb[i][j] = last_matrix[i][j]

        return comb
    
def get_turns(folder, i):

    with open(f'{folder}/{i}_turns.txt', 'r') as file:
        player_data = []
        for line in file:
            player, number = line.strip().split()
            if player == "Player1":
                player = 1
            elif player == "Player2":
                player = 2
            number = int(number) 
            player_data.append((player, number))
        if player == 1:
            player = 2
        elif player == 2:
            player
        player_data.append((player, 50))  

    return player_data