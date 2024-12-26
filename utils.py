import os
from PIL import Image
import psutil
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
        if 'PD-L1' in text or 'pd-l1' in text or 'PDL-1' in text:
            return 'PD-L1'
        if 'TTF-1' in text or 'ttf-1' in text:
            return 'TTF-1'
        if 'PR' in text or 'pr' in text:
            return 'PR'
        if 'Her-2' in text or 'her-2' in text or 'HER-2' in text or 'Her' in text:
            return 'Her-2'
        if 'PSA' in text or 'psa' in text:
            return 'PSA'
        if 'ER' in text or 'er' in text:
            return 'ER'
        if 'syn' in text or 'Syn' in text:
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
        if 'PHH3' in text or 'phh3' in text:
            return 'PHH3'        
        if 'Desmin' in text or 'DESMIN' in text or 'desmin' in text:
            return 'Desmin'
        if 'CerbB-2'  in text or 'cerbb-2' in text:
            return 'CerbB-2'
        if 'CATENIN' in text or 'catenin' in text:
            return 'catenin'
        if 'CK' in text or 'ck' in text:
            return 'CK'
        if 'CDX2' in text or 'cdx2' in text:
            return 'CDX2'
        if 'CD34' in text or 'cd34' in text:
            return 'CD34'
        if '网染' in text:
            return '网染'
        if '网状纤维' in text:
            return '网状纤维'
        if '普鲁士蓝' in text:
            return '普鲁士蓝'
        if 'PTEN' in text or 'pten' in text:
            return 'PTEN'
        if 'SALL4' in text or 'sall4' in text:
            return 'SALL4'
        if 'VIMENTIN' in text or 'vimentin' in text:
            return 'VIMENTIN'
        if 'MC' in text or 'mc' in text:
            return 'MC'
        if 'CD45' in text or 'cd45' in text:
            return 'CD45'
        if 'CgA' in text or 'cga' in text:
            return 'CgA'
        if 'MOC31' in text or 'moc31' in text:
            return 'MOC31'
        if 'NeuN' in text or 'neun' in text:
            return 'NeuN'
        if 'DOG-1' in text:
            return 'DOG-1'
        if 'GS' in text:
            return 'GS'
        if 'Vimentin' in text:
            return 'Vimentin'
        if 'CD117' in text:
            return 'CD117'
        if 'WT-1' in text:
            return 'WT-1'
        if 'Hepatocyte' in text:
            return 'Hepatocyte'
        if 'MASSON' in text:
            return 'MASSON'
        if 'FRA' in text:
            return 'FRA'
        if 'Gastrin' in text:
            return 'Gastrin'
        if 'Moc31' in text:
            return 'Moc31'
        if 'P40' in text:
            return 'P40'
        if 'SDHB' in text:
            return 'SDHB'
        if 'PTEN' in text:
            return 'PTEN'
        if 'SALL4' in text:
            return 'SALL4'
        # CerbB-2 catenin HMB45 CD34 SDHB CD31 CK CgA TPO MC DESM CDX2 BRAF CK DPC4 ERG NapsinA MOC31 SALL4 SYN NeuN  VIMENTIN PTEN
     
    
    return 'HE' 

def judge_has_rename(basename):
    # rename_label = ['HE','D2-40','GATA-3','CD-31','KI-67','PD-L1','TTF-1','PR','Her-2','PSA','ER','SYN','PAX-8','GALECTIN-3','CD-56','HNF1-B','P53','PMS2','MUC6','MUC5AC','MSH6','CD-20','MSH2','MLH1','INSM1','P63','MUC-6','CK20','EBERpb','TRPS1','SF-1','GZB','TIA-1','CD-3','CMV','Clad18.2','CK7',
    #                 'MUC-1','MUC-2','MUC-3','MUC-4','MUC-5','MUC5AC','PAX8','VILLIN','SMA','CK19','S-100','SATB2','PHH3','Desmin','CerbB-2','CK',]  
    rename_label = ['D2-40','GATA-3','CD-31','KI-67','PD-L1','TTF-1','PR','Her-2','PSA','ER','SYN','PAX-8','GALECTIN-3',
                'CD-56','HNF1-B','P53','PMS2','MUC6','MUC5AC','MSH6','CD-20','MSH2','MLH1','INSM1','P63','MUC-6','CK20',
                'EBERpb','TRPS1','SF-1','GZB','TIA-1','CD-3','CMV','Clad18.2','CK7','MUC-1','MUC-2','MUC-3','MUC-4','MUC-5','MUC-6','MUC-7','MUC'
                'MUC5AC','PAX8','VILLIN','SMA','CK19','S-100','SATB2','SATB-2','Ki-67','普鲁士蓝','网状纤维','PAS','MASSON','DPC4','Desmin','DOG-1','S100','SDHB','CD117','ck','HER-2','CLAD8.2','CK','网染',
                'CDX2','CAM5.2','P53yul','PHH3','phh3','dog-1','DESMIN','SALL4','Gly3','S100P','SDHBM','STAT6M','DOG1','KI67','Cerb-2','CD31','CD34','HMB45','CD10','MIB1','Pax-8','ki67','Ki67','P16','Ki-67',
                'Mammag','MUC1','KI67','SMA','AR','CITOGLAS','Her-2','P53','P63','CK5/6','CK5','CK6','CK7','CK8','CK18','CK19','CK20','CK22','CK23','CK34','CK35','CK56','CK68','CK72','CK73','CK74','CK75','CK76','CK77','CK78','CK79','CK80','CK81','CK82','CK83','CK84','CK85','CK86','CK87','CK88','CK89','CK90','CK91','CK92','CK93','CK94','CK95','CK96','CK97','CK98','CK99','CK100','CK101','CK102','CK103','CK104','CK105','CK106','CK107','CK108','CK109','CK110','CK111','CK112','CK113','CK114','CK115','CK116','CK117','CK118','CK119','CK120','CK121','CK122','CK123','CK124','CK125','CK126','CK127','CK128','CK129','CK130','CK131','CK132','CK133',
                'CK134','CK135','CK136','CK137','CK138','CK139','CK140','CK141','CK142','CK143','CK144','CK145','CK146','CK147','CK148','CK149','CK150','CK151','CK152','CK153','CK154','CK155','CK156','CK157','CK158','CK159','CK160','CK161','CK162','CK163','CK164','CK165','CK166','CK167','CK168','CK169','CK170','CK171','CK172','CK173','CK174','CK175','CK176','CK177','CK178','CK179','CK180','CK181','CK182','CK183','CK184','CK185','CK186','CK187','CK188','CK189','CK190','CK191','CK192','CK193','CK194','CK195','CK196','CK197','CK198','CK199','CK200','CK201','CK202','CK203','CK204','CK205','CK206','CK207','CK208','CK209','CK210','CK211','CK212','CK213','CK214','CK215','CK216','CK217','CK218','CK219','CK220','CK221',
                'ER','CD','SALL','DPC','PHH','GS','Vimentin','WT-1','Hepatocyte','FRA','Gastrin','P40','SALL4','SDHB','PTEN']
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


def get_memory_usage_percentage():
    memory_info = psutil.virtual_memory()
    memory_usage_percentage = (memory_info.used / memory_info.total) * 100
    return memory_usage_percentage

