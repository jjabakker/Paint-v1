
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from scipy.optimize import OptimizeWarning


######################################################################################
# First a set of functions to manipulate tracks and spots data imported from Trackmate
######################################################################################


def ReadTrackMateData(csvfilename, istrack):

    """
    Function is not to be called externally, but by ReadTracksData or ReadSpotsData
    Read in the data file (it can be either 'tracks' or 'spots').
    Row 0 contains the header.
    Rows 1, 2 and 3 contain commentary, so skip those.
    :param csvfilename:
    :param istrack: A boolean value indicating whether it is tracks data (True) or spots data (False)
    :return: the dataframe with tracks
    """

    try:
        tmd = pd.read_csv(csvfilename, header=0, skiprows=[1, 2, 3])
    except FileNotFoundError:
        print(f'Could not open {csvfilename}')
        sys.exit()
    except:
        print(f'Problem parsing {csvfilename}')
        sys.exit()

    # Drop unused columns for 'tracks' data or 'plots' data
    try:
        if istrack:
            tmd.drop(['NUMBER_GAPS', 'NUMBER_SPLITS', 'NUMBER_MERGES', 'TRACK_Z_LOCATION',
                      'NUMBER_COMPLEX'], axis=1, inplace=True)
        else:
            tmd.drop(['POSITION_Z', 'MANUAL_SPOT_COLOR'], axis=1, inplace=True)
        return tmd
    except KeyError:
        print(f'Unexpected column names in {csvfilename}')
        sys.exit()

def ReadTracksData(csvfilename):
    return ReadTrackMateData(csvfilename, istrack=True)


def ReadSpotsData(csvfilename):
    return ReadTrackMateData(csvfilename, istrack=False)


def RestrictTracksLength(tracks, minimum_track_length=3, maximum_track_length=1000):
    """
    The function removes the tracks shorter  than minimum_track_length
    :param tracks: the datafrane containing tracks
    :param minimum_track_length:
    :param maximum_track_length:
    :return: the updates dataframe containing fewer tracks
    """

    old_tracks_count = tracks.shape[0]
    mask = (tracks['NUMBER_SPOTS'] >= minimum_track_length) & (tracks['NUMBER_SPOTS'] <= maximum_track_length)
    tracks = tracks.loc[tracks['NUMBER_SPOTS'] >= minimum_track_length]
    new_tracks_count = tracks.shape[0]

    print(f'Length restriction: selected/total tracks: {new_tracks_count}/{old_tracks_count}')

    return tracks


def RestrictTracksTime(tracks, begin_time=0, end_time=1000):
    """
    Only let tracks through that start later than begintime and end before endtime
    :param tracks:
    :param begin_time:
    :param end_time:
    :return: the updates dataframe containing fewer tracks
    """

    old_tracks_count = tracks.shape[0]
    mask = (tracks['TRACK_START'] >= begin_time) & (tracks['TRACK_STOP'] <= end_time)
    tracks = tracks.loc[mask]
    new_tracks_count = tracks.shape[0]

    print(f'Time restriction: selected/total tracks: {new_tracks_count}/{old_tracks_count}')

    return tracks


def RestrictTracksSquare(tracks, x_min, y_min, x_max, y_max):

    """
    Only let tracks through that start later than begintime and end before endtime
    :param tracks:
    :param x_min:
    :param y_min:
    :param x_max:
    :param y_max:
    :return: he updates dataframe containing fewer tracks
    """

    old_tracks_count = tracks.shape[0]
    mask = (tracks['POSITION_X'] >= x_min) & (tracks['POSITION_X'] <= x_max)
    mask = mask & (tracks['POSITION_Y'] >= y_min) & (tracks['POSITION_Y'] <= y_max)

    tracks = tracks.loc[mask]
    new_tracks_count = tracks.shape[0]

    print(f'Time restriction: selected/total tracks: {new_tracks_count}/{old_tracks_count}')

    return tracks


######################################################################################
# Then a set of functions to create histograms and curve fit
######################################################################################


def CompileHistogram(tracks):

    """
    The function produces a histogram
    :param tracks: a dataframe containing the histogram data
    :return: a dataframe containing the histogram
    """

    histdata = tracks.groupby('TRACK_DURATION')['TRACK_DURATION'].size()

    # histdata is returned as a Panda Series, make histdata into a dataframe
    # The index values are the duration and the first (and only) column is 'Frequency'
    histdata = pd.DataFrame(histdata)
    histdata.columns = ['Frequency']

    # print(f'long/total tracks: {long_tracks_count}/{total_tracks_count}')

    return histdata


def PlotHistogram(histodata):

    """
    The function simply plots a histogram
    :param histodata: the histogram data as a Pandas dataframe
    :return: nothing
    """

    # Extract the x and y data from the dataframe and convert them into Numpy arrays
    x = list(histodata.index)
    x = np.asarray(x)

    y = list(histodata["Frequency"])
    y = np.asarray(y)

    fig, ax = plt.subplots()

    ax.set_xlabel('Duration')  # Add an x-label to the axes.
    ax.set_ylabel('Number of tracks')  # Add a y-label to the axes.
    ax.set_title("Duration Histogram")  # Add a title to the axes.

    ax.plot(x, y, linewidth=1.0)
    plt.show()
    return()


def monoExp(x, m, t, b):
    # Define the exponential decay function that will be used for fitting
    return m * np.exp(-t * x) + b


def CurveFitAndPlot(histdata):

    """

    :param histdata: the histogram data as a Pandas dataframe
    :return: nothing
    """

    # Convert the pd dataframe to Numpy arrays fur further curve fitting

    x = list(histdata.index)
    x = np.asarray(x)

    y = list(histdata["Frequency"])
    y = np.asarray(y)

    # Perform the fit
    p0 = (200, .1, 50)  # start with values near those we expect
    try:
        params, cv = scipy.optimize.curve_fit(monoExp, x, y, p0)
        m, t, b = params
    except ValueError:
        print('CurveFitAndPlot: ydata or xdata contain NaNs, or incompatible options are used')
        return
    except RuntimeError:
        print('CurveFitAndPlot: The least-squares optimisation fails')
        return
    except OptimizeWarning:
        print('CurveFitAndPlot: Covariance of the parameters can not be estimated')
        return

    tauSec = (1 / t)

    # Determine quality of the fit
    squaredDiffs = np.square(y - monoExp(x, m, t, b))
    squaredDiffsFromMean = np.square(y - np.mean(y))
    rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
    print(f'R² = {rSquared}')

    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=1.0, label="Data")
    ax.plot(x, monoExp(x, m, t, b), linewidth=1.0, label="Fitted")
    ax.set_xlabel('Duration')
    ax.set_ylabel('Number of tracks')
    ax.set_title('Duration Histogram')
    ax.legend()
    plt.show()

    # Inspect the parameters
    print(f'Y = {m} * e^(-{t} * x) + {b}')
    print(f'Tau = {tauSec * 1e3} ms')

######################################################################################
# Then functions to plot tracks in a Fiji like manner
######################################################################################


def PlotTracks(spots, line_width=0.5, xlim=100, ylim=100):

    '''
    Plot the tracks in a rectangle
    :param spots:
    :param line_width:
    :param xlim:
    :param ylim:
    :return:
    '''

    track_names = list(spots["TRACK_ID"].unique())
    fig, ax = plt.subplots()
    for track_name in track_names:
        df = spots[spots['TRACK_ID'] == track_name]
        x = np.asarray(df['POSITION_X'])
        y = np.asarray(df['POSITION_Y'])
        ax.plot(x, y, linewidth=line_width)

    ax.set_xlabel('X [micrometer]')  # Add an x-label to the axes.
    ax.set_ylabel('Y [micrometer]')  # Add a y-label to the axes.
    ax.set_title("Position of tracks")  # Add a title to the axes.
    ax.set_xlim([0, xlim])
    ax.set_ylim([0, ylim])

    plt.show()
