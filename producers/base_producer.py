"""Base producer class for handling image messages"""
import abc
from typing import Dict
import json
import time
import utils
import numpy as np


class BaseProducer(abc.ABC):
    """Abstract base class for Producers"""

    @abc.abstractmethod
    def send_image(
        self,
        img_array: np.ndarray,
        model_name: str,
        topic: str,
    ) -> None:
        """Send an image array to a streaming topic"""
        pass

    @staticmethod
    def encode_message(model_name: str, img_array: np.ndarray) -> Dict:
        """Prepare payload to be sent to GCP Pub/Sub"""
        payload = {
            "model": model_name,
            "img_data": json.dumps(img_array, cls=utils.NumpyArrayEncoder),
            "time": time.time(),
        }
        return json.dumps(payload).encode("utf-8")