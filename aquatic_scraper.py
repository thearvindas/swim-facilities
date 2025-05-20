"""
Aquatic facility data loader for Calgary and surrounding area pools.
"""

import json
import os
from typing import List, Dict

class AquaticScraper:
    def __init__(self):
        self.cache_file = "data/aquatic_facilities.json"

    def load_cached_data(self) -> List[Dict]:
        """Load aquatic facility data from cache if it exists."""
        if os.path.exists(self.cache_file):
            print("Loading aquatic facilities from cache...")
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return []

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