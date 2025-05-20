"""
Aquatic facility data loader for Calgary and surrounding area pools.
"""

import json
import os
from typing import List, Dict

class AquaticScraper:
    def __init__(self):
        self.cache_file = "data/aquatic_facilities.json"
        print(f"Debug: Current working directory: {os.getcwd()}")
        print(f"Debug: Looking for file at: {os.path.abspath(self.cache_file)}")
        print(f"Debug: Directory contents: {os.listdir('.')}")
        if os.path.exists('data'):
            print(f"Debug: Data directory contents: {os.listdir('data')}")

    def get_potential_sites(self) -> List[Dict]:
        """Hardcoded potential sites as fallback."""
        return [
            {
                "name": "Westbrook Station Site",
                "address": "17 Avenue & 33 Street SW, Calgary, AB",
                "type": "Potential",
                "features": [
                    "Potential aquatic facility site",
                    "Transit-oriented location",
                    "Existing infrastructure"
                ],
                "latitude": 51.0375,
                "longitude": -114.1339
            },
            {
                "name": "Viscount Bennett Centre Site",
                "address": "2501 Richmond Road SW, Calgary, AB",
                "type": "Potential",
                "features": [
                    "Potential aquatic facility site",
                    "Former educational facility",
                    "Existing infrastructure"
                ],
                "latitude": 51.0308,
                "longitude": -114.1226
            },
            {
                "name": "Former R.B. Bennett School Site",
                "address": "Bowness, Calgary, AB",
                "type": "Potential",
                "features": [
                    "Potential aquatic facility site",
                    "Former school location",
                    "Community accessible"
                ],
                "latitude": 51.0876,
                "longitude": -114.1891
            },
            {
                "name": "Kingsland Former School Site",
                "address": "7500 block of 5 Street SW, Calgary, AB",
                "type": "Potential",
                "features": [
                    "Potential aquatic facility site",
                    "Former school location",
                    "Central location"
                ],
                "latitude": 50.9868,
                "longitude": -114.0724
            },
            {
                "name": "Fairview Arena Site",
                "address": "8038 Fairmount Drive SE, Calgary, AB",
                "type": "Potential",
                "features": [
                    "Potential aquatic facility site",
                    "Former arena location",
                    "Existing recreational zoning"
                ],
                "latitude": 50.9783,
                "longitude": -114.0628
            },
            {
                "name": "Beltline Aquatic & Fitness Centre",
                "address": "221 12 Avenue SW, Calgary, AB",
                "type": "Potential",
                "features": [
                    "Potential aquatic facility site",
                    "Former aquatic facility",
                    "Central location"
                ],
                "latitude": 51.0421,
                "longitude": -114.0667
            }
        ]

    def load_cached_data(self) -> List[Dict]:
        """Load aquatic facility data from cache if it exists."""
        facilities = []
        if os.path.exists(self.cache_file):
            print("Loading aquatic facilities from cache...")
            print(f"Debug: Found cache file at {self.cache_file}")
            try:
                with open(self.cache_file, 'r') as f:
                    facilities = json.load(f)
                    print(f"Debug: Loaded {len(facilities)} facilities from cache")
            except Exception as e:
                print(f"Debug: Error loading cache file: {str(e)}")
                facilities = []
        else:
            print(f"Debug: Cache file not found at {self.cache_file}")
        
        # Add potential sites if they're not already in the data
        potential_sites = self.get_potential_sites()
        potential_names = set(site["name"] for site in potential_sites)
        existing_names = set(facility["name"] for facility in facilities)
        
        # Only add potential sites that aren't already in the data
        for site in potential_sites:
            if site["name"] not in existing_names:
                facilities.append(site)
                print(f"Debug: Added potential site {site['name']}")
        
        return facilities

    def scrape_facilities(self, force_refresh=False) -> List[Dict]:
        """
        Load aquatic facility data from JSON file.
        The force_refresh parameter is kept for API compatibility but ignored.
        """
        return self.load_cached_data()

def main():
    """Main function to demonstrate loader usage."""
    scraper = AquaticScraper()
    facilities = scraper.scrape_facilities()
    print(f"\nFound {len(facilities)} aquatic facilities")
    print("\nSample of facilities found:")
    for facility in facilities[:3]:
        print(f"- {facility['name']}")
        print(f"  Type: {facility['type']}")
        print(f"  Address: {facility['address']}")
        if 'latitude' in facility and 'longitude' in facility:
            print(f"  Coordinates: ({facility['latitude']}, {facility['longitude']})")
        print(f"  Features: {', '.join(facility['features'])}")
        print()

if __name__ == "__main__":
    main() 