""" Module for handling model compilation and training """
import pickle
from typing import Tuple

import data_processing as dproc
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.python.keras.callbacks as cbacks

MODEL_DIR = "models/"
TRAIN_EPOCHS = 10


def create_and_compile_model(D_x: int, D_y: int) -> keras.models.Sequential:
    """Compiles a baseline CNN model using ReLu activation and He Weight Initialization scheme"""
    theModel = keras.models.Sequential(
        [
            keras.layers.Conv2D(
                10,
                (3, 3),
                activation="relu",
                kernel_initializer="he_uniform",
                input_shape=(D_x, D_x, 1),
            ),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(10, activation="relu", kernel_initializer="he_uniform"),
            keras.layers.Dense(D_y, activation="softmax"),
        ]
    )

    theModel.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    return theModel


def save_trained_model(
    model_name: str, theModel: keras.models.Sequential, trainHistory: cbacks.History
) -> None:
    """Saves a tensorflow model and training history to local file storage"""
    with open(f"{MODEL_DIR}{model_name}_trainHistoryDict.p", "wb") as fp:
        pickle.dump(trainHistory.history, fp)
    theModel.save(model_name)


def load_model_history(
    model_name: str,
) -> Tuple[keras.models.Sequential, cbacks.History]:
    """Loads a training tensorflow model and training history from local file storage"""
    model = keras.models.load_model(f"{MODEL_DIR}{model_name}")
    trainHistory = pickle.load(
        open(f"{MODEL_DIR}{model_name}_trainHistoryDict.p", "rb")
    )
    return model, trainHistory


def plot_training_history(model_name: str, trainHistory: cbacks.History) -> None:
    metric_names = list(trainHistory.keys())
    for name in metric_names:
        plt.plot(trainHistory[name])
        plt.legend(metric_names)

    plt.title(f"Training Metrics for Model {model_name}")
    plt.show()


def fit_cnn_model(
    model: keras.models.Sequential,
    trainGen: dproc.DataGenerator,
    valGen: dproc.DataGenerator,
    enable_gpu: bool = True,
) -> Tuple[keras.models.Sequential, cbacks.History]:
    """Train a compiled Tensorflow CNN model on GPU"""

    if enable_gpu:
        tf.config.run_functions_eagerly(False)
        tf.device(device_name="/GPU:0")

    trainHistory = model.fit(
        trainGen,
        epochs=TRAIN_EPOCHS,
        verbose=1,
        callbacks=[
            cbacks.EarlyStopping(monitor="val_accuracy", mode="max", min_delta=1)
        ],
        validation_data=valGen,
    )
    return model, trainHistory