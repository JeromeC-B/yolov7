"""
1. faire une liste des images
2. Les mettre dans un /train/images
3. Créer leur label et les mettre dans /train/labels
"""


from pathlib import Path
import os
import shutil


def move_data_n_labels(names_train_n_val, path_in, path_out):

    Path(path_out).mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(path_in):
        if filename not in names_train_n_val:
            shutil.copy(path_in + filename, path_out)


