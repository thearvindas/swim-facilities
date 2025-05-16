"""
Population density data handler for Calgary and Edmonton.
Creates heatmap layers based on census data.
"""

import geopandas as gpd
import numpy as np
from typing import List, Tuple, Dict
import folium
from folium import plugins
import requests
import tempfile
import os
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
        
        points = []
        for area in data:
            try:
                # Extract coordinates
                latitude = float(area.get('latitude', 0))
                longitude = float(area.get('longitude', 0))
                
                if latitude != 0 and longitude != 0:
                    # For now, we'll use a weight of 1 for all points since we don't have population data
                    # This will still show the distribution of communities
                    points.append([latitude, longitude, 1])
                    
            except (KeyError, ValueError) as e:
                print(f"Error processing Calgary area: {e}")
                continue
                
        return points
        
    def _download_edmonton_data(self) -> List[List[float]]:
        """Download and process Edmonton census data."""
        response = requests.get(self.edmonton_data_url)
        data = response.json()
        
        # First, get the maximum population to normalize the weights
        max_population = 0
        for area in data:
            try:
                population = float(area.get('total_population', 0))
                max_population = max(max_population, population)
            except (ValueError, TypeError):
                continue
        
        points = []
        for area in data:
            try:
                # Get the population
                population = float(area.get('total_population', 0))
                
                # Get the neighborhood name to look up coordinates
                neighborhood = area.get('neighbourhood', '')
                
                # For Edmonton, we'll need to geocode the neighborhoods
                # For now, we'll use approximate coordinates based on the city center
                # TODO: Add proper geocoding for Edmonton neighborhoods
                latitude = 53.5461  # Edmonton center
                longitude = -113.4937
                
                # Normalize population as weight (0 to 1 scale)
                weight = population / max_population if max_population > 0 else 0
                
                points.append([latitude, longitude, weight])
                    
            except (KeyError, ValueError) as e:
                print(f"Error processing Edmonton area: {e}")
                continue
                
        return points
        
    def create_heatmap_layer(self, city: str) -> folium.plugins.HeatMap:
        """
        Create a heatmap layer for the specified city.
        
        Args:
            city: Either 'calgary' or 'edmonton'
            
        Returns:
            A folium heatmap layer
        """
        # Get density points based on city
        if city.lower() == 'calgary':
            density_points = self._download_calgary_data()
        else:
            density_points = self._download_edmonton_data()
        
        # Create the heatmap layer with adjusted parameters
        heatmap = plugins.HeatMap(
            density_points,
            name=f"{city.title()} Population Distribution",
            show=False,  # Hidden by default
            min_opacity=0.4,
            max_zoom=18,
            radius=35,  # Increased radius for better visibility
            blur=25,  # Increased blur for smoother appearance
            gradient={
                0.2: 'blue',
                0.4: 'cyan',
                0.6: 'lime',
                0.8: 'yellow',
                1.0: 'red'
            }
        )
        
        return heatmap 