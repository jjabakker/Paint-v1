
import pandas as pd
from tmUtility import ReadTracksData, ReadSpotsData, PlotTracks, RestrictTracksLength

tracksfilename = '/Users/hans/tracks_1000x.csv'
spotsfilename = '/Users/hans/spots_1000x.csv'

#tracksfilename  = '/Users/hans/tracks.csv'
#spotsfilename = '/Users/hans/spots.csv'

min_length=10

# Read in the tracks and spots file
tracks = ReadTracksData(tracksfilename)
spots = ReadSpotsData(spotsfilename)

# Determine the maximum x and y values and plot the unprocessed spots
xmax = spots['POSITION_X'].max()
ymax = spots['POSITION_Y'].max()
PlotTracks(spots, line_width=0.5, xlim=xmax, ylim=ymax)

# Determine the track names of tracks longer than the minimum
tracks = RestrictTracksLength(tracks, minimum_track_length=min_length)
track_ids = tracks['TRACK_ID'].unique()
track_ids = pd.DataFrame(track_ids, columns=['TRACK_ID'])

# Select the spots of those tracks
reduced_spots = pd.merge(spots, track_ids, on='TRACK_ID')

# Plot the reduced spots with the earlier established xmax and ymax
PlotTracks(reduced_spots, line_width=0.5, xlim=xmax, ylim=ymax)