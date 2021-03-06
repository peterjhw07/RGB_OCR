import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import pandas as pd
import math

# Insert parameters
directory = r'C:\Users\Peter\Documents\Postdoctorate\Work\CAKE\Photos\M.17 LT INT Timelapse - DPA CAKE'  # input path
bounding_box = (510, 235, 940, 500)  # enter cropping bounds in the form (x1, y1, x2, y2)
deskew_angle = -6  # enter anticlockwise angle to rotate image for deskewing (0 if no rotation)
thresh_value = 95  # enter thresholding value (~10-200)
erod_it = 3  # enter number of eroding iterations (1-10)
dil_it = 1  # enter number of dilution iterations (1-10)
show_first_image = "Yes"  # enter "Y" or "Yes" if you would like to see first image modified and "No" if not
exportpath = r'C:\Users\Peter\Documents\Postdoctorate\Work\CAKE\Blank.xlsx'  # Excel export path
exportsheet = "Sheet1"  # enter Excel sheet for export

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)  # cv2.medianBlur(image, 5)

# thresholding
def thresholding(image):
    return cv2.threshold(image, thresh_value, 255, cv2.THRESH_BINARY)[1]  # + cv2.THRESH_OTSU

# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=erod_it)

# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=dil_it)

# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

# skew correction
def deskew(image):
    angle = deskew_angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# apply picture filters
def overall_filter(img):
    img = img.crop(bounding_box)
    img = np.array(img)
    img = get_grayscale(img)
    img = deskew(img)
    img = remove_noise(img)
    img = thresholding(img)
    img = erode(img)
    img = dilate(img)
    return img

# extract time photo was taken
def get_time_taken(path):
    return Image.open(path)._getexif()[36867]

# extract time photo was modified
def get_time_modified(path):
    return os.path.getmtime(path)

def pre_dec_8to0_switch(out_below_replace):
    if "8." in out_below_replace:
        out_below_replace = out_below_replace.replace('8.', '0.')
    return out_below_replace

def post_dec_8to0_switch(out_below_replace):
    if ".8" in out_below_replace:
        out_below_replace = out_below_replace.replace('.8', '.0')
    return out_below_replace

def pre_dec_3to0_switch(out_below_replace):
    if "3." in out_below_replace:
        out_below_replace = out_below_replace.replace('3.', '0.')
    return out_below_replace

def remove_space(out_below_replace):
    out_below_replace = out_below_replace.replace(' ', '')
    return out_below_replace

def only_symbol(out_below_replace):
    if out_below_replace == '.' or out_below_replace == '-' or out_below_replace == '':
        out_below_replace = '999'
    return out_below_replace

def point_first(out_below_replace):
    if out_below_replace[0] == '.':
        out_below_replace = out_below_replace[1:]
    return out_below_replace

def dash_not_point(out_below_replace):
    if '-' in out_below_replace and '.' not in out_below_replace:
        out_below_replace = out_below_replace.replace('-', '.')
    return out_below_replace

def dash_not_first(out_below_replace):
    if '-' in out_below_replace[1:]:
        out_below_replace = "".join((out_below_replace[0], out_below_replace[1:].replace('-', '')))
    return out_below_replace

def trunc(out_below_replace):
    out_below_replace = str(math.trunc((int(float(out_below_replace) * 100))) / 100)
    return out_below_replace

def swap_8to0(out_below_replace):
    it_check = max([0, it - 6])
    check_total = np.ndarray.tolist(last_digit[it_check:it - 1])
    if '8' in out_below_replace[-1]:
        check_total = str([val for sublist in check_total for val in sublist])
        if '8' not in check_total and '7' not in check_total and '6' not in check_total:
            if '8' not in check_total and '9' not in check_total and '1' not in check_total:
                out_below_replace = "".join((out_below_replace[0:-1], out_below_replace[-1].replace('8', '0')))
    return out_below_replace

def first8to0_switch(out_below_replace):
    if "8" in out_below_replace[0] and len(out_below_replace) == 3:
        out_below_replace = "".join((out_below_replace[0].replace('8', '0'), out_below_replace[1:]))
    return out_below_replace

def first6to0_switch(out_below_replace):
    if "6" in out_below_replace[0] and len(out_below_replace) == 3:
        out_below_replace = "".join((out_below_replace[0].replace('6', '0'), out_below_replace[1:]))
    return out_below_replace

def second8to0_switch(out_below_replace):
    if "8" in out_below_replace[1] and len(out_below_replace) == 3:
        out_below_replace = "".join((out_below_replace[0], out_below_replace[1].replace('8', '0'), out_below_replace[2:]))
    return out_below_replace

def len4to000(out_below_replace):
    if len(out_below_replace) > 3:
        out_below_replace = "000"
    return out_below_replace

def add_deci(out_below_replace):
    if len(out_below_replace) == 3:
        out_below_replace = "".join((out_below_replace[0:2], '.', out_below_replace[-1]))
    return out_below_replace

def grad_2to0adj1(out_below_replace):
    if "2" in out_below_replace[1] and len(out_below_replace) == 4 and it > 1:
        pred_val = (2 * float(total[it - 1])) - float(total[it - 2])
        sub_2 = abs((float(out_below_replace) - pred_val))
        sub_1 = abs(((int(float(out_below_replace) / 10) * 10) - pred_val))
        if sub_2 > sub_1:
            out_below_replace = "".join((out_below_replace[0], out_below_replace[1].replace('2', '1'), out_below_replace[2:]))
    return out_below_replace

def grad_8to0adj(out_below_replace):
    if "8" in out_below_replace[-1] and len(out_below_replace) == 4 and it > 1:
        pred_val = (2 * float(total[it - 1])) - float(total[it - 2])
        sub_8 = abs((float(out_below_replace) - pred_val))
        sub_0 = abs((int(float(out_below_replace)) - pred_val))
        if sub_8 > sub_0:
            out_below_replace = "".join((out_below_replace[0:3], out_below_replace[-1].replace('8', '0')))
    return out_below_replace

def grad_6to0adj2(out_below_replace):
    if "6" in out_below_replace[1] and len(out_below_replace) == 4 and it > 1:
        pred_val = (2 * float(total[it - 1])) - float(total[it - 2])
        sub_6 = abs((float(out_below_replace) - pred_val))
        sub_0 = abs(((int(float(out_below_replace) / 10) * 10) - pred_val))
        if sub_6 > sub_0:
            out_below_replace = "".join((out_below_replace[0], out_below_replace[1].replace('6', '0'), out_below_replace[2:]))
    return out_below_replace

def grad_6to0adj(out_below_replace):
    if "6" in out_below_replace[-1] and len(out_below_replace) == 4 and it > 1:
        pred_val = (2 * float(total[it - 1])) - float(total[it - 2])
        sub_6 = abs((float(out_below_replace) - pred_val))
        sub_0 = abs((int(float(out_below_replace)) - pred_val))
        if sub_6 > sub_0:
            out_below_replace = "".join((out_below_replace[0:3], out_below_replace[-1].replace('6', '0')))
    return out_below_replace

# apply data manipulations
def data_manip(out_below_replace):
    out_below_replace = remove_space(out_below_replace)
    out_below_replace = only_symbol(out_below_replace)
    out_below_replace = first8to0_switch(out_below_replace)
    out_below_replace = first6to0_switch(out_below_replace)
    out_below_replace = second8to0_switch(out_below_replace)
    out_below_replace = remove_space(out_below_replace)
    out_below_replace = len4to000(out_below_replace)
    out_below_replace = add_deci(out_below_replace)
    out_below_replace = grad_2to0adj1(out_below_replace)
    out_below_replace = grad_8to0adj(out_below_replace)
    out_below_replace = grad_6to0adj2(out_below_replace)
    out_below_replace = grad_6to0adj(out_below_replace)
    return out_below_replace

files = os.listdir(directory)
it_num = len(files)

total = np.empty((it_num, 1))
total_time_data = []
last_digit = np.empty((it_num, 1))
it = 0

if "Y" in show_first_image:
    current_img = os.path.join(directory, os.listdir(directory)[int(it_num / 2)])
    img = Image.open(current_img)
    img = overall_filter(img)
    plot_col = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(plot_col)
    plt.show()

for filename in files:
    with open(os.path.join(directory, filename)) as current_img:
        img = Image.open(current_img.name)

        # img_time_data = get_date_taken(current_img.name)
        img_time_data = get_time_modified(current_img.name)
        total_time_data.append(img_time_data)

        img = overall_filter(img)

        out_below = pytesseract.image_to_string(img, lang="letsgodigital",
                    config='-c tessedit_char_whitelist=0123456789 --psm 7')

        out_below_replace = out_below.strip()
        out_below_replace = data_manip(out_below_replace)

        # print("Modified Output:", out_below_replace)
        print([out_below, out_below_replace])
        total[it] = out_below_replace
        last_digit[it] = out_below_replace[-1]
        it = it + 1

export_files = np.array(files)
export_total = np.ndarray.tolist(total)
exportdf = pd.DataFrame({"File": export_files, "Date time": total_time_data, "Light intensity / Lux": export_total})
exportdf['Light intensity / Lux'] = exportdf['Light intensity / Lux'].str[0]
writer = pd.ExcelWriter(exportpath, engine='openpyxl')
exportdf.to_excel(writer, exportsheet, index=False)
writer.save()