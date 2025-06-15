import os 

BATCH = 16
EPOCHS = 100
WANDBON = True
LR = 0.0001
N_CLASSES = 9
DEVICE = "cuda:0"
SAVE_DIR = os.path.join(os.getcwd(), "training\\weights")
