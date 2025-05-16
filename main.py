"""
Calgary Schools and Aquatic Facilities Map Generator

This script creates an interactive map showing schools and aquatic facilities in Calgary.
It uses cached school data and real aquatic facility data from the City of Calgary.
"""

import folium
import pandas as pd
from typing import List, Dict, Optional
from school_scraper import CBEScraper
from aquatic_scraper import AquaticScraper
from population_density import PopulationDensityLayer

class MapGenerator:
    def __init__(self):
        """Initialize the map generator with Calgary's center coordinates."""
        self.CALGARY_CENTER = [51.0486, -114.0708]
        self.EDMONTON_CENTER = [53.5461, -113.4937]
        self.ZOOM_LEVEL = 11
        self.density_layer = PopulationDensityLayer()

    def create_base_map(self) -> folium.Map:
        """Create the base map centered on Calgary."""
        map_obj = folium.Map(
            location=self.CALGARY_CENTER,
            zoom_start=self.ZOOM_LEVEL,
            tiles='cartodbpositron'
        )
        
        # Add layer control
        folium.LayerControl().add_to(map_obj)
        return map_obj

    def add_school_markers(self, map_obj: folium.Map, schools: List[Dict]) -> folium.FeatureGroup:
        """Add school markers to the map."""
        school_layer = folium.FeatureGroup(name="K-12 Schools", show=False)
        
        for school in schools:
            # Skip schools without coordinates
            if 'latitude' not in school or 'longitude' not in school:
                continue
                
            popup_html = f"""
                <b>{school['name']}</b><br>
                Type: {school['type']}<br>
                Board: {school.get('board', 'Unknown')}<br>
                Area: {school.get('area', 'Unknown')}<br>
                Address: {school.get('address', 'Unknown')}
            """
            
            folium.Marker(
                location=[school['latitude'], school['longitude']],
                popup=popup_html,
                icon=folium.Icon(color='gray', icon='info-sign')
            ).add_to(school_layer)
            
        school_layer.add_to(map_obj)
        return school_layer

    def add_facility_markers(self, map_obj: folium.Map, facilities: List[Dict]) -> None:
        """Add aquatic facility markers to the map with color-coded layers."""
        # Create feature groups for different facility types
        municipal_layer = folium.FeatureGroup(name="Municipal Facilities")
        ymca_layer = folium.FeatureGroup(name="YMCA Facilities")
        university_layer = folium.FeatureGroup(name="University Facilities")
        private_layer = folium.FeatureGroup(name="Private Facilities")
        
        for facility in facilities:
            # Skip facilities without coordinates
            if 'latitude' not in facility or 'longitude' not in facility:
                continue
                
            # Create popup content
            popup_html = f"""
                <b>{facility['name']}</b><br>
                Type: {facility['type']}<br>
                Address: {facility['address']}<br>
                Features: {', '.join(facility.get('features', []))}
            """
            
            # Determine facility type and color
            if 'YMCA' in facility['name'] or facility['type'] == 'YMCA':
                color = 'red'
                layer = ymca_layer
            elif facility['type'] == 'University':
                color = 'purple'
                layer = university_layer
            elif facility['type'] == 'Private':
                color = 'orange'
                layer = private_layer
            else:  # Municipal/Public
                color = 'green'
                layer = municipal_layer
            
            # Add marker
            folium.Marker(
                location=[facility['latitude'], facility['longitude']],
                popup=popup_html,
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(layer)
            
            # Add 5km radius circle
            folium.Circle(
                location=[facility['latitude'], facility['longitude']],
                radius=5000,  # 5km in meters
                color=color,
                fill=True,
                opacity=0.2
            ).add_to(layer)
        
        # Add all layers to map
        municipal_layer.add_to(map_obj)
        ymca_layer.add_to(map_obj)
        university_layer.add_to(map_obj)
        private_layer.add_to(map_obj)

    def generate_map(self, schools: List[Dict], facilities: List[Dict]) -> None:
        """Generate the map with all markers and save it."""
        # Create base map
        map_obj = self.create_base_map()
        
        # Add school markers
        self.add_school_markers(map_obj, schools)
        
        # Add facility markers
        self.add_facility_markers(map_obj, facilities)
        
        # Add population density layers
        self.density_layer.add_to_map(map_obj)
        
        # Save the map
        map_obj.save('index.html')

def main():
    """Main function to generate the map."""
    # Load school data from cache
    school_scraper = CBEScraper()
    schools = school_scraper.load_cached_data()
    print(f"Loaded {len(schools)} schools from cache")
    
    # Load aquatic facility data
    aquatic_scraper = AquaticScraper()
    facilities = aquatic_scraper.load_cached_data()
    print(f"Loaded {len(facilities)} aquatic facilities")
    
    # Generate map
    map_generator = MapGenerator()
    map_generator.generate_map(schools, facilities)
    print("Map generated successfully!")

if __name__ == "__main__":
    main() 