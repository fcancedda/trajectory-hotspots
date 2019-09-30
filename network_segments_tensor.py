import json
from math import sin, cos, pi, sqrt, atan2, radians
import itertools
from app.lib.data_serializer import DataSerializer as DS

EARTH_CIRCUMFERENCE_AT_EQUATOR_METERS = 40075160
EARTH_CIRCUMFERENCE_THROUGH_POLES_METERS = 40008000
relative_null_lat = 39.75872
relative_null_lon = 116.04142

# set ds and dt fot creating fragments
ds = 200  # 100 500 1000
dt = 500  # 300 600 1200


class DictList(dict):

    def __setitem__(self, key, value):
        try:
            # Assumes there is a list on the key
            self[key].extend(value)
        except KeyError:  # if fails because there is no key
            super(DictList, self).__setitem__(key, value)
        except AttributeError:  # if fails because it is not a list
            super(DictList, self).__setitem__(key, [self[key], value])


def get_lat_lng_from_meters(lat, lon):
    latitude_circumference = EARTH_CIRCUMFERENCE_AT_EQUATOR_METERS * cos(deg_to_rad(relative_null_lat))
    delta_latitude = lon * 360 / EARTH_CIRCUMFERENCE_THROUGH_POLES_METERS
    delta_longitude = lat * 360 / latitude_circumference

    result_lat = delta_latitude + relative_null_lat
    result_lng = delta_longitude + relative_null_lon

    return result_lat, result_lng


def deg_to_rad(degrees):
    return degrees * pi / 180


def check_for_outliers(key, p1, p2):
    r = 6373.0
    u1, x1, y1, t_min1, t_max1 = p1
    u2, x2, y2, t_min2, t_max2 = p2
    lat1 = radians(float(x1))
    lng1 = radians(float(y1))
    lat2 = radians(float(x2))
    lng2 = radians(float(y2))
    lng_d = lng2 - lng1
    lat_d = lat2 - lat1

    a = sin(lat_d / 2) ** 2 + cos(lat1) * cos(lat2) * sin(lng_d / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c * ds
    if u1 != u2:
        if distance <= ds:
            return distance
        else:
            with open("app/data/fragments/exclusions/out_of_threshold_" + str(ds) + "_" + str(dt) + ".txt", 'a+') as ob:
                ob.write(str((key, p1, p2, distance)) + "\n")
            # print("tiles out of bound")
            return -1


def create_fragments(load_dictionary, delta_s, delta_t):
    fragment_dict = DictList()
    print("Creating Fragments")
    for key, values in load_dictionary.items():
        frag_count = 1
        for pt_i in range(0, len(values) - 1):
            curr_usr = values[pt_i][0]
            # print(pt_i)
            # if current pid - next pid == next or previous point
            if abs(values[pt_i][3] - values[pt_i + 1][3]) == 1:
                # key is value at point
                fragment_dict[key + "&" + curr_usr + "&" + str(frag_count)] = [values[pt_i]]  # TODO move for efficiency
                # if penultimate point key is last value
                if pt_i == max(range(len(values) - 1)):
                    fragment_dict[key + "&" + curr_usr + "&" + str(frag_count)] = [values[pt_i + 1]]
            else:
                # key is value at point
                fragment_dict[key + "&" + curr_usr + "&" + str(frag_count)] = [values[pt_i]]
                # increment frag count
                frag_count = frag_count + 1
                continue
    fg = fragment_dict  # make a copy
    final_frag = DictList()
    for k1, v1 in fg.items():
        if len(v1) > 0:  # if fragment not empty
            avg_lat = sum([float(pair[1]) for pair in v1]) / len(v1)
            avg_lng = sum([float(pair[2]) for pair in v1]) / len(v1)
            max_time = max([float(pair[4]) for pair in v1])
            min_time = min([float(pair[4]) for pair in v1])

            avg_lat, avg_lng = get_lat_lng_from_meters(avg_lat, avg_lng)

            # print(lat_avg,lng_avg,max_time)
            final_frag[k1.split('&')[0]] = [(k1.split('&')[1], avg_lat, avg_lng, min_time, max_time)]
    # print(final_frag)
    print("Writing CSV")
    with open("app/data/fragments/fragments_ds" + str(delta_s) + "_dt" + str(delta_t) + ".csv", 'w') as wr:
        # creating column names for csv
        wr.write(
            "UserA,LatA,LngA,Min_time_UserA,Max_time_UserA,UserB,LatB,LngB,Min_time_UserB,Max_time_UserB,"
            "Distance_apart(m),Interaction_time(ms),Tile_x,Tile_y,Tile_t,Tile_key\n")
    interaction_time = 0
    # iterate over fragments
    for ft, vt in final_frag.items():
        if len(vt) > 1:  # if key has more than a single segment (fragment)
            for x, y in itertools.combinations(vt, 2):
                # extrapolate values for user pair x, y
                u1, la1, lo1, t1_min, t1_max = x
                u2, la2, lo2, t2_min, t2_max = y

                # if different UIDS -- Proceed
                if u1 != u2:
                    # if last_u1 after last_u2 *and first_u1 before first_u2
                    # *or*
                    # if last_u1 before last_u2 *and first_u1 after first_u2
                    # --> interaction time is min(last1,last2) - max(first1, first2)
                    if t1_max > t2_max and t1_min < t2_min:
                        interaction_time = min(t1_max, t2_max) - max(t1_min, t2_min)
                    elif t1_max < t2_max and t1_min > t2_min:
                        interaction_time = min(t1_max, t2_max) - max(t1_min, t2_min)
                    # if last_u1 after last_u2 and first_u1 after first_u2
                    # or
                    # if last_u1 before last_u2 and first_u1 before first_u2
                    # --> interaction time is min(last1,last2) - max(first1, first2)
                    elif t1_max > t2_max and t1_min > t2_min:
                        interaction_time = max(t1_max, t2_max) - min(t1_min, t2_min)
                    elif t1_max < t2_max and t1_min < t2_min:
                        interaction_time = max(t1_max, t2_max) - min(t1_min, t2_min)
                    # final check for threshold satisfaction
                    check = check_for_outliers(ft, x, y)

                    x_key, y_key, t_key = ft.split('_')

                    # x_new, y_new = get_lat_lng_from_meters(int(x_key), int(y_key))
                    # ft_new = "{}_{}_{}".format(x_new, y_new, t_key)

                    # if check is not -1:
                    with open("app/data/fragments/fragments_ds" + str(delta_s) + "_dt" + str(delta_t) + ".csv", 'a+') \
                            as fn:  # appending to csv
                        fn.write(u1 + "," + str(la1) + "," + str(lo1) + "," + str(t1_min) + "," +
                                 str(t1_max) + "," + u2 + "," + str(la2) + "," + str(lo2) + "," +
                                 str(t2_min) + "," + str(t2_max) + "," + str(check) + "," +
                                 str(interaction_time) + "," + x_key + "," + y_key + "," + t_key + "," + ft + "\n")


# with open("app/data/tiles/generated_grid_op_" + str(ds) + "_" + str(dt) + ".pkl") as f:
#     load_dict = pickle.load(f)
# load_dict = json.load(f)
load_dict = DS.reload_data("app/data/tiles/generated_grid_op_" + str(ds) + "_" + str(dt) + ".pkl")
create_fragments(load_dict, ds, dt)
