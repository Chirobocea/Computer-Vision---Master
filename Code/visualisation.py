import cv2 as cv
import numpy as np

def show_image(image_, window_name='image', timeout=0, resize_factor = 8, alpha = None):

    resized_image = image_
    resized_image = cv.resize(np.uint8(image_), (image_.shape[1] // resize_factor, image_.shape[0] // resize_factor))

    if alpha is not None:
        alpha = cv.resize(np.uint8(alpha), (alpha.shape[1] // resize_factor, alpha.shape[0] // resize_factor), interpolation=cv.INTER_NEAREST)
        for i in range(alpha.shape[0]):
            for j in range(alpha.shape[1]):

                if alpha[i, j] == 0:
                    resized_image[i, j, 2] = min(255, resized_image[i, j, 2] + 200)

    cv.imshow(window_name, resized_image)
    cv.waitKey(timeout)
    cv.destroyAllWindows()


def draw_grid(image, n, k, matrix=None):
    if matrix is not None:
        font = cv.FONT_HERSHEY_SIMPLEX
        for i in range(0, matrix.shape[1]):
            for j in range(0, matrix.shape[0]):
                x = int((i + 0.5) * k) 
                y = int((j + 0.5) * k)
                text = matrix[j, i]
                color = (180, 60, 60)
                cv.putText(image, text, (x, y), font, 1.1, color, 2, cv.LINE_AA)
    for i in range(0, int(n/k)+1):
        x = int(i * k)
        cv.line(image, (0, x), (n, x), (255, 0, 0), 2) 
        cv.line(image, (x, 0), (x, n), (255, 0, 0), 2) 
    return image