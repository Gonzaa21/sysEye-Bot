import os
import pandas as pd
import matplotlib.pyplot as plt

# indentify last snapshot
SNAPSHOT_DIR = "C:\Users\Usuario\Downloads\sysEye\snapshots"
def load_last_snapshot(snapshot_dir=SNAPSHOT_DIR):
    with open(os.path.join(snapshot_dir, "latest.txt"), "r") as f:
        filename = f.read().strip()
    filepath = os.path.join(snapshot_dir, filename)
    return pd.read_csv(filepath), filename

# generate graphs
def graphs():
    pass
# send to main.