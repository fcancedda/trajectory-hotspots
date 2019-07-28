import os
from pandas import DataFrame
from app.lib.parsing_ops import DataSerializer as Pickle
from app.lib.parsing_ops import UserLister as Users


# def get_user_count():
#     files = 0
#     path = 'app/data/geolife/Data'
#     for _, dirnames, filenames in os.walk(path):
#         # ^ this idiom means "we won't be using this value"
#         files += len(dirnames)
#     return int(files / 2)
#
#
# def generate_user_list(n):
#     user_list = []
#     for i in range(n):
#         user_list.append('%03d' % i)
#     return user_list

def parse(user):
    print("------------USER----------" + user)
    user_raw_location = 'app/data/geolife/Data/' + user + '/Trajectory/'
    file_list = os.listdir(user_raw_location)  # TODO REMOVE SRTING
    results, index = [], []
    for f in file_list:
        with open(user_raw_location + f, 'r') as user_data:
            for n, line in enumerate(user_data):
                if n > 5:
                    vals = line.split(',')
                    # results.append((user, float(vals[0]), float(vals[1]), float(vals[4]) * 86400))  # lat, lng, time
                    results.append(",".join(vals[0:2]) + "," + str(int((float(vals[4]) - 39744) * 86400)))
    # DS.save_data(DataFrame(results, columns=['user', 'lat', 'lng', 'time']), 'app/data/parsed/output_'+user+'.pkl')
    Pickle.save_data(results, 'app/data/parsed/output_' + user + '.pkl')


def main():
    # MULTI THREADING DEMO
    from multiprocessing.dummy import Pool as ThreadPool

    # make the Pool of workers
    pool = ThreadPool(4)
    #
    pool.map(parse, Users.get_user_list())
    # close the pool and wait for the work to finish
    pool.close()
    # pool.join()


main()
