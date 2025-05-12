"""
School data scraper for Calgary Board of Education schools.
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json
import os

class CBEScraper:
    def __init__(self):
        self.base_url = "https://cbe.ab.ca/about-us/leadership/Pages/schools-by-area.aspx"
        self.geolocator = Nominatim(user_agent="calgary_schools_map")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)
        self.cache_file = "data/cbe_schools.json"
        
    def load_cached_data(self) -> List[Dict]:
        """Load school data from cache if it exists."""
        if os.path.exists(self.cache_file):
            print("Loading schools from cache...")
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return None
        
    def save_to_cache(self, schools: List[Dict]):
        """Save school data to cache file."""
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        
        with open(self.cache_file, 'w') as f:
            json.dump(schools, f, indent=2)
        print(f"Saved {len(schools)} schools to cache file")
        
    def scrape_schools(self, force_refresh=False) -> List[Dict]:
        """
        Scrape school information from the CBE website.
        
        Args:
            force_refresh: If True, ignore cache and fetch fresh data
        """
        # Try to load from cache first
        if not force_refresh:
            cached_data = self.load_cached_data()
            if cached_data:
                return cached_data
        
        schools = []
        print("Fetching CBE website...")
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The schools are organized in sections by area
        areas = soup.find_all(['h2', 'h3'])
        
        current_area = None
        for element in areas:
            text = element.text.strip()
            
            # If it's an area header
            if element.name == 'h2' and ('Area' in text or 'Central' in text):
                current_area = text
                print(f"Processing {current_area}...")
                continue
            
            # If it's a school (h3) and we have a current area
            if element.name == 'h3' and current_area and not any(x in text for x in ['Contact Information', 'Education Director', 'Schools']):
                school_data = {
                    'name': text,
                    'area': current_area,
                    'type': 'Public',
                    'board': 'CBE'
                }
                
                # Try to find phone number which is usually right after the school name
                phone_div = element.find_next('div', string=lambda s: s and 'Phone' in s)
                if phone_div and phone_div.find_next('div'):
                    phone = phone_div.find_next('div').text.strip()
                    school_data['phone'] = phone
                
                # For now, we'll construct a basic address search string
                search_address = f"{school_data['name']}, Calgary, AB, Canada"
                try:
                    print(f"Geocoding {school_data['name']}...")
                    location = self.geocode(search_address)
                    if location:
                        school_data['latitude'] = location.latitude
                        school_data['longitude'] = location.longitude
                        school_data['address'] = location.address
                except (GeocoderTimedOut, GeocoderServiceError) as e:
                    print(f"Could not geocode {school_data['name']}: {str(e)}")
                except Exception as e:
                    print(f"Error processing {school_data['name']}: {str(e)}")
                
                schools.append(school_data)
                # Be nice to the geocoding service
                time.sleep(1)
        
        # Save to cache before returning
        self.save_to_cache(schools)
        return schools

def main():
    """Main function to demonstrate scraper usage."""
    scraper = CBEScraper()
    # Use force_refresh=True to ignore cache and fetch fresh data
    schools = scraper.scrape_schools(force_refresh=False)
    print(f"\nFound {len(schools)} schools")
    print("\nSample of schools found:")
    for school in schools[:5]:
        print(f"- {school['name']} ({school['area']})")
        if 'address' in school:
            print(f"  Address: {school['address']}")
        if 'latitude' in school and 'longitude' in school:
            print(f"  Coordinates: ({school['latitude']}, {school['longitude']})")
        print()

if __name__ == "__main__":
    main() 