"""
But du script:

- c'est de s'assurer et de créer un dossier test intègre
- jeu de train dans le bon format avec les bons labels
- jeu de val intègre et avec les bons labels

À VOIR: si je prend le jeu de val comme un réel jeu de test pour avoir les labels pour les performances...


Les labesl seront:
image_name.txt == id x0 y0 x1 y2 x3 y3 ....
"""

import datetime
import os
from pathlib import Path
import time

from src_jer.isaid.raw_processing import train, val


if __name__ == '__main__':

    print('début: ', os.path.abspath(__file__))
    print("heure: ", datetime.datetime.now())
    print('\n')

    time_debut = time.time()

    path_in = r"C:\projets\external\database\isaid\raw-data\dota-v0\\"
    path_out = r"C:\projets\external\database\isaid\data-2022-09-21\data\\"
    which_seg = "inst"  # inst == instance segmentation, sem == semantic segmentation

    train.move_data_n_labels(which_seg=which_seg, path_in=path_in + "train/", path_out=path_out + "train/")


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

