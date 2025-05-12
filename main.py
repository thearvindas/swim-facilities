"""
Calgary Schools and Aquatic Facilities Map Generator

This script creates an interactive map showing schools and aquatic facilities in Calgary.
It uses cached school data and sample aquatic facility data for development.
"""

import folium
import pandas as pd
from typing import List, Dict, Optional
from school_scraper import CBEScraper

# Sample aquatic facilities data
SAMPLE_AQUATIC = [
    {
        "name": "Repsol Sport Centre",
        "address": "2225 Macleod Trail SE, Calgary, AB",
        "type": "Municipal",
        "latitude": 51.0312,
        "longitude": -114.0577
    },
    {
        "name": "Killarney Aquatic Centre",
        "address": "1919 29 St SW, Calgary, AB",
        "type": "Municipal",
        "latitude": 51.0356,
        "longitude": -114.1298
    }
]

class MapGenerator:
    def __init__(self):
        """Initialize the map generator with Calgary's center coordinates."""
        self.CALGARY_CENTER = [51.0486, -114.0708]
        self.ZOOM_LEVEL = 11

    def create_base_map(self) -> folium.Map:
        """Create the base map centered on Calgary."""
        return folium.Map(
            location=self.CALGARY_CENTER,
            zoom_start=self.ZOOM_LEVEL,
            tiles="OpenStreetMap"
        )

    def add_school_markers(self, map_obj: folium.Map, schools: List[Dict]) -> folium.FeatureGroup:
        """Add school markers to the map."""
        school_layer = folium.FeatureGroup(name="K-12 Schools")
        
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
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign'),
            ).add_to(school_layer)
        
        school_layer.add_to(map_obj)
        return school_layer

    def add_aquatic_markers(self, map_obj: folium.Map, facilities: List[Dict]) -> folium.FeatureGroup:
        """Add aquatic facility markers to the map."""
        aquatic_layer = folium.FeatureGroup(name="Aquatic Facilities")
        
        for facility in facilities:
            popup_html = f"""
                <b>{facility['name']}</b><br>
                Type: {facility['type']}<br>
                Address: {facility['address']}
            """
            
            folium.Marker(
                location=[facility['latitude'], facility['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='green', icon='tint', prefix='fa'),
            ).add_to(aquatic_layer)
        
        aquatic_layer.add_to(map_obj)
        return aquatic_layer

    def generate_map(self, schools: List[Dict], aquatic_facilities: List[Dict]) -> folium.Map:
        """Generate the complete map with all markers and layers."""
        # Create base map
        map_obj = self.create_base_map()
        
        # Add markers
        self.add_school_markers(map_obj, schools)
        self.add_aquatic_markers(map_obj, aquatic_facilities)
        
        # Add layer control
        folium.LayerControl().add_to(map_obj)
        
        return map_obj

def main():
    """Main function to generate the map."""
    # Initialize map generator
    generator = MapGenerator()
    
    # Get school data from cache (or scrape if needed)
    print("Getting schools data...")
    scraper = CBEScraper()
    schools = scraper.scrape_schools(force_refresh=False)  # Use cache if available
    print(f"Found {len(schools)} schools")
    
    # Generate map using scraped schools and sample aquatic facilities
    map_obj = generator.generate_map(schools, SAMPLE_AQUATIC)
    
    # Save the map
    output_file = "calgary_schools_aquatic_map.html"
    map_obj.save(output_file)
    print(f"Map has been generated and saved to {output_file}")

if __name__ == "__main__":
    main() 