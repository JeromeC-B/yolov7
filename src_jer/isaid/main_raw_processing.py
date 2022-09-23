"""
But du script:

- jeu de train dans le bon format avec les bons labels (va devenir train/val)
- jeu de val va devenir un jeu de dev...


- jeu de test

Les labels seront:
image_name.txt == id x0 y0 x1 y2 x3 y3 ....
"""

import datetime
import os
from pathlib import Path
import time
import json

from src_jer.isaid.raw_processing import train_n_val, test


def check_integrity(path_in):
    t = 0
    names = {}
    annots_tot = {}
    for name in ["train", "val", "test"]:
        with open(path_in + "iSAID_{}.json".format(name), "r", encoding="utf-8") as f:
            annots = json.load(f)
        annots_tot[name] = annots
        names[name] = []
        for i in range(len(annots["images"])):
            names[name].append(annots["images"][i]["file_name"])

    if len(set(names["train"]).intersection(set(names["val"]))) != 0:
        raise Exception("Pas normal")
    if len(set(names["train"]).intersection(set(names["test"]))) != 0:
        raise Exception("Pas normal")
    if len(set(names["val"]).intersection(set(names["test"]))) != 0:
        raise Exception("Pas normal")

    names_train_n_val = names["train"] + names["val"]
    return annots_tot["train"], annots_tot["val"], names_train_n_val


if __name__ == '__main__':

    print('début: ', os.path.abspath(__file__))
    print("heure: ", datetime.datetime.now())
    print('\n')

    time_debut = time.time()

    path_in = r"C:\projets\external\database\isaid\raw-data\dota-v0\data_tot\\"
    path_out = r"C:\projets\external\database\isaid\data-2022-09-21\data\\"
    which_seg = "inst"  # inst == instance segmentation, sem == semantic segmentation

    annots_train, annots_val, names_train_n_val = check_integrity(path_in=path_in)

    train_n_val.move_data_n_labels(annots=annots_train, which_seg=which_seg, path_in=path_in, path_out=path_out + "train/")
    train_n_val.move_data_n_labels(annots=annots_val, which_seg=which_seg, path_in=path_in, path_out=path_out + "dev/")

    test.move_data_n_labels(names_train_n_val=names_train_n_val, path_in=path_in + "/images/", path_out=path_out + "test/images/")

    # ### fonction poura ller path/train/imgs vs path/val/imgs ###

    with open(path_out + r"\notes.txt", "w", encoding="utf-8") as f:
        f.write("Le type des labels: {}".format(which_seg))
        f.write("\n")
        f.write("Si == inst, alors cela veut dire que les labels sont fait pour de l'instance segmentation.\n")
        f.write("Si == sem, alors cela veut dire que les labels sont fait pour de la semantic segmentation.")

    print('\n')
    print("temps d'exécution: ", datetime.timedelta(seconds=time.time() - time_debut))
    print("heure: ", datetime.datetime.now())
    print('fin')

