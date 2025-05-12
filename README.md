# Calgary Schools and Aquatic Facilities Map

An interactive map visualization showing all K-12 schools and aquatic facilities in Calgary, Alberta. This tool helps identify potential build sites for new aquatic facilities by visualizing areas with high school density but few aquatic facilities.

## Features

- Displays all Calgary Board of Education (CBE) schools with detailed information
- Shows aquatic facilities (municipal pools, university pools, and community centers)
- Interactive layer controls to toggle visibility of schools and facilities
- Popup information for each location including name, type, and address
- Caches school data to improve performance
- Built with Python using Folium for map visualization

## Requirements

- Python 3.8+
- Required packages (install via `pip install -r requirements.txt`):
  - folium
  - pandas
  - geopy
  - beautifulsoup4
  - requests

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/thearvindas/swim-facilities.git
   cd swim-facilities
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```bash
python main.py
```

This will:
1. Load or scrape school data from the CBE website
2. Generate an interactive map (`calgary_schools_aquatic_map.html`)
3. Save the map in your current directory

## Data Sources

- School data is scraped from the [Calgary Board of Education website](https://cbe.ab.ca/)
- School locations are geocoded using OpenStreetMap's Nominatim service
- Aquatic facility data is currently using sample data (to be expanded)

## Project Structure

```
calgary_map_project/
├── main.py                # Main script to generate the map
├── school_scraper.py      # Module for scraping school data
├── requirements.txt       # Python dependencies
└── data/                  # Cached data directory
    └── cbe_schools.json   # Cached school data
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 