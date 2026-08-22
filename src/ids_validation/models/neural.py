"""Exact Stage 2 and Stage 3 Keras architecture builders."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def build_mlp_baseline() -> Any:
    """Build the Stage 2 baseline MLP without fitting it.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 95
    Original stage: Stage 2
    Frozen artifacts generated: metadata/neural_baseline_configurations.json, results/baseline/baseline4_neural_validation_results.csv
    Notes: TensorFlow version is not proven by frozen repository evidence.
    """

    import tensorflow as tf

    return tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(78,)),
            tf.keras.layers.Dense(256, activation="relu", kernel_initializer="he_normal"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.20),
            tf.keras.layers.Dense(128, activation="relu", kernel_initializer="he_normal"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.20),
            tf.keras.layers.Dense(64, activation="relu", kernel_initializer="he_normal"),
            tf.keras.layers.Dropout(0.20),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ],
        name="mlp_baseline",
    )


def build_cnn_baseline() -> Any:
    """Build the Stage 2 baseline 1D-CNN without fitting it.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 95
    Original stage: Stage 2
    Frozen artifacts generated: metadata/neural_baseline_configurations.json, results/baseline/baseline4_neural_validation_results.csv
    Notes: The input shape is (78, 1) in the authoritative run.
    """

    from tensorflow.keras import Model
    from tensorflow.keras.layers import BatchNormalization, Conv1D, Dense, Dropout, GlobalAveragePooling1D, Input, MaxPooling1D

    inputs = Input(shape=(78, 1))
    x = Conv1D(128, 3, padding="same", activation="relu")(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling1D(pool_size=2)(x)
    x = Dropout(0.25)(x)
    x = Conv1D(256, 3, padding="same", activation="relu")(x)
    x = BatchNormalization()(x)
    x = GlobalAveragePooling1D()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.30)(x)
    outputs = Dense(1, activation="sigmoid")(x)
    return Model(inputs=inputs, outputs=outputs, name="cnn_baseline")


def build_lstm_baseline() -> Any:
    """Build the Stage 2 baseline LSTM without fitting it.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 95
    Original stage: Stage 2
    Frozen artifacts generated: metadata/neural_baseline_configurations.json, results/baseline/baseline4_neural_validation_results.csv
    Notes: Uses one 64-unit LSTM with return_sequences=False and dropout=0.20.
    """

    from tensorflow.keras import Model
    from tensorflow.keras.layers import Dense, Dropout, Input, LSTM

    inputs = Input(shape=(78, 1))
    x = LSTM(64, return_sequences=False, dropout=0.20)(inputs)
    x = Dense(64, activation="relu")(x)
    x = Dropout(0.25)(x)
    outputs = Dense(1, activation="sigmoid")(x)
    return Model(inputs=inputs, outputs=outputs, name="lstm_baseline")


def build_transformer_baseline() -> Any:
    """Build the Stage 2 single-block Transformer encoder without fitting it.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 95
    Original stage: Stage 2
    Frozen artifacts generated: metadata/neural_baseline_configurations.json, results/baseline/baseline4_neural_validation_results.csv
    Notes: Recreates the trainable positional Embedding layer locally.
    """

    import tensorflow as tf
    from tensorflow.keras import Model
    from tensorflow.keras.layers import Add, Dense, Dropout, Embedding, GlobalAveragePooling1D, Input, Layer, LayerNormalization, MultiHeadAttention

    sequence_length = 78
    embedding_dimension = 64

    class TrainablePositionEmbedding(Layer):
        def __init__(self, sequence_length: int, embedding_dimension: int, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self.sequence_length = sequence_length
            self.embedding_dimension = embedding_dimension
            self.position_embedding = Embedding(input_dim=sequence_length, output_dim=embedding_dimension)

        def call(self, inputs: Any) -> Any:
            positions = tf.range(start=0, limit=self.sequence_length, delta=1)
            return inputs + self.position_embedding(positions)

        def get_config(self) -> dict[str, Any]:
            config = super().get_config()
            config.update({"sequence_length": self.sequence_length, "embedding_dimension": self.embedding_dimension})
            return config

    inputs = Input(shape=(sequence_length, 1))
    x = Dense(embedding_dimension)(inputs)
    x = TrainablePositionEmbedding(sequence_length, embedding_dimension, name="position_embedding")(x)
    attention = MultiHeadAttention(num_heads=4, key_dim=16, dropout=0.10)(query=x, value=x, key=x)
    x = LayerNormalization(epsilon=1e-6)(Add()([x, attention]))
    feed_forward = Dense(128, activation="relu")(x)
    feed_forward = Dropout(0.10)(feed_forward)
    feed_forward = Dense(embedding_dimension)(feed_forward)
    x = LayerNormalization(epsilon=1e-6)(Add()([x, feed_forward]))
    x = GlobalAveragePooling1D()(x)
    x = Dense(64, activation="relu")(x)
    x = Dropout(0.20)(x)
    outputs = Dense(1, activation="sigmoid")(x)
    return Model(inputs=inputs, outputs=outputs, name="transformer_baseline")


def build_tuned_mlp(hidden_layers: Sequence[int], dropout: float, learning_rate: float) -> Any:
    """Build and compile one Stage 3 validation-safe MLP candidate.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 99
    Original stage: Stage 3
    Frozen artifacts generated: results/tuning/mlp/mlp_best_parameters.json, results/tuning/mlp/mlp_candidate_validation_results.csv
    Notes: Candidate selection uses external validation F1 at threshold 0.50.
    """

    import tensorflow as tf

    inputs = tf.keras.layers.Input(shape=(78,), name="traffic_features")
    x = inputs
    for layer_number, units in enumerate(hidden_layers, start=1):
        x = tf.keras.layers.Dense(units, activation=None, kernel_initializer="he_normal", name=f"dense_{layer_number}")(x)
        x = tf.keras.layers.BatchNormalization(name=f"batch_norm_{layer_number}")(x)
        x = tf.keras.layers.Activation("relu", name=f"relu_{layer_number}")(x)
        x = tf.keras.layers.Dropout(dropout, name=f"dropout_{layer_number}")(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid", name="attack_probability")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="validation_safe_mlp")
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="binary_crossentropy", metrics=["accuracy"])
    return model


def build_tuned_cnn(filters: Sequence[int], kernel_size: int, dropout: float, dense_units: int, learning_rate: float) -> Any:
    """Build and compile one Stage 3 validation-safe 1D-CNN candidate.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 100
    Original stage: Stage 3
    Frozen artifacts generated: results/tuning/cnn/cnn_best_parameters.json, results/tuning/cnn/cnn_candidate_validation_results.csv
    Notes: Max pooling is omitted after the final convolution, exactly as sourced.
    """

    import tensorflow as tf

    inputs = tf.keras.layers.Input(shape=(78, 1), name="traffic_features")
    x = inputs
    for layer_number, filter_count in enumerate(filters, start=1):
        x = tf.keras.layers.Conv1D(filters=filter_count, kernel_size=kernel_size, padding="same", activation=None, kernel_initializer="he_normal", name=f"conv_{layer_number}")(x)
        x = tf.keras.layers.BatchNormalization(name=f"batch_norm_{layer_number}")(x)
        x = tf.keras.layers.Activation("relu", name=f"relu_{layer_number}")(x)
        if layer_number < len(filters):
            x = tf.keras.layers.MaxPooling1D(pool_size=2, name=f"pool_{layer_number}")(x)
        x = tf.keras.layers.Dropout(dropout, name=f"conv_dropout_{layer_number}")(x)
    x = tf.keras.layers.GlobalAveragePooling1D(name="global_average_pooling")(x)
    x = tf.keras.layers.Dense(dense_units, activation="relu", kernel_initializer="he_normal", name="dense_hidden")(x)
    x = tf.keras.layers.BatchNormalization(name="dense_batch_norm")(x)
    x = tf.keras.layers.Dropout(dropout, name="dense_dropout")(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid", name="attack_probability")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="validation_safe_1d_cnn")
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss="binary_crossentropy", metrics=["accuracy"])
    return model
