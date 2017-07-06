import pandas as pd
import numpy as np
from datetime import timedelta
from tools import sequence_to_interval, lazyprop
from interval import Interval
from constants import *


class Observation:
    def __init__(self, path, reactor_site, suffix_list, format="%Y-%m-%dT%H:%M:%S.000Z",
                 hours_backfill=1, verbose=0, ignore_keys=[], remove_on = [deb1[0]]):
        self.verboseprint = print if verbose else lambda *a, **k: None
        self.verboseprint("Loading in memory %i observations..." % (int(len(suffix_list)),))
        self.hours_backfill = hours_backfill
        files_name = [reactor_site + "-" + suffix + ".txt" for suffix in suffix_list]
        list_df = [pd.read_csv(path + file_name, sep=";") for file_name in files_name]
        self.ignore_keys = ignore_keys # TODO : remove deprecated
        self.remove_on = remove_on
        for df, tag in zip(list_df, suffix_list):
            df.columns = ["date", tag]
            df.drop_duplicates(subset="date", inplace=True)
            df['date'] = pd.to_datetime(df['date'], format=format)
            df.set_index('date', inplace=True)
        self.verboseprint("Concatenation...")
        self.df = pd.concat(list_df, axis=1)
        self.bad_labels_dict = {}
        self.change_isolated_wrong_values()
        self.verboseprint("Forward Filling...")
        self.df.fillna(method='ffill', inplace=True)
        self.verboseprint("Backward Filling...")
        self.df.fillna(method='bfill', inplace=True)

        self.compute_intervals_to_remove()
        self.compute_full_concatenated_df()
        self.compute_low_regime_intervals()

    def change_isolated_wrong_values(self):
        self.verboseprint("Changing isolated wrong values...")
        for column in self.df:
            bad_labels = self.df.index[((self.df[column] == MAX_VALUE) | (self.df[column] == 0))] ## >= THRESHOLD
            bad_labels = sequence_to_interval(bad_labels, timedelta(minutes=10))  # Stricly consecutive wrong values
            to_change_index = (bad_labels[:, 1] - bad_labels[:, 0]) <= timedelta(hours=self.hours_backfill)
            for begin, end in bad_labels[to_change_index]:
                self.df[column][begin:end] = np.nan
            if column in self.remove_on:
                self.bad_labels_dict[column] = bad_labels[~to_change_index]
            else:
                for begin, end in bad_labels[~to_change_index]:
                    self.df[column][begin:end] = np.nan

    def compute_intervals_to_remove(self):
        self.intervals_to_remove = Interval([])
        for key, intervals_bad_level in self.bad_labels_dict.items():
            if (key not in self.ignore_keys):
                self.intervals_to_remove.update(intervals_bad_level)

    def compute_low_regime_intervals(self):
        #time_precision = '10m'#'6H'
        low_regime_merge_time = timedelta(days=15)  # In days: The merging time for low regime
        margin_intervals_to_remove = timedelta(minutes=10)  # In days: Be careful, a high time_precision can make this wrong !
        filter_spike = timedelta(hours=1)  # In days: below that, the interval is considered as a spike !

        #subsample = self.full_concatenated_df[deb1[0]].resample(time_precision, label='right').min()
        subsample = self.full_concatenated_df[deb1[0]]
        self.low_regime_intervals = sequence_to_interval(subsample.index[(subsample < 200)],
                                                         low_regime_merge_time)
        self.low_regime_intervals = Interval(self.low_regime_intervals)
        self.low_regime_intervals.update_conditionally(
            self.intervals_to_remove.enlarge(margin_intervals_to_remove))
        self.low_regime_intervals.filter(filter_spike)

    def compute_full_concatenated_df(self):
        self.full_concatenated_df = pd.concat(self.intervals_to_remove.split_between(self.df),axis=0)
