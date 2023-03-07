import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
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

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    labelnames = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    target_size = (28, 28, 3)

    model = tf.keras.models.load_model(FLAGS.model)

    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
    dataset = image_generator.flow_from_directory(FLAGS.dataset, classes=labelnames,
                                                  target_size=target_size[:-1], shuffle=True,
                                                  follow_links=True)

    model.fit(dataset, epochs=FLAGS.epochs, verbose=0)

    model.save(FLAGS.output)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Debug message')
    parser.add_argument('--dataset', required=True, type=str,
                        help='The dataset path')
    parser.add_argument('--model', required=True, type=str,
                        help='The global model path')
    parser.add_argument('--epochs', default=10, type=int,
                        help='The local epochs')
    parser.add_argument('--output', required=True, type=str,
                        help='The output directory')

    FLAGS, _ = parser.parse_known_args()
    FLAGS.dataset = os.path.abspath(os.path.expanduser(FLAGS.dataset))
    FLAGS.model = os.path.abspath(os.path.expanduser(FLAGS.model))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))
    DEBUG = FLAGS.debug

    main()
