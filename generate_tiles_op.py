from app.lib.ops.tiles import GenerateTilesOp
from app.lib.data_serializer import DataSerializer as DS
import os

global_origin = (39.75872, 116.04142)
ds = 200  # 100 200 500 1000 delta_space
dt = 500  # 300 500 600 1200 delta_time
step = 60  # integration step size ( 1 MIN )
max_tp = 1  # maximum throughput allowed by system

# ___LOAD TILES____ #
directory = "app/data/out/generated_grid_" + str(ds) + "_" + str(dt) + ".csv"
new_directory = "app/data/out/generated_grid_new_" + str(ds) + "_" + str(dt) + ".csv"
op_directory = "app/data/out/generated_grid_op_" + str(ds) + "_" + str(dt) + ".csv"

if not os.path.isfile(op_directory):
    tiles = GenerateTilesOp(ds, dt, global_origin).output()
    DS.save_data(tiles, op_directory)
    # with open(op_directory, 'wb') as f:
    #     pickle.dump(tiles, f)
else:
    print("File Already Exists...")

    # ____READ OP TILES___ #
    load_dict = DS.reload_data(op_directory)
    # with open(op_directory, 'rb') as f:
    #     load_dict = pickle.load(f)
    # ___ANALYZE EACH TILE INDIVIDUALLY____ #
    for key, data in load_dict.items():
        print("\nOP key: {}".format(str(key)))
        print(len(load_dict.keys()))
        total = 0
        for item in load_dict.items():
            total += len(item)
        print(total)
        print(data)
        break

    # ____READ OG TILES___ #
    load_dict = DS.reload_data(directory)
    # with open(directory, 'rb') as f:
    #     load_dict = pickle.load(f)
    # ___ANALYZE EACH TILE INDIVIDUALLY____ #
    for key, data in load_dict.items():
        print("\nOG key: {}".format(str(key)))
        print(len(load_dict.keys()))
        total = 0
        for item in load_dict.items():
            total += len(item)
        print(total)
        print(data)
        break

