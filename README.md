# AMTrafficPhase2-Task_1
Detection of stopped vehicles

A Python algorithm to detect stationary objects in a video, frame-by-frame.

# INSTALLATAION

Run ```pip3 install -r requirements.txt```.
The module ```StationaryDetector``` will be ready for import and use.

# METHODS, TOOLS
The algorithm is based on a sliding-window approach to object displacement calculation. Information about object locaion (object id and its boundig box coordinates) is accumulated from each frame in a per-object fixed-size buffer. With pre-defined steps in time, the algorithm 
1. retrieves the history of oject locations stored in buffer.
2. smoothens the coordinates with median filter to remove nose from automated detection.
3. calculates total displacement of object.
4. compares the displacement to a threshold. 

If the displacement is smaller than threshold, the object is deemed as stationary.

### Usage
```detector = StationaryDetector(*args, **kwargs)```\
Parameters
* image_size (tuple(height, width)): input frame size\
* interval (int): number of previous frames to consider (history buffer length)\
* check_period (int): checks are done every so many frames\
* thres (int): displacemet threshold, objects with \
* displacement > thres are considered moving.\
 Depends on image size, for 960x540 images use thres=10.\
 For other sizes you may follow\
 10 * ((image_height / 540) + (image_width / 960)) / 2
 
```detector.process_next_frame(frame_data={obj_id: [x1, y1, x2, y2]}) ```\
For every frame, detections in form of dictionary {obj_id: [x1, y1, x2, y2]} are feeded to `process_next_frame` method, and list of static object ids is returned.\
If the object disappears from the image for 20 consequtive frames, its buffer is deleted.\
        
 Displacement threshold is automatically scaled down for objects that are further away in the image (and thus have smaller velocity
 in pixels)       

### Methods:
1. Python 3.x
2. Scipy library for median filtering

### TESTING

1. Download sample frames and .xml from [here](https://drive.google.com/open?id=1HT8bfzucocSJR9fnjZl4wdjZgmOvEMzQ)
2. Unzip files in root folder
3. Run ```python3 run_on_video.py --video MVI_XXXXX```
4. Videofile would be produced, named 'MVI_XXXXX_processed.avi'. 
4.1 Video would contain bounding boxes around annotated objects (cars, trucks, buses). 
4.2 If object is considered 'moving' bounding box would be green
4.3 If object is considered 'stopped' bounding box would be red
4.4 Output results depends on parameters passed in StationaryDetector

Pre-generated sample videos can be found [here](https://drive.google.com/open?id=1M33jMYyIhF68fmPi5KLKNt4WbI1QhUCZ)
