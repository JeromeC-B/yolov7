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
    """
    Intégrité du split train/dev est regardé ici. ET c'est correct. Par contre, dans les annotations, pour un même id, il y a
    plusieurs string label selon si on est en train ou dev... donc aller voir ./labels.json pour les labels officiels de mon projet
    :param path_in:
    :return:
    """
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


def write_labels_num():
    """
    Aller chercher les bons chiffres représentant les targets..

    :return:
    """

    num_to_label = {}
    for name in ["train", "val"]:
        with open(path_in + "iSAID_{}.json".format(name), "r", encoding="utf-8") as f:
            annots = json.load(f)
        for annot in annots["annotations"]:
            if annot["category_id"] in num_to_label:
                if annot["category_name"] not in num_to_label[annot["category_id"]]:
                    num_to_label[annot["category_id"]].append(annot["category_name"])
            else:
                num_to_label[annot["category_id"]] = [annot["category_name"]]


if __name__ == '__main__':

    print('début: ', os.path.abspath(__file__))
    print("heure: ", datetime.datetime.now())
    print('\n')

    time_debut = time.time()

    path_in = r"C:\projets\external\database\isaid\raw-data\dota-v0\data_tot\\"
    path_out = r"C:\projets\external\database\isaid\data-2022-09-21\data\\"
    which_seg = "inst"  # inst == instance segmentation, sem == semantic segmentation

    with open(path_in + "labels.json", "r", encoding="utf-8") as f:
        labels = json.load(f)

    annots_train, annots_val, names_train_n_val = check_integrity(path_in=path_in)

    train_n_val.move_data_n_labels(labels=labels, annots=annots_train, which_seg=which_seg, path_in=path_in, path_out=path_out + "train/")
    train_n_val.move_data_n_labels(labels=labels, annots=annots_val, which_seg=which_seg, path_in=path_in, path_out=path_out + "dev/")

    test.move_data_n_labels(names_train_n_val=names_train_n_val, path_in=path_in + "/images/", path_out=path_out + "test/images/")

    # ### pu obligatoire, c'était pour aller voir... et effectivment dans train et val json annotations, il y a différents labels pour le même chiffre...
    # ### voir le labels.json pour les chiffres officiels dans mon projet (ou dataset.yaml)
    # write_labels_num()

    with open(path_out + r"\notes.txt", "w", encoding="utf-8") as f:
        f.write("Le type des labels: {}".format(which_seg))
        f.write("\n")
        f.write("Si == inst, alors cela veut dire que les labels sont fait pour de l'instance segmentation.\n")
        f.write("Si == sem, alors cela veut dire que les labels sont fait pour de la semantic segmentation.")

    print('\n')
    print("temps d'exécution: ", datetime.timedelta(seconds=time.time() - time_debut))
    print("heure: ", datetime.datetime.now())
    print('fin')
