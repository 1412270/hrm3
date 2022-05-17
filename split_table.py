#  Copyright (c) 2021 Fujinet Systems JSC. All rights reserved.
import cv2
from itertools import groupby


sample_file = "sample_2_2.png"
sample_data = [[396, 172, 688, 194], [155, 185, 184, 194], [396, 185, 455, 194], [396, 194, 455, 217],
               [184, 194, 396, 217], [455, 194, 505, 217], [505, 194, 551, 217], [551, 194, 602, 217],
               [602, 194, 688, 217], [155, 194, 184, 217], [396, 217, 455, 235], [184, 217, 396, 235],
               [455, 217, 505, 235], [505, 217, 551, 235], [551, 217, 602, 235], [602, 217, 688, 235],
               [155, 217, 184, 235], [396, 235, 455, 446], [184, 235, 396, 446], [455, 235, 505, 446],
               [505, 235, 551, 446], [551, 235, 602, 446], [602, 235, 688, 446], [155, 235, 184, 446],
               [396, 446, 455, 458], [455, 446, 505, 458], [505, 446, 551, 458], [271, 446, 355, 458],
               [355, 446, 396, 458], [155, 446, 271, 463], [271, 458, 355, 463], [355, 458, 688, 515],
               [271, 463, 355, 480], [155, 463, 271, 480], [271, 480, 355, 498], [155, 480, 271, 498],
               [271, 498, 355, 515], [155, 498, 271, 515], [155, 515, 688, 533], [355, 533, 688, 616],
               [155, 533, 355, 616], [155, 616, 688, 633], [396, 120, 688, 172], [155, 120, 396, 185]]


def split_table(field_list, img_path):
    def key_rows(x): return x[0]

    img = cv2.imread(img_path)
    sort_table = [list(v) for k, v in groupby(field_list, key_rows)]

    for index, cell in enumerate(sort_table):
        cut_cell = img[cell[1]:cell[1]+cell[3], cell[0]:cell[0]+cell[0]]
        cv2.imwrite("C:/Users/ASUS/OneDrive/Documents/table_split/" + str(index) + ".png", cut_cell)


def get_data_from_table(ocr_field_page):
    rs = []
    if len(ocr_field_page.ocr_fields) > 0:
        for index, ocr_field in enumerate(ocr_field_page.ocr_fields):
            rect = {
                'x': ocr_field.x,
                'y': ocr_field.y,
                'w': ocr_field.w,
                'h': ocr_field.h
            }
            get_img = Global.project_manager.get_image_from_ocr_field_folder_by_id(ocr_field.ocr_field_id)
            ocr_text = Global.ocr.do_ocr(get_img, 'eng+vie')
            ocr_field.set_ocr_field(
                ocr_field.labels_id,
                ocr_field.note,
                ocr_text,
                rect
            )


split_table(sample_data, "C:/Users/ASUS/OneDrive/Documents/invoice/sample_2_2.png")
