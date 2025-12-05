"""
Enhanced emissions data with regional factors and more detailed categories
"""

EMISSIONS = {
    "transport": {
        "car_petrol": 0.192,
        "car_diesel": 0.171,
        "car_hybrid": 0.109,
        "car_electric": 0.053,
        "bus": 0.105,
        "train": 0.041,
        "metro": 0.033,
        "bike": 0.0,
        "walk": 0.0,
        "motorcycle": 0.103,
        "scooter_electric": 0.025
    },
    "diet": {
        "vegan": 1.5,
        "vegetarian": 2.5,
        "pescatarian": 3.2,
        "omnivore_low_meat": 4.0,
        "omnivore": 5.0,
        "omnivore_high_meat": 6.5
    },
    "heating": {
        "natural_gas": 2.0,
        "oil": 2.5,
        "electric": 0.4,
        "heat_pump": 0.2,
        "solar": 0.0,
        "wood_pellets": 0.39
    },
    "electricity": {
        "kwh_default": 0.233  # EU average, will be replaced by real-time grid data
    },
    "consumption": {
        "new_clothes_monthly": 8.0,
        "secondhand_clothes": 0.5,
        "electronics_yearly": 2.0,
        "streaming_hours_daily": 0.055
    }
}

# Global CO2 targets and benchmarks
TARGETS = {
    "paris_agreement_daily": 6.0,  # kg CO2/day per person to limit warming to 1.5°C
    "world_average_daily": 12.0,
    "us_average_daily": 44.0,
    "eu_average_daily": 20.0,
    "developing_average_daily": 4.0
}

# Regional grid carbon intensity (kg CO2 per kWh) - fallback values
GRID_INTENSITY = {
    "default": 0.233,
    "france": 0.056,  # Nuclear-heavy
    "germany": 0.338,
    "uk": 0.233,
    "us": 0.417,
    "china": 0.555,
    "india": 0.708,
    "norway": 0.013,  # Hydro-heavy
    "poland": 0.766  # Coal-heavy
}
