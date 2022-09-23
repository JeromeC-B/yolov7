"""
1. faire une liste des images
2. Les mettre dans un /train/images
3. Créer leur label et les mettre dans /train/labels
"""


from pathlib import Path
import os
import shutil
import copy

import json


def get_imgs_names(annots):
    imgs_names = []
    for i in range(len(annots["images"])):
        imgs_names.append(annots["images"][i]["file_name"])
    return imgs_names


def copy_data(annots, path_in, path_out):

    Path(path_out + "images/").mkdir(parents=True, exist_ok=True)
    Path(path_out + "imgs-inst-labels/").mkdir(parents=True, exist_ok=True)

    imgs_name = get_imgs_names(annots=annots)

    print("les images segmentées ne sont pas transférées")
    for filename in imgs_name:
        path_file = path_in + "/images/" + filename
        path_imgs_inst_labels = path_in + "/imgs-labels/Instance_masks/" + "{}_instance_id_RGB.png".format(filename[:-4])
        # path_imgs_seg_labels = path_in + "/imgs-labels/????SEGMETATION/" + "{}_instance_id_RGB.png".format(filename)
        if os.path.isfile(path_file):
            if not os.path.isfile(path_out + "/images/" + filename):
                shutil.copy(path_file, path_out + "/images/")
        if os.path.isfile(path_imgs_inst_labels):
            if not os.path.isfile(path_out + "/imgs-inst-labels/" + "{}_instance_id_RGB.png".format(filename[:-4])):
                shutil.copy(path_imgs_inst_labels, path_out + "/imgs-inst-labels/")


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
            os.remove(path=path_file)
        if filename in filename_to_id:
            if filename_to_id[filename] in strs_to_file:
                with open(path_file, "w", encoding="utf-8") as f:
                    f.write(strs_to_file[filename_to_id[filename]])
            else:
                print("filename_ and id", filename, filename_to_id[filename])
        else:
            with open(path_file, "w", encoding="utf-8") as f:
                f.write("")
            print("filename: ", filename)


def create_labels_in_out_folder(annots, which_seg, path_imgs, path_out):

    Path(path_out).mkdir(parents=True, exist_ok=True)

    if which_seg == "inst":
        strs_to_file = create_strs_to_file_inst(annots=annots)
    elif which_seg == "sem":
        raise Exception("Pas encore implémenté")
        path_in = path_in + "/train-labels/train/Semantic_masks/images/images"
    else:
        raise Exception("pas normal, c'est soit inst, soit sem, non?")

    write_labels(annots=annots, strs_to_file=strs_to_file, path_imgs=path_imgs, path_out=path_out)


def move_data_n_labels(annots, which_seg, path_in, path_out):

    copy_data(annots=annots, path_in=path_in, path_out=path_out)

    create_labels_in_out_folder(annots=annots, which_seg=which_seg, path_imgs=path_out + "/images/", path_out=path_out + "/labels/")

