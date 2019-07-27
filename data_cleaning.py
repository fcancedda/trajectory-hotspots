import os
from pandas import DataFrame
from app.lib.data_serializer import DataSerializer as DS


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
                    results.append(",".join(vals[0:2]) + "," + str(float(vals[4]) * 86400))
    # DS.save_data(DataFrame(results, columns=['user', 'lat', 'lng', 'time']), 'app/data/parsed/output_'+user+'.pkl')
    DS.save_data(results, 'app/data/parsed/output_' + user + '.txt')


def main():
    user_count = get_user_count()
    print('{} users in Data'.format(user_count))

    # MULTI THREADING DEMO
    from multiprocessing.dummy import Pool as ThreadPool

    # make the Pool of workers
    pool = ThreadPool(4)
    #
    pool.map(parse, generate_user_list(user_count))
    # close the pool and wait for the work to finish
    pool.close()
    # pool.join()


main()
