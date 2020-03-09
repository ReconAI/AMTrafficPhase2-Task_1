# AMTrafficPhase2-Task_1
Detection of stopped vehicles

The algorithm to detect stationary objects in a video, frame-by-frame.

Tested on UA-Detrac dataset, which can be downloaded at
http://detrac-db.rit.albany.edu/download

# HOW TO TEST

0) run ```pip3 install -r requirements.txt```
1) Download sample frames and .xml from [here](https://drive.google.com/open?id=1HT8bfzucocSJR9fnjZl4wdjZgmOvEMzQ)
2) Unzip files in root folder
3) run ```python3 run_on_video.py --video MVI_XXXXX```

The script will generate a video with objects highlighted.

Pre-generated sample videos can be found [here](https://drive.google.com/open?id=1M33jMYyIhF68fmPi5KLKNt4WbI1QhUCZ)
