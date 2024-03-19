import os
import uuid

import torch

DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

DEVICE_ID = [0]

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(PROJECT_PATH, "data")

MODEL_PATH = os.path.join(PROJECT_PATH, "trained_model")

if __name__ == '__main__':
    image_name = str(uuid.uuid4()) + ".png"
    image_path = os.path.join(DATA_PATH, image_name)
    print(image_path)

