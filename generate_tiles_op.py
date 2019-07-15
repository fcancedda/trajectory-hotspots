from app.lib.ops.tiles import GenerateTilesOp
import pickle
import os

global_origin = (39.75872, 116.04142)
ds = 200  # 100 200 500 1000 delta_space
dt = 500  # 300 500 600 1200 delta_time
step = 60  # integration step size ( 1 MIN )
max_tp = 1  # maximum throughput allowed by system

# ___LOAD TILES____ #
directory = "app/data/out/generated_grid_op_" + str(ds) + "_" + str(dt) + ".csv"
if not os.path.isfile(directory):
    tiles = GenerateTilesOp(ds, dt, global_origin).output()
    with open(directory, 'wb') as f:
        pickle.dump(tiles, f)
else:
    print("File Already Exists...")

# ____READ TILES___ #
with open(directory, 'rb') as f:
    load_dict = pickle.load(f)

# ___ANALYZE EACH TILE INDIVIDUALLY____ #
for key, data in load_dict.items():
    print("key: {}".format(str(key)))
    print(data)
    break
