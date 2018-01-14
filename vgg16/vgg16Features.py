import sys
sys.path.append('../')
sys.path.append('Model')

import numpy as np

from model import VGG16
from loadBatches import imageGenerator

from config import train_aug_melanoma_dir, train_aug_benign_dir
from config import validation_aug_melanoma_dir, validation_aug_benign_dir

from config import train_transfer_melanoma_dir, train_transfer_benign_dir
from config import validation_transfer_melanoma_dir, validation_transfer_benign_dir

from config import batch_size, nb_train_samples, nb_validation_samples

model = VGG16(include_top = False, weights = "imagenet", pooling = "avg")

aug_dir_arr = [
	validation_aug_melanoma_dir, validation_aug_benign_dir,
	train_aug_melanoma_dir, train_aug_benign_dir,
]

transfer_dir_arr = [
	validation_transfer_melanoma_dir, validation_transfer_benign_dir,
	train_transfer_melanoma_dir, train_transfer_benign_dir
]

sample_size_arr = [
	nb_validation_samples / 2, nb_validation_samples / 2,
	nb_train_samples / 2, nb_train_samples / 2
]

for i in range(len(aug_dir_arr)):
	G = imageGenerator(aug_dir_arr[i], batch_size)
	transfer_values = model.predict_generator(
	    G,
	    steps = sample_size_arr[i] / batch_size,
	    verbose=1,
	)

	print("Transfer Value Shape : {0} ".format(transfer_values.shape))
	np.save(open("{0}transfer-values.npy".format(transfer_dir_arr[i]), "w"), transfer_values)