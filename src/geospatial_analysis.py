import fiona
from shapely.geometry import Point, shape
from pyproj import Transformer
import matplotlib.pyplot as plt

def analyze_geospatial(geospatial_data):
    # Convert to Shapely Points
    points = [Point(lon, lat) for _, lon, lat, _ in geospatial_data]

    # Plot the points
    plt.figure()
    for point in points:
        print(point)
        plt.plot(point.x, point.y, 'o')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Geospatial Data Points')
    plt.show()