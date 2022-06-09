import sys
import pandas as pd
import numpy as np

from tmUtility import ReadTracksData, ReadSpotsData, PlotTracks
from tmUtility import RestrictTracksLength, RestrictTracksTime

import tmUtility as tmu

def AnalyseTracks(tracks, spots, minimum_size):

    tracks = tracks.loc[tracks['NUMBER_SPOTS'] >= minimum_size]

    # Find the area of each track
    nr_tracks = tracks.shape[0]

    for i in range(0, nr_tracks):
        track = tracks.iloc[i]
        track_name = track['LABEL']
        track_index = track['TRACK_INDEX']
        nr_spots = track['NUMBER_SPOTS']

        # Select the spots

        spots_in_track = spots.loc[spots['TRACK_ID'] == track_index]
        max_values = spots_in_track.max()
        min_values = spots_in_track.min()

        min_x = min_values['POSITION_X']
        max_x = max_values['POSITION_X']
        min_y = min_values['POSITION_Y']
        max_y = max_values['POSITION_Y']

        print(f'Track {track_name:10s} with {nr_spots:5d} spots:   xmin = {min_x:5.2f}   xmax = {max_x:5.2f}   ymin = {min_y:5.2f}   xmax = {max_y:5.2f}')
        pass

trackfilename = '/Users/hans/Downloads/tracks.csv'
spotfilename = '/Users/hans/Downloads/spots.csv'

tracks = ReadTracksData(trackfilename)
spots = ReadSpotsData(spotfilename)

while True:
    number = input('Specify a value for the minimum string length: ')
    if number.isdecimal():
        print(f'Analysing for a track length of {int(number)} and larger\n\n')
        AnalyseTracks(tracks, spots, int(number))
        print('\n\n')
    else:
        break

tracks = RestrictTracksLength(tracks, 3)
tracks = RestrictTracksTime(tracks, 5, 8)
tracks = RestrictTracksTime(tracks, 6, 8)

i = 1
