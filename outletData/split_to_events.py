import pandas as pd
import os
import shutil
import numpy as np
import scipy.integrate as integrate

names_of_outlets = ["kitchenBasin", "showerHead", "washingMachine", "washroomBasin"]

class event_splitter:
    
    outlet_name = None
    outlet_file_path = None
    event_dir = None
    
    def __init__(self, outlet_name):
        if os.path.isdir("eventData") == False:
            os.mkdir("eventData")
        self.outlet_name = outlet_name
        self.event_dir = "eventData"+'/'+outlet_name+"_events"
        self.outlet_file_path = "flowData"+'/'+outlet_name+".csv"
        if os.path.isdir(self.event_dir) == True:
            shutil.rmtree(self.event_dir)
        os.mkdir(self.event_dir)

    def split_into_events(self, sep=' ', header=None, flow_threshold=2, min_data_points=5, generateFeatures=False):

        df = pd.read_csv(self.outlet_file_path, sep=sep, header=header, names=['time', 'flow'])
        counter = 0
        startEvent = 0
        endEvent = 0
        outlet_ts = df.to_numpy()
        timegap = np.zeros([len(outlet_ts), 1])
        flow_val = outlet_ts[:,1]

        for index in range(0, len(outlet_ts) - 1):
            timegap[index + 1] = outlet_ts[index + 1, 0] - outlet_ts[index, 0]

        timeLimit = 5
        curr_event_index = []

        for index in range(2, len(outlet_ts) - 1):
            if timegap[index] <= timeLimit and flow_val[index] > flow_threshold:
                curr_event_index.append(index - 1)
            else:
                if len(curr_event_index) >= min_data_points:
                    startEvent = curr_event_index[0] if flow_val[curr_event_index[0]] > 0 else curr_event_index[1]
                    endEvent = curr_event_index[-1] + 2
                    counter+=1
                    np.savetxt(self.event_dir + '/' + str(counter) + '.csv', outlet_ts[startEvent:endEvent], delimiter=sep,fmt="%d")
                    # if(generateFeatures == True):
                    #     currFeature = np.array([(np.mean(flow_val[startEvent:endEvent]), np.sum(flow_val[startEvent:endEvent]), outlet_ts[endEvent,0] - outlet_ts[startEvent,0])])
                    #     if os.path.isdir("featureData") == False:
                    #         os.mkdir("featureData")
                    #     feature_Dir = "featureData"+'/'+self.outlet_name+"_events"
                    #     if os.path.isdir(feature_Dir) == False:
                    #         os.mkdir(feature_Dir)
                    #     np.savetxt(feature_Dir + '/' + str(counter) + '.csv', currFeature, delimiter=sep,fmt="%d")    
                startEvent = 0
                endEvent = 0
                curr_event_index = []






class Splitter:

    ts = None
    out_data_dir = None

    def __init__(self, time_series, out_dir):
        """

        :param time_series: a csv files with two columns, epoch and water flow as float
        :param out_dir: a directory where the splitted files will be saved
        """
        self.ts = time_series
        self.out_data_dir = out_dir

    def split(self, sep=' ', head=None, threshold=0):
        """

        :param sep:
        :param head:
        :param threshold:
        :return:
        """
        df = pd.read_csv(self.ts, sep=sep, header=head, names=['time', 'flow'])
        cont = 0

        start_event = 0

        end_event = 0

        ts = df.to_numpy()

        timegap = np.zeros([len(ts), 1])

        Q = ts[:, 1]

        for k in range(0, len(ts) - 1):
            timegap[k + 1] = ts[k + 1, 0] - ts[k, 0]

        timelim = 4

        Qlim = 6

        idx = []

        vlim = 0.125  # volume in [l]

        for i in range(2, len(ts) - 1):

            ratioq = (np.mean(Q[i - 2:i + 3]) / Q[i])

            if timegap[i] <= timelim and Q[i] > Qlim:

                idx.append(i - 1)

            elif timegap[i] > timelim and timegap[i] < 90 and Q[i] > Qlim and ratioq > 0.9 and ratioq < 1.1:

                idx.append(i - 1)
            #per ogni time series e' richiesto un numero di elementi maggiore di 3
            elif timegap[i] > timelim and len(idx) > 3:

                if Q[idx[0]] > 0:
                    start_event = idx[0]

                elif Q[idx[0]] == 0:

                    start_event = idx[1]

                end_event = idx[len(idx) - 1] + 2

                y = ts[start_event:end_event, 1] / 1000

                x = ts[start_event:end_event, 0]

                volume = integrate.trapz(y, x)  # volume [l]

                if volume > vlim:
                    cont += 1

                    np.savetxt(self.out_data_dir + '/' + str(cont) + '.csv', ts[start_event:end_event],
                               delimiter=sep, fmt="%d")

                end_event = 0

                start_event = 0

                idx = []

            elif timegap[i] <= timelim and Q[i] <= Qlim and len(
                    idx) > 3:  # per ogni time series e' richiesto un numero di elementi maggiore di 3

                if Q[idx[0]] > 0:

                    start_event = idx[0]

                elif Q[idx[0]] == 0:

                    start_event = idx[1]

                end_event = idx[len(idx) - 1] + 2

                y = ts[start_event:end_event, 1] / 1000

                x = ts[start_event:end_event, 0]

                volume = integrate.trapz(y, x)

                if volume > vlim:
                    cont += 1

                    np.savetxt(self.out_data_dir + '/' + str(cont) + '.csv', ts[start_event:end_event], delimiter=sep,
                               fmt="%d")

                end_event = 0

                start_event = 0

                idx = []

            elif timegap[i] > timelim and len(idx) <= 3:

                end_event = 0

                start_event = 0

                idx = []

            elif timegap[i] <= timelim and Q[i] <= Qlim and len(idx) <= 3:

                end_event = 0

                start_event = 0

                idx = []

class SimpleSplitter:
    """
    SimpleSplitter class provides methods to split a time-series in multiple usages using threshold as unique criteria
    """
    ts = None
    out_data_dir = None

    def __init__(self, time_series, out_dir):
        """

        :param time_series: a csv files with two columns, epoch and water flow as float
        :param out_dir: a directory where the splitted files will be saved
        """
        self.ts = time_series
        self.out_data_dir = out_dir

    def split(self, sep=' ', head=None, threshold=0):
        """
        This method split a time-series using a threshold as only one criteria.
        Splitted timeseries must be at least five samples long.

        :param sep: the delimiter for the csv file, default is the space
        :param head: not None if the first line of the csv contains column titles
        :param threshold: a float value that is compared with the samples to identify
         first and last sample for splitting

        """
        df = pd.read_csv(self.ts, sep=sep, header=head,
                         names=['time', 'flow'])

        this_usage = []
        cont = 0

        for i in range(0, len(df)):
            elemento = df.iloc[i]
            if abs(elemento[1]) > abs(threshold):
                riga = [elemento[0], elemento[1]]
                this_usage.append(riga)
            elif abs(elemento[1]) <= abs(threshold) and len(this_usage) >= 5:
                cont += 1

                df2 = pd.DataFrame(this_usage)
                df2.to_csv(self.out_data_dir + '/' + str(cont) + '.csv', header=None, sep=sep, index=False,
                           date_format='%d %d %f %d %d %d')
                this_usage = []
            elif elemento[1] == 0 and len(this_usage) < 5:
                this_usage = []


for outlet in names_of_outlets:
    splitter = event_splitter(outlet)
    splitter.split_into_events(generateFeatures=True)

    

    # df_time_series = pd.read_csv(outlet+".csv", sep=' ', header=None, names=["time","flow"])
    # current_event = []
    # counter = 0 

    # for index in range(0,len(df_time_series)):
    #     row = df_time_series.iloc[index]


