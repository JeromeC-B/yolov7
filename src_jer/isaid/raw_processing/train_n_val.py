"""
1. faire une liste des images
2. Les mettre dans un /train/images
3. Créer leur label et les mettre dans /train/labels
"""


from pathlib import Path
import os
import shutil

from PIL import Image


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


def create_str_segm(annot_list, x_size, y_size):

    str_segm = ""
    for i in range(len(annot_list)):
        if i % 2 == 0:
            v_scaled = annot_list[i] / x_size
        else:
            v_scaled = annot_list[i] / y_size
        str_segm = str_segm + str(v_scaled)
        if i != len(annot_list) - 1:
            str_segm = str_segm + " "

    return str_segm


def create_strings_instance_labels(annots, path_imgs):
    """
    Ne pas oublier la différence entre inst et sem... si c'est inst, alors la même catégorie dans l'image va avoir plusieurs labels...
    du style
    12 x0 y0 x1 y1 x2 y2 ...
    12 x0' y0' x1' y1' x2' y2' ....

    Alors qu'en sem
    12 x0 y0 x1 y1 x2 y2 x0' y0' x1' y1' x2' y2' ....
    """
    # ### but faire un dict de {filename: string_labels}
    string_labels = {}
    for annot in annots["annotations"]:
        filename = annots["images"][annot["image_id"]]["file_name"]
        x_size, y_size = Image.open(path_imgs + filename).size
        filename = filename[:-4]
        for i in range(len(annot["segmentation"])):
            if annots["images"][annot["image_id"]]["id"] != annot["image_id"]:
                raise Exception("Pas normal?")
            if filename in string_labels:
                string_labels[filename] = string_labels[filename] + "\n"
            else:
                string_labels[filename] = ""
            str_segm = create_str_segm(annot_list=annot["segmentation"][i], x_size=x_size, y_size=y_size)
            string_labels[filename] = string_labels[filename] + "{} ".format(annot["category_id"]) + str_segm
    return string_labels


def write_labels(string_labels, path_out):
    for filename in string_labels:
        path_file = path_out + filename + ".txt"
        # ### check if img_name.txt exist ###
        if os.path.isfile(path_file):
            # ### delete le file
            os.remove(path=path_file)
        with open(path_file, "w", encoding="utf-8") as f:
            f.write(string_labels[filename])


def create_labels_in_out_folder(annots, which_seg, path_imgs, path_out):

    Path(path_out).mkdir(parents=True, exist_ok=True)

    if which_seg == "inst":
        string_labels = create_strings_instance_labels(annots=annots, path_imgs=path_imgs)
    elif which_seg == "sem":
        raise Exception("Pas encore implémenté")
        path_in = path_in + "/train-labels/train/Semantic_masks/images/images"
    else:
        raise Exception("pas normal, c'est soit inst, soit sem, non?")

    write_labels(string_labels=string_labels, path_out=path_out)


def move_data_n_labels(annots, which_seg, path_in, path_out):

    copy_data(annots=annots, path_in=path_in, path_out=path_out)

    create_labels_in_out_folder(annots=annots, which_seg=which_seg, path_imgs=path_out + "/images/", path_out=path_out + "/labels/")
