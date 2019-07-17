import math as m
import pickle
import os

# setting constants
datetimeFormat = '%Y-%m-%d %H:%M:%S'
p = {}


def as_radians(degrees):
    return degrees * m.pi / 180


def get_xy_pos(relative_null_point, lat, lng):
    """ Calculates X and Y distances in meters."""
    delta_latitude = float(lat) - relative_null_point[0]
    delta_longitude = float(lng) - relative_null_point[1]
    latitude_circumference = 40075160 * m.cos(as_radians(relative_null_point[0]))
    result_x = delta_longitude * latitude_circumference / 360
    result_y = delta_latitude * 40008000 / 360
    return result_x, result_y


# def get_lat_lng(relative_null_point, x, y):
#     latitude_circumference = 40075160 * m.cos(as_radians(relative_null_point['latitude']))
#     delta_latitude = y * 360 / 40008000
#     delta_longitude = x * 360 / latitude_circumference
#
#     result_lat = delta_latitude + relative_null_point['latitude']
#     result_lng = delta_longitude + relative_null_point['longitude']
#     return result_lat, result_lng


def get_user_count():
    files = 0
    path = 'app/data/geolife/Data'
    for _, dirnames, filenames in os.walk(path):
        # ^ this idiom means "we won't be using this value"
        files += len(dirnames)
    return int(files / 2)


def generate_user_list(n):
    user_list = []
    for i in range(n):
        user_list.append('%03d' % i)
    return user_list


def parse(users, d_s, d_t, relative_null_point):
    d = {}
    for user in users:
        pid = 0
        print("------------USER----------"+user)
        user_data = 'app/data/geolife/Data/' + user + '/Trajectory/'
        file_list = os.listdir(user_data)
        for f in file_list:
            with open('data/' + user + '/Trajectory/' + f, 'r') as file1:
                for n, line in enumerate(file1):
                    if n > 5:
                        pid += 1

                        row = (",".join(line.split(',')[0:2]) + "," + ",".join(line.split(',')[4]))
                        lat, lng, time = row.split(',')[0:3]

                        pt_lat_conv, pt_lng_conv = get_xy_pos(relative_null_point, lat, lng)
                        tile_lat_conv = int(pt_lat_conv / d_s) * d_s
                        tile_lng_conv = int(pt_lng_conv / d_s) * d_s

                        time = (time - 39421) * 24 * 60 * 60  # total time to seconds
                        # df1 = date + " " + time
                        # t = datetime.datetime.strptime(df1, datetimeFormat)
                        # ttotal = t.timestamp()
                        t = int(float(time) / d_t) * d_t

                        hash_str = str(str(tile_lat_conv)) + '_' + str(str(tile_lng_conv) + '_' + str(t))
                        # hash_str = str(str(hash_lat)) + '_' + str(str(hash_lng) + '_' + str(t))
                        d[hash_str] = [(user, pt_lat_conv, pt_lng_conv, pid, time, (lat, lng))]
    print("Tiles generated")
    print("No of tiles are: {} for ({}, {})".format(str(len(d.keys())), str(d_s), str(d_t)))
    with open("app/data/out/generated_grid_new_" + str(d_s) + "_" + str(d_t) + ".csv", 'wb') as f:
        pickle.dump(d, f)


global_origin = (39.75872, 116.04142)
ds = 200  # 100 500 1000
dt = 500  # 300 600 1200
# map_function(ds, dt)  # call based on ds and dt
parse(generate_user_list(get_user_count()), ds, dt, global_origin)
