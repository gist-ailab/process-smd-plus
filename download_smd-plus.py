import os
import gdown

output = 'SMD-Plus.zip'
url = 'https://drive.google.com/uc?id=1yokFvx_cJu-Fl5ti1wgF1WPHao_2kcKE'
gdown.download(url, output, quiet=False)

os.system('unzip SMD-Plus -d ./SMD-Plus')
os.system('unzip ./SMD-Plus/VIS_Onboard.zip -d ./SMD-Plus/VIS_Onboard')
os.system('unzip ./SMD-Plus/VIS_Onshore.zip -d ./SMD-Plus/Vis_Onshore')
