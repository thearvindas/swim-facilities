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
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign'),
            ).add_to(school_layer)
        
        school_layer.add_to(map_obj)
        return school_layer

    def add_aquatic_markers(self, map_obj: folium.Map, facilities: List[Dict]) -> None:
        """Add aquatic facility markers to the map, separated by type."""
        # Create separate feature groups for each facility type and their radius circles
        municipal_layer = folium.FeatureGroup(name="Municipal Facilities (Green)")
        municipal_radius = folium.FeatureGroup(name="Municipal 5km Radius")
        ymca_layer = folium.FeatureGroup(name="YMCA Facilities (Red)")
        ymca_radius = folium.FeatureGroup(name="YMCA 5km Radius")
        university_layer = folium.FeatureGroup(name="University Facilities (Purple)")
        university_radius = folium.FeatureGroup(name="University 5km Radius")
        private_layer = folium.FeatureGroup(name="Private Facilities (Orange)")
        private_radius = folium.FeatureGroup(name="Private 5km Radius")
        regional_layer = folium.FeatureGroup(name="Regional Facilities (Yellow)")
        regional_radius = folium.FeatureGroup(name="Regional 5km Radius")
        potential_layer = folium.FeatureGroup(name="Potential Sites (Blue)")
        potential_radius = folium.FeatureGroup(name="Potential Sites 5km Radius")
        
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
            
            # Determine which layer to add the marker to
            if facility['type'] == 'Municipal':
                icon_color = 'green'
                target_layer = municipal_layer
                radius_layer = municipal_radius
            elif facility['type'] == 'YMCA':
                icon_color = 'red'
                target_layer = ymca_layer
                radius_layer = ymca_radius
            elif facility['type'] == 'University':
                icon_color = 'purple'
                target_layer = university_layer
                radius_layer = university_radius
            elif facility['type'] == 'Regional':
                icon_color = 'orange'  # Using orange for regional since folium doesn't have yellow
                target_layer = regional_layer
                radius_layer = regional_radius
            elif facility['type'] == 'Potential':
                icon_color = 'blue'
                target_layer = potential_layer
                radius_layer = potential_radius
            else:  # Private facilities
                icon_color = 'orange'
                target_layer = private_layer
                radius_layer = private_radius
                
            # Add marker
            folium.Marker(
                location=[facility['latitude'], facility['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=icon_color, icon='info-sign'),
            ).add_to(target_layer)
            
            # Add 5km radius circle
            folium.Circle(
                location=[facility['latitude'], facility['longitude']],
                radius=5000,  # 5km in meters
                color=icon_color,
                fill=False,
                weight=2,
                popup=f"5km radius around {facility['name']}"
            ).add_to(radius_layer)
        
        # Add all layers to the map
        municipal_layer.add_to(map_obj)
        municipal_radius.add_to(map_obj)
        ymca_layer.add_to(map_obj)
        ymca_radius.add_to(map_obj)
        university_layer.add_to(map_obj)
        university_radius.add_to(map_obj)
        private_layer.add_to(map_obj)
        private_radius.add_to(map_obj)
        regional_layer.add_to(map_obj)
        regional_radius.add_to(map_obj)
        potential_layer.add_to(map_obj)
        potential_radius.add_to(map_obj)

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