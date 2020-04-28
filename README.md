# AMTrafficPhase2-Task_1
A Python algorithm to detect stationary objects in a video, frame-by-frame.

Detailed description:
Develop and implement algorithm to detect immobile objects on the video
sequence. As an input you would receive a list of bounding boxes (output of
Yolo detector, or similar); each bounding box contains 1+4+4* n values: 1 -
class, 4 - relative bbox center coordinate, width and height (for example
<relative_x> = <absolute_x>/<image_width>); 4 - 4 points from previous
frame; n - is the number of previous frames.
Algorithm must have O(log(n* m)), O(n* m) complexity (this point is
discussable), where ‘m’ is number of bounding boxes in the frame and ‘n’ is
number of previous states (frames) for each object.
Ideally it has to be a light-weight statistical module (not neural network or
tree), which would make a decision depending on image size and object
dimensions.

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
 displacement > thres are considered moving.\
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
1. Download sample frames (unzip) and .xml from [here](https://drive.google.com/drive/folders/1JIlapTGeaaDHd3YW0zMwy7zE9-7q8SEt?usp=sharing). These files are sampled from [DETRAC](http://detrac-db.rit.albany.edu/) dataset.
2. Unzip files in root folder, keeping directory structure.
3. Run `python3 evaluate.py --ann TestingData/StaticObjectsAnnotation.json`
The script should print metrics in stdout. For the data from above, algorithm achieves **0.81 recall, 0.71 precision**. The main source of errors is the ~2 second lag originating from the sliding window approach, and specifics of data: objects moving very slowly may get classified as stationary. E.g. a bus approaching and positioning at the stop at a very low speed will get marked as static earlier than annotated in test data.

#### Visualization
1. Download sample frames (unzip) and .xml from [here](https://drive.google.com/drive/folders/1JIlapTGeaaDHd3YW0zMwy7zE9-7q8SEt?usp=sharing). These files are sampled from [DETRAC](http://detrac-db.rit.albany.edu/) dataset.
2. Unzip files in root folder
3. Run ```python3 run_on_video.py --video MVI_XXXXX```
4. Videofile would be produced, named 'MVI_XXXXX_processed.avi'. 
4.1. Video would contain bounding boxes around annotated objects (cars, trucks, buses). 
4.2. If object is considered 'moving' bounding box would be green
4.3. If object is considered 'stopped' bounding box would be red
4.4. Output results depends on parameters passed in StationaryDetector

Pre-generated sample videos can be found [here](https://drive.google.com/drive/folders/1eGF9n1a5DLjWFDgS-dgpkmBm8AK_XdLk?usp=sharing)
