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
    if len(annot["segmentation"]) != 1:
        t = 0
        raise Exception("pas normal?")
    str_segm = ""
    for i in range(len(annot["segmentation"][0])):
        str_segm = str_segm + str(annot["segmentation"][0][i])
        if i != len(annot["segmentation"][0]) - 1:
            str_segm = str_segm + " "

    return str_segm


def create_strs_to_file_inst(annots):

    strs_to_file = {}
    for annot in annots["annotations"]:
        if annot["image_id"] in strs_to_file:
            strs_to_file[annot["image_id"]] = strs_to_file[annot["image_id"]] + "\n"
            str_segm = create_str_segm(annot=annot)
            strs_to_file[annot["image_id"]] = strs_to_file[annot["image_id"]] + "{} ".format(annot["category_id"]) + str_segm
        else:
            strs_to_file[annot["image_id"]] = ""
            str_segm = create_str_segm(annot=annot)
            strs_to_file[annot["image_id"]] = strs_to_file[annot["image_id"]] + "{} ".format(annot["category_id"]) + str_segm
    return strs_to_file


def create_labels_in_folder(which_seg, path_in, path_imgs, path_out):

    Path(path_out).mkdir(parents=True, exist_ok=True)

    with open(path_in + "/train-labels/train/Annotations/iSAID_train.json", "r", encoding="utf-8") as f:
        annots = json.load(f)
    annots["annotations"] = annots["annotations"][:10]

    if which_seg == "inst":
        strs_to_file = create_strs_to_file_inst(annots=annots)
        t = 0
    elif which_seg == "sem":
        raise Exception("Pas encore implémenté")
        path_in = path_in + "/train-labels/train/Semantic_masks/images/images"
    else:
        raise Exception("pas normal, c'est soit inst, soit sem, non?")

    img_id_to_img_key = {}
    for filename in os.listdir(path_imgs):
        prefix = filename[1:5]
        path_file = path_out + filename[:-4] + ".txt"
        key_name = int(prefix)
        img_id = annots["images"][key_name][
            "id"]  # f = os.path.join(path_imgs, filename)  # ### checking if it is a file  # if not os.path.isfile(f):  #     raise Exception("pas normal")

    # ### dans la fonction write, sassurer que le .txt nexiste pas, si oui il faut le delete


    t = 0

    t = 0


def move_data_n_labels(which_seg, path_in, path_out):

    move_train_data(path_in=path_in, path_out=path_out)

    create_labels_in_folder(which_seg=which_seg, path_in=path_in, path_imgs=path_out + "/images/", path_out=path_out + "/labels/")

    t = 0

