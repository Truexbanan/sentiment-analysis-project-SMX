import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def geospatial_analyzer(data):
    df = pd.DataFrame(data, columns=['postid', 'longitude', 'latitude', 'location'])
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

    # Set the coordinate reference system (CRS)
    gdf.set_crs(epsg=4326, inplace=True)

    print(gdf)
    # Plotting the geospatial data (optional)
    gdf.plot()
    plt.show()