__author__ = 'Jann Kleen'

from pytesseract import image_to_string
import cv2
import numpy as np
from collections import Counter
from itertools import product
from copy import copy
import Image


def detect_character(img):
    _img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pil_im = Image.fromstring("L", _img.shape[:2], _img.tostring())

    print image_to_string(pil_im)


def merge_colours(pixels, max_distance=5):
    """ Merge a Counter() dictionary by euclidean distance in RGB space.

    :param pixels: Dictionary with BGR tuples as keys and counts as values
    :return: Dictionary with BGR tuples as keys and counts as values
    """
    pixels = copy(pixels)

    distances = [(item,
                  np.sqrt(np.sum((np.array(item[0])-np.array(item[1]))**2))) for item in product(pixels.keys(),
                                                                                                 pixels.keys())]

    for pair, distance in distances:
        if pair[0] == pair[1]:
            continue  # comparing the same colours
        if distance < max_distance:
            try:
                if pixels[pair[0]] > pixels[pair[1]]:
                    pixels[pair[0]] += pixels[pair[1]]
                    del pixels[pair[1]]
                else:
                    pixels[pair[1]] += pixels[pair[0]]
                    del pixels[pair[0]]
            except KeyError:
                continue  # one of them is already gone

    return pixels


def detect_colour(field):
    """ Detect the background colour of a field.

    :param field: cv2 image object
    :return: BGR value of the most prominent colour
    """
    # create list of BGR tuples and count them
    pixels = Counter(map(tuple, np.reshape(field, (-1, 3)).tolist()))
    # filter out the colours which just have a few occurrences
    pixels = dict(filter(lambda pixel: pixel[1] > 100, dict(pixels).items()))
    # and merge the nearby colours
    pixels = merge_colours(pixels)

    # the background color should be the one with the most pixels present
    return Counter(pixels).most_common(1)[0][0]


def detect_fields(img):
    """ Separates the image into a 5x5 matrix of fields

    :param img: cv2 image object
    :return: 2-dimensional list of image objects
    """
    lines = np.array_split(img, 5, axis=1)
    fields = [np.array_split(line, 5, axis=0) for line in lines]
    return fields


def detect_board(img):
    """ Detects the beginning of the playing board

    i.e. it detects the first horizontal line and returns the coordinate
    This code was copied from the line detection example on http://docs.opencv.org

    :param img: OpenCV image object
    :return: Height of the first detected horizontal line
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        y0 = b * rho
        y1 = int(y0 + 1000 * a)
        y2 = int(y0 - 1000 * a)

        if abs(y1 - y2) < 5:
            return int(y0)

    return None


if __name__ == '__main__':
    grid_img = cv2.imread('fixtures/sample.png')
    grid_start_y = detect_board(grid_img)
    grid_img = grid_img[grid_start_y:, :]
    grid_img = detect_fields(grid_img)
    colours = []
    for line_idx, field_line in enumerate(grid_img):
        for field_idx, field_img in enumerate(field_line):
            # print field_img
            colours.append(detect_colour(field_img))
            cv2.imshow('field-%s-%s' % (line_idx, field_idx), cv2.cvtColor(field_img, cv2.COLOR_BGR2GRAY))
            detect_character(field_img)

    colours = merge_colours(dict(Counter(colours)))
    print colours
    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()
