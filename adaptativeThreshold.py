import cv2
import numpy as np
import argparse
import ntpath
import os


def adaptative_thresholding(path, threshold):
    # Load image
    I = cv2.imread(path)

    gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

    orignrows, origncols = gray.shape

    M = int(np.floor(orignrows / 16) + 1)
    N = int(np.floor(origncols / 16) + 1)

    # Image border padding related to windows size
    Mextend = round(M / 2) - 1
    Nextend = round(N / 2) - 1

    # Padding image
    aux = cv2.copyMakeBorder(gray, top=Mextend, bottom=Mextend, left=Nextend,
                             right=Nextend, borderType=cv2.BORDER_REFLECT)

    windows = np.zeros((M, N), np.int32)

    # Image integral calculation
    imageIntegral = cv2.integral(aux, windows, -1)

    # Integral image size
    nrows, ncols = imageIntegral.shape

    # Memory allocation for cumulative region image
    result = np.zeros((orignrows, origncols))

    # Image cumulative pixels in windows size calculation
    for i in range(nrows - M):
        for j in range(ncols - N):
            result[i, j] = imageIntegral[i + M, j + N] - imageIntegral[i, j + N] + imageIntegral[i, j] - imageIntegral[
                i + M, j]

    # Output binary image memory allocation
    binar = np.ones((orignrows, origncols), dtype=np.bool)

    # Gray image weighted by windows size
    graymult = (gray).astype('float64') * M * N

    # Output image binarization
    binar[graymult <= result * (100.0 - threshold) / 100.0] = False

    # binary image to UINT8 conversion
    binar = (255 * binar).astype(np.uint8)

    # binar = cv2.bitwise_not(binar)

    return binar
