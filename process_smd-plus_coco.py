import os
import glob
import json
import datetime
from scipy.io import loadmat
from PIL import Image
import pycococreatortools


train_list = [
    'MVI_1451',
    'MVI_1452',
    'MVI_1470',
    'MVI_1471',
    'MVI_1478',
    'MVI_1479',
    'MVI_1481',
    'MVI_1482',
    'MVI_1483',
    'MVI_1484',
    'MVI_1485',
    'MVI_1486',
    'MVI_1578',
    'MVI_1582',
    'MVI_1583',
    'MVI_1584',
    'MVI_1609',
    'MVI_1610',
    'MVI_1619',
    'MVI_1612',
    'MVI_1617',
    'MVI_1620',
    'MVI_1622',
    'MVI_1623',
    'MVI_1624',
    'MVI_1625',
    'MVI_1626',
    'MVI_1627',
    'MVI_0788',
    'MVI_0789',
    'MVI_0790',
    'MVI_0792',
    'MVI_0794',
    'MVI_0795',
    'MVI_0796',
    'MVI_0797',
    'MVI_0801'
]


test_list = [
    'MVI_1469',
    'MVI_1474',
    'MVI_1587',
    'MVI_1592',
    'MVI_1613',
    'MVI_1614',
    'MVI_1615',
    'MVI_1644',
    'MVI_1645',
    'MVI_1646',
    'MVI_1448',
    'MVI_1640',
    'MVI_0799',
    'MVI_0804'
]

INFO = {
    "description": "SMD-Plus dataset",
    "url": "https://github.com/kjunhwa/SMD-Plus",
    "version": "1.0.0",
    "year": 2022,
    "contributor": "Seongju Lee",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'Boat',
        'supercategory': 'Boat',
    },
    {
        'id': 2,
        'name': 'Vessel/ship',
        'supercategory': 'Vessel/ship',
    },
    {
        'id': 3,
        'name': 'Ferry',
        'supercategory': 'Ferry',
    },
    {
        'id': 4,
        'name': 'Kayak',
        'supercategory': 'Kayak',
    },
    {
        'id': 5,
        'name': 'Buoy',
        'supercategory': 'Buoy',
    },
    {
        'id': 6,
        'name': 'Sail boat',
        'supercategory': 'Sail boat',
    },
    {
        'id': 7,
        'name': 'Other',
        'supercategory': 'Other',
    }
]

CATEGORY2ID = {
    'Boat': 1,
    'Vessel/ship': 2,
    'Ferry': 3,
    'Kayak': 4,
    'Buoy': 5,
    'Sail boat': 6,
    'Other': 7
}

MODE = 'train'

train_coco_output = {
    "info": INFO,
    "licenses": LICENSES,
    "categories": CATEGORIES,
    "images": [],
    "annotations": []
}

test_coco_output = {
    "info": INFO,
    "licenses": LICENSES,
    "categories": CATEGORIES,
    "images": [],
    "annotations": []
}

mat_list = sorted(glob.glob('./smd-plus/VIS_Onboard/ObjectGT/*.mat')) + sorted(glob.glob('./smd-plus/VIS_Onshore/ObjectGT/*.mat'))
image_list = sorted(glob.glob('./smd-plus/train/*.png'))

train_image_id = 1
test_image_id = 1

train_annotation_id = 1
test_annotation_id = 1

for mat_file in mat_list:
    video_key = os.path.basename(mat_file).replace('_ObjectGT.mat', '')
    list_key = video_key.replace('_OB', '').replace('_Haze', '').replace('_VIS', '')
    frames = loadmat(mat_file)['structXML'][0]
    if list_key in train_list:
        mode = 'train'
    elif list_key in test_list:
        mode = 'test'
    else:
        raise NotImplementedError

    for frame_index in range(len(frames)):
        anns = frames[frame_index]
        if 'VIS_Onboard' in mat_file:
            image_path = os.path.join('./smd-plus/{}'.format(mode), video_key + '_OB_{:03d}.png'.format(frame_index))
        else:
            image_path = os.path.join('./smd-plus/{}'.format(mode), video_key + '_{:03d}.png'.format(frame_index))

        image = Image.open(image_path)
        if mode == 'train':
            image_info = pycococreatortools.create_image_info(train_image_id, os.path.basename(image_path), image.size)
            train_coco_output["images"].append(image_info)
        elif mode == 'test':
            image_info = pycococreatortools.create_image_info(test_image_id, os.path.basename(image_path), image.size)
            test_coco_output["images"].append(image_info)
        
        _, _, class_ids, _, class_names, _, bboxes = anns
        # movable_dis, class_ids, distance_ids, string_movable_labels, string_class_labels, string_distance_labels, bboxes
        for class_id, class_name, bbox in zip(class_ids, class_names, bboxes):
            if len(class_id) == 0:
                continue
            class_name = class_name[0][0]
            class_id = CATEGORY2ID[class_name]
            # class_name = class_name[0][0]
            # print(class_name, class_id)
            # assert class_id == CATEGORY2ID[class_name]
            category_info = {'id': class_id, 'is_crowd': False}
            
            if mode == 'train':
                annotation_info = pycococreatortools.create_annotation_info(train_annotation_id, train_image_id, category_info, None, image.size, bounding_box=bbox)
                train_annotation_id += 1
                train_coco_output['annotations'].append(annotation_info)
            elif mode == 'test':
                annotation_info = pycococreatortools.create_annotation_info(test_annotation_id, test_image_id, category_info, None, image.size, bounding_box=bbox)
                test_annotation_id += 1
                test_coco_output['annotations'].append(annotation_info)
        
        if mode == 'train':
            train_image_id += 1
        elif mode == 'test':
            test_image_id += 1
        else:
            raise NotImplementedError

with open('train_coco.json', 'w') as json_file:
    json.dump(train_coco_output, json_file)
    
print('train_coco.json saved! Number of images: {}, annotations: {}'.format(train_image_id - 1, train_annotation_id - 1))

with open('test_coco.json', 'w') as json_file:
    json.dump(test_coco_output, json_file)
    
print('test_coco.json saved! Number of images: {}, annotations: {}'.format(test_image_id - 1, test_annotation_id - 1))
    