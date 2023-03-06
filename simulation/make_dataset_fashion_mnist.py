import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTHGRAPH_VERBOSITY'] = '0'
import random

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
import numpy as np
import pandas as pd
import PIL.Image as Image


FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    os.makedirs(FLAGS.output) # If FLAGS.output exists, then raise Exception
    # https://www.tensorflow.org/api_docs/python/tf/keras/datasets/fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()
    images = np.concatenate((train_images, test_images))
    labels = np.concatenate((train_labels, test_labels))
    print(f'Train: {len(train_images)}, Test: {len(test_images)}, Total: {len(images)}')

    # https://www.tensorflow.org/api_docs/python/tf/keras/datasets/fashion_mnist/load_data
    labelnames = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    total = {}
    for idx, data in enumerate(zip(images, labels), start=0):
        label = labelnames[data[1]]
        total[label] = total.get(label, 0) + 1

    test_ratio = FLAGS.test_ratio
    train_ratio = 1 - test_ratio

    counter = {}
    for idx, data in enumerate(zip(images, labels), start=0):
        image = Image.fromarray(data[0])
        label = labelnames[data[1]]
        cnt = counter.get(label, 0)

        if cnt <= total[label]*test_ratio:
            party = 'global'
        else:
            party = (cnt%FLAGS.clients)+1

        odir = os.path.join(FLAGS.output, f'{party}', f'{label}')
        os.makedirs(odir, exist_ok=True)
        opath = os.path.join(odir, f'{cnt:04d}.jpg')
        image.save(opath)

        counter[label] = cnt + 1


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Debug message')
    parser.add_argument('--output', required=True, type=str,
                        help='The output directory')
    parser.add_argument('--clients', required=True, type=int,
                        help='The number of clients')
    parser.add_argument('--test_ratio', default=0.2, type=float,
                        help='Test data ratio')

    FLAGS, _ = parser.parse_known_args()
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))
    DEBUG = FLAGS.debug

    main()
