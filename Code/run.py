import cv2 as cv
import os

from task1 import *
from task2 import *
from task3 import *
from visualisation import *
from utils import *

# Code is reused from my own previous project that is publicly available on github under my name: https://github.com/Chirobocea/Computer-Vision/tree/main/Scrabble%20score%20calculator

def run(images_location, mask_location, solutions_location):

    files=os.listdir(images_location)
    
    i=1
    j=1
    k_move = 0

    if not os.path.exists(solutions_location):
        os.makedirs(solutions_location)

    last_matrix = None
    file_score = open(solutions_location + '/' + str(i) +"_scores.txt", "w+")
    player_data = get_turns(images_location, i)

    score1 = 0
    score2 = 0

    for file in files:
    
        if file[-3:]=='jpg':
            if j > 50:
                file_score.close()
                i = i+1
                j = 1
                k_move = 0
                last_matrix = None
                file_score = open(solutions_location + '/' + str(i) +"_scores.txt", "w+")
                player_data = get_turns(images_location, i)
                # print(f"Game {i} started")

            path = images_location+'/'+file
            image = cv.imread(path) 
            mask_board = get_mask(image, (100,  90,  80), (140, 230, 255))
            board = extract_board(image, mask_board)
            lines_horizontal, lines_vertical = make_lines(900, 64.28)
            mask_letters = get_mask(board, (10,20,120), (70,100,240), 16, 26)
            current_matrix = board_configuration(mask_letters, lines_horizontal, lines_vertical)
            diff_matrix = find_new_changes(last_matrix, current_matrix)
            new_letters, str_config = board_configuration_letters(mask_location, board, diff_matrix, lines_horizontal, lines_vertical)
            current_matrix = combine(last_matrix, new_letters)
            # image_grid = draw_grid(board, 900, 64.28, np.array(current_matrix))
            # show_image(image_grid, resize_factor=1)
            last_matrix = current_matrix.copy()

            points = calculate_points(diff_matrix, current_matrix)


            if j == player_data[k_move][1]:
                if k_move != 0:
                    if j == 50:
                        if player_data[k_move][0] == 1:
                            score1 += points
                        elif player_data[k_move][0] == 2:
                            score2 += points
                    if player_data[k_move][0] == 1:
                        file_score.write(f"Player2 {player_data[k_move-1][1]} {score1}\n") 
                        # print(f"Player2 {player_data[k_move-1][1]} {score1}")
                    elif player_data[k_move][0] == 2:
                        # print(f"Player1 {player_data[k_move-1][1]} {score2}")
                        file_score.write(f"Player1 {player_data[k_move-1][1]} {score2}\n") 
                if j != 50:
                    k_move += 1
                score1 = 0
                score2 = 0

            if player_data[k_move][0] == 1:
                score1 += points
            elif player_data[k_move][0] == 2:
                score2 += points

            if j<10:
                file_name = str(i)+"_0"+str(j)
            else:
                file_name = str(i)+"_"+str(j)

            file_move = open(solutions_location + '/' + file_name+".txt", "w+")
            file_move.write(str_config) 
            file_move.close()  

            j = j+1

    file_score.close()

images_location = 'D:/University/Sem 2/Cv/CV-2024-Project1/test/'
mask_location = 'D:/University/Sem 2/Cv/test/407_Chirobocea_Mihail/407_Chirobocea_Mihail/Masks'
solutions_location = 'D:/University/Sem 2/Cv/test/407_Chirobocea_Mihail/407_Chirobocea_Mihail/Solutions'

run(images_location, mask_location, solutions_location)