import os
import math as m
from pandas import concat
from multiprocessing.dummy import Pool as ThreadPool

from app.lib.data_serializer import DataSerializer as DS

# setting constants
datetimeFormat = '%Y-%m-%d %H:%M:%S'
p = {}

d_s = 200  # 100 500 1000
d_t = 500  # 300 600 1200
origin = {'latitude': 39.75872, 'longitude': 116.04142}


def get_user_count(path):
    files = 0
    for _, dirnames, filenames in os.walk(path):
        # ^ this idiom means "we won't be using this value"
        files += len(filenames)
    return int(files)


def generate_user_list(n):
    user_list = []
    for i in range(n):
        user_list.append('%03d' % i)
    return user_list


def as_radians(degrees):
    return degrees * m.pi / 180


def get_xy_pos(lat, lng):
    """ Calculates X and Y distances in meters."""
    delta_latitude = lat - origin['latitude']
    delta_longitude = lng - origin['longitude']
    latitude_circumference = 40075160 * m.cos(as_radians(origin['latitude']))
    result_x = delta_longitude * latitude_circumference / 360
    result_y = delta_latitude * 40008000 / 360
    return result_x, result_y


def get_lat_lng(x, y):
    latitude_circumference = 40075160 * m.cos(as_radians(origin['latitude']))
    delta_latitude = y * 360 / 40008000
    delta_longitude = x * 360 / latitude_circumference

    result_lat = delta_latitude + origin['latitude']
    result_lng = delta_longitude + origin['longitude']
    return result_lat, result_lng


def map_function(user):
    print(user)
    user_df = DS.reload_data('app/data/parsed/output_' + user + '.pkl')
    converted_lat, converted_lng = get_xy_pos(user_df['lat'], user_df['lng'])

    tile_lat = (converted_lat / d_s).astype(int) * d_s
    tile_lng = (converted_lng / d_s).astype(int) * d_s
    tile_t = (user_df['time'] / d_t).astype(int) * d_t

    user_df['tile_key'] = tile_lat.astype(str) + '_' + tile_lng.astype(str) + '_' + tile_t.astype(str)
    return user_df


user_ids = generate_user_list(get_user_count('app/data/parsed'))  # change to accommodate number of users

# MULTI THREADING DEMO

# make the Pool of workers
pool = ThreadPool(4)

df = pool.map(map_function, user_ids)

# close the pool and wait for the work to finish
pool.close()

pool.join()

df = concat(df)


DS.save_data(df, "app/data/out/generated_grid_" + str(d_s) + "_" + str(d_t) + ".pkl")

# user_data = DS.reload_data('app/data/parsed/output_' + user_str + '.txt')
#     pid, time = 0, 0.0
#     for point in user_data:
#         pid += 1
#         lat, lng, t_days = point.split(',')
#
#         if float(t_days) > float(time):
#             time = t_days
#         else:
#             print('{} from {} is not sequential order'.format(time, point))
#             break
#
#         p['latitude'] = float(lat)
#         p['longitude'] = float(lng)
#         converted_lat, converted_lng = get_xy_pos(origin, p)
#
#         tile_lat = int(converted_lat / d_s) * d_s
#         tile_lng = int(converted_lng / d_s) * d_s
#
#         t_seconds = float(t_days) * 86400  # days to seconds
#         t = int(t_seconds / d_t) * d_t
#         hash_str = str(str(tile_lat)) + '_' + str(str(tile_lng) + '_' + str(t))
#         d[hash_str] = [(user_str, converted_lat, converted_lng, pid, t_seconds, (lat, lng), (d_s, d_t))]
# print("Tiles generated")
# print("No of tiles are: " + str(len(d.keys())) + str(d_s) + str(d_t))
# DS.save_data(d, "app/data/out/generated_grid_" + str(d_s) + "_" + str(d_t) + ".csv")
