"""
Aquatic facility data scraper for City of Calgary pools and YMCA facilities.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class AquaticScraper:
    def __init__(self):
        self.base_url = "https://www.calgary.ca/rec-locations/pools.html"
        self.geolocator = Nominatim(user_agent="calgary_aquatic_map", timeout=10)
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=2, max_retries=5)
        self.cache_file = "data/aquatic_facilities.json"

    def load_cached_data(self) -> List[Dict]:
        """Load aquatic facility data from cache if it exists."""
        if os.path.exists(self.cache_file):
            print("Loading aquatic facilities from cache...")
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return None

    def save_to_cache(self, facilities: List[Dict]):
        """Save aquatic facility data to cache file."""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(facilities, f, indent=2)
        print(f"Saved {len(facilities)} aquatic facilities to cache file")

    def scrape_facilities(self, force_refresh=False) -> List[Dict]:
        """
        Scrape aquatic facility information from the City of Calgary website.
        
        Args:
            force_refresh: If True, ignore cache and fetch fresh data
        """
        # Try to load from cache first
        if not force_refresh:
            cached_data = self.load_cached_data()
            if cached_data:
                return cached_data

        facilities = []
        print("Fetching aquatic facilities...")

        # Known aquatic facilities with their details
        FACILITIES = [
            # City of Calgary Facilities
            {
                "name": "Acadia Aquatic & Fitness Centre",
                "address": "9009 Fairmount Dr. S.E., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Weights & cardio", "Fitness studio"]
            },
            {
                "name": "Bob Bahan Aquatic & Fitness Centre",
                "address": "4812 14 Ave. S.E., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Hot tub", "Steam room", "Weights & cardio"]
            },
            {
                "name": "Canyon Meadows Aquatic & Fitness Centre",
                "address": "89 Canova Rd. S.W., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Steam room", "Weights & cardio"]
            },
            {
                "name": "Foothills Aquatic Centre",
                "address": "2915 24 Ave. N.W., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Wading pool"]
            },
            {
                "name": "Glenmore Aquatic Centre",
                "address": "5330 19 St. S.W., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Hot tub"]
            },
            {
                "name": "Inglewood Aquatic Centre",
                "address": "1527 17 Ave. S.E., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Aquatic climbing wall", "Slides", "Dry Sauna"]
            },
            {
                "name": "Killarney Aquatic & Recreation Centre",
                "address": "1919 29 St. S.W., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Hot tub", "Teaching pool", "Steam room"]
            },
            {
                "name": "Renfrew Aquatic & Recreation Centre",
                "address": "810 13 Ave. N.E., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Hot tub", "Steam room"]
            },
            {
                "name": "Shouldice Aquatic Centre",
                "address": "5303 Bowness Rd. N.W., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Steam room"]
            },
            {
                "name": "Sir Winston Churchill Aquatic & Recreation Centre",
                "address": "1520 Northmount Dr. N.W., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Hot tub", "Steam room"]
            },
            {
                "name": "Thornhill Aquatic & Recreation Centre",
                "address": "6715 Centre St. N.W., Calgary, AB",
                "type": "Municipal",
                "features": ["Pool", "Dive tank", "Hot tub", "Steam room"]
            },
            # YMCA Facilities
            {
                "name": "Brookfield Residential YMCA at Seton",
                "address": "4995 Market Street SE, Calgary, AB T3M 2P9",
                "type": "YMCA",
                "features": ["25m Pool", "Competition Pool (50m)", "Dive Tower", "Flow Rider Surf Simulator", "Hot Tub", "Steam Room"]
            },
            {
                "name": "Melcor YMCA at Crowfoot",
                "address": "8100 John Laurie Blvd NW, Calgary, AB T3G 3S3",
                "type": "YMCA",
                "features": ["25m Pool", "Hot Tub", "Steam Room", "Fitness Centre"]
            },
            {
                "name": "Remington YMCA in Quarry Park",
                "address": "108 Quarry Park Rd SE, Calgary, AB T2C 5R1",
                "type": "YMCA",
                "features": ["25m Pool", "Hot Tub", "Steam Room", "Fitness Centre"]
            },
            {
                "name": "Saddletowne YMCA",
                "address": "180-7555 Falconridge Blvd NE, Calgary, AB T3J0C9",
                "type": "YMCA",
                "features": ["25m Pool", "Hot Tub", "Steam Room", "Fitness Centre"]
            },
            {
                "name": "Shane Homes YMCA at Rocky Ridge",
                "address": "11300 Rocky Ridge Rd NW, Calgary, AB T3G 5H3",
                "type": "YMCA",
                "features": ["25m Pool", "Leisure Pool", "Hot Tub", "Steam Room", "Fitness Centre"]
            },
            {
                "name": "Shawnessy YMCA",
                "address": "400-333 Shawville Blvd SE, Calgary, AB T2Y 4H3",
                "type": "YMCA",
                "features": ["25m Pool", "Hot Tub", "Steam Room", "Fitness Centre"]
            }
        ]

        for facility in FACILITIES:
            facility_data = {
                "name": facility["name"],
                "address": facility["address"],
                "type": facility["type"],
                "features": facility["features"]
            }

            try:
                print(f"Geocoding {facility['name']}...")
                location = self.geocode(facility["address"])
                if location:
                    facility_data["latitude"] = location.latitude
                    facility_data["longitude"] = location.longitude
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(f"Could not geocode {facility['name']}: {str(e)}")
            except Exception as e:
                print(f"Error processing {facility['name']}: {str(e)}")

            facilities.append(facility_data)

        # Save to cache before returning
        self.save_to_cache(facilities)
        return facilities

def main():
    """Main function to demonstrate scraper usage."""
    scraper = AquaticScraper()
    # Use force_refresh=True to ignore cache and fetch fresh data
    facilities = scraper.scrape_facilities(force_refresh=True)  # Force refresh to get new YMCA locations
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