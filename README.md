# TrafficSignRecognitionCNN

Traffic Sign Recognition AI with CNN

## Datasets used

- [https://www.kaggle.com/datasets/tuanai/traffic-signs-dataset/code](https://www.kaggle.com/datasets/tuanai/traffic-signs-dataset/code) - preprocessed by [organiser1.py](./organiser1.py)
- [https://www.kaggle.com/datasets/aychul/30kmh-traffic-sign](https://www.kaggle.com/datasets/aychul/30kmh-traffic-sign) - preprocessed by [organiser2.py](./organiser2.py)
- [https://www.kaggle.com/datasets/aychul/60kmh-traffic-sign](https://www.kaggle.com/datasets/aychul/60kmh-traffic-sign)- preprocessed by [organiser2.py](./organiser2.py)

- [https://www.kaggle.com/datasets/dmitryyemelyanov/chinese-traffic-signs](https://www.kaggle.com/datasets/dmitryyemelyanov/chinese-traffic-signs) - created csv mapping for my own dataset [mapping](./annotations_category_names.csv) + [organiser3.py](./organiser3.py)

- [https://universe.roboflow.com/sit-asmsw/road-sign-detection-in-real-time](https://universe.roboflow.com/sit-asmsw/road-sign-detection-in-real-time) - organised by [organiser4_helper.py](./organiser4_helper.py) [organiser4.py](./organiser4.py)

- [https://nlpr.ia.ac.cn/pal/trafficdata/recognition.html](https://nlpr.ia.ac.cn/pal/trafficdata/recognition.html) - turns out that this is an older version of the same chinese traffic signs dataset

## Data processing steps in order:

- Download and extract every dataset to the `dataset` subdirectory
- From root directory run [organiser1.py](./organiser1.py)
- From root directory run [organiser2.py](./organiser2.py)
- From root directory run [organiser3.py](./organiser3.py)
- From root directory run [organiser4_helper.py](./organiser4_helper.py)
- Move a single image from a directory called `"-"` to `speed_limit_30` in `temp_road_sign_dataset` MANUALLY
- From root directory run [organiser4.py](./organiser4.py)
- Move the images from `final_dataset/barrier_ahead` to `final_dateset/fences` and `final_dataset/train_crossing` MANUALLY
- Update the `final_dataset/info.cs v` with [info_updater.py](./info_updater.py)
- Extra: added the following DALL-E generated images as well to `final_dataset/stop`: `5b93dfde-544a-4eb4-93be-795ba4de2528.png` and `db27620d-3ec7-4709-9612-6d256cd17d90.png`
- Compress the dataset, and upload to google drive
