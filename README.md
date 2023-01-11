# process-smd-plus
This is repository for converting SMD-Plus dataset into coco format.

## Requirements
* gdown
* tqdm
* opencv-python
* scipy
* pillow
* pycocotools

You can install reqirements via ```pip install -r requirements.txt``` 

## Usage
* How to download and prepare SMD-Plus dataset [1]

```python download_smd-plus.py```

* How to parse image

```python process_smd-plus_image.py```

* How to create coco json file

```python process_smd-plus_coco.py```


## Reference
[1] https://github.com/kjunhwa/SMD-Plus

[2] https://github.com/waspinator/pycococreator