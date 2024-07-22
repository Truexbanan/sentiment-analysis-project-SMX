from shapely.geometry import Point
from pyproj import Transformer
import matplotlib.pyplot as plt
import cartopy.crs as ccrs  # coordinate reference system
import cartopy.feature as cf
import logging
import warnings

# Suppress specific download warnings
warnings.filterwarnings("ignore", category=UserWarning, module="cartopy.io")

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def is_within_us(longitude, latitude):
    """
    Check if the given longitude and latitude fall within the approximate bounds of the US.

    @param longitude (float): The longitude of the point.
    @param latitude (float): The latitude of the point.
    @ret (bool): True if the point is within the US, otherwise False.
    """
    return (-125.0 <= longitude <= -66.93457) and (24.396308 <= latitude <= 49.384358)

def process_geospatial_data(geospatial_data, sentiment_results):
    """
    Process geospatial data, filtering out US locations and transforming coordinates.

    @param geospatial_data (list of list): A list of lists formatted as [[id, longitude, latitude, location], ...].
    @param sentiment_results (np.ndarray): A NumPy array with sentiment analysis results.
    @ret: Two lists of tuples - 
        - Transformed coordinates (list of tuple): Transformed coordinates excluding US locations.
        - Original coordinates and sentiments (list of tuple): Original coordinates and sentiments excluding US locations.
    """
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

    transformed_points = []
    original_points_and_sentiments = []

    for i, data in enumerate(geospatial_data):
        _, lon, lat, _ = data
        try:
            lon, lat = float(lon), float(lat)
            if not is_within_us(lon, lat):
                point = Point(lon, lat)
                x, y = transformer.transform(point.x, point.y)
                transformed_points.append((x, y))
                original_points_and_sentiments.append((lon, lat, sentiment_results[i][2]))  # Include sentiment label
        except ValueError as e:
            logging.error(f"Invalid data point {data}: {e}")
            continue

    return transformed_points, original_points_and_sentiments

def sentiment_to_color(sentiment):
    """
    Map sentiment labels to colors.

    @param sentiment (str): Sentiment label (negative, positive, neutral).
    @ret (str): Corresponding color for the sentiment.
    """
    if sentiment == 'Negative' or sentiment == 'Slightly Negative':
        return 'red'
    elif sentiment == 'Positive' or sentiment == 'Slightly Positive':
        return 'green'
    elif sentiment == 'Neutral':
        return 'blue'
    return 'black' # Default color

def plot_geospatial_data(original_points_and_sentiments, model_name):
    """
    Plot geospatial data on world and UK maps.

    @param original_points_and_sentiments (list of tuple): List of tuples containing original coordinates and sentiments.
    @param model_name (str): The name of the sentiment analysis model.
    @ret: None.
    """
    fig, ax = plt.subplots(1, 2, figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})

    # Define colors and labels for the legend
    if model_name.lower() == 'vader':
        legend_labels = {
            'Negative': 'red',
            'Neutral': 'blue',
            'Positive': 'green'
        }
    elif model_name.lower == 'roberta':
        legend_labels = {
            'Negative': 'red',
            'Neutral': 'blue',
            'Positive': 'green'
        }
    
    # World Map
    ax[0].set_title(f'World Map - Sentiment Analysis by {model_name}')
    ax[0].add_feature(cf.BORDERS, linestyle=':')
    ax[0].add_feature(cf.COASTLINE)
    ax[0].add_feature(cf.LAND, edgecolor='black')
    ax[0].add_feature(cf.OCEAN)
    ax[0].add_feature(cf.LAKES, edgecolor='black')
    ax[0].add_feature(cf.RIVERS)
    ax[0].gridlines(draw_labels=True)

    # Plot data points
    for lon, lat, sentiment in original_points_and_sentiments:
        color = sentiment_to_color(sentiment)
        ax[0].scatter(lon, lat, color=color, s=20)
    
    # Add legend to World Map
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in legend_labels.values()]
    labels = [label for label in legend_labels.keys()]
    ax[0].legend(handles, labels, title='Sentiment', loc='upper right')

    # UK Map
    ax[1].set_extent([-10, 3, 49, 61], ccrs.PlateCarree())  # UK extent
    ax[1].set_title(f'UK Map - Sentiment Analysis by {model_name}')
    ax[1].add_feature(cf.BORDERS, linestyle=':')
    ax[1].add_feature(cf.COASTLINE)
    ax[1].add_feature(cf.LAND, edgecolor='black')
    ax[1].add_feature(cf.OCEAN)
    ax[1].add_feature(cf.LAKES, edgecolor='black')
    ax[1].add_feature(cf.RIVERS)
    ax[1].gridlines(draw_labels=True)

    # Plot data points
    for lon, lat, sentiment in original_points_and_sentiments:
        color = sentiment_to_color(sentiment)
        ax[1].scatter(lon, lat, color=color, s=30)

    # Add legend to UK Map
    ax[1].legend(handles, labels, title='Sentiment', loc='upper right')

    plt.tight_layout()
    plt.show()

def analyze_geospatial(geospatial_data, sentiment_results, model_name):
    """
    Perform geospatial analysis on the sentiment results and plot the data.

    @param geospatial_data (list of list): The geospatial data.
    @param sentiment_results (np.ndarray): The sentiment analysis results.
    @param model_name (str): The name of the sentiment analysis model.
    @ret: None.
    """
    transformed_points, original_points_and_sentiments = process_geospatial_data(geospatial_data, sentiment_results)

    # Plot geospatial data
    plot_geospatial_data(original_points_and_sentiments, model_name)