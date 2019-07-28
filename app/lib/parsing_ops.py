import os
import pickle


class DataSerializer:
    # Save the data for easy access
    @staticmethod
    def save_data(
            data,
            pickle_file,
            overwrite=False
    ):
        os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
        if overwrite or not os.path.isfile(pickle_file):
            print('Saving data to pickle file...')
            try:
                with open(pickle_file, 'wb') as pfile:
                    pickle.dump(
                        data,
                        pfile, pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print('Unable to save data to', pickle_file, ':', e)
                raise
        else:
            print('WARNING: {} already exists.'.format(pickle_file))

        print('Data cached in pickle file.')

    @staticmethod
    def reload_data(pickle_file):
        pickle_data = None
        if os.path.isfile(pickle_file):
            with open(pickle_file, 'rb') as f:
                pickle_data = pickle.load(f)
            print('Data loaded from pickle file.')
        return pickle_data


class UserLister:
    @staticmethod
    def get_user_list():
        count = 0
        ls = ['app/data/parsed', 'app/data/out']
        if os.path.isdir(ls[0]):
            for _, dirnames, filenames in os.walk(ls[0]):
                count += len(filenames)
            if not count:
                print("Users not found please check directories")
        else:
            for directory in ls:
                if not os.path.exists(directory):
                    os.mkdir(directory)
            for _, dirnames, filenames in os.walk('app/data/geolife/Data'):
                count += len(dirnames)
            count = count / 2
        count = int(count)
        user_list = []
        for i in range(count):
            user_list.append('%03d' % i)
        print('users list {}'.format(user_list))
        return user_list

# from pandas import to_pickle, read_pickle, DataFrame
# class DataSerializer:
#     # Save the data for easy access
#     @staticmethod
#     def save_data(
#             dataframe,
#             pickle_file,
#             overwrite=False
#     ):
#         os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
#         if overwrite or not os.path.isfile(pickle_file):
#             print('Saving data to pickle file...')
#             try:
#                 dataframe.to_pickle(pickle_file)
#             except Exception as e:
#                 print('Unable to save data to', pickle_file, ':', e)
#                 raise
#         else:
#             print('WARNING: {} already exists.'.format(pickle_file))
#
#         print('Data cached in pickle file.')
#
#     @staticmethod
#     def reload_data(pickle_file):
#         pickle_data = None
#         if os.path.isfile(pickle_file):
#             pickle_data = read_pickle(pickle_file)
#             print('Data loaded from pickle file.')
#         return pickle_data
