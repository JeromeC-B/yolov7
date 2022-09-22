"""
1. faire une liste des images
2. Les mettre dans un /train/images
3. Créer leur label et les mettre dans /train/labels
"""


from pathlib import Path
import os
import shutil

import json


def move_train_data(path_in, path_out):

    path_out = path_out + "images/"
    Path(path_out).mkdir(parents=True, exist_ok=True)

    for i in range(1, 4):
        path_dir = path_in + "part{}/images/".format(i)
        for filename in os.listdir(path_dir):
            f = os.path.join(path_dir, filename)
            # checking if it is a file
            if not os.path.isfile(f):
                raise Exception("pas normal")
            if not Path(path_out + filename).is_file():
                shutil.move(f, path_out)


def create_str_segm(annot):

    str_segm = ""
    for i in range(len(annot["segmentation"][0])):
        str_segm = str_segm + str(annot["segmentation"][0][i])
        if i != len(annot["segmentation"][0]) - 1:
            str_segm = str_segm + " "

    return str_segm


def create_strs_to_file_inst(annots):
    """
    Ne pas oublier la différence entre inst et sem... si c'est inst, alors la même catégorie dans l'image va avoir plusieurs labels...
    du style
    12 x0 y0 x1 y1 x2 y2 ...
    12 x0' y0' x1' y1' x2' y2' ....

    Alors qu'en sem
    12 x0 y0 x1 y1 x2 y2 x0' y0' x1' y1' x2' y2' ....
    """
    strs_to_file = {}
    for annot in annots["annotations"]:
        if len(annot["segmentation"]) > 1:
            t = 0
        for i in range(len(annot["segmentation"])):
            if annot["image_id"] in strs_to_file:
                strs_to_file[annot["image_id"]] = strs_to_file[annot["image_id"]] + "\n"
            else:
                strs_to_file[annot["image_id"]] = ""
            str_segm = create_str_segm(annot=annot)
            strs_to_file[annot["image_id"]] = strs_to_file[annot["image_id"]] + "{} ".format(annot["category_id"]) + str_segm
    return strs_to_file


def write_labels(annots, strs_to_file, path_imgs, path_out):
    filename_to_id = {}
    for i in range(len(annots["images"])):
        filename_to_id[annots["images"][i]["file_name"]] = annots["images"][i]["id"]
    for filename in os.listdir(path_imgs):
        path_file = path_out + filename[:-4] + ".txt"
        # ### check if img_name.txt exist ###
        if os.path.isfile(path_file):
            # ### delete le file
            t = 0
        with open(path_file, "r", encoding="utf-8") as f:
            f.write(strs_to_file[filename_to_id[filename]])
            t = 0
        t = 0


def create_labels_in_folder(which_seg, path_in, path_imgs, path_out):

    Path(path_out).mkdir(parents=True, exist_ok=True)

    with open(path_in + "/train-labels/train/Annotations/iSAID_train.json", "r", encoding="utf-8") as f:
        annots = json.load(f)
    annots["annotations"] = annots["annotations"][:10]

    if which_seg == "inst":
        strs_to_file = create_strs_to_file_inst(annots=annots)
        raise Exception("Venir s'assurer que strs_to_file est ok!")
    elif which_seg == "sem":
        raise Exception("Pas encore implémenté")
        path_in = path_in + "/train-labels/train/Semantic_masks/images/images"
    else:
        raise Exception("pas normal, c'est soit inst, soit sem, non?")

    write_labels(annots=annots, strs_to_file=strs_to_file, path_imgs=path_imgs, path_out=path_out)
    t = 0

    # ### dans la fonction write, sassurer que le .txt nexiste pas, si oui il faut le delete


    t = 0

    t = 0


def move_data_n_labels(which_seg, path_in, path_out):

    move_train_data(path_in=path_in, path_out=path_out)

    create_labels_in_folder(which_seg=which_seg, path_in=path_in, path_imgs=path_out + "/images/", path_out=path_out + "/labels/")

    t = 0

