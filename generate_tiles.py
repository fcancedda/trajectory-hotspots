import math as m

from app.lib.parsing_ops import DataSerializer as Pickle
from app.lib.parsing_ops import UserLister as Users

# setting constants
datetimeFormat = '%Y-%m-%d %H:%M:%S'
p = {}


ds = 1000  # 100 500 1000
dt = 1200  # 300 600 1200


def as_radians(degrees):
    return degrees * m.pi / 180


def get_xy_pos(relative_null_point, point):
    """ Calculates X and Y distances in meters."""
    delta_latitude = point['latitude'] - relative_null_point['latitude']
    delta_longitude = point['longitude'] - relative_null_point['longitude']
    latitude_circumference = 40075160 * m.cos(as_radians(relative_null_point['latitude']))
    result_x = delta_longitude * latitude_circumference / 360
    result_y = delta_latitude * 40008000 / 360
    return result_x, result_y


def get_lat_lng(relative_null_point, x, y):
    latitude_circumference = 40075160 * m.cos(as_radians(relative_null_point['latitude']))
    delta_latitude = y * 360 / 40008000
    delta_longitude = x * 360 / latitude_circumference

    result_lat = delta_latitude + relative_null_point['latitude']
    result_lng = delta_longitude + relative_null_point['longitude']
    return result_lat, result_lng


def map_function(d_s, d_t):
    d = {}
    # fragment_dict = DictList()
    relative_null_point = {'latitude': 39.75872, 'longitude': 116.04142}
    for uid in Users.get_user_list():  # change to accomodate number of users
        user_data = Pickle.reload_data('app/data/parsed/output_' + uid + '.pkl')
        # with open('app/data/parsed/output_' + user_str + '.pkl') as f:
        print(uid)
        pid = 0
        for point in user_data:
            pid += 1
            lat, lng, time = point.strip('\n').split(',')[0:4]
            p['latitude'] = float(lat)
            p['longitude'] = float(lng)
            converted_lat, converted_lng = get_xy_pos(relative_null_point, p)

            tile_lat = int(converted_lat / d_s) * d_s
            tile_lng = int(converted_lng / d_s) * d_s
            t = int(float(time) / d_t) * d_t
            hash_str = str(str(tile_lat)) + '_' + str(str(tile_lng) + '_' + str(t))
            if hash_str in d:
                d[hash_str].append((uid, converted_lat, converted_lng, pid, float(time), (lat, lng), (d_s, d_t)))
            else:
                d[hash_str] = [(uid, converted_lat, converted_lng, pid, float(time), (lat, lng), (d_s, d_t))]

    print("Number of tiles generated: " + str(len(d.keys())) + str(d_s) + str(d_t))
    Pickle.save_data(d, "app/data/out/generated_grid_" + str(d_s) + "_" + str(d_t) + ".pkl")


map_function(ds, dt)  # call based on ds and dt
