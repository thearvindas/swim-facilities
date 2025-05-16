"""
Population density data handler for Calgary and Edmonton.
Creates heatmap layers based on census data.
"""

import numpy as np
from typing import List, Tuple, Dict
import folium
from folium import plugins
import requests
import json
import pandas as pd

class PopulationDensityLayer:
    def __init__(self):
        """Initialize the population density layer handler."""
        self.calgary_data_url = "https://data.calgary.ca/resource/j9ps-fyst.json"
        self.edmonton_data_url = "https://data.edmonton.ca/resource/eg3i-f4bj.json"
        
    def _download_calgary_data(self) -> List[List[float]]:
        """Download and process Calgary census data."""
        response = requests.get(self.calgary_data_url)
        data = response.json()
        
        # Process data into [lat, lon, weight] format
        points = []
        for item in data:
            try:
                lat = float(item.get('latitude', 0))
                lon = float(item.get('longitude', 0))
                population = float(item.get('population', 0))
                
                if lat != 0 and lon != 0 and population > 0:
                    points.append([lat, lon, population])
            except (ValueError, TypeError):
                continue
                
        return points
        
    def _download_edmonton_data(self) -> List[List[float]]:
        """Download and process Edmonton census data."""
        response = requests.get(self.edmonton_data_url)
        data = response.json()
        
        # Process data into [lat, lon, weight] format
        points = []
        for item in data:
            try:
                lat = float(item.get('latitude', 0))
                lon = float(item.get('longitude', 0))
                population = float(item.get('population', 0))
                
                if lat != 0 and lon != 0 and population > 0:
                    points.append([lat, lon, population])
            except (ValueError, TypeError):
                continue
                
        return points

    def add_to_map(self, map_obj: folium.Map) -> None:
        """Add population density heatmap layers to the map."""
        # Add Calgary population density
        calgary_data = self._download_calgary_data()
        if calgary_data:
            calgary_layer = plugins.HeatMap(
                calgary_data,
                name='Calgary Population Density',
                show=False,
                min_opacity=0.4,
                max_zoom=18,
                radius=25,
                blur=15,
                gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'}
            )
            calgary_layer.add_to(map_obj)

        # Add Edmonton population density
        edmonton_data = self._download_edmonton_data()
        if edmonton_data:
            edmonton_layer = plugins.HeatMap(
                edmonton_data,
                name='Edmonton Population Density',
                show=False,
                min_opacity=0.4,
                max_zoom=18,
                radius=25,
                blur=15,
                gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'}
            )
            edmonton_layer.add_to(map_obj) 