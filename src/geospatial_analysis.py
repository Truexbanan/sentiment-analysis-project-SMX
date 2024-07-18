import fiona
from shapely.geometry import Point
from pyproj import Transformer
import matplotlib.pyplot as plt
import cartopy.crs as ccrs # coordinate reference system
import cartopy.feature as cf
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def analyze_geospatial(geospatial_data):
    """
    Implement geospatial analysis, plotting on a world map and UK map.

    @param geospatial_data: A list of lists formatted as [[id, longitude, latitude, location], ...].
    @ret: None.
    """
    # Set up a transformer for coordinate system conversion if needed
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

    # Convert to Shapely Points and apply coordinate transformation
    transformed_points = []
    original_points = []
    for data in geospatial_data:
        _, lon, lat, _ = data
        try:
            lon, lat = float(lon), float(lat)
            point = Point(lon, lat)
            # Transform coordinates if necessary
            x, y = transformer.transform(point.x, point.y)
            transformed_points.append((x, y))
            original_points.append((lon, lat))
        except ValueError as e:
            logging.error(f"Invalid data point {data}: {e}")
            continue

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