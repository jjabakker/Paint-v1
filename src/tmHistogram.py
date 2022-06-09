
from tmUtility import ReadTracksData, ReadSpotsData, PlotTracks
from tmUtility import RestrictTracksLength, RestrictTracksTime
from tmUtility import CompileHistogram, PlotHistogram, CurveFitAndPlot



trackfilename = '/Users/hans/tracks.csv'
minimum_track_length: int = 7

maximum_nr_tracks = 50

tracks = ReadTracksData(trackfilename)

# The old code is what Kas had, the other is the simpler variant
old = False

if old:
    tracks = RestrictTracksLength(tracks, minimum_track_length=3)
    histdata = CompileHistogram(tracks)
    histdata = histdata.iloc[1:30, :]
else:
    tracks = RestrictTracksLength(tracks, minimum_track_length=minimum_track_length)
    histdata = CompileHistogram(tracks)
    histdata = histdata.iloc[0:maximum_nr_tracks-1, :]

PlotHistogram(histdata)
CurveFitAndPlot(histdata)

