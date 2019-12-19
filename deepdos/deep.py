import os

import deepdos.conf as conf
import deepdos.data as data
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.utils.np_utils import to_categorical


class DeepdosNN:
    def __init__(self):
        self.learning_rate = 0.001
        self.training_epochs = 15
        self.batch_size = 50
        self.display_step = 1

        # Initialize our weights and biases alongside with creating a list
        # of pointers to all of our trainable variables
        self.weights, self.biases = self.initialize_weights_and_biases()
        self.trainable_vars = list(self.weights.values()) + list(self.biases.values())

        # Instantiate the adam optimizer, our categorical cross entropy
        # loss function, and our accuracy metrics
        self.optimizer = tf.optimizers.Adam(learning_rate=self.learning_rate)
        self.loss_fn = tf.losses.BinaryCrossentropy()
        self.accuracy = tf.metrics.Accuracy()

    def forward_pass(self, inputs):
        """
            Create the MLP layer for constructing our model
        """
        # Hidden fully connected layer with 256 neurons
        layer_1 = tf.nn.relu(
            tf.add(
                tf.matmul(tf.cast(inputs, tf.float32), self.weights["h1"]),
                self.biases["b1"],
            )
        )
        # Hidden fully connected layer with 256 neuorns
        layer_2 = tf.nn.relu(
            tf.add(tf.matmul(layer_1, self.weights["h2"]), self.biases["b2"])
        )
        # Output fully connected layer with a neuron for each class
        out_layer = tf.matmul(layer_2, self.weights["out"]) + self.biases["out"]

        return out_layer

    def initialize_weights_and_biases(self):
        """
            Initialize the weights and biases that will be applied to our
            neural network.

            Returns:
                Dictionaries containing the tensorflow variables
        """
        # Setup weights with randomly distributed data inside of a 2D tensor with
        # the dimenisons equal to the amount of mappings between each layer.
        n_hidden_1 = 256
        n_hidden_2 = 256
        n_input = 78
        n_classes = 2

        weights = {
            "h1": tf.Variable(
                tf.random.normal([n_input, n_hidden_1]), name="h1-weights"
            ),
            "h2": tf.Variable(
                tf.random.normal([n_hidden_1, n_hidden_2]), name="h2-weights"
            ),
            "out": tf.Variable(
                tf.random.normal([n_hidden_2, n_classes]), name="h3-weights"
            ),
        }

        # Setup biases with a random distribution of a 1D tensor equal to the amount
        # of perceptrons at each layer.
        biases = {
            "b1": tf.Variable(tf.random.normal([n_hidden_1]), name="h1-bias"),
            "b2": tf.Variable(tf.random.normal([n_hidden_2]), name="h2-bias"),
            "out": tf.Variable(tf.random.normal([n_classes]), name="out-bias"),
        }

        return weights, biases

    @tf.function
    def propagate(self, x_batch, y_batch):
        """
            Complete both forward and backward propagation on our
            batches.
        """
        # Record operations to automatically obtain the gradients
        with tf.GradientTape() as tape:
            logits = self.forward_pass(x_batch)
            # Calculates the total loss of the entire network
            loss = self.loss_fn(y_batch, tf.nn.sigmoid(logits))

            # Compute the accuracy of our model
            # (Convert our logits to softmax distribution)
            self.accuracy(y_batch, tf.nn.sigmoid(logits))

            gradients = tape.gradient(loss, self.trainable_vars)
            self.optimizer.apply_gradients(zip(gradients, self.trainable_vars))

        return loss

    def load_dataframes(self, batch_size: int) -> pd.DataFrame:
        """
            Load up our dataframes that have now split the data.

            Returns:
                A dataframe that contains 100k samples of both
        """

        processed_ddos_chunk = None
        processed_benign_chunk = None
        counter = 0

        features = None

        # TODO This reads through the dataset at two separate points, but has
        # to open the same file descriptor twice in order to read at
        # different sections. Is it possible to avoid this?

        ddos_dataset = pd.read_csv(
            f"{conf.ROOT_DIR}/../ddos_balanced/xaa.csv", chunksize=batch_size // 2
        )

        benign_dataset = pd.read_csv(
            f"{conf.ROOT_DIR}/../ddos_balanced/xab.csv", chunksize=batch_size // 2
        )

        for ddos_chunk, benign_chunk in zip(ddos_dataset, benign_dataset):

            if features is None:
                features = ddos_chunk.columns
                benign_chunk.columns = features
            else:
                ddos_chunk.columns = features
                benign_chunk.columns = features

            data.preprocess_df(ddos_chunk)
            data.preprocess_df(benign_chunk)

            yield pd.concat([ddos_chunk, benign_chunk])

    def train_model(self):
        """
            Train the model
        """
        # Wrap funcion within this scope for easy access to variables
        batch_size = 10000

        # Iteratively loop over each batch of data
        for epoch in range(self.training_epochs):
            avg_cost = 0

            counter = 1
            # Iterate over each batch and compute the average loss
            for chunk in self.load_dataframes(batch_size):

                x_train, x_test, y_train, y_test = data.get_train_test(chunk)

                # Obtain batches
                x_batch, y_batch = (x_train, to_categorical(y_train, num_classes=2))

                cost = self.propagate(x_batch, y_batch)
                avg_cost += cost / batch_size
                print(f"Chunk {counter} / {12794627 // batch_size}")
                counter += 1

            # When to display output
            if epoch % self.display_step == 0:
                print(f"Epoch:{epoch + 1}")
                print(f"Avg loss: {avg_cost}")
                print(f"accuracy: {float(self.accuracy.result())}")

            self.accuracy.reset_states()

    def shuffle_csv(self, csv_location, batch_size):
        """
            Shuffle the csv so that we can obtain better results
        """
        curr_csv = csv_location
        # FIXME this doesn't shuffle the dataset in the way we'd like it to.
        # How can we fix that?
        for i in range(1000):
            for chunk in pd.read_csv(curr_csv, index_col=0, chunksize=batch_size):
                sampled = chunk.sample(1).reset_index(drop=True)
                sampled.to_csv(f"samples/test.csv", mode="a")

            print(f"Shuffled {i} / 1000 times")

            curr_csv = f"samples/test{i}.csv"


def main():
    deepdos_nn = DeepdosNN()

    deepdos_nn.train_model()


if __name__ == "__main__":
    main()
