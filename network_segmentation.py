import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import quad
from itertools import combinations
import pandas as pd
import os

from app.lib.data_serializer import DataSerializer as DS
from app.lib.ops.tiles import GenerateTilesOp  # , GraphContactPointsOp


def find_bounding_tiles(tile_x_pos, tile_y_pos, tile_time, d_s):
    bounding_tiles = [str(tile_x_pos - d_s) + "_" + str(tile_y_pos + d_s) + "_" + str(tile_time),
                      str(tile_x_pos) + "_" + str(tile_y_pos + d_s) + "_" + str(tile_time),
                      str(tile_x_pos + d_s) + "_" + str(tile_y_pos + d_s) + "_" + str(tile_time),
                      str(tile_x_pos - d_s) + "_" + str(tile_y_pos) + "_" + str(tile_time),
                      str(tile_x_pos + d_s) + "_" + str(tile_y_pos) + "_" + str(tile_time),
                      str(tile_x_pos - d_s) + "_" + str(tile_y_pos - d_s) + "_" + str(tile_time),
                      str(tile_x_pos) + "_" + str(tile_y_pos - d_s) + "_" + str(tile_time),
                      str(tile_x_pos + d_s) + "_" + str(tile_y_pos - d_s) + "_" + str(tile_time)]
    return bounding_tiles


def add_bounding_point_to_user(user_segment_pts, bd_pt, pid_diff):
    if pid_diff == 1:
        user_segment_pts.insert(0, (bd_pt[1], bd_pt[2], bd_pt[3], bd_pt[4], bd_pt[5]))
    elif pid_diff == -1:
        user_segment_pts.append((bd_pt[1], bd_pt[2], bd_pt[3], bd_pt[4], bd_pt[5]))
    return user_segment_pts


def user_distance_euclid(time, x1, x2, y1, y2):
    return np.sqrt((x2(time) - x1(time)) ** 2 + (y2(time) - y1(time)) ** 2)


def throughput_analysis(tiles, delta_s, delta_t, step, max_tp):
    # ___ distance function & results array____ #
    columns = ['USER 1', 'Loc1', 'USER 2', 'Loc2', 't_start', 't_end', 'Distance', 'TP']
    output = []
    index = []
    for tile_key, tile_points in tiles.items():
        number_of_points = len(tile_points)
        if number_of_points > 1:
            user_tracker_d = {}
            splines = []
            # ___(X_KEY, Y_KEY, TIME_KEY)____ #  alternative: list(map(int, tile_key.split('_')))
            (x_key, y_key, time_key) = [int(x) for x in tile_key.split("_")]  # grab tile details
            # ___LOOK AT EACH POINT IN TILE____ #
            print("number of points in {}: {}".format(tile_key, number_of_points))
            for pt_i in range(number_of_points):
                current_user = tile_points[pt_i][0]
                data = (tile_points[pt_i][1], tile_points[pt_i][2], tile_points[pt_i][3], tile_points[pt_i][4],
                        tile_points[pt_i][5])
                if current_user not in user_tracker_d:
                    user_tracker_d[current_user] = [data]
                else:
                    user_tracker_d[current_user].append(data)
            # ______SCAN BOUNDING TILES________ #
            surrounding_tiles = find_bounding_tiles(x_key, y_key, time_key, int(delta_s))

            for surrounding_key in surrounding_tiles:

                if surrounding_key in tiles:  # if tile exists
                    print("Found bounding tile_key: {}".format(surrounding_key))
                    points_in_b_tile = tiles[surrounding_key]  # grab points
                    for bounding_pt_i in range(len(points_in_b_tile)):
                        current_point = points_in_b_tile[bounding_pt_i]
                        current_user = current_point[0]
                        if current_user in user_tracker_d:
                            initial_user_pid = user_tracker_d[current_user][0][2]
                            final_user_pid = user_tracker_d[current_user][-1][2]
                            # ___APPEND TO CURRENT USER SEGMENT____ #
                            if initial_user_pid - current_point[3] == 1:  # predecessor
                                print("found pred")
                                user_tracker_d[current_user] = add_bounding_point_to_user(user_tracker_d[current_user],
                                                                                          current_point, 1)
                            elif current_point[3] - final_user_pid == 1:  # successor
                                print("found successor")
                                user_tracker_d[current_user] = add_bounding_point_to_user(user_tracker_d[current_user],
                                                                                          current_point, -1)
            for user, segment in user_tracker_d.items():
                seg_count = len(segment)
                print("current user {} has {} points".format(user, seg_count))
                if seg_count < 2:
                    continue
                else:
                    # ___RETRIEVE USER DATA___
                    x_vals = [x[0] for x in segment]  # x_Axis values
                    y_vals = [x[1] for x in segment]  # y_Axis values
                    t_vals = [x[3] for x in segment]  # time values
                    c_vals = [x[4] for x in segment]  # coordinate values
                    # ____INTERPOLATE AND SAVE____ #
                    x_spline = interp1d(t_vals, x_vals, fill_value="extrapolate")
                    y_spline = interp1d(t_vals, y_vals, fill_value="extrapolate")
                    splines.append([x_spline, y_spline, t_vals, user, c_vals])

                # ___COMPARE POSSIBLE SPLINE COMBINATIONS___ #
            for combo in combinations(splines, 2):
                x1, y1, t1, u1, coord1 = combo[0]  # x_interp, y_interp, time, user
                x2, y2, t2, u2, coord2 = combo[1]  # x_interp, y_interp, time, user
                # __CONFIRM USER INTERACTION___ #
                if max(t1) < min(t2) or max(t2) < min(t1):  # check interaction time overlaps
                    print("users {}, {} have no interaction time in ".format(u1, u2, tile_key))
                    continue
                else:
                    # ___GRAB SPLINE DURING INTERACTION SPAN___ #
                    start_time = max(t1[0], t2[0])
                    stop_time = min(t1[-1], t2[-1])
                    t = np.arange(start_time, stop_time + 1, step)
                    # t = np.linspace(start_time, stop_time, int(delta_t / 60))  # one minute intervals
                    # ___THROUGHPUT CALCULATIONS----
                    for i in range(len(t) - 1):
                        integral = quad(user_distance_euclid, t[i], t[i + 1], args=(x1, x2, y1, y2))[0] / step
                        if integral != 0:
                            tp = max_tp * integral / integral ** 2
                            output.append([u1, coord1[0], u2, coord2[0], t[i], t[i + 1], integral, tp])
                        else:
                            output.append([u1, coord1[0], u2, coord2[0], t[i], t[i + 1], integral, max_tp])
                        index.append(t[i])

    df = pd.DataFrame(data=output, index=index, columns=columns)
    print(df)


def main():
    ds = 200  # 100 200 500 1000 delta_space
    dt = 500  # 300 500 600 1200 delta_time
    step = 60  # integration step size ( 1 MIN )
    max_tp = 1  # maximum throughput allowed by system

    # ___LOAD TILES____ #
    directory = "app/data/out/generated_grid_" + str(ds) + "_" + str(dt) + ".csv"
    op_directory = "app/data/out/generated_grid_op_" + str(ds) + "_" + str(dt) + ".csv"
    # new_directory = "app/data/out/generated_grid_new_" + str(ds) + "_" + str(dt) + ".csv"

    # ___ANALYZE EACH TILE INDIVIDUALLY____ #
    if os.path.isfile(directory):
        tiles = DS.reload_data(directory)
        # with open(op_directory, 'rb') as f:
        #     tiles = pickle.load(f)
        throughput_analysis(tiles, ds, dt, step, max_tp)
    else:
        print("missing tile dictionary")

    # graph_op = GraphContactPointsOp(tiles, weight='dist_weight').hottest_tile()


main()
