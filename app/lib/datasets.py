import glob
import os
import re

import pandas as pd
from numpy import array as arr
from app.lib.pipeline_ops import PipelineOp


class GeolifeData(PipelineOp):
    def __init__(self):
        PipelineOp.__init__(self)
        self.__users = []
        self.__trajectories = {}

    def perform(self):
        self.__load_trajectories()
        return self._apply_output({'users': self.users(), 'trajectories': self.trajectories()})

    def users(self):
        self.__load_trajectories()
        return self.__users

    def trajectories(self, uid=None):
        self.__load_trajectories()
        if uid is None:
            return self.__trajectories
        else:
            return self.load_user_trajectory_points(uid)

    def __load_trajectories(self):
        trajectories = self.__trajectories
        if len(trajectories) <= 0:
            self.__users = arr([
                uid for uid in os.listdir('app/data/geolife/Data') if re.findall(r'\d{3}', uid)
            ])
            for uid in self.__users:
                trajectories[uid] = trajectories.get(uid, self.load_user_trajectory_points(uid))
            self.__trajectories = trajectories
        return trajectories

    def load_user_trajectory_points(self, uid):
        for trajectory_plt in self.load_user_trajectory_plts(uid):
            for point in self.load_trajectory_plt_points(trajectory_plt):
                yield (point)
                # yield (point, trajectory_plt)

    @staticmethod
    def load_user_trajectory_plts(uid):
        return glob.glob('app/data/geolife/Data/{}/Trajectory/*.plt'.format(uid))
        # return np.sort(glob.glob('app/data/geolife/Data/{}/Trajectory/*.plt'.format(uid)))

    @staticmethod
    def load_trajectory_plt_points(trajectory_plt):
        # return np.genfromtxt(trajectory_plt, delimiter=',', skip_header=6, usecols=range(0, 7))
        df = pd.read_csv(trajectory_plt, sep=",", header=6,
                         names=["lat", "lon", "constant0", "alt", "tot_time", "date", "time"])
        return df.drop(['constant0', 'alt', 'date', 'time'], axis=1)
