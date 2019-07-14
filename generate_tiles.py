import math as m
import pickle
import datetime

# setting constants
datetimeFormat = '%Y-%m-%d %H:%M:%S'
p = {}


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
    for i in range(182):  # change to accomodate number of users
        user_str = '%03d' % i
        with open('processing/parsed_data/output_' + user_str + '.txt') as f:
            print(user_str)
            pid = 0
            for line in f:
                pid += 1
                lat, lng, date1, time1 = line.strip('\n').split(',')[0:5]
                p['latitude'] = float(lat)
                p['longitude'] = float(lng)
                pt_lat_conv, pt_lng_conv = get_xy_pos(relative_null_point, p)

                tile_lat_conv = int(pt_lat_conv / d_s) * d_s
                tile_lng_conv = int(pt_lng_conv / d_s) * d_s

                df1 = date1 + " " + time1
                t = datetime.datetime.strptime(df1, datetimeFormat)
                ttotal = t.timestamp()
                t = int(t.timestamp() / d_t) * d_t
                hash_str = str(str(tile_lat_conv)) + '_' + str(str(tile_lng_conv) + '_' + str(t))
                d[hash_str] = [(user_str, pt_lat_conv, pt_lng_conv, date1, time1, pid, ttotal, (lat, lng))]
    print("Tiles generated")
    print("No of tiles are: " + str(len(d.keys())) + str(d_s) + str(d_t))
    with open("app/data/out/generated_grid_" + str(d_s) + "_" + str(d_t) + ".csv", 'wb') as f:
        pickle.dump(d, f)


ds = 1000  # 100 500 1000
dt = 1200  # 300 600 1200
map_function(ds, dt)  # call based on ds and dt
