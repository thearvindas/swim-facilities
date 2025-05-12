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
            # Skip facilities without coordinates
            if 'latitude' not in facility or 'longitude' not in facility:
                continue
                
            popup_html = f"""
                <b>{facility['name']}</b><br>
                Type: {facility['type']}<br>
                Address: {facility['address']}<br>
                Features: {', '.join(facility['features'])}
            """
            
            # Color coding based on facility type
            if facility['type'] == 'Municipal':
                icon_color = 'green'
            elif facility['type'] == 'YMCA':
                icon_color = 'red'
            elif facility['type'] == 'University':
                icon_color = 'purple'
            else:  # Private facilities
                icon_color = 'orange'
                
            folium.Marker(
                location=[facility['latitude'], facility['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=icon_color, icon='info-sign'),
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
    
    # Get school data
    print("Getting schools data...")
    school_scraper = CBEScraper()
    schools = school_scraper.scrape_schools(force_refresh=False)
    print(f"Found {len(schools)} schools")
    
    # Get aquatic facility data
    print("\nGetting aquatic facilities data...")
    aquatic_scraper = AquaticScraper()
    facilities = aquatic_scraper.scrape_facilities(force_refresh=False)
    print(f"Found {len(facilities)} aquatic facilities")
    
    # Generate map
    map_obj = generator.generate_map(schools, facilities)
    
    # Save the map
    output_file = "index.html"
    map_obj.save(output_file)
    print(f"\nMap has been generated and saved to {output_file}")

if __name__ == "__main__":
    main() 