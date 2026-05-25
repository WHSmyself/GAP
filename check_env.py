# -*- coding: utf-8 -*-
import sys

print("Python:", sys.version)

import torch
print("torch:", torch.__version__)
print("torch.version.cuda:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

import torch_geometric
print("torch_geometric:", torch_geometric.__version__)

import numpy, pandas, sklearn, joblib, optuna
print("numpy:", numpy.__version__)
print("pandas:", pandas.__version__)
print("sklearn:", sklearn.__version__)
print("joblib:", joblib.__version__)
print("optuna:", optuna.__version__)

# Test compiled project modules.
# Run this file in the same directory as:
# data_loader.cpython-311-x86_64-linux-gnu.so
# model.cpython-311-x86_64-linux-gnu.so
# train_test.cpython-311-x86_64-linux-gnu.so
# utils.cpython-311-x86_64-linux-gnu.so
import data_loader
import model
import utils
import train_test

print("Compiled modules import OK.")
