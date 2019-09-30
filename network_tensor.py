import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import torch
import scipy.io

import time
import sys

# set ds and dt fot creating fragments
ds = 200  # 100 500 1000
dt = 500  # 300 600 1200


def user_user_mat(filename, n):
    df = pd.read_csv(filename)
    df['date_from_key'] = df['Tile_key'].apply(
        lambda x: x.split('_')[2])  # please note Tile_key has a space at the end.

    df['date_from_key'] = pd.to_datetime(df['date_from_key'], unit='s').dt.date
    tensor = np.zeros((n, n, (df['date_from_key'].nunique())))

    df = df.groupby(['date_from_key'])
    day = 0
    for date, list_rows in df:
        for row in list_rows.values:
            tensor[row[0]][row[0]][day] = 1
            tensor[row[5]][row[5]][day] = 1
            if tensor[row[0], row[5], day] == 0 or tensor[row[0], row[5], day] > row[10]:
                tensor[row[0], row[5], day] = row[10]
                tensor[row[5], row[0], day] = row[10]
        day += 1
    return tensor


def location_count_mat(filename):
    df = pd.read_csv(filename)

    # granularity reduction
    df["Tile_x"] = (df["Tile_x"]/100).astype(int)  # M -> DM
    df["Tile_y"] = (df["Tile_y"]/100).astype(int)

    df['Tile_t'] = round(df['Tile_t'] * 0.000011574074074)  # seconds -> days

    # boolean filtering
    df = df[(df["Tile_x"] > 200) & (df["Tile_y"] > 100)]  # remove negatives
    # df = df[(df["Tile_x"] > 100) & (df["Tile_y"] > 0)]  # remove negatives
    df = df[(df["Tile_x"] < 300) & (df["Tile_y"] < 350)]  # focus on high density region
    # df = df[(df["Tile_x"] < 400) & (df["Tile_y"] < 400)]  # focus on high density region

    # new origin
    # first = df['Tile_x'].min()
    # df['Tile_x'] = df['Tile_x'] - first
    # first = df['Tile_y'].min()
    # df['Tile_y'] = df['Tile_y'] - first

    # plot 2D results
    df.plot(kind='scatter', x='Tile_x', y='Tile_y', color='red')
    plt.show()

    # plot 3D results
    # threedee = plt.figure().gca(projection='3d')
    # threedee.scatter(df["Tile_x"], df["Tile_y"], df['Tile_t'])
    # threedee.set_xlabel('X')
    # threedee.set_ylabel('Y')
    # threedee.set_zlabel('T')
    # plt.show()

    first = df['Tile_t'].min()
    df['Tile_t'] = df['Tile_t'] - first

    i = df['Tile_x'].max() + 1
    j = df['Tile_y'].max() + 1
    k = int(df['Tile_t'].max()) + 1

    tensor = np.zeros((i, j, k))

    df = df.groupby(['Tile_key'])

    for date, list_rows in df:
        tensor[list_rows['Tile_x'].iloc[0]][list_rows['Tile_y'].iloc[0]][int(list_rows['Tile_t'].iloc[0])] = len(list_rows)
    print(tensor)
    return tensor


def main():
    tensor = location_count_mat('network/rit/lab/dmmlab/cisco/trajectory-hotspots/app/data/fragments/fragments_ds' + str(ds) + '_dt' + str(dt) + '.csv')
    # tensor = user_user_mat('app/data/fragments/fragments_ds' + str(ds) + '_dt' + str(dt) + '.csv', 182)
    scipy.io.savemat('network/rit/lab/dmmlab/cisco/trajectory-hotspots/app/data/tensors/tensor' + str(ds) + '_dt' + str(dt) + '.mat', mdict={'tensor': tensor})


main()

# if i,j pair is false -> update to new distance value
# if mat[row[0]][row[5]] is 0 or mat[row[0]][row[5]] > row[10]:
#     mat[row[0]][row[5]] = row[10]
#     mat[row[5]][row[0]] = row[10]
# else:
#     if row[10] < mat[row[0]][row[5]]:
#         print("Updating distance between User " + str(row[0]) + " and User " + str(row[5]))
#         print("From distance " + str(mat[row[0]][row[5]]) + " to " + str(row[10]))
#         mat[row[0]][row[5]] = row[10]
#         mat[row[5]][row[0]] = row[10]

# for i in range(len(mat)):
#     mat[i][i] = 1
# if mat[i][i] is False:
# n = 3
# distance = [[[0 for k in xrange(n)] for j in xrange(n)] for i in xrange(n)]

# for i in range(len(mat)):
#     for j in range(len(mat[0])):
#         if mat[i][j] != mat[j][i]:
#             print("ERROR I and J values not same")
#             return {}

# d[str(date)] = mat
# print("Tensor created of length", len(d))
# return d

# def update_dist_from_date_user_id(T, key, UserA, UserB, dist_value):
#     target_mat = T.get(key)
#     try:
#         print("Updating")
#         target_mat[UserA][UserB] = dist_value
#         target_mat[UserB][UserA] = dist_value
#     except:
#         print("Can't update value. Check indices")
#
#     return target_mat[UserA][UserB] == target_mat[UserB][UserA]

# save and load pickle file
# def save_obj(obj, name):
#     with open('Tensor_file/' + name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.DEFAULT_PROTOCOL)
#
#
# def load_obj(name):
#     with open('Tensor_file/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)

# def validate(key, Tensor_file):
#     values = Tensor_file.get(key)  # dates within tensor
#     print(values)
#     print(values[0])
#     for i in range(len(values)):  # for each day
#         for j in range(len(values[0])):
#                     if values[i][j] is not 0:
#
#                         if i != j:
#                             print(i)
#                             print(j)
#                             print(values[i][j])
#                             with open("test_mat.txt",'a+') as f: #to validate write it to a file as 182 X 182 is 33124 cells and viewing it in console is not a good idea.
#                                 print("check for "+str(i)+"row"+str(j)+"column"+"\n")
#                                 f.write("check for "+str(i)+"row"+str(j)+"column"+"\n")
#                                 f.write(str(values[i])+"\n")# write the row to a file and check for the jth cell in this row to check if it is false or float value
# validate('2012-03-26')# pick a random key

# print(update_dist_from_date_user_id(Tensor_file, '2012-06-17', 153, 163, 10))
# 0.9638707755094332
# Tensor_file = load_obj('tensor_dict')
# for k in Tensor_file.keys():
#     validate(k, Tensor_file)
# for k, v in Tensor_dict.items():
#     print(k)
#     for i in v:
#         print(i)
#     break


# for x in Tensor_file:
#     print(x)
#     for y in Tensor_file[x]:
#         print(Tensor_file[x][y])
