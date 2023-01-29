"""
Ethan L Simpson
29th January 2023
"""


import gpxpy
import pandas as pd
import folium
from geopy import distance
import matplotlib.pyplot as plt
import math
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np

horizontal_speed = lambda A,B : distance.distance(A,B).meters

def euclidean_speed(A,B):
    # Where A,B are 3-dimensional tuples
    return math.sqrt(horizontal_speed(A[:2],B[:2])**2 +(A[2]-B[2])**2)

def load_gpx(gpx_path):

    """
    Parses GPX file and converts into pandas dataframe, where the columns
    are time, and latitude, longitude and elevation data.
    """

    # Load gpx.
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)

    # Convert to a dataframe one point at a time.
    points = []
    for segment in gpx.tracks[0].segments:
        for p in segment.points:
            points.append({
                'time': p.time,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'elevation': p.elevation,
            })

    return pd.DataFrame.from_records(points)


def init_map(df):

    """
    Initialises a folium OpenStreetMap based on dataframe of positions
    """
    mymap = folium.Map( location=[ df.latitude.mean(), df.longitude.mean() ], zoom_start=11, tiles=None)
    folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(mymap)
    # folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}', attr="Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC", name="Nat Geo Map").add_to(mymap)
    # folium.TileLayer('http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg', attr="terrain-bcg", name="Terrain Map").add_to(mymap)
    return mymap


def plot_points(df,mymap):
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
        ).add_to(mymap)


def plot_route(df,name,mymap,colour="blue"):

    """
    Generates a route map from temporal-positional data in pandas DF.
    """
    fg = folium.FeatureGroup(name=name, show=True)
    mymap.add_child(fg)
    coordinates = [tuple(x) for x in df[['latitude', 'longitude']].to_numpy()]
    folium.PolyLine(coordinates, weight=6, color=colour).add_to(mymap).add_to(fg)


def plot_euclidean_velocity_route(df,mymap,delta_t=1):

    """
    Generate a velocity map based on temporal-positional data in pandas
    dataframe.
    The velocity is computed using latitude, longitude and elevation:
        a Euclidean approximation  of horizontal (lat,long) and change in elevation
    """

    coarse_df = df.iloc[::delta_t, :]
    arr = coarse_df[['latitude', 'longitude', 'elevation']].to_numpy()

    velocity_arr = []
    for i in range(len(arr)-1):
        velocity_arr.append(euclidean_speed(arr[i],arr[i+1]))

    velocity_arr = np.asarray(velocity_arr)
    
    norm = mpl.colors.Normalize(vmin=0, vmax=max(velocity_arr))
    cmap = mpl.cm.get_cmap('inferno')

    for i in range(len(arr)-1):
        points = (arr[i][:2],arr[i+1][:2])
        vel    = velocity_arr[i]
        folium.PolyLine(points, color=mpl.colors.to_hex(cmap(norm(vel))), weight=6, opacity=1).add_to(mymap)


def multi_route_map(dict_of_dataframes,savename):

    """
    Generate a series of routes, for different persons or different days.
    """

    # Make one big datafram
    full_dataframe = pd.concat(list(dict_of_dataframes.values()))
    # Initialise map
    mymap = init_map(full_dataframe)
    # Default matplotlib colours 
    def_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    # Plot routes
    for i,(name,df) in enumerate(full_dataframe.items()):
        plot_route(df,name=name,mymap=mymap,colour=def_colors[i])
    # Add multiple elements to map 
    folium.LayerControl().add_to(mymap)
    # Save map
    mymap.save(f"{savename}.html")

