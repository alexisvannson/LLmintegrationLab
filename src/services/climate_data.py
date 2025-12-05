"""
Real-time climate data extraction service
Fetches data from various public APIs
"""

import requests
from datetime import datetime
from typing import Dict, Optional
import json

class ClimateDataService:
    """
    Extracts real-time climate and environmental data
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ClimateFootprintApp/1.0'
        })

    def get_carbon_intensity(self, country_code: str = "GB") -> Optional[Dict]:
        """
        Get real-time grid carbon intensity from Carbon Intensity API (UK)
        Free API, no key required for UK data
        """
        try:
            url = "https://api.carbonintensity.org.uk/intensity"
            response = self.session.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if data.get('data') and len(data['data']) > 0:
                    intensity = data['data'][0]['intensity']
                    return {
                        'actual': intensity.get('actual'),
                        'forecast': intensity.get('forecast'),
                        'index': intensity.get('index'),
                        'timestamp': data['data'][0]['from'],
                        'source': 'carbonintensity.org.uk'
                    }
        except Exception as e:
            print(f"Error fetching carbon intensity: {e}")

        return None

    def get_atmospheric_co2(self) -> Optional[Dict]:
        """
        Get current atmospheric CO2 levels from CO2.earth
        Scrapes recent data
        """
        try:
            # Using NOAA's public data endpoint
            url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_weekly_mlo.txt"
            response = self.session.get(url, timeout=5)

            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                # Skip header lines (start with #)
                data_lines = [l for l in lines if not l.startswith('#') and l.strip()]

                if data_lines:
                    # Get the most recent measurement (last line)
                    recent = data_lines[-1].split()
                    if len(recent) >= 5:
                        return {
                            'ppm': float(recent[4]),
                            'year': int(recent[0]),
                            'month': int(recent[1]),
                            'day': int(recent[2]),
                            'source': 'NOAA Mauna Loa Observatory'
                        }
        except Exception as e:
            print(f"Error fetching CO2 data: {e}")

        # Fallback to approximate current value
        return {
            'ppm': 425.0,
            'source': 'Estimated (2025)',
            'note': 'Live data unavailable'
        }

    def get_climate_news_summary(self) -> str:
        """
        Get recent climate news headlines
        Using a simple RSS feed parser approach
        """
        try:
            # NASA Climate RSS feed
            url = "https://climate.nasa.gov/news/rss.xml"
            response = self.session.get(url, timeout=5)

            if response.status_code == 200:
                # Simple extraction of first headline
                import re
                titles = re.findall(r'<title>(.*?)</title>', response.text)
                if len(titles) > 2:  # First is usually the feed title
                    return f"Latest: {titles[1]}"
        except Exception as e:
            print(f"Error fetching climate news: {e}")

        return "Climate action remains critical for limiting global warming to 1.5°C"

    def get_electricity_carbon_intensity_estimate(self, region: str = "default") -> float:
        """
        Get electricity carbon intensity in kg CO2/kWh
        Tries real-time API first, falls back to regional estimates
        """
        # Try UK Carbon Intensity API
        if region.lower() in ["uk", "gb", "default"]:
            intensity_data = self.get_carbon_intensity()
            if intensity_data and intensity_data.get('actual'):
                # Convert from gCO2/kWh to kgCO2/kWh
                return intensity_data['actual'] / 1000.0

        # Fallback to regional estimates
        from src.data.emissions import GRID_INTENSITY
        return GRID_INTENSITY.get(region.lower(), GRID_INTENSITY['default'])

    def get_climate_context(self) -> Dict:
        """
        Get comprehensive climate context for the user
        """
        co2_data = self.get_atmospheric_co2()
        carbon_intensity = self.get_carbon_intensity()
        news = self.get_climate_news_summary()

        context = {
            'atmospheric_co2_ppm': co2_data.get('ppm') if co2_data else 425.0,
            'co2_source': co2_data.get('source', 'Estimated') if co2_data else 'Estimated',
            'grid_intensity': carbon_intensity,
            'climate_headline': news,
            'timestamp': datetime.now().isoformat(),
            'paris_agreement_target': 1.5,  # degrees C
            'daily_co2_budget_kg': 6.0  # kg CO2/day per person for 1.5°C target
        }

        return context


if __name__ == "__main__":
    # Test the service
    service = ClimateDataService()

    print("Testing Climate Data Service...")
    print("\n1. Atmospheric CO2:")
    co2 = service.get_atmospheric_co2()
    print(json.dumps(co2, indent=2))

    print("\n2. Carbon Intensity (UK Grid):")
    intensity = service.get_carbon_intensity()
    print(json.dumps(intensity, indent=2))

    print("\n3. Climate News:")
    print(service.get_climate_news_summary())

    print("\n4. Full Climate Context:")
    context = service.get_climate_context()
    print(json.dumps(context, indent=2, default=str))
