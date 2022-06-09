
import tmUtility as tmu

from tmUtility import ReadTracksData, ReadSpotsData, PlotTracks
from tmUtility import RestrictTracksLength, RestrictTracksTime, RestrictTracksSquare
from tmUtility import CompileHistogram, PlotHistogram, CurveFitAndPlot

spotfilename = '/Users/hans/Downloads/spots.csv'

spots = ReadSpotsData(spotfilename)

mask = spots['TRACK_ID'] == 0
mask = mask + spots['TRACK_ID'] == 1
mask = mask + spots['TRACK_ID'] == 2

PlotTracks(spots)

spots1 = RestrictTracksSquare(spots, x_min=15, y_min=0, x_max=40, y_max=25)
tmu.PlotTracks(spots1, 0.1)

spots2 = RestrictTracksSquare(spots, x_min=20, y_min=7, x_max=25, y_max=12)
tmu.PlotTracks(spots2, 0.1)

spots3 = spots[mask]
tmu.PlotTracks(spots3, 0.1)


