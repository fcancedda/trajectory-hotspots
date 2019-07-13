from app.lib.ops.tiles import GenerateTilesOp
import pickle


global_origin = (39.75872, 116.04142)
ds = 200  # 100 200 500 1000 delta_space
dt = 500  # 300 500 600 1200 delta_time
step = 60  # integration step size ( 1 MIN )
max_tp = 1  # maximum throughput allowed by system

# ___LOAD TILES____ #
tiles = GenerateTilesOp(ds, dt, global_origin).output()
with open("app/data/out/generated_grid2_" + str(ds) + "_" + str(dt) + ".csv", 'wb') as f:
    pickle.dump(tiles, f)