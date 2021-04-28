# Author  : WangXiao
# File    : parse_json_dir.py
# Function: TODO

import json
import os
import cv2
from labelme import utils
import random






if __name__ == '__main__':
    #----------------------------------------------------------#
    # 构建一个data文件夹                                         #
    # 将本文件与Coco格式的json文件夹放在data文件夹下                #
    # 修改制定json_dir为json文件夹的地址                          #
    # 运行脚本即可得到从json解析的数据，已经tranval和test两个txt     #
    #----------------------------------------------------------#
    # 初始化
    json_dir = './瑕疵分类'
    wcd = os.getcwd()
    classes_dic = {}
    classes_id = 0
    trainval_percent = 0.9
    # 1、 根据文件名，划分数据集
    json_name_list = [os.path.splitext(name)[0] for name in os.listdir(json_dir) if name.endswith('.json')]
    total_num = len(json_name_list)
    tranval_num = int(total_num * trainval_percent)
    test_num = total_num-tranval_num
    trainval_name_list = random.sample(json_name_list,tranval_num)
    test_name_list = random.sample(json_name_list,test_num)
    # print(json_name_list)

    # 2、读取json文件
    classes_txt = open('../model_data/new_classes.txt','w')
    for index,name_list in enumerate([trainval_name_list,test_name_list]):
        if index == 0:
            label_info = open('../trainval.txt','w')
        elif index ==1:
            label_info = open('../test.txt','w')
        for name in name_list:
            json_path = os.path.join(json_dir,name+'.json')
            with open(json_path,'r',encoding='utf-8') as f:
                ret_dic = json.load(f)

                image_data = ret_dic['imageData']

                # 保存图片
                save_image_dir = os.path.join(wcd,'images')
                if not os.path.exists(save_image_dir):
                    os.mkdir(save_image_dir)
                image = utils.img_b64_to_arr(image_data)
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                save_image_path = os.path.join(save_image_dir,name+'.jpg')
                cv2.imwrite(save_image_path,image)

                # 写入txt
                label_info.write(save_image_path)
                for shape in ret_dic['shapes']:
                    cls = shape['label']
                    if cls not in classes_dic:
                        classes_dic[cls] = classes_id
                        classes_id += 1
                        classes_txt.write(cls+'\n')

                    xmin = str(int(shape['points'][0][0]))
                    ymin = str(int(shape['points'][0][1]))
                    xmax = str(int(shape['points'][1][0]))
                    ymax = str(int(shape['points'][1][1]))
                    label_info.write(' '+ '%s,%s,%s,%s,%s'%(xmin,ymin,xmax,ymax,str(classes_dic[cls])))
                label_info.write('\n')
                # print(ret_dic['shapes'][]['label'])
        f.close()
    classes_txt.close()




    # 3、解析json文件，生成image、和tranval.txt,test.txt(内容包括图片绝对地址、box类别和box坐标)