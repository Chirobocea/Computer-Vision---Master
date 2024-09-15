from utils import *
from visualisation import *

def board_configuration(board, lines_horizontal, lines_vertical):

    matrix = [[0 for i in range(len(lines_vertical)-1)] for j in range(len(lines_horizontal)-1)]
    for i in range(len(lines_horizontal)-1):
        for j in range(len(lines_vertical)-1):

            patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 20, 20)
            if np.mean(patch) > 128:
                matrix[i][j] = '+'
            else:
                matrix[i][j] = '-'

    return matrix


def two_greatest_numbers(cifers):

    cifers = np.array(cifers)
    indexes = np.argpartition(cifers, -2)[-2:]
    indexes = indexes[np.argsort(cifers[indexes])][::-1]
    numbers = cifers[indexes]

    return numbers.tolist(), indexes.tolist()


def get_number_index(i1, i2, numbers):
    idxs = []
    for key, value in numbers.items():
        if str(i1) in value and str(i2) in value:
            idxs.append(key)
    return idxs

def get_composed_letter(scores, y_values, i1, i2, letters):

    idxs = get_number_index(i1, i2, letters)

    if len(idxs) == 0:
        return None
    if len(idxs) == 1:
        if scores[idxs[0]-1] < 0.75:
            
            return None
        return letters[idxs[0]]


    
    if scores[idxs[0]-1] < 0.75 and scores[idxs[1]-1] < 0.75:
        return None
    if scores[idxs[0]-1] > scores[idxs[1]-1]:
        return letters[idxs[0]]
    else:
        return letters[idxs[1]]


def classify_letter(mask_location, patch):

    letters = {
        1: "0",
        2: "1",
        3: "2",
        4: "3",
        5: "4",
        6: "5",
        7: "6",
        8: "7",
        9: "8",
        10: "9",
        11: "10",
        12: "11",
        13: "12",
        14: "13",
        15: "14",
        16: "15",
        17: "16",
        18: "17",
        19: "18",
        20: "19",
        21: "20",
        22: "21",
        23: "24",
        24: "25",
        25: "27",
        26: "28",
        27: "30",
        28: "32",
        29: "35",
        30: "36",
        31: "40",
        32: "42",
        33: "45",
        34: "48",
        35: "49",
        36: "50",
        37: "54",
        38: "56",
        39: "60",
        40: "63",
        41: "64",
        42: "70",
        43: "72",
        44: "80",
        45: "81",
        46: "90",
    }

    scale_factor = 2
    gray_patch = cv.cvtColor(patch, cv.COLOR_BGR2GRAY)
    gray_patch = cv.inRange(gray_patch, ( 0), (90))
    gray_patch = cv.erode(gray_patch, np.ones((3, 3), np.uint8), iterations=1)
    gray_patch = cv.dilate(gray_patch, np.ones((6, 6), np.uint8), iterations=1)
    gray_patch = cv.resize(gray_patch, (gray_patch.shape[1] * scale_factor, gray_patch.shape[0] * scale_factor), interpolation = cv.INTER_LINEAR)

    letter= None
    scores = []
    y_values = []
    max_numar = [72, 100]
    for j in range(1, len(letters)+1):

        img_template=cv.imread(mask_location+'/'+letters[j]+'.jpg')
        img_template=cv.cvtColor(img_template, cv.COLOR_BGR2GRAY)
        img_template = 255 - img_template
        top, bottom, left, right = [1, 1, 1, 1] 
        img_template = cv.copyMakeBorder(img_template, top, bottom, left, right, cv.BORDER_CONSTANT, value=0)
        img_template = cv.dilate(img_template , np.ones((3, 3), np.uint8), iterations=1)
        img_template = cv.resize(img_template, (img_template.shape[1] * scale_factor, img_template.shape[0] * scale_factor), interpolation = cv.INTER_LINEAR)


        corr = cv.matchTemplate(gray_patch, img_template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(corr)
        y = max_loc[1] + img_template.shape[0]
        m=np.max(corr)

        y_values.append(y)
        scores.append(m)

        if j == 2:
            img_teamplate2 = img_template.copy()
            x_axis = (max_numar[1] - img_teamplate2.shape[1]) // 2
            y_axis = (max_numar[0] - img_teamplate2.shape[0]) // 2
            top, bottom, left, right = [y_axis, y_axis, x_axis, x_axis]
            img_teamplate2 = cv.copyMakeBorder(img_teamplate2, top, bottom, left, right, cv.BORDER_CONSTANT, value=0)   
            corr2 = cv.matchTemplate(gray_patch, img_teamplate2, cv.TM_CCOEFF_NORMED)
            corr2 = np.max(corr2)

    if len(letters) != len(scores):
        print("Error: The number of letters and scores is not the same")
        return None

    cifers = scores[:10]
    
    [c1, c2], [i1, i2] = two_greatest_numbers(cifers)

    if (i1 == 1 and c1 > 0.8) or (i2 == 1 and c2 > 0.8):

        if scores[11] > 0.6 or corr2 > 0.6:
            if corr2 > scores[11]:
                letter = "1"
            else:
                letter = "11"
        else:
            letter = None

    if (abs(c1-c2) < 0.21 and c1 > 0.79 and c2 > 0.79) or (abs(c1-c2) < 0.1 and 0.65 < c1 < 0.9 and 0.65 < c2 < 0.9):
        letter = get_composed_letter(scores, y_values, i1, i2, letters)
    
    if letter is None:
        if c1 > c2:
            letter = letters[i1+1]
        else:
            letter = letters[i2+1]

    return letter


def board_configuration_letters(mask_location, board, matrix, lines_horizontal, lines_vertical):

    col = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H",
        8: "I",
        9: "J",
        10: "K",
        11: "L",
        12: "M",
        13: "N",
    }

    str_config = ""
    pad = 5
    values = [0, 255]

    for i in range(len(lines_horizontal)-1):
        for j in range(len(lines_vertical)-1):

            if matrix[i][j] != '-':

                if i!=0 and j!=0 and i!=len(lines_horizontal)-2 and j!=len(lines_vertical)-2:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, -pad, -pad)
                elif i==0 and j==0:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 0, 0)
                    top, bottom, left, right = [0, pad, 0, pad]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                elif i==0 and j==len(lines_vertical)-2:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 0, 0)
                    top, bottom, left, right = [0, pad, pad, 0]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                elif j==0 and i==len(lines_horizontal)-2:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 0, 0)
                    top, bottom, left, right = [pad, 0, 0, pad]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                elif i==len(lines_horizontal)-2 and j==len(lines_vertical)-2:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 0, 0)
                    top, bottom, left, right = [pad, 0, pad, 0]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                elif i == 0:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 0, -3)
                    top, bottom, left, right = [0, pad, pad, pad]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                elif i == len(lines_horizontal)-2:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 0, -3)
                    top, bottom, left, right = [pad, 0, pad, pad]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                elif j == 0:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, -3, 0)
                    top, bottom, left, right = [pad, pad, 0, pad]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                elif j == len(lines_vertical)-2:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, -3, 0)
                    top, bottom, left, right = [pad, pad, pad, 0]
                    patch = pad_image_random(patch, top, bottom, left, right, values)
                else:
                    patch = cut_patch(board, lines_horizontal, lines_vertical, i, j, 0, 0)
                
                matrix[i][j] = classify_letter(mask_location, patch)
                str_config = str_config + str(i+1)+str(col[j]) + " " + str(matrix[i][j]) + "\n" 

    return matrix, str_config