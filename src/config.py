import os

BASE_DIR = "/home/vitor/govtrack-br"
DATA_PATH = os.getenv("DATA_PATH", os.path.join(BASE_DIR, "data"))