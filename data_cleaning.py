import os


# def parse(n):
#     for i in range(n):
#         user = '%03d' % i
#         print("------------USER----------"+user)
#         user_data = 'data/' + user + '/Trajectory/'
#         file_list = os.listdir(user_data)
#         for f in file_list:
#             # fp = open('data/' + user + '/Trajectory/' + filelist[f])
#             with open('data/' + user + '/Trajectory/' + f, 'r') as file1,\
#                     open('processing/parsed_data/output_'+user+'.txt', 'a+') as file2:
#                 for n, line in enumerate(file1):
#                     if n > 5:
#                         file2.write(",".join(line.split(',')[0:2]) + "," + ",".join(line.split(',')[5:7]))
#
#
# parse(182)  # change for number of users

from multiprocessing.dummy import Pool as ThreadPool
import os


def get_user_count():
    files = 0
    path = 'data'
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
    print("------------USER----------"+user)
    user_data = 'app/data/geolife/Data/' + user + '/Trajectory/'
    file_list = os.listdir(user_data)
    for f in file_list:
        with open('app/data/geolife/Data/' + user + '/Trajectory/' + f, 'r') as file1,\
                open('app/data/parsed/output_' + user + '.txt', 'a+') as file2:
            for n, line in enumerate(file1):
                if n > 5:
                    file2.write(",".join(line.split(',')[0:2]) + "," + ",".join(line.split(',')[5:7]))


def main():
    print(get_user_count())
    # make the Pool of workers
    pool = ThreadPool(4)

    pool.map(parse, generate_user_list(get_user_count()))

    pool.close()


main()

# MULTI THREADING DEMO
# open the urls in their own threads
# and return the results
# results = pool.map(urllib2.urlopen, urls)

# close the pool and wait for the work to finish
# pool.close()
# pool.join()



