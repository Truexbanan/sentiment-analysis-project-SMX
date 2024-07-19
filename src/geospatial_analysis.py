import fiona
from shapely.geometry import Point
from pyproj import Transformer
import matplotlib.pyplot as plt
import cartopy.crs as ccrs # coordinate reference system
import cartopy.feature as cf
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def is_within_us(longitude, latitude):
    """
    Check if the given longitude and latitude fall within the approximate bounds of the US.

    @param longitude: The longitude of the point.
    @param latitude: The latitude of the point.
    @return: True if the point is within the US, otherwise False.
    """
    return (-125.0 <= longitude <= -66.93457) and (24.396308 <= latitude <= 49.384358)

def process_geospatial_data(geospatial_data):
    """
    Process geospatial data, filtering out US locations and transforming coordinates.

    @param geospatial_data: A list of lists formatted as [[id, longitude, latitude, location], ...].
    @return: Two lists of tuples - one with transformed coordinates and one with original coordinates.
    """
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

    transformed_points = []
    original_points = []

    for data in geospatial_data:
        _, lon, lat, _ = data
        try:
            lon, lat = float(lon), float(lat)
            if not is_within_us(lon, lat):
                point = Point(lon, lat)
                x, y = transformer.transform(point.x, point.y)
                transformed_points.append((x, y))
                original_points.append((lon, lat))
        except ValueError as e:
            logging.error(f"Invalid data point {data}: {e}")
            continue

    return transformed_points, original_points

def plot_geospatial_data(original_points):
    """
    Plot geospatial data on world and UK maps.

    @param original_points: List of tuples containing original coordinates.
    @return: None.
    """
    # Color mapping based on sentiment
    color_map = {
        'negative': 'red',
        'positive': 'green',
        'neutral': 'yellow'
    }

    # Plot on world map
    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.add_feature(cf.COASTLINE)
    ax.set_title("World Map with Geospatial Data Points")
    for lon, lat in original_points:
        plt.plot(lon, lat, 'o', markersize=5, transform=ccrs.Geodetic())
    plt.show()
    logging.info("Plotted world map.")

    # Plot on UK map
    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([-10.5, 2.0, 49.5, 59.5], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='10m')
    ax.add_feature(cf.BORDERS)
    for lon, lat in original_points:
        plt.plot(lon, lat, 'o', markersize=5, transform=ccrs.Geodetic())
    ax.set_title('UK Map with Geospatial Data Points')
    plt.show()
    logging.info("Plotted UK map.")

def analyze_geospatial(geospatial_data):
    """
    Analyze geospatial data by processing and plotting it.

    @param geospatial_data: A list of lists formatted as [[id, longitude, latitude, location], ...].
    @return: None.
    """
    # Process the data
    transformed_points, original_points = process_geospatial_data(geospatial_data)

    # Plot the data
    plot_geospatial_data(original_points)