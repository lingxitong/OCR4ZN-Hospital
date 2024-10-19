import os
from PIL import Image

def get_slide_type(OCR_text):
    for text in OCR_text:
        if 'D2-40' in text or 'd2-40' in text:
            return 'D2-40'
        if 'GATA-3' in text or 'gata-3' in text:
            return 'GATA-3'
        if 'CD-31' in text or 'cd-31' in text:
            return 'CD-31'
        if 'Ki-67' in text or 'ki-67' in text:
            return 'KI-67'
        if 'PD-L1' in text or 'pd-l1' in text:
            return 'PD-L1'
        if 'TTF-1' in text or 'ttf-1' in text:
            return 'TTF-1'
        if 'PR' in text or 'pr' in text:
            return 'PR'
        if 'Her-2' in text or 'her-2' in text:
            return 'Her-2'
        if 'PSA' in text or 'psa' in text:
            return 'PSA'
        if 'ER' in text or 'er' in text:
            return 'ER'
        if 'syn' in text:
            return 'SYN'
        if 'pax' in text:
            return 'PAX-8'
        if 'Galectin' in text:
            return 'GALECTIN-3'
        if 'CD56' in text:
            return 'CD-56'
        if 'HNF1-B' in text:
            return 'HNF1-B'
        if 'P53' in text or 'p53' in text:
            return 'P53'
        if 'PMS2' in text or 'pms2' in text:
            return 'PMS2'
        if 'MUC6' in text or 'muc6' in text:
            return 'MUC6'
        if 'MUC5AC' in text or 'muc5ac' in text:
            return 'MUC5AC'
        if 'MSH6' in text or 'msh6' in text:
            return 'MSH6'
        if 'CD20' in text or 'cd20' in text:
            return 'CD-20'
        if 'MSH2' in text or 'msh2' in text:
            return 'MSH2'
        if 'MLH1' in text or 'mlh1' in text:
            return 'MLH1'
        if 'INSM1' in text or 'insm1' in text:
            return 'INSM1'
        if 'P63' in text or 'p63' in text:
            return 'P63'
        if 'MUC-6' in text or 'muc-6' in text:
            return 'MUC-6'
        if 'CK20' in text or 'ck20' in text:
            return 'CK20'
        if 'EBERpb' in text or 'eberpb' in text:
            return 'EBERpb'
        if 'TRPS1' in text or 'trps1' in text:
            return 'TRPS1'
        if 'SF-1' in text or 'sf-1' in text:
            return 'SF-1'
        if 'GZB' in text or 'gzb' in text:
            return 'GZB'
        if 'TIA-1' in text or 'tia-1' in text:
            return 'TIA-1'
        if 'CD3' in text or 'cd3' in text:
            return 'CD-3'
        if 'CMV' in text or 'cmv' in text:
            return 'CMV'
        if 'Clad18.2' in text:
            return 'Clad18.2'
        if 'CK7' in text or 'ck7' in text:
            return 'CK7'
        if 'MUC-1' in text or 'muc-1' in text or 'MUC1' in text or 'muc1' in text:
            return 'MUC-1'
        if 'MUC-2' in text or 'muc-2' in text or 'MUC2' in text or 'muc2' in text:
            return 'MUC-2'
        if 'MUC-3' in text or 'muc-3' in text or 'MUC3' in text or 'muc3' in text:
            return 'MUC-3'
        if 'MUC-4' in text or 'muc-4' in text:
            return 'MUC-4'
        if 'MUC-5' in text or 'muc-5' in text:
            return 'MUC-5'
        if 'MUC5AC' in text or 'muc5ac' in text:
            return 'MUC5AC'
        if 'PAX8' in text or 'pax8' in text:
            return 'PAX-8'
        if 'VILLIN' in text or 'villin' in text:
            return 'VILLIN'
        if 'SMA' in text or 'sma' in text:
            return 'SMA'
        if 'CK19' in text or 'ck19' in text:
            return 'CK19'
        if 'S-100' in text or 's-100' in text:
            return 'S-100'
        if 'SATB2' in text or 'satb2' in text or 'SATB-2' in text or 'satb-2' in text:
            return 'SATB2'
    return 'HE' 

def judge_has_rename(basename):
    rename_label = ['-HE','D2-40','GATA-3','CD-31','KI-67','PD-L1','TTF-1','PR','Her-2','PSA','ER','SYN','PAX-8','GALECTIN-3','CD-56','HNF1-B','P53','PMS2','MUC6','MUC5AC','MSH6','CD-20','MSH2','MLH1','INSM1','P63','MUC-6','CK20','EBERpb','TRPS1','SF-1','GZB','TIA-1','CD-3','CMV','Clad18.2','CK7',
                    'MUC-1','MUC-2','MUC-3','MUC-4','MUC-5','MUC5AC','PAX8','VILLIN','SMA','CK19','S-100','SATB2']  
    if any(label in basename for label in rename_label):
        return True

def remove_chinese(text):
    return ''.join([char for char in text if not '\u4e00' <= char <= '\u9fa5'])

def remove_chinese_from_OCR_text(OCR_text):
    return [remove_chinese(text) for text in OCR_text]
def fileter_path_and_id(path_or_id):
    # Remove leading and trailing hyphens and spaces
    path_or_id = path_or_id.strip('<').strip()
    path_or_id = path_or_id.strip('-').strip()
    path_or_id = path_or_id.strip('<').strip()
    path_or_id = path_or_id.strip('≤').strip()
    path_or_id = path_or_id.strip('←').strip()
    
    return path_or_id
        
def judge_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            return True
    return False

def remove_chinese(text):
    return ''.join([char for char in text if not '\u4e00' <= char <= '\u9fa5'])

def remove_spaces(text):
    return text.replace(' ', '')

def is_substring(substring, string):
    return substring in string

def is_not_substring(substring, string):
    return substring not in string

def filter_OCR_text(OCR_text):
    OCR_text = [text for text in OCR_text if text != '']
    # OCR_text = [text for text in OCR_text if is_not_substring('病', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('理', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('武', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('中', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('医', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('院', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('南', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('大', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('学', text)]
    # OCR_text = [text for text in OCR_text if is_not_substring('汉', text)]
    OCR_text = [text for text in OCR_text if is_not_substring('=', text)]
    OCR_text = [text for text in OCR_text if is_not_substring('/', text)]
    OCR_text = remove_chinese_from_OCR_text(OCR_text)
    OCR_text = [text.replace(' ','') for text in OCR_text]
    OCR_text = [text for text in OCR_text if text != '']
    # OCR_text = [text for text in OCR_text if text.startswith('0') == False] 
    return OCR_text
def is_alphanumeric(text):
    return text.isalnum()


def get_path_id_Baidu(OCR_text):
    # 首先处理HE切片的编号
    # path_id = _path + _id
    OCR_text_length = len(OCR_text)
    if OCR_text_length < 2:
        return None
    if OCR_text_length > 2:
        OCR_text = [text for text in OCR_text if judge_chinese(text) == False]
        OCR_text_length = len(OCR_text)
    if OCR_text_length == 2:
        First_text = remove_spaces(remove_chinese(OCR_text[0]))
        Second_text = remove_spaces(remove_chinese(OCR_text[1]))
        if len(First_text) == 0 or len(Second_text) == 0:
            return None
        if First_text == '‖‖' or Second_text == '‖‖' or First_text == '‖！' or Second_text == '‖！':
            return None
        First_L = len(First_text)
        Second_L = len(Second_text)
        _path = First_text if First_L > Second_L else Second_text
        _id = First_text if First_L <= Second_L else Second_text
        _path = fileter_path_and_id(_path)
        _id = fileter_path_and_id(_id)
        path_id = _path + '-' + _id
        return path_id
    return None


def is_number_or_alphanumeric_with_digit(text):
    return text.isalnum() and any(char.isdigit() for char in text)

def find_possible_path_id(OCR_text):
    for text in OCR_text:
        num = text.count('-')
        if num == 2:
            return text
        if num == 1:
            jnum = text.replace('-', '0')
            if is_alphanumeric(jnum):
                return text
    return None
        
def find_id(OCR_text):
    for text in OCR_text:
        if len(text) == 2:
            if is_number_or_alphanumeric_with_digit(text):
                return text
        if len(text) == 1:
            if is_number_or_alphanumeric_with_digit(text):
                return text
            if text.isalnum():
                return text
        if len(text) == 3:
            if is_number_or_alphanumeric_with_digit(text):
                return text
    return None
    

def get_path_id_Paddle(Real_OCR_texts):
    possible_path_id = find_possible_path_id(Real_OCR_texts)
    if possible_path_id != None:
        if possible_path_id.count('-') == 2:
            return possible_path_id
        else:
            posid = find_id(Real_OCR_texts)
            if posid != None:
                return possible_path_id + '-' + posid
    return None
                
def is_all_digits(text):
    return text.isdigit()
    
def Find_Real_OCR_Text(OCR_text_0, OCR_text_90, OCR_text_180, OCR_text_270):
    all_OCRs = [OCR_text_0, OCR_text_90, OCR_text_180, OCR_text_270]
    Is_maybe = [0, 0, 0, 0]
    Leg = [len(OCR_text_0), len(OCR_text_90), len(OCR_text_180), len(OCR_text_270)]
    i = 0
    for OCR_text in all_OCRs:
        for sub_text in OCR_text:
            if sub_text.count('-') == 2:
                if len(sub_text) > 5:
                    judge = sub_text.replace('-', '0')
                    if is_alphanumeric(judge):
                        Is_maybe[i] = 1
            if sub_text.count('-') == 1:
                if len(sub_text) > 5:
                    judge = sub_text.replace('-', '0')
                    if is_all_digits(judge):
                        Is_maybe[i] = 1
        i += 1
    
    if sum(Is_maybe) == 0:
        return None
    else:
        max_leg_index = -1
        max_leg_value = -1
        for index, value in enumerate(Is_maybe):
            if value == 1 and Leg[index] > max_leg_value:
                max_leg_value = Leg[index]
                max_leg_index = index
        return max_leg_index
        
         
         
def rotate_and_save_image(image_path):
    image = Image.open(image_path)
    rotations = [90, 180, 270]
    for angle in rotations:
        rotated_image = image.rotate(angle, expand=True)
        rotated_image_path = image_path.replace('.jpg', f'_{angle}.jpg')
        rotated_image.save(rotated_image_path)
        print(f'Saved rotated image: {rotated_image_path}')
    return image_path.replace('.jpg', '_90.jpg'), image_path.replace('.jpg', '_180.jpg'), image_path.replace('.jpg', '_270.jpg')

def get_OCR_ANS(img_path,ocr):
    result = ocr.ocr(img_path, cls=True)
    OCR_text = []
    for line in result:
        for sub_line in line:
            OCR_text.append(sub_line[1][0])
    return OCR_text

def uniform_rename(wsi_path, new_path,label_path, new_label_path):
    os.rename(wsi_path, new_path)
    os.rename(label_path, new_label_path)
    print(f'\033[92mRenamed {os.path.basename(wsi_path)} to {os.path.basename(new_path)}\033[0m')
