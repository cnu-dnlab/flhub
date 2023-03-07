import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTHGRAPH_VERBOSITY'] = '0'
import random
import copy

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

    model = tf.keras.models.Sequential([
                tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=target_size),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D((2, 2)),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dense(len(labelnames))])
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    if FLAGS.mode == 'init':
        model.summary()
        model_path = os.path.join(FLAGS.output, '0', 'global')
        model.save(model_path)
    elif FLAGS.mode == 'agg':
        client_models = []
        rpath = os.path.join(FLAGS.output, f'{FLAGS.round}')
        with os.scandir(rpath) as it:
            for entry in it:
                if entry.is_dir() and entry.name != 'global':
                    client_models.append(entry.path)

        knowledges = []
        for lpath in client_models:
            lmodel = tf.keras.models.load_model(lpath)
            knowledges.append(lmodel.get_weights())

        aggregates = copy.deepcopy(knowledges[0])
        for knowledge in knowledges[1:]:
            for i in range(len(knowledge)):
                aggregates[i] = aggregates[i] + knowledge[i]
        for i in range(len(aggregates)):
            aggregates[i] = aggregates[i] / len(knowledges)
        model.set_weights(aggregates)

        model_path = os.path.join(FLAGS.output, f'{FLAGS.round}', 'global')
        model.save(model_path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Debug message')
    parser.add_argument('--mode', choices=['init', 'agg'],
                        help='The server mode')
    parser.add_argument('--output', required=True, type=str,
                        help='The output directory')
    parser.add_argument('--round', type=int,
                        help='The round in aggregation mode')

    FLAGS, _ = parser.parse_known_args()
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))
    DEBUG = FLAGS.debug

    main()
