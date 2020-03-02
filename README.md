# AMTrafficPhase2-Task_1
Detection of stopped vehicles

The algorithm to detect stationary objects in a video, frame-by-frame.

Tested on UA-Detrac dataset. Can be downloaded at
http://detrac-db.rit.albany.edu/download

When dowloaded, extract (some) image folders and corresponding .xml annotations
to this folder, then run
```python3 run_on_video.py --video MVI_XXXXX```
where XXXXX is the desired video number.
The script will generate the video with objects highlighted.