"""
1. faire une liste des images
2. Les mettre dans un /train/images
3. Créer leur label et les mettre dans /train/labels
"""


from pathlib import Path
import os
import shutil


def move_train_data(path_in, path_out):

    path_out = path_out + "/train/images/"
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


def move_data_n_labels(path_in, path_out):

    move_train_data(path_in=path_in, path_out=path_out)

    path_out = path_out + "/train/labels/"
    Path(path_out).mkdir(parents=True, exist_ok=True)


    t = 0

