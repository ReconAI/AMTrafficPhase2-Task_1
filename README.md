# AMTrafficPhase2-Task_1
Detection of stopped vehicles

The algorithm to detect stationary objects in a video, frame-by-frame.

Tested on UA-Detrac dataset, which can be downloaded at
http://detrac-db.rit.albany.edu/download

# HOW TO TEST

0) Run ```pip3 install -r requirements.txt```
1) Download sample frames and .xml from [here](https://drive.google.com/open?id=1HT8bfzucocSJR9fnjZl4wdjZgmOvEMzQ)
2) Unzip files in root folder
3) Run ```python3 run_on_video.py --video MVI_XXXXX```
4) Videofile would be produced, named 'MVI_XXXXX_processed.avi'. 
4.1) Video would contain bounding boxes around annotated objects (cars, trucks, buses). 
4.2) If object is considered 'moving' bounding box would be green
4.3) If object is considered 'stopped' bounding box would be red
4.4) Output results depens on parameters passed in StationaryDetector

The script will generate a video with objects highlighted.

Pre-generated sample videos can be found [here](https://drive.google.com/open?id=1M33jMYyIhF68fmPi5KLKNt4WbI1QhUCZ)
