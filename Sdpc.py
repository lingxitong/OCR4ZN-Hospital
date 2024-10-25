import numpy.ctypeslib as npCtypes
import ctypes
from ctypes import *
import gc
import os
import sys
from sdpc.Sdpc_struct import SqSdpcInfo

import numpy as np
import json
from tqdm import tqdm
import copy
from PIL import Image



# windows下环境配置，调用.dll文件
dirname, _ = os.path.split(os.path.abspath(__file__))
os.chdir(os.path.join(dirname, 'DLL\\dll'))
sys.path.append(os.path.join(dirname, 'DLL\\dll'))
soPath = os.path.join(dirname, 'DLL\\dll\\DecodeSdpcDll.dll')
# 接口指针设置
so = ctypes.CDLL(soPath)
so.GetLayerInfo.restype = POINTER(c_char)
so.SqGetRoiRgbOfSpecifyLayer.argtypes = [POINTER(SqSdpcInfo), POINTER(POINTER(c_uint8)),
                                             c_int, c_int, c_uint, c_uint, c_int]
so.SqGetRoiRgbOfSpecifyLayer.restype = c_int
so.SqOpenSdpc.restype = POINTER(SqSdpcInfo)
so.GetLabelJpeg.argtypes = [POINTER(SqSdpcInfo), POINTER(c_uint), POINTER(c_uint), POINTER(c_size_t)]
so.GetLabelJpeg.restype = POINTER(c_uint8)


class Sdpc:

    def __init__(self, sdpcPath):
        print(sdpcPath)
        self.sdpc = self.readSdpc(sdpcPath)
        self.level_count = self.getLevelCount()
        self.level_downsample = self.getLevelDownsamples()
        self.level_dimensions = self.getLevelDimensions()

    def getRgb(self, rgbPos, width, height):

        intValue = npCtypes.as_array(rgbPos, (height, width, 3))
        return intValue
    
    def saveLabelImg(self, save_path):
        wPos = POINTER(c_uint)(c_uint(0))
        hPos = POINTER(c_uint)(c_uint(0))
        sizePos = POINTER(c_size_t)(c_size_t(0))
        rgb_pos = so.GetLabelJpeg(self.sdpc, wPos, hPos, sizePos)
        with open(save_path, 'bw') as f:
            buf = bytearray(rgb_pos[:sizePos.contents.value])
            f.write(buf)
        f.close()
        
    def readSdpc(self, fileName):

        sdpc = so.SqOpenSdpc(c_char_p(bytes(fileName, 'gbk')))
        sdpc.contents.fileName = bytes(fileName, 'gbk')

        return sdpc

    def getLevelCount(self):

        return self.sdpc.contents.picHead.contents.hierarchy

    def getLevelDownsamples(self):

        levelCount = self.getLevelCount()
        rate = self.sdpc.contents.picHead.contents.scale
        rate = 1 / rate
        _list = []
        for i in range(levelCount):
            _list.append(rate ** i)
        return tuple(_list)

    def read_region(self, location, level, size):

        startX, startY = location
        scale = self.level_downsample[level]
        startX = int(startX / scale)
        startY = int(startY / scale)

        width, height = size

        rgbPos = POINTER(c_uint8)()
        rgbPosPointer = byref(rgbPos)
        so.SqGetRoiRgbOfSpecifyLayer(self.sdpc, rgbPosPointer, width, height, startX, startY, level)
        rgb = self.getRgb(rgbPos, width, height)[..., ::-1]
        rgbCopy = rgb.copy()

        so.Dispose(rgbPos)
        del rgbPos
        del rgbPosPointer
        gc.collect()

        return rgbCopy

    def getLevelDimensions(self):

        def findStrIndex(subStr, str):
            index1 = str.find(subStr)
            index2 = str.find(subStr, index1 + 1)
            index3 = str.find(subStr, index2 + 1)
            index4 = str.find(subStr, index3 + 1)
            return index1, index2, index3, index4

        levelCount = self.getLevelCount()
        levelDimensions = []
        for level in range(levelCount):
            layerInfo = so.GetLayerInfo(self.sdpc, level)
            count = 0
            byteList = []
            while (ord(layerInfo[count]) != 0):
                byteList.append(layerInfo[count])
                count += 1

            strList = [byteValue.decode('utf-8') for byteValue in byteList]
            str = ''.join(strList)

            equal1, equal2, equal3, equal4 = findStrIndex("=", str)
            line1, line2, line3, line4 = findStrIndex("|", str)

            rawWidth = int(str[equal1 + 1:line1])
            rawHeight = int(str[equal2 + 1:line2])
            boundWidth = int(str[equal3 + 1:line3])
            boundHeight = int(str[equal4 + 1:line4])
            w, h = rawWidth - boundWidth, rawHeight - boundHeight
            levelDimensions.append((w, h))

        return tuple(levelDimensions)

    def close(self):

        so.SqCloseSdpc(self.sdpc)


# def getcoords(sdpc_path, label_dic, save_dir, ROI_size=(224, 224), ):
#     template = copy.deepcopy(label_dic['LabelRoot']['LabelInfoList'][0])
#     Ref_area = template['LabelInfo']['Dimensioning']
#     Ref_area, postfix = float(Ref_area[:-3]), Ref_area[-3:]
#     _, _, Ref_w, Ref_h = template['LabelInfo']['Rect'].split(', ')
#     Ref_w, Ref_h = int(Ref_w), int(Ref_h)
#     Ref_area = Ref_area / (Ref_w * Ref_h) * ROI_size[0] * ROI_size[1]
#     Ref_area = '%.3f%s' % (Ref_area, postfix)
#     rec_index = len(label_dic['LabelRoot']['LabelInfoList']) + 1
#     template['LabelInfo']['Dimensioning'] = rec_index
#     template['LabelInfo']['PenColor'] = 'Red'
#
#
#
#     #------每个轮廓的最小矩形-------
#     template1 = copy.deepcopy(label_dic['LabelRoot']['LabelInfoList'][0])
#     # Ref_area1 = template1['LabelInfo']['Dimensioning']
#     # Ref_area1, psotfix1 = float(Ref_area1[:-3]), Ref_area1[-3:]
#     rec_index1 = len(label_dic['LabelRoot']['LabelInfoList']) + 1
#     template1['LabelInfo']['Dimensioning'] = rec_index1
#     template1['LabelInfo']['PenColor'] = 'Blue'
#
#
#
#
#     sdpc, _, _ = Sdpc(sdpc_path)
#     idx = 0
#     for counter in tqdm(label_dic['LabelRoot']['LabelInfoList'][1:]):              #遍历的是自己画的所有标注轮廓
#         idx += 1
#         ROI_path = 'ROI' + '%d' % idx
#         # 获取闭合曲线的spa，spb
#         Points = list(zip(*[list(map(int, point.split(', '))) for point in counter['PointsInfo']['ps']]))
#         _SPA_x, _SPA_y = (min(Points[0]), min(Points[1]))                  #相对坐标的 最小值 x值，y值
#         _SPB_x, _SPB_y = (max(Points[0]), max(Points[1]))                  #相对坐标的 最大值 x值，y值
#
#         # 将其化归到40倍坐标下
#         Ref_x, Ref_y, _, _ = counter['LabelInfo']['CurPicRect'].split(', ')           #5571  3360
#         Ref_x, Ref_y = int(Ref_x), int(Ref_y)
#         ratio = counter['LabelInfo']['ZoomScale']                                   # 40倍的小矩形是0.5，     我自己画的是0.125，这里是0.125
#         SPA_x = int((_SPA_x + Ref_x) / ratio * mag_dic['40x'] - Ref_x)
#         SPA_y = int((_SPA_y + Ref_y) / ratio * mag_dic['40x'] - Ref_y)
#         SPB_x = int((_SPB_x + Ref_x) / ratio * mag_dic['40x'] - Ref_x)
#         SPB_y = int((_SPB_y + Ref_y) / ratio * mag_dic['40x'] - Ref_y)
#         # *************************************************
#         Pointsx = []
#         Pointsy = []
#         for i in range(len(Points[0])):
#             Pointsx.append(int((Points[0][i] + Ref_x) / ratio * mag_dic['40x'] - Ref_x))
#             Pointsy.append(int((Points[1][i] + Ref_y) / ratio * mag_dic['40x'] - Ref_y))
#         Pointslist = polygon_preprocessor([Pointsx, Pointsy])
#         # *************************************************
#         # 计算循环次数
#         x0 = np.mean(np.array(Pointsx[:-1]))
#         y0 = np.mean(np.array(Pointsy[:-1]))
#         start_kx = -np.ceil((x0 - SPA_x - (ROI_size[0]+offset[0])/2) / (ROI_size[0]+offset[0]))
#         end_kx = np.ceil((SPB_x - x0 - (ROI_size[0]+offset[0])/2) / (ROI_size[0]+offset[0]))
#         start_ky = -np.ceil((y0 - SPA_y - (ROI_size[1]+offset[1])/2) / (ROI_size[1]+offset[1]))
#         end_ky = np.ceil((SPB_y - y0 - (ROI_size[1]+offset[1])/2) / (ROI_size[1]+offset[1]))
#         cX = int((SPB_x - SPA_x) / (ROI_size[0] + offset[0]))
#         cY = int((SPB_y - SPA_y) / (ROI_size[1] + offset[1]))
#
#         # 循环操作，生成标注
#
#         big_patch_w = int((BIG_PATCH_SIZE[0] * 2) / (4 ** patch_level))
#         big_patch_h = int((BIG_PATCH_SIZE[1] * 2) / (4 ** patch_level))
#
#         need_patch_w = int(((SPB_x - SPA_x) * 2) / (4 ** patch_level))
#         need_patch_h = int(((SPB_y - SPA_y) * 2) / (4 ** patch_level))
#
#         # start_kx1 = -np.ceil((x0 - SPA_x - (BIG_PATCH_SIZE[0] + offset[0]) / 2) / (BIG_PATCH_SIZE[0] + offset[0]))
#         # start_ky1 = -np.ceil((y0 - SPA_y - (BIG_PATCH_SIZE[1] + offset[1]) / 2) / (BIG_PATCH_SIZE[1] + offset[1]))
#
#         # 修改大patch模版中的相关变量
#         # rect_x1 = x0 + SPA_x * (BIG_PATCH_SIZE[0] + offset[0]) - BIG_PATCH_SIZE[0] / 2
#         # rect_y1 = y0 + SPA_y * (BIG_PATCH_SIZE[1] + offset[1]) - BIG_PATCH_SIZE[0] / 2
#
#         template1['LabelInfo']['StartPoint'] = '%d, %d' % (SPA_x, SPA_y)
#         template1['LabelInfo']['EndPoint'] = '%d, %d' % (
#             SPA_x + int(SPB_x - SPA_x), SPA_y + int(SPB_y - SPA_y))
#         template1['LabelInfo']['Rect'] = '%d, %d, %d, %d' % (
#             SPA_x, SPA_y, int(SPB_x - SPA_x),
#             int(SPB_y - SPA_y))
#
#         big_img = sdpc.read_region(((SPA_x + Ref_x) * 2, (SPA_y + Ref_y) * 2), patch_level,
#                                    (need_patch_w, need_patch_h))
#         big_image_file = ROI_path + '\\' + 'ROI' + '%d' % idx + '-1.png'
#         save_big_image_path = os.path.join(save_dir, big_image_file)
#         if not os.path.exists(os.path.join(save_dir, ROI_path)):
#             os.makedirs(os.path.join(save_dir, ROI_path))
#         Image.fromarray(big_img).resize((1000, 1000)).save(save_big_image_path)
#
#
#         # 将其添加到LabelList中
#         label_dic['LabelRoot']['LabelInfoList'].append(template1)
#         # 模版重新初始化
#         template1 = copy.deepcopy(label_dic['LabelRoot']['LabelInfoList'][0])
#         rec_index1 += 1
#         template1['LabelInfo']['Dimensioning'] = rec_index1
#         # template1['LabelInfo']['Dimensioning'] = Ref_area
#         template1['LabelInfo']['PenColor'] = 'Blue'
#
#         for x in range(int(start_kx), int(end_kx)+1):
#             for y in range(int(start_ky), int(end_ky)+1):
#                 # *************************************************
#                 # testx = (SPA_x + x0 + x * (ROI_size[0] + offset[0])) + ROI_size[0] / 2
#                 # testy = (SPA_y + y0 + y * (ROI_size[1] + offset[1])) + ROI_size[1] / 2
#                 testx = (x0 + x * (ROI_size[0] + offset[0]))
#                 testy = (y0 + y * (ROI_size[1] + offset[1]))
#                 count = inorout(Pointslist, testx, testy)
#                 if (count % 2) == 0:
#                     continue
#                 # *************************************************
#                 # 修改模版中的相关变量
#                 rect_x = x0 + x * (ROI_size[0] + offset[0]) - ROI_size[0] / 2
#                 rect_y = y0 + y * (ROI_size[1] + offset[1]) - ROI_size[0] / 2
#                 template['LabelInfo']['StartPoint'] = '%d, %d' % (rect_x, rect_y)
#                 template['LabelInfo']['EndPoint'] = '%d, %d' % (
#                     rect_x + ROI_size[0], rect_y + ROI_size[1])
#                 template['LabelInfo']['Rect'] = '%d, %d, %d, %d' % (
#                     rect_x, rect_y, ROI_size[0],
#                     ROI_size[1])
#                 # template['LabelInfo']['Dimensioning'] = count
#
#                 roi_w = int((ROI_size[0] * 2) / (4 ** patch_level))
#                 roi_h = int((ROI_size[1] * 2) / (4 ** patch_level))
#
#                 try:
#                     img = sdpc.read_region(((rect_x + Ref_x) * 2, (rect_y + Ref_y) * 2), patch_level, (roi_w, roi_h))
#                 except:
#                     print('(%d, %d) is out of the WSI, continue...' % ((rect_x + Ref_x) * 2, (rect_y + Ref_y) * 2))
#                     continue
#                 if not os.path.exists(save_dir):
#                     os.mkdir(save_dir)
#                 pre_file = save_dir.split('\\')[-1]
#                 # image_file=pre_file+'_'+str(int(rect_x)) + '_' + str(int(rect_y)) + '.png'
#                 image_file = ROI_path + '\\' + 'patch' + '%d' % rec_index + '-1.png'
#                 if not os.path.exists(os.path.join(save_dir, ROI_path)):
#                     os.makedirs(os.path.join(save_dir, ROI_path))
#                 save_path = os.path.join(save_dir, image_file)
#                 Image.fromarray(img).save(save_path)
#
#                 # 将其添加到LabelList中
#                 label_dic['LabelRoot']['LabelInfoList'].append(template)
#                 # 模版重新初始化
#                 template = copy.deepcopy(label_dic['LabelRoot']['LabelInfoList'][0])
#                 rec_index += 1
#                 template['LabelInfo']['Dimensioning'] = rec_index
#                 # template['LabelInfo']['Dimensioning'] = Ref_area
#                 template['LabelInfo']['PenColor'] = 'Red'



def getcoords(sdpc_path, label_dic, save_dir, patch_w, patch_h, colors, wins_linux=0, patch_level=0, zoomscale=0.25,
              rect_color="Red"):
    x_final_size, y_final_size = patch_w, patch_h

    template = None
    std_color = None
    flag = True
    count = 0
    # 寻找标注的矩形模板，并以该倍率作为参考坐标系
    for counter in (label_dic['LabelRoot']['LabelInfoList'][0:]):
        # 设置矩形模板的公用参数
        if counter['LabelInfo']['ToolInfor'] == "btn_brush" or counter['LabelInfo']['ToolInfor'] == "btn_pen":
            if flag:
                std_color = counter['LabelInfo']['PenColor']

                template = copy.deepcopy(counter)
                rec_index = len(label_dic['LabelRoot']['LabelInfoList']) + 1
                template['LabelInfo']['Id'] = rec_index
                template['LabelInfo']['PenColor'] = rect_color
                template['LabelInfo']['FontColor'] = rect_color
                template['LabelInfo']['ZoomScale'] = zoomscale
                template['LabelInfo']['Dimensioning'] = 1
                template['LabelInfo']['ToolInfor'] = "btn_rect"
                template['PointsInfo']['ps'] = None
                template['TextInfo']['Text'] = None
                flag = False
            counter['LabelInfo']['Dimensioning'] = count
            count = count + 1

        if counter['LabelInfo']['PenColor'] not in colors:
            colors.append(counter['LabelInfo']['PenColor'])

    if template is None:
        print('Please add a brush annotation')
        sys.exit()
    # 读取sdpc文件
    sdpc = Sdpc(sdpc_path)
    # 对所有标注遍历
    for counter in tqdm(label_dic['LabelRoot']['LabelInfoList'][0:]):
        # 对笔刷标注切片
        if counter['LabelInfo']['ToolInfor'] == "btn_brush" or counter['LabelInfo']['ToolInfor'] == "btn_pen":
            color_index = colors.index(counter['LabelInfo']['PenColor'])
            Points = list(zip(*[list(map(int, point.split(', '))) for point in counter['PointsInfo']['ps']]))
            # 获取笔刷所在的屏幕位置
            Ref_x, Ref_y, _, _ = counter['LabelInfo']['CurPicRect'].split(', ')
            Ref_x, Ref_y = int(Ref_x), int(Ref_y)
            # 计算参考坐标系与绝对坐标系的比率
            std_scale = counter['LabelInfo']['ZoomScale']
            # 将标注的点放缩到参考坐标系下
            Pointsx = []
            Pointsy = []
            for i in range(len(Points[0])):
                Pointsx.append(int((Points[0][i] + Ref_x) * zoomscale / std_scale) - Ref_x)
                Pointsy.append(int((Points[1][i] + Ref_y) * zoomscale / std_scale) - Ref_y)
            # 获取闭合曲线在参考坐标系下的左上角起点spa，右下角终点spb
            SPA_x, SPA_y = (min(Pointsx), min(Pointsy))
            SPB_x, SPB_y = (max(Pointsx), max(Pointsy))
            Pointslist = polygon_preprocessor([Pointsx, Pointsy])
            # *************************************************
            # 以标注的中心点作为原点，计算patch下标
            x0 = np.mean(np.array(Pointsx[:-1]))
            y0 = np.mean(np.array(Pointsy[:-1]))
            start_kx = -np.ceil((x0 - SPA_x - patch_w / 2) / patch_w)
            end_kx = np.ceil((SPB_x - x0 - patch_w / 2) / patch_w)
            start_ky = -np.ceil((y0 - SPA_y - patch_h / 2) / patch_h)
            end_ky = np.ceil((SPB_y - y0 - patch_h / 2) / patch_h)

            # 循环操作，生成标注
            for x in range(int(start_kx), int(end_kx) + 1):
                for y in range(int(start_ky), int(end_ky) + 1):
                    # 每个patch的中心点
                    test_x = (x0 + x * patch_w)
                    test_y = (y0 + y * patch_h)

                    test_x_left = (x0 + x * patch_w - patch_w / 2)
                    test_y_bottom = (y0 + y * patch_h - patch_h / 2)

                    test_x_right = (x0 + x * patch_w + patch_w / 2)
                    test_y_top = (y0 + y * patch_h + patch_h / 2)

                    # 判断中心点、左上、左下、右上、右下点以及上边框中点、下边框中点、左边框中点、右边框中点是否在框中
                    count_mid = inorout(Pointslist, test_x, test_y)
                    count_left_top = inorout(Pointslist, test_x_left, test_y_top)
                    count_left_bottom = inorout(Pointslist, test_x_left, test_y_bottom)
                    count_right_top = inorout(Pointslist, test_x_right, test_y_top)
                    count_right_bottom = inorout(Pointslist, test_x_right, test_y_bottom)
                    count_mid_top = inorout(Pointslist, test_x, test_y_top)
                    count_mid_bottom = inorout(Pointslist, test_x, test_y_bottom)
                    count_left_mid = inorout(Pointslist, test_x_left, test_y)
                    count_right_mid = inorout(Pointslist, test_x_right, test_y)

                    if (count_mid % 2) == 0 and (count_left_top % 2) == 0 and (count_left_bottom % 2) == 0 and \
                            (count_right_top % 2) == 0 and (count_right_bottom % 2) == 0 and (count_mid_top % 2) == 0 \
                            and (count_mid_bottom % 2) == 0 and (count_left_mid % 2) == 0 and (
                            count_right_mid % 2) == 0:
                        continue

                    # 如果在框中，更新标注信息
                    rect_x = test_x - patch_w / 2
                    rect_y = test_y - patch_h / 2
                    # 设置要添加的标注信息
                    template1 = copy.deepcopy(template)
                    template1['LabelInfo']['StartPoint'] = '%d, %d' % (50, 50)
                    template1['LabelInfo']['EndPoint'] = '%d, %d' % (50 + patch_w, 50 + patch_h)
                    template1['LabelInfo']['Rect'] = '%d, %d, %d, %d' % (50, 50, patch_w, patch_h)
                    template1['LabelInfo']['CurPicRect'] = '%d, %d, %d, %d' % (
                        Ref_x + rect_x - 50, Ref_y + rect_y - 50, 0, 0)
                    try:
                        img = sdpc.read_region((int((Ref_x + rect_x) / zoomscale), int((Ref_y + rect_y) / zoomscale)),
                                               patch_level, (int(patch_w / zoomscale), int(patch_h / zoomscale)))
                    except:
                        print('(%d, %d) is out of the WSI, continue...' % (
                            (Ref_x + rect_x) * 2, (Ref_y + rect_y) * 2))
                        continue
                    save_dir1 = copy.deepcopy(save_dir) + "/" + colors[color_index] + "_" + str(counter['LabelInfo']['Dimensioning'])
                    if not os.path.exists(save_dir1):
                        os.mkdir(save_dir1)
                    if wins_linux == 1:
                        pre_file = save_dir.split('/')[-1]
                    else:
                        pre_file = save_dir.replace('/', '\\').split('\\')[-1]
                    image_file = pre_file + '_%d.png' % template1['LabelInfo']['Id']
                    save_path = os.path.join(save_dir1, image_file)
                    im = Image.fromarray(img)
                    im.thumbnail((x_final_size, y_final_size))
                    if wins_linux == 1:
                        im.save(save_path)
                    else:
                        im.save(save_path.replace('/', '\\'))

                    # 将其添加到LabelList中
                    label_dic['LabelRoot']['LabelInfoList'].append(template1)
                    # 模版迭代
                    rec_index += 1
                    template['LabelInfo']['Id'] = rec_index
                    template['LabelInfo']['Dimensioning'] = template['LabelInfo']['Dimensioning'] + 1


def polygon_preprocessor(points):
    n = len(points[0])

    # 对平行的线段施加扰动
    for i in range(n - 2):
        if points[1][i] == points[1][i + 1]:
            points[1][i + 1] += 1
    if points[1][n - 2] == points[1][n - 1]:
        if points[1][n - 2] == points[1][n - 3] - 1:
            points[1][n - 2] -= 1
        else:
            points[1][n - 2] += 1

    # 将第二个点添加到末行以备用
    points[0].append(points[0][1])
    points[1].append(points[1][1])

    return points


def inorout(points, x, y):
    n = len(points[0])
    count = 0

    for i in range(n - 2):
        # 排除掉出界的情况
        if points[1][i] > points[1][i + 1]:
            if y >= points[1][i] or y < points[1][i + 1]:
                continue
            if y == points[1][i + 1] and y < points[1][i + 2]:
                continue  # 排除掉可能相切的情况
        else:
            if y <= points[1][i] or y > points[1][i + 1]:
                continue
            if y == points[1][i + 1] and y > points[1][i + 2]:
                continue  # 排除掉可能相切的情况

        # 讨论线段垂直的情况
        if points[0][i] == points[0][i + 1]:
            if x < points[0][i]:
                count += 1

        # 讨论一般情况
        else:
            slope = (points[1][i + 1] - points[1][i]) / (points[0][i + 1] - points[0][i])  # 计算线段的斜率
            y_hat = slope * (x - points[0][i]) + points[1][i]
            if slope * (y - y_hat) > 0:
                count += 1

    return count


def sdpl_cut(data_path, patch_level, patch_w, patch_h, rect_color='Red'):

    files = os.listdir(data_path)
    colors = []
    for i, file in enumerate(files):
        if file.endswith('.sdpc'):
            print('file = ', file)
            fi_path_, _ = file.split('.')
            fi_path = os.path.join(data_path, fi_path_ + '_' + str(patch_level))
            folder = os.path.exists(fi_path)
            # 新建保存patch的文件夹
            if not folder:
                os.makedirs(fi_path)
            else:
                print('...There is this folder')
                continue

            print('---------------* Processing: %s *---------------' % file)

            if not os.path.exists(os.path.join(data_path, file.replace('sdpc', 'sdpl'))):
                continue
            # 已经得到了每张wsi的各个patch的坐标位置
            sdpc_path = os.path.join(data_path, file)
            sdpl_path = sdpc_path.replace('.sdpc', '.sdpl')
            # 保存原有的sdpl至*_old.sdpl
            os.system('copy %s %s' % (sdpl_path.replace('/', '\\'),
                                      sdpl_path.replace('/', '\\').replace('.sdpl', '_old.sdpl')))  # window下拷文件
            with open(sdpl_path, 'r', encoding='UTF-8') as f:
                label_dic = json.load(f)
                # 计算在第0层需要切patch的大小
                getcoords(sdpc_path=sdpc_path, label_dic=label_dic, save_dir=fi_path, patch_w=patch_w,
                          patch_h=patch_h, colors=colors, wins_linux=0, patch_level=patch_level,
                          rect_color=rect_color)
                # 保存新的sdpl覆盖*.sdpl
                with open(sdpl_path, 'w') as f:
                    json.dump(label_dic, f)

    print('-----------------* Patching Finished *---------------------')


if __name__ == '__main__':
    wsi_path = r'D:\LocalPC_PythonProject\demo\sdpc'
    sdpl_cut(wsi_path, 0, 224, 224)

