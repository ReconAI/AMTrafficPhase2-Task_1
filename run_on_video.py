import copy
import os
from xml.etree import ElementTree
import cv2
from skimage import io
from StationaryDetector import StationaryDetector


def get_coords(b_info):
    t, l, w, h = [float(b_info.get(i)) for i in ['top', 'left', 'width', 'height']]
    x1, y1, x2, y2 = l, t, l+w, t+h
    return [x1, y1, x2, y2]


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='detector inference')
    parser.add_argument('-v', '--video', default='',
                        help='name of the video to run on)')
    args = parser.parse_args()
    vid = args.video
    data_tree = ElementTree.parse(vid+'.xml')
    root = data_tree.getroot()

    tg = []
    for elem in root:
        target = elem.findall('target_list/target')
        if target:
            tg.append((elem.get('num'), [(t.get('id'), t.find('box')) for t in target]))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    image_height = 540
    image_width = 960
    vw = cv2.VideoWriter(vid+'_processed.avi', fourcc, 25, (image_width, image_height))

    detector = StationaryDetector((540, 960), 72, 24, 15)
    is_stat = False

    for i, (pic, target) in enumerate(tg):
        im = io.imread(os.path.join(vid, 'img' + pic.rjust(5, '0')+'.jpg'))
        det_dict = {}
        for o, box in target:
            x1, y1, x2, y2 = get_coords(box)
            det_dict.update({o: [x1, y1, x2, y2]})
        stat_objs = detector.process_next_frame(copy.copy(det_dict))

        for o, box in det_dict.items():
            x1, y1, x2, y2 = box
            color = (0, 255, 0)
            if o in stat_objs:
                color = (0, 0, 255)
            cv2.rectangle(im, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
        vw.write(im)

    vw.release()
