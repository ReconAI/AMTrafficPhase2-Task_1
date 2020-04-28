import copy
import os
import json
from xml.etree import ElementTree
from StationaryDetector import StationaryDetector


def get_coords(b_info):
    t, l, w, h = [float(b_info.get(i)) for i in ['top', 'left', 'width', 'height']]
    x1, y1, x2, y2 = l, t, l+w, t+h
    return [x1, y1, x2, y2]


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='detector inference')
    parser.add_argument('-a', '--ann', default='',
                        help='annotations file)')
    args = parser.parse_args()
    tp, fp, tn, fn = 0, 0, 0, 0
    base_dir = os.path.dirname(args.ann)
    with open(args.ann, 'r') as ann_f:
        ann = json.load(ann_f)['Annotation']
    for item in ann:
        vid = item['Name']
        gt = {x['ID']: [x['Start'], x['End']] for x in item['StaticObjects']}
        data_tree = ElementTree.parse(os.path.join(base_dir, vid+'.xml'))
        root = data_tree.getroot()
        tg = []
        for elem in root:
            target = elem.findall('target_list/target')
            if target:
                tg.append((elem.get('num'), [(t.get('id'), t.find('box')) for t in target]))

        detector = StationaryDetector((540, 960), 72, 24, 15)

        for i, (pic, target) in enumerate(tg):
            gt_f = []
            det_dict = {}
            for o, box in target:
                x1, y1, x2, y2 = get_coords(box)
                det_dict.update({o: [x1, y1, x2, y2]})
            stat_objs = [int(o) for o in detector.process_next_frame(copy.copy(det_dict))]
            # which objs should be detected
            for o, interval in gt.items():
                if interval[1] >= int(pic) and interval[0] <= int(pic):
                    gt_f.append(o)

            tp_f = sum([o in gt_f for o in stat_objs])
            fp_f = len(stat_objs) - tp_f
            fn_f = sum([o not in stat_objs for o in gt_f])
            tn_f = sum([o not in stat_objs and o not in gt_f for o in det_dict.keys()])

            tp += tp_f
            fp += fp_f
            fn += fn_f
            tn += tn_f

    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    fscore = 2 * (recall * precision / (recall + precision))
    tnr = tn / (tn + fp)
    fpr = 1 - tnr
    fnr = 1 - recall

    print('Recall {}, Precision {}, F1 {}, TNR {}, FPR {}, FNR {}'\
        .format(recall, precision, fscore, tnr, fpr, fnr))
