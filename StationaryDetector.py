'''
Main module of stationary object detection
'''

import numpy as np
from scipy.signal import medfilt


class StationaryDetector():
    '''
    Detects statinary objects by calculating displacement over time
    '''

    def __init__(self, image_size, interval, check_period, thres):
        '''
        Parameters:
        image_size (tuple(height, width))
        interval (int): number of previous frames to consider
        check_period (int): checks are done every so many frames
        thres (int): displacemet threshold, objects with
        displacement > thres are considered moving.
        Depends on image size, for 960x540 images use thres=10.
        For other sizes you may follow
        10 * ((image_height / 540) + (image_width / 960)) / 2

        '''
        self.image_h, self.image_w = image_size
        self.interval = interval
        self.check_period = check_period
        self.thres = thres
        self.object_buffers = {}
        self.absence_count = {}
        self.static_objs = set([])
        self.num_frames_tracked = 0
        self.drop_thres = 20

    def process_next_frame(self, detections):
        '''
        Manages and updates buffers

        Parameters:
        detections (dict): {obj_id: [x1, y1, x2, y2]}

        Returns:
        static_objs(list): array of static object ids

        '''
        static_objs = []
        objs_to_drop = []
        for obj_id in self.object_buffers:
            if obj_id not in detections:
                if obj_id in self.absence_count:
                    objs_to_drop = self.update_missing_object(obj_id, objs_to_drop)
                else:
                    # register missing
                    self.absence_count[obj_id] = 1
            else:
                static_objs = self.update_present_object(obj_id, static_objs, detections)
                del detections[obj_id]
        # add new objects if any
        self.object_buffers.update({k: [v] for k, v in detections.items()})
        # reset/update counters
        if self.num_frames_tracked == self.check_period:
            self.num_frames_tracked = 0
        else:
            self.num_frames_tracked += 1
        # add new static objects, drop those missing for long
        self.static_objs.update(static_objs)
        for obj_id in objs_to_drop:
            del self.object_buffers[obj_id]
        return self.static_objs

    def update_missing_object(self, obj_id, objs_to_drop):
        '''increment missing counters, drop objects that are away for long'''
        self.absence_count[obj_id] += 1
        if self.absence_count[obj_id] == self.drop_thres:
            # been missing for long, forget it
            objs_to_drop.append(obj_id)
            if obj_id in self.static_objs:
                self.static_objs.remove(obj_id)
        return objs_to_drop

    def update_present_object(self, obj_id, static_objs, detections):
        '''Check if is static, update a registered object'''
        if obj_id in self.absence_count:
            # was missing, reset its missing counter
            self.absence_count[obj_id] = 0
        # store only m=interval previous steps
        self.object_buffers[obj_id] = self.object_buffers[obj_id][-self.interval:]
        self.object_buffers[obj_id].append(detections[obj_id])
        if self.num_frames_tracked == self.check_period:
            # check if is static
            if self._is_static(obj_id):
                static_objs.append(obj_id)
            else:
                if obj_id in self.static_objs:
                    self.static_objs.remove(obj_id)
        return static_objs

    def _is_static(self, obj_id):
        '''Check displacement to decide if object is static'''

        history = np.asarray(self.object_buffers[obj_id])
        if len(history) < self.interval:
            # not enough history to decide
            return False
        # smoothen the coords
        history = medfilt(history, [11, 1])
        # absolute displacement per point
        dist = history[-1] - history[0]
        # if object is in upper image part, decrease threshold
        is_far = history[:, 1].mean() < (self.image_h * 0.33)
        thres = self.thres - (int(is_far) * self.thres * 0.33)
        # total euclidean displacement, averaged for x's and y's separately
        dist = np.linalg.norm([np.mean(dist[[0, 2]]), \
                               np.mean(dist[[1, 3]])]
                             )
        if dist < thres:
            return True
        return False
