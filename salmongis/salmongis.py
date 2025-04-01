"""Main module."""

import ipyleaflet
import geopandas as gpd
from ipyleaflet import GeoJSON

class Map(ipyleaflet.Map):
    """A custom map class extending ipyleaflet.Map."""

    def __init__(self, center=[20, 0], zoom=2, height="600px", **kwargs):
        """
        Initializes the map with a given center, zoom level, and height.

        Args:
            center (list): The initial center of the map as [latitude, longitude].
            zoom (int): The initial zoom level of the map.
            height (str): The height of the map in pixels or percentage.
            **kwargs: Additional keyword arguments for ipyleaflet.Map.
        """
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.layout.height = height

    def add_basemap(self, basemap="OpenTopoMap"):
        """
        Adds a basemap layer to the map.

        Args:
            basemap (str): The name of the basemap to add. Must be a valid basemap
                available in ipyleaflet.basemaps.
        """
        url = eval(f"ipyleaflet.basemaps.{basemap}").build_url()
        layer = ipyleaflet.TileLayer(url=url, name=basemap)
        self.add_layer(layer)

    def add_layer_control(self):
        """
        Adds a layer control widget to the map.

        The layer control allows users to toggle visibility of layers on the map.
        """
        control = ipyleaflet.LayersControl(position="topright")
        self.add(control)

    def add_google_map(self, map_type="ROADMAP"):
        """
        Adds a Google Maps layer to the map.

        Args:
            map_type (str): The type of Google Map to add. Options are:
                "ROADMAP", "SATELLITE", "TERRAIN", "HYBRID".
        """
        map_types = {
            "ROADMAP": "m",
            "SATELLITE": "s",
            "TERRAIN": "p", 
            "HYBRID": "y",
        }

        map_type = map_types[map_type]

        url = f"https://mt1.google.com/vt/lyrs={map_type.lower()}&x={{x}}&y={{y}}&z={{z}}"
        layer = ipyleaflet.TileLayer(ur1=url, name="Google Map")
        self.add(layer)
    
    def add_vector(self, data, **kwargs):
        """
        Adds a vector layer to the map from a GeoJSON or file.

        Args:
            data (str): The path or URL to the vector data (e.g., GeoJSON file).
            **kwargs: Additional keyword arguments for ipyleaflet.GeoJSON.
        """
        import geopandas as gpd

        # Load the data into a GeoDataFrame
        gdf = gpd.read_file(data)

        # Reproject to EPSG:4326
        gdf = gdf.to_crs(epsg=4326)

        # Convert to GeoJSON
        geojson = gdf.__geo_interface__

        # Add the GeoJSON layer to the map
        self.add_layer(ipyleaflet.GeoJSON(data=geojson, **kwargs))