from typing import Any, Dict, Tuple

import keras
import tensorflow as tf
from tensorflow.keras.saving import deserialize_keras_object, serialize_keras_object
from numpy.typing import NDArray

@keras.utils.register_keras_serializable("nengo-edge-models")
class TiedDeembedding(keras.layers.Layer):
    """Layer to perform deembedding using the weights of an embedding layer."""

    def __init__(
        self,
        embedding_layer: keras.layers.Layer,
        use_bias: bool = True,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.supports_masking = True
        self.embedding_layer = embedding_layer
        self.use_bias = use_bias

    @property
    def embeddings(self) -> NDArray:
        """Retrieve embeddings."""
        if not hasattr(self.embedding_layer, "embeddings"):
            self.embedding_layer.build(None)
        return self.embedding_layer.embeddings

    def build(self, input_shape: Tuple[int, ...]) -> None:
        super().build(input_shape)

        self.bias = None
        if self.use_bias:
            output_dim = self.embedding_layer.input_dim
            self.bias = self.add_weight(
                name="bias", shape=output_dim, initializer="zeros"
            )

    def call(self, inputs: NDArray) -> NDArray:
        y = tf.matmul(inputs, self.embeddings, transpose_b=True)
        if self.bias is not None:
            y = tf.nn.bias_add(y, self.bias)
        return y

    def get_config(self) -> Dict:
        return {
            **super().get_config(),
            "embedding_layer": serialize_keras_object(self.embedding_layer),
            "use_bias": self.use_bias,
        }

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "TiedDeembedding":
        config["embedding_layer"] = deserialize_keras_object(config["embedding_layer"])
        return cls(**config)
