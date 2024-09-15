import numpy as np
import cv2 as cv
from utils import *
from visualisation import *


def pad_image(image_, return_pad=False, procent=0.1):
    pad_h = int(image_.shape[0] * procent)
    pad_w = int(image_.shape[1] * procent)
    big_image = np.zeros((image_.shape[0] + 2 * pad_h, image_.shape[1] + 2 * pad_w, 3), np.uint8)
    big_image[pad_h: pad_h + image_.shape[0], pad_w: pad_w + image_.shape[1]] = image_.copy()
    if return_pad:
        return big_image, pad_h, pad_w
    return big_image

def unpad_image(image_, pad_h, pad_w):
    cropped_image = image_[pad_h: -pad_h, pad_w: -pad_w]
    return cropped_image




def find_corners(mask):

    if len(mask.shape) == 3:
        mask_gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
    else:
        mask_gray = mask

    mask_gray = mask_gray.astype('uint8')

    contours, _ = cv.findContours(mask_gray, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    max_area = 0

    possible_top_left = None
    possible_bottom_right = None
    possible_top_right = None
    possible_bottom_left = None

    top_left,top_right,bottom_right,bottom_left = None,None,None,None

    for i in range(len(contours)):
        if(len(contours[i]) > 5):

            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point
                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + possible_bottom_right[1]:
                    possible_bottom_right = point
                if possible_top_right is None or point[0] - point[1] > possible_top_right[0] - possible_top_right[1]:
                    possible_top_right = point
                if possible_bottom_left is None or -point[0] + point[1] > -possible_bottom_left[0] + possible_bottom_left[1]:
                    possible_bottom_left = point

            if cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left
                
    return top_left,top_right,bottom_right,bottom_left


def crop_board(top_left,top_right,bottom_right,bottom_left, new_size, image, crop_size):

    puzzle = np.array([top_left,top_right,bottom_right,bottom_left], dtype = "float32")
    destination_of_puzzle = np.array([[0,0],[new_size,0],[new_size,new_size],[0,new_size]], dtype = "float32")
    M = cv.getPerspectiveTransform(puzzle, destination_of_puzzle)

    board = cv.warpPerspective(image, M, (new_size, new_size), flags = cv.BORDER_REFLECT + cv.WARP_FILL_OUTLIERS)

    y, x, _ = board.shape
    start_x = x//2 - crop_size//2
    start_y = y//2 - crop_size//2  

    return board[start_y:start_y+crop_size, start_x:start_x+crop_size]


def extract_board(image, mask, new_size=1215, crop_size=900): 

    top_left,top_right,bottom_right,bottom_left = find_corners(mask)

    board = crop_board(top_left,top_right,bottom_right,bottom_left, new_size, image, crop_size)

    return board
