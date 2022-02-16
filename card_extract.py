import os
import pytesseract
import cv2
import re
import unicodedata
import unidecode
import numpy as np

from itertools import islice
from pytesseract import Output
from idcard_extract_app.process.ocr.adaptativeThreshold import adaptative_thresholding, \
    adaptative_thresholding_with_denoise

OCR_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_card(img_path):

    threshold_list = [40, 20, 60]
    pytesseract.pytesseract.tesseract_cmd = OCR_PATH

    form_image = cv2.imread(img_path)
    form_image = cv2.resize(form_image, (550, 375))

    check_image = cv2.imread(img_path, 0)
    cv2.imwrite('idcard_extract_app/static/img/grayscale.png', check_image)

    img = adaptative_thresholding(img_path, 25)
    cv2.imwrite('idcard_extract_app/static/img/thresholding.png', img)

    whitelist = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\\ -\u00E0\u00C0\u1EA3\u1EA2\u00E3\u00C3\u00E1\u00C1\u1EA1\u1EA0\u0103\u0102\u1EB1\u1EB0\u1EB3\u1EB2\u1EB5\u1EB4\u1EAF\u1EAE\u1EB7\u1EB6\u00E2\u00C2\u1EA7\u1EA6\u1EA9\u1EA8\u1EAB\u1EAA\u1EA5\u1EA4\u1EAD\u1EAC' \
                '\u0111\u0110\u00E8\u00C8\u1EBB\u1EBA\u1EBD\u1EBC\u00E9\u00C9\u1EB9\u1EB8\u00EA\u00CA\u1EC1\u1EC0\u1EC3\u1EC2\u1EC5\u1EC4\u1EBF\u1EBE\u1EC7\u1EC6\u00EC\u00CC\u1EC9\u1EC8\u0129\u0128\u00ED\u00CD\u1ECB\u1ECA\u00F2\u00D2\u1ECF\u1ECE\u00F5\u00D5\u00F3\u00D3\u1ECD\u1ECC\u00F4\u00D4\u1ED3\u1ED2\u1ED5\u1ED4\u1ED7' \
                '\u1ED6\u1ED1\u1ED0\u1ED9\u1ED8\u01A1\u01A0\u1EDD\u1EDC\u1EDF\u1EDE\u1EE1\u1EE0\u1EDB\u1EDA\u1EE3\u1EE2\u00F9\u00D9\u1EE7\u1EE6\u0169\u0168\u00FA\u00DA\u1EE5\u1EE4\u01B0\u01AF\u1EEB\u1EEA\u1EED\u1EEC\u1EEF\u1EEE\u1EE9\u1EE8\u1EF1\u1EF0\u1EF3\u1EF2\u1EF7\u1EF6\u1EF9\u1EF8\u00FD\u00DD\u1EF5\u1EF4'
    img = remove_small_obj(img)
    read_img = cv2.resize(img, (1100, 750))
    raw_text = pytesseract.image_to_string(read_img, lang='vie',
                                           config='--oem 3 --psm 6 -c tessedit_char_blacklist=<>_[]@?()|')
    # raw_text = "".join([s for s in raw_text.splitlines(True) if s.strip("\r\n")])
    identity_code, full_name, day_of_birth, place_of_birth, address = get_info_from_rawtext(raw_text)

    cv2.imwrite('idcard_extract_app/static/img/idcard.png', read_img)
    count_none = sum(x is None for x in [identity_code, full_name, day_of_birth, place_of_birth, address])

    i = 0
    while count_none >= 2 and i < len(threshold_list):
        identity_code, full_name, day_of_birth, place_of_birth, address = preprocess_then_read(img_path,
                                                                                               threshold_list[i], 0)
        count_none = sum(x is None for x in [identity_code, full_name, day_of_birth, place_of_birth, address])
        i = i + 1

    else:
        data_to_string('idcard_extract_app/static/img/idcard.png')

    if count_none >= 2:
        identity_code, full_name, day_of_birth, place_of_birth, address = preprocess_then_read(img_path, 40, 1)
        count_none = sum(x is None for x in [identity_code, full_name, day_of_birth, place_of_birth, address])

    else:
        data_to_string('idcard_extract_app/static/img/idcard.png')

    if count_none >= 2:
        identity_code, full_name, day_of_birth, place_of_birth, address = preprocess_then_read(img_path, 60, 1)

    else:
        data_to_string('idcard_extract_app/static/img/idcard.png')

    img = cv2.resize(img, (1100, 750))
    
    if identity_code is None:
        code_area = img[190:270, 520:970]
        code_area = cv2.resize(code_area, (450, 80))

        # code_area = cv2.morphologyEx(code_area, cv2.MORPH_OPEN, kernel)
        identity_code = pytesseract.image_to_string(code_area, lang='eng',
                                                    config='-c tessedit_char_whitelist=0123456789 --psm 7')
        cv2.imwrite('idcard_extract_app/static/img/code_area.png', code_area)

    if full_name == '' or full_name is None:
        name_area = img[260:350, 440:1050]
        name_area = cv2.resize(name_area, (610, 90))
        full_name = pytesseract.image_to_string(name_area, lang='vie')
        cv2.imwrite('idcard_extract_app/static/img/name_area.png', name_area)
       
