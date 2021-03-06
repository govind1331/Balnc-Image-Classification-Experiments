import numpy as np
import pandas as pd
import keras.backend as K

# from keras.models import K
from keras.preprocessing import image
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.resnet50 import preprocess_input
from sklearn.metrics import accuracy_score, f1_score

from utils import getFilesInDir, create_labels
# from rnn_backend import RnnClassifier, preprocess_input_rnn
from architecture import Classifier
from utils import one_hot_to_integer
from utils import one_hot
from utils import missclassification_rate
from utils import test_train_split

fraction = 100


def img_to_tensor(image_path, target_size):
    img = load_img(image_path, target_size=target_size)
    tensor = img_to_array(img)
    # print(tensor.shape)
    tensor = np.expand_dims(tensor, axis=0)
    # tensor = preprocess_input(tensor)
    print("Image """ + str(image_path) +
          " "" converted to tensor with shape " + str(tensor.shape))
    return tensor


def input_maker(input_folder, target_size, output_classes):
    images = getFilesInDir(input_folder)
    # images = getFilesInDir(folder)
    images_train, images_test = test_train_split(images, fraction)
    tensors_train = []
    tensors_test = []
    for i, j in images_train.items():
        for k in j:
            tensors_train.append(img_to_tensor(k, target_size=(target_size)))
            print("Train Tensor :" + str(k) + " Created..\n")
    for i, j in images_test.items():
        for k in j:
            tensors_test.append(img_to_tensor(k, target_size=(target_size)))
            print("Test Tensor :" + str(k) + " Created..\n")

    print("Total Training Tensors:" + str(len(tensors_train)) +
          " each of shape " + str(tensors_train[0].shape))
    print("Total Testing Tensors:" + str(len(tensors_train)) +
          " each of shape " + str((tensors_test[0].shape)))

    labels_train = create_labels(images_train, output_classes=output_classes)
    labels_test = create_labels(images_test, output_classes=output_classes)

    print("Total Training Lables created:" + str(len(labels_train)))
    print("Total Testing Lables created:" + str(len(labels_test)))

    return (tensors_train, labels_train, tensors_test, labels_test)


if __name__ == '__main__':
    c1 = Classifier()
    X_train, Y_train, X_test, Y_test = input_maker('Sport', (224, 224), 4)
    c1.create_architecture(input_shape=(224, 224, 3), output_dimension=4)
    c1.train_model(X_train, Y_train)
