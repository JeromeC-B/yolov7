"""
But du script: c'est pour faire de l'inférence
"""

import datetime
import os
import sys
import time
import yaml
import ast


import seg.segment.predict as predict

if __name__ == '__main__':

    print('début: ', os.path.abspath(__file__))
    print("heure: ", datetime.datetime.now())
    print('\n')

    time_debut = time.time()

    with open(r"C:\projets\yolov7\src_jer\isaid\configs\predict_config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    predict.run(weights=config["weights"],
                source=config["source"],
                data=config["data"],
                imgsz=ast.literal_eval(config["imgsz"]),
                conf_thres=config["conf_thres"],
                iou_thres=config["iou_thres"],
                max_det=config["max_det"],
                device=config["device"],
                view_img=config["view_img"],
                save_txt=config["save_txt"],
                save_conf=config["save_conf"],
                save_crop=config["save_crop"],
                nosave=config["nosave"],
                classes=ast.literal_eval(config["classes"]),
                agnostic_nms=config["agnostic_nms"],
                augment=config["augment"],
                visualize=config["visualize"],
                update=config["update"],
                project=config["project"],
                name=config["name"],
                exist_ok=config["exist_ok"],
                line_thickness=config["line_thickness"],
                hide_labels=config["hide_labels"],
                hide_conf=config["hide_conf"],
                half=config["half"],
                dnn=config["dnn"])

    #                 ast.literal_eval(config["imgsz"]),
    print('\n')
    print("temps d'exécution: ", datetime.timedelta(seconds=time.time() - time_debut))
    print("heure: ", datetime.datetime.now())
    print('fin')

