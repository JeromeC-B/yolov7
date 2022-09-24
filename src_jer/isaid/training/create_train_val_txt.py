
import yaml
import os
import numpy as np


class KFold:
    # ### va aller écrire le imgs-train.txt et imgs-val.txt selon le i-fold qu'on est rendu
    # ### et créer imgs-train-i.txt et ..val....txt pour garder un historique?
    t = 0


def get_imgs_name(path_imgs):

    onlyfiles = [f for f in os.listdir(path_imgs) if os.path.isfile(os.path.join(path_imgs, f))]
    return onlyfiles


def split_train_val(split_ratio, nb_data):
    rows = np.arange(nb_data)
    np.random.shuffle(rows)

    lim = int(nb_data*split_ratio)
    return rows[:lim], rows[lim:]


def create_txt(rows, imgs_name, name_file, path_imgs):
    if os.path.isfile(name_file):
        # ### delete le file
        os.remove(path=name_file)
    with open(name_file, "w") as f:
        for i in range(rows.shape[0]):
            f.write(path_imgs + "/" + imgs_name[rows[i]])
            if i != rows.shape[0] - 1:
                f.write("\n")

    t = 0


def create_train_val_txt(split_ratio, train_name, val_name, path_imgs, path_out):
    # ### gérer k-fold plus tard!! ###
    # ### gérer k-fold plus tard!! ###
    # ### gérer k-fold plus tard!! ###

    # ### aller chercher le nom de toutes les images
    imgs_name = get_imgs_name(path_imgs=path_out + "/" + path_imgs)
    # ### doit faire un split
    train_rows, val_rows = split_train_val(split_ratio=split_ratio, nb_data=len(imgs_name))

    print("ICI MODIFICATION DES TRAIN ET VAL ROWS!!!!")
    train_rows = train_rows[:25]
    val_rows = val_rows[:25]
    # ### créer les .txt
    create_txt(rows=train_rows, imgs_name=imgs_name, name_file=path_out + "/" + train_name, path_imgs=path_imgs)
    create_txt(rows=val_rows, imgs_name=imgs_name, name_file=path_out + "/" + val_name, path_imgs=path_imgs)

    t = 0


def create_train_val_txt_from_yaml(path_data_yaml):

    with open(path_data_yaml, 'r') as stream:
        config = yaml.safe_load(stream)

    for filename in ["imgs-train.cache", "imgs-train.cache.npy", "imgs-train.txt", "imgs-val.cache", "imgs-val.cache.npy", "imgs-val.txt"]:
        path_file = config["path"] + filename
        if os.path.isfile(path_file):
            # ### delete le file
            os.remove(path=path_file)

    create_train_val_txt(split_ratio=config["split_ratio"], train_name=config["train"], val_name=config["val"],
                         path_imgs=config["images_folder"], path_out=config["path"])
    t = 0
