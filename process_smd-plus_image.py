import os
import cv2
import glob
from scipy.io import loadmat


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

video_list = sorted(glob.glob('./SMD_Plus/VIS_Onboard/Videos/*.avi')) + sorted(glob.glob('./SMD_Plus/VIS_Onshore/Videos/*.avi'))

for video_file in video_list:
    video_name = os.path.basename(video_file)
    key = video_name.replace('.avi', '').replace('_OB', '').replace('_Haze', '').replace('_VIS', '')

    if key in train_list:
        set_name = 'train'
    elif key in test_list:
        set_name = 'test'
    else:
        raise NotImplementedError

    cap = cv2.VideoCapture(video_file)
    property_id = int(cv2.CAP_PROP_FRAME_COUNT) 
    length = int(cv2.VideoCapture.get(cap, property_id))

    success, image = cap.read()
    num_frame = 0
    while success:
        cv2.imwrite(os.path.join('./smd-plus', set_name, video_name.replace('.avi', '') + '_{:03d}.png'.format(num_frame)), image)
        success, image = cap.read()
        num_frame += 1

    cap.release()
    cv2.destroyAllWindows()
