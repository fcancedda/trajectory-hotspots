import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, interp2d
from scipy.integrate import quad
from itertools import combinations
import pandas as pd
import os

from app.lib.parsing_ops import DataSerializer as Pickle

from app.lib.ops.tiles import GenerateTilesOp  # , GraphContactPointsOp
data = {'0_0_0': [
    ["000", 0, 0, 5892, 10.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["000", 89, 25, 5893, 25.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["000", 300, 26, 5894, 80.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["000", 682, 20.556466667167, 5895, 120.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["000", 782, 200.556466667167, 5896, 130.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["000", 982, 280.556466667167, 5897, 160.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 0.250088684767, 823.78153333345, 60266, 0.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 20.105854214085, 629.00480000035,  60267, 20.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 100.105854214085, 537.895466666683,  60268, 40.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 198.191430766772, 647.675200000598,  60269, 60.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 250.763548002113, 252.89846666671,  60270, 100.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 699.421241790144, 157.89946666672,  60271, 120.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 720.421241790144, 207.89946666672,  60272, 121.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 759.421241790144, 157.89946666672,  60273, 130.0, ('39.994622', '116.326757'), (1000, 1200)],
    ["012", 900.43851912883, 251.342600000025, 60274, 149.0, ('39.994622', '116.326757'), (1000, 1200)]],
    '0_1000_0': [
        ['000', 1200, 499, 5898, 190.0, ('39.994622', '116.326757'), (1000, 1200)],
        ['012', 1050, 350, 60275, 185.0, ('39.994622', '116.326757'), (1000, 1200)]
    ]}


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


def add_point_to_user_segment(user_segment_pts, bd_pt, pid_diff):
    if pid_diff == 1:
        user_segment_pts.insert(0, (bd_pt[1:6]))  # , bd_pt[2], bd_pt[3], bd_pt[4], bd_pt[5]))
    elif pid_diff == -1:
        user_segment_pts.append((bd_pt[1:6]))  # , bd_pt[2], bd_pt[3], bd_pt[4], bd_pt[5]))
    return user_segment_pts


def user_distance_euclid(time, x1, x2, y1, y2):
    return np.sqrt((x2(time) - x1(time)) ** 2 + (y2(time) - y1(time)) ** 2)


def throughput_analysis(tiles, delta_s, delta_t, step, max_tp):
    # ___ distance function & results array____ #
    columns = ['USER 1', 'Loc 1', 'USER 2', 'Loc2', 't_start', 't_end', 'Distance', 'TP']
    output = []
    index = []
    for tile_key, tile_pts in tiles.items():
        fig1, ax1 = plt.subplots()
        users_in_tile = set()
        for i in tile_pts:
            users_in_tile.add(i[0])
        if 3 > len(users_in_tile) > 1:
            user_tracker_d = {}
            splines = []
            # ___(X_KEY, Y_KEY, TIME_KEY)____ #  alternative: list(map(int, tile_key.split('_')))
            (x_key, y_key, time_key) = [int(x) for x in tile_key.split("_")]  # grab tile details
            # ___LOOK AT EACH POINT IN TILE____ #
            print("number of users in {}: {}".format(tile_key, users_in_tile))
            for pt_i in range(len(tile_pts)):
                current_user = tile_pts[pt_i][0]
                user_data = (tile_pts[pt_i][1:6])  #  tile_pts[pt_i][2], tile_pts[pt_i][3], tile_pts[pt_i][4], tile_pts[pt_i][5]
                if current_user not in user_tracker_d:
                    user_tracker_d[current_user] = [user_data]
                else:
                    user_tracker_d[current_user].append(user_data)
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
                                print("found predecessor")
                                user_tracker_d[current_user] = add_point_to_user_segment(user_tracker_d[current_user],
                                                                                         current_point, 1)
                            elif current_point[3] - final_user_pid == 1:  # successor
                                print("found successor")
                                user_tracker_d[current_user] = add_point_to_user_segment(user_tracker_d[current_user],
                                                                                         current_point, -1)
            for user, segment in user_tracker_d.items():
                seg_count = len(segment)
                print("current user {} has {} points".format(user, seg_count))
                if seg_count < 2:
                    print('user {} seg count too short. spline not saved'.format(user))
                    continue
                else:
                    # ___RETRIEVE USER DATA___
                    x_vals = [x[0] for x in segment]  # x_Axis values
                    y_vals = [x[1] for x in segment]  # y_Axis values
                    t_vals = [x[3] for x in segment]  # time values
                    c_vals = [x[4] for x in segment]  # coordinate values
                    # ____INTERPOLATE AND SAVE____ #
                    x_spline = interp1d(t_vals, x_vals, kind='cubic', fill_value="extrapolate")
                    y_spline = interp1d(t_vals, y_vals, kind='cubic', fill_value="extrapolate")
                    splines.append([x_spline, y_spline, t_vals, user, c_vals])

                    # ____PLOT REAL USER POINTS____ #
                    ax1.plot(x_vals, y_vals, 'o', label='User: ' + str(user))
            # ___COMPARE POSSIBLE SPLINE COMBINATIONS___ #
            for combo in combinations(splines, 2):
                x1, y1, t1, u1, coord1 = combo[0]  # x_interp, y_interp, time, user, location
                x2, y2, t2, u2, coord2 = combo[1]  # x_interp, y_interp, time, user, location
                # __CONFIRM USER INTERACTION___ #
                if max(t1) < min(t2) or max(t2) < min(t1):  # check interaction time overlaps
                    print("users {}, {} have no interaction in ".format(u1, u2, tile_key))
                    fig1, ax1 = plt.subplots()
                    continue
                else:
                    print("Found Interaction")
                    # ___GRAB SPLINE DURING INTERACTION SPAN___ #
                    start_time, stop_time = max(t1[0], t2[0]), min(t1[-1], t2[-1])
                    c_i = np.arange(start_time, stop_time + 1, step)  # communication intervals
                    # t = np.linspace(start_time, stop_time, int(delta_t / 60))  # one minute intervals
                    print(c_i)
                    # ____PLOT SPLINE____ #
                    x_spline_u1, y_spline_u1, x_spline_u2, y_spline_u2 = x1(c_i), y1(c_i), x2(c_i), y2(c_i)
                    ax1.plot(x_spline_u1, y_spline_u1, '-', label=u1)
                    ax1.plot(x_spline_u2, y_spline_u2, '-', label=u2)

                    distance = np.sqrt((x_spline_u2 - x_spline_u1) ** 2 + (y_spline_u2 - y_spline_u1) ** 2)
                    # ___THROUGHPUT CALCULATIONS----
                    integrals = []
                    for i in range(len(c_i) - 1):
                        integral = quad(user_distance_euclid, c_i[i], c_i[i + 1], args=(x1, x2, y1, y2))[0] / step
                        integrals.append(integral)
                        if integral != 0:
                            tp = max_tp * integral / integral ** 2
                            output.append([u1, coord1[0], u2, coord2[0], c_i[i], c_i[i + 1], integral, tp])
                        else:
                            output.append([u1, coord1[0], u2, coord2[0], c_i[i], c_i[i + 1], integral, max_tp])
                        index.append(c_i[i])
                    # ___PLOT DISTANCE AT GIVEN TIME____ #
                    # temp_x_val = min(x_spline_u1[0], x_spline_u2[0])
                    for i in range(len(x_spline_u1)):
                        # if abs(temp_x_val - max(x_spline_u1[i], x_spline_u2[i])) < 100:
                        #     print('distance failure')
                        #     continue
                        # else:
                        xx = [x_spline_u1[i], x_spline_u2[i]]
                        yy = [y_spline_u1[i], y_spline_u2[i]]
                        ax1.plot(xx, yy, '--', color='gray', label='t_' + str(int(c_i[i])) + ' d_' + str(int(distance[i])))
                            # temp_x_val = max(x_spline_u1[i], x_spline_u2[i])

            # ___ SHOW RESULTS___ #
            ax1.legend(loc='best')
            plt.xlim([x_key, x_key + delta_s])
            plt.ylim([y_key, y_key + delta_s])
            plt.show()
            if output:
                break
        # break  # run only first tile

    print(output)
    print(index)
    df = pd.DataFrame(data=output, index=index, columns=columns)
    print(df.head())


def main():
    ds = 1000  # 100 200 500 1000 delta_space
    dt = 1200  # 300 500 600 1200 delta_time
    step = 60  # integration step size ( 1 MIN )
    max_tp = 1  # maximum throughput allowed by system

    # ___LOAD TILES____ #
    directory = "app/data/out/generated_grid_" + str(ds) + "_" + str(dt) + ".pkl"
    op_directory = "app/data/out/generated_grid_op_" + str(ds) + "_" + str(dt) + ".pkl"
    # new_directory = "app/data/out/generated_grid_new_" + str(ds) + "_" + str(dt) + ".csv"

    # ___ANALYZE EACH TILE INDIVIDUALLY____ #
    if os.path.isfile(directory):
        tiles = Pickle.reload_data(directory)
        # with open(op_directory, 'rb') as f:
        #     tiles = pickle.load(f)
        throughput_analysis(data, ds, dt, step, max_tp)
    else:
        print("missing tile dictionary")

    # graph_op = GraphContactPointsOp(tiles, weight='dist_weight').hottest_tile()


main()
