
from pytrackmate import trackmate_peak_import

fname = "/users/hans/downloads/FakeTracks.xml"
spots = trackmate_peak_import(fname)
spots.head()