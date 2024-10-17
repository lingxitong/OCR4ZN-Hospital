from PIL import JpegImagePlugin
import os
import glob
JpegImagePlugin._getmp = lambda x: None
from tqdm import tqdm
import sdpc
from paddleocr import PaddleOCR, draw_ocr
import os
import glob
from tqdm import tqdm
from utils import *
#################################### 指定参数
WSI_DIR_LIST = [
    r'F:\2024-08-27',
    r'F:\2024-08-28',
    r'F:\2024-08-29',
    r'F:\2024-08-30',
    r'F:\2024-09-01',
    r'F:\2024-09-02',
    r'F:\2024-09-03',
    r'F:\2024-09-04',
    r'F:\2024-09-05',
    r'F:\2024-09-06',
    r'F:\2024-09-07',
    r'F:\2024-09-08',
    r'F:\2024-09-09',
    r'F:\2024-09-10',
    r'F:\2024-09-11',
    r'F:\2024-09-12',
    r'F:\2024-09-13'
]
 
WORK_DIR = r'F:\WORK_DIR'

#################################### 指定参数


if __name__ == '__main__':
    if not os.path.exists(WORK_DIR):
        os.makedirs(WORK_DIR)
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    wsi_list = []
    for wsi_dir in WSI_DIR_LIST:
        files = glob.glob(os.path.join(wsi_dir, '*.sdpc'))
        files.sort()  # Sort the files to maintain order
        wsi_list.extend(files)
            
    for wsi_path in tqdm(wsi_list):
        try:
            print('当前文件：', wsi_path)
            label_path = os.path.join(WORK_DIR, os.path.basename(wsi_path).replace('.sdpc', '.jpg'))
            if os.path.exists(label_path):
                print('已经完成重命名：')
                continue
            basename = os.path.basename(wsi_path)
            wsi = sdpc.Sdpc(wsi_path)
            wsi.saveLabelImg(label_path)
            img_path90,img_path180,img_path270 = rotate_and_save_image(label_path)
            OCR_text_0 = get_OCR_ANS(label_path,ocr)
            OCR_text_90 = get_OCR_ANS(img_path90,ocr)
            OCR_text_180 = get_OCR_ANS(img_path180,ocr)
            OCR_text_270 = get_OCR_ANS(img_path270,ocr)
            OCR_text_0 = filter_OCR_text(OCR_text_0)
            OCR_text_90 = filter_OCR_text(OCR_text_90)
            OCR_text_180 = filter_OCR_text(OCR_text_180)
            OCR_text_270 = filter_OCR_text(OCR_text_270)
            Real_OCR_text = Find_Real_OCR_Text(OCR_text_0,OCR_text_90,OCR_text_180,OCR_text_270)
            if Real_OCR_text == None:
                print('解析OCR失败')
                continue
            elif Real_OCR_text == 0:
                Real_OCR_texts = OCR_text_0
            elif Real_OCR_text == 1:
                Real_OCR_texts = OCR_text_90
            elif Real_OCR_text == 2:
                Real_OCR_texts = OCR_text_180
            elif Real_OCR_text == 3:
                Real_OCR_texts = OCR_text_270

            slide_type = get_slide_type(Real_OCR_texts)
            print('slide_type:', slide_type)
            path_id = get_path_id_Paddle(Real_OCR_texts)
            path_id = path_id.upper()
            print('path_id:', path_id)
            if path_id == None:
                print('解析path_id失败')
                continue
            
            new_name = path_id + '-' + slide_type + '.sdpc'
            new_name = new_name.replace('--', '-')
            new_path = wsi_path.replace(basename, new_name)
            new_label_path = os.path.join(WORK_DIR, new_name.replace('.sdpc', '.jpg'))
            uniform_rename(wsi_path, new_path,label_path, new_label_path)
        except:
            continue

