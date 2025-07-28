import xarray as xr
import numpy as np
import pandas as pd
import os
import pycountry
import json

# --- Country Mapping Functions ---

def create_country_mapping(lat_coords, lon_coords, sample_rate=3):
    """
    Create a mapping of lat/lon coordinates to countries.
    Uses a simple land-based country boundaries approach.
    """
    print("🌍 Creating country mapping for grid points...")
    
    # Simple country boundaries (rough approximations)
    country_boundaries = {
        'USA': {'lat': (25, 49), 'lon': (-125, -66)},
        'CAN': {'lat': (42, 60), 'lon': (-141, -52)},  # Focus on southern Canada
        'MEX': {'lat': (14, 33), 'lon': (-118, -86)},
        'BRA': {'lat': (-34, 5), 'lon': (-74, -34)},
        'ARG': {'lat': (-55, -22), 'lon': (-73, -53)},
        'CHN': {'lat': (18, 54), 'lon': (73, 135)},
        'IND': {'lat': (6, 37), 'lon': (68, 97)},
        'RUS': {'lat': (41, 82), 'lon': (19, 169)},
        'AUS': {'lat': (-44, -10), 'lon': (113, 154)},
        'ZAF': {'lat': (-35, -22), 'lon': (16, 33)},
        'EGY': {'lat': (22, 32), 'lon': (25, 35)},
        'DEU': {'lat': (47, 55), 'lon': (5, 15)},
        'FRA': {'lat': (42, 51), 'lon': (-5, 8)},
        'GBR': {'lat': (50, 61), 'lon': (-8, 2)},
        'ESP': {'lat': (36, 44), 'lon': (-9, 3)},
        'ITA': {'lat': (36, 47), 'lon': (6, 19)},
        'JPN': {'lat': (24, 46), 'lon': (123, 146)},
        'IDN': {'lat': (-11, 6), 'lon': (95, 141)},
        'THA': {'lat': (5, 21), 'lon': (97, 106)},
        'VNM': {'lat': (8, 24), 'lon': (102, 110)},
        'TUR': {'lat': (36, 42), 'lon': (26, 45)},
        'IRN': {'lat': (25, 40), 'lon': (44, 63)},
        'SAU': {'lat': (16, 33), 'lon': (34, 56)},
        'NGA': {'lat': (4, 14), 'lon': (2, 15)},
        'KEN': {'lat': (-5, 5), 'lon': (34, 42)},
        'ETH': {'lat': (3, 15), 'lon': (33, 48)},
        'MAR': {'lat': (21, 36), 'lon': (-17, -1)},
        'DZA': {'lat': (19, 37), 'lon': (-9, 12)},
        'LBY': {'lat': (20, 33), 'lon': (9, 25)},
        'PER': {'lat': (-18, -0), 'lon': (-81, -68)},
        'COL': {'lat': (-4, 13), 'lon': (-79, -66)},
        'VEN': {'lat': (0, 13), 'lon': (-73, -59)},
        'CHL': {'lat': (-56, -17), 'lon': (-76, -66)},
        'NOR': {'lat': (58, 71), 'lon': (4, 31)},
        'SWE': {'lat': (55, 69), 'lon': (11, 24)},
        'FIN': {'lat': (60, 70), 'lon': (20, 32)},
        'POL': {'lat': (49, 55), 'lon': (14, 24)},
        'UKR': {'lat': (44, 53), 'lon': (22, 40)},
        'KAZ': {'lat': (40, 55), 'lon': (46, 87)},
        'MNG': {'lat': (41, 52), 'lon': (87, 120)},
        'AFG': {'lat': (29, 39), 'lon': (60, 75)},
        'PAK': {'lat': (24, 37), 'lon': (61, 77)},
        'BGD': {'lat': (20, 27), 'lon': (88, 93)},
        'MMR': {'lat': (9, 29), 'lon': (92, 102)},
        'KOR': {'lat': (33, 39), 'lon': (124, 132)},
        'PRK': {'lat': (37, 43), 'lon': (124, 131)},
        'MYS': {'lat': (0, 7), 'lon': (99, 119)},
        'PHL': {'lat': (4, 22), 'lon': (116, 127)},
        'SGP': {'lat': (1, 2), 'lon': (103, 104)},
        'NZL': {'lat': (-47, -34), 'lon': (166, 179)},
        'PNG': {'lat': (-11, -1), 'lon': (140, 156)},
        'FJI': {'lat': (-21, -12), 'lon': (177, 180)},
        'NCL': {'lat': (-23, -19), 'lon': (163, 168)},
        'MDG': {'lat': (-26, -11), 'lon': (43, 51)},
        'MWI': {'lat': (-17, -9), 'lon': (32, 36)},
        'ZMB': {'lat': (-18, -8), 'lon': (21, 34)},
        'ZWE': {'lat': (-23, -15), 'lon': (25, 33)},
        'BWA': {'lat': (-27, -17), 'lon': (20, 29)},
        'NAM': {'lat': (-29, -16), 'lon': (11, 25)},
        'AGO': {'lat': (-18, -4), 'lon': (11, 24)},
        'MOZ': {'lat': (-27, -10), 'lon': (30, 41)},
        'TZA': {'lat': (-12, -1), 'lon': (29, 41)},
        'UGA': {'lat': (-2, 4), 'lon': (29, 35)},
        'RWA': {'lat': (-3, -1), 'lon': (28, 31)},
        'BDI': {'lat': (-5, -2), 'lon': (28, 31)},
        'COD': {'lat': (-14, 6), 'lon': (12, 32)},
        'CAF': {'lat': (2, 11), 'lon': (14, 28)},
        'TCD': {'lat': (7, 23), 'lon': (13, 24)},
        'SDN': {'lat': (8, 22), 'lon': (21, 39)},
        'SSD': {'lat': (3, 13), 'lon': (24, 36)},
        'ERI': {'lat': (12, 18), 'lon': (36, 44)},
        'DJI': {'lat': (10, 13), 'lon': (41, 44)},
        'SOM': {'lat': (-2, 12), 'lon': (41, 52)},
        'GHA': {'lat': (4, 12), 'lon': (-4, 2)},
        'CIV': {'lat': (4, 11), 'lon': (-9, -2)},
        'BFA': {'lat': (9, 15), 'lon': (-6, 3)},
        'MLI': {'lat': (10, 25), 'lon': (-13, 5)},
        'NER': {'lat': (11, 24), 'lon': (-1, 16)},
        'TUN': {'lat': (30, 38), 'lon': (7, 12)},
        'LBN': {'lat': (33, 35), 'lon': (35, 37)},
        'SYR': {'lat': (32, 38), 'lon': (35, 43)},
        'JOR': {'lat': (29, 34), 'lon': (34, 40)},
        'ISR': {'lat': (29, 34), 'lon': (34, 36)},
        'PSE': {'lat': (31, 33), 'lon': (34, 36)},
        'IRQ': {'lat': (29, 38), 'lon': (38, 49)},
        'KWT': {'lat': (28, 31), 'lon': (46, 49)},
        'QAT': {'lat': (24, 27), 'lon': (50, 52)},
        'BHR': {'lat': (25, 27), 'lon': (50, 51)},
        'ARE': {'lat': (22, 27), 'lon': (51, 57)},
        'OMN': {'lat': (16, 27), 'lon': (51, 60)},
        'YEM': {'lat': (12, 19), 'lon': (42, 54)},
        'GEO': {'lat': (41, 44), 'lon': (39, 47)},
        'ARM': {'lat': (38, 42), 'lon': (43, 47)},
        'AZE': {'lat': (38, 42), 'lon': (44, 51)},
        'UZB': {'lat': (37, 46), 'lon': (55, 74)},
        'TKM': {'lat': (35, 43), 'lon': (52, 67)},
        'TJK': {'lat': (36, 41), 'lon': (67, 75)},
        'KGZ': {'lat': (39, 44), 'lon': (69, 81)},
        'NPL': {'lat': (26, 31), 'lon': (80, 89)},
        'BTN': {'lat': (26, 29), 'lon': (88, 93)},
        'LKA': {'lat': (5, 10), 'lon': (79, 82)},
        'MDV': {'lat': (-1, 8), 'lon': (72, 74)},
        # Additional European countries
        'GBR': {'lat': (50, 61), 'lon': (-8, 2)},
        'NLD': {'lat': (50, 54), 'lon': (3, 8)},
        'BEL': {'lat': (49, 52), 'lon': (2, 7)},
        'AUT': {'lat': (46, 49), 'lon': (9, 17)},
        'CHE': {'lat': (45, 48), 'lon': (5, 11)},
        'CZE': {'lat': (48, 51), 'lon': (12, 19)},
        'SVK': {'lat': (47, 50), 'lon': (16, 23)},
        'HUN': {'lat': (45, 49), 'lon': (16, 23)},
        'ROU': {'lat': (43, 49), 'lon': (20, 30)},
        'BGR': {'lat': (41, 44), 'lon': (22, 29)},
        'GRC': {'lat': (34, 42), 'lon': (19, 30)},
        'PRT': {'lat': (36, 43), 'lon': (-10, -6)},
        'IRL': {'lat': (51, 56), 'lon': (-11, -5)},
        'DNK': {'lat': (54, 58), 'lon': (8, 15)},
        'LTU': {'lat': (53, 57), 'lon': (20, 27)},
        'LVA': {'lat': (55, 58), 'lon': (20, 28)},
        'EST': {'lat': (57, 60), 'lon': (21, 29)},
        'SVN': {'lat': (45, 47), 'lon': (13, 17)},
        'HRV': {'lat': (42, 47), 'lon': (13, 20)},
        'BIH': {'lat': (42, 46), 'lon': (15, 20)},
        'SRB': {'lat': (42, 47), 'lon': (18, 23)},
        'MNE': {'lat': (41, 44), 'lon': (18, 21)},
        'MKD': {'lat': (40, 43), 'lon': (20, 23)},
        'ALB': {'lat': (39, 43), 'lon': (19, 22)},
        'LUX': {'lat': (49, 51), 'lon': (5, 7)},
        'MLT': {'lat': (35, 36), 'lon': (14, 15)},
        # Additional South American countries
        'ARG': {'lat': (-55, -21), 'lon': (-74, -53)},
        'PER': {'lat': (-18, 0), 'lon': (-82, -68)},
        'CHL': {'lat': (-56, -17), 'lon': (-76, -66)},
        'ECU': {'lat': (-5, 2), 'lon': (-81, -75)},
        'BOL': {'lat': (-23, -9), 'lon': (-70, -57)},
        'URY': {'lat': (-35, -30), 'lon': (-58, -53)},
        'GUY': {'lat': (1, 9), 'lon': (-61, -56)},
        'SUR': {'lat': (1, 6), 'lon': (-58, -53)},
        'GUF': {'lat': (2, 6), 'lon': (-55, -51)},  # French Guiana
        # Southeast Asian countries
        'KHM': {'lat': (10, 15), 'lon': (102, 108)},  # Cambodia
        'LAO': {'lat': (13, 23), 'lon': (100, 108)},  # Laos
        'BRN': {'lat': (4, 5), 'lon': (114, 115)},   # Brunei
    }
    
    # Create coordinate mapping
    country_map = {}
    for i, lat in enumerate(lat_coords[::sample_rate]):
        for j, lon in enumerate(lon_coords[::sample_rate]):
            country_code = 'OCEAN'  # Default for ocean/unknown
            
            # Convert longitude from 0-360 to -180-180 system for country matching
            lon_converted = lon if lon <= 180 else lon - 360
            
            # Check which country this coordinate falls in
            for country, bounds in country_boundaries.items():
                if (bounds['lat'][0] <= lat <= bounds['lat'][1] and 
                    bounds['lon'][0] <= lon_converted <= bounds['lon'][1]):
                    country_code = country
                    break
            
            country_map[(lat, lon)] = country_code
    
    print(f"✅ Created country mapping for {len(country_map):,} grid points")
    return country_map

def aggregate_by_country(data_array, country_map):
    """
    Aggregate gridded data by country using the country mapping.
    """
    print("🔄 Aggregating data by country...")
    
    country_data = {}
    lat_coords = data_array.latitude.values
    lon_coords = data_array.longitude.values
    
    # Use the same complete country boundaries as in create_country_mapping
    country_boundaries = {
        'USA': {'lat': (25, 49), 'lon': (-125, -66)},
        'CAN': {'lat': (42, 60), 'lon': (-141, -52)},  # Focus on southern Canada
        'MEX': {'lat': (14, 33), 'lon': (-118, -86)},
        'BRA': {'lat': (-34, 5), 'lon': (-74, -34)},
        'ARG': {'lat': (-55, -22), 'lon': (-73, -53)},
        'CHN': {'lat': (18, 54), 'lon': (73, 135)},
        'IND': {'lat': (6, 37), 'lon': (68, 97)},
        'RUS': {'lat': (41, 82), 'lon': (19, 169)},
        'AUS': {'lat': (-44, -10), 'lon': (113, 154)},
        'ZAF': {'lat': (-35, -22), 'lon': (16, 33)},
        'EGY': {'lat': (22, 32), 'lon': (25, 35)},
        'DEU': {'lat': (47, 55), 'lon': (5, 15)},
        'FRA': {'lat': (42, 51), 'lon': (-5, 8)},
        'GBR': {'lat': (50, 61), 'lon': (-8, 2)},
        'ESP': {'lat': (36, 44), 'lon': (-9, 3)},
        'ITA': {'lat': (36, 47), 'lon': (6, 19)},
        'JPN': {'lat': (24, 46), 'lon': (123, 146)},
        'IDN': {'lat': (-11, 6), 'lon': (95, 141)},
        'THA': {'lat': (5, 21), 'lon': (97, 106)},
        'VNM': {'lat': (8, 24), 'lon': (102, 110)},
        'TUR': {'lat': (36, 42), 'lon': (26, 45)},
        'IRN': {'lat': (25, 40), 'lon': (44, 63)},
        'SAU': {'lat': (16, 33), 'lon': (34, 56)},
        'NGA': {'lat': (4, 14), 'lon': (2, 15)},
        'KEN': {'lat': (-5, 5), 'lon': (34, 42)},
        'ETH': {'lat': (3, 15), 'lon': (33, 48)},
        'MAR': {'lat': (21, 36), 'lon': (-17, -1)},
        'DZA': {'lat': (19, 37), 'lon': (-9, 12)},
        'LBY': {'lat': (20, 33), 'lon': (9, 25)},
        'PER': {'lat': (-18, -0), 'lon': (-81, -68)},
        'COL': {'lat': (-4, 13), 'lon': (-79, -66)},
        'VEN': {'lat': (0, 13), 'lon': (-73, -59)},
        'CHL': {'lat': (-56, -17), 'lon': (-76, -66)},
        'NOR': {'lat': (58, 71), 'lon': (4, 31)},
        'SWE': {'lat': (55, 69), 'lon': (11, 24)},
        'FIN': {'lat': (60, 70), 'lon': (20, 32)},
        'POL': {'lat': (49, 55), 'lon': (14, 24)},
        'UKR': {'lat': (44, 53), 'lon': (22, 40)},
        'KAZ': {'lat': (40, 55), 'lon': (46, 87)},
        'MNG': {'lat': (41, 52), 'lon': (87, 120)},
        'AFG': {'lat': (29, 39), 'lon': (60, 75)},
        'PAK': {'lat': (24, 37), 'lon': (61, 77)},
        'BGD': {'lat': (20, 27), 'lon': (88, 93)},
        'MMR': {'lat': (9, 29), 'lon': (92, 102)},
        'KOR': {'lat': (33, 39), 'lon': (124, 132)},
        'PRK': {'lat': (37, 43), 'lon': (124, 131)},
        'MYS': {'lat': (0, 7), 'lon': (99, 119)},
        'PHL': {'lat': (4, 22), 'lon': (116, 127)},
        'SGP': {'lat': (1, 2), 'lon': (103, 104)},
        'NZL': {'lat': (-47, -34), 'lon': (166, 179)},
        'PNG': {'lat': (-11, -1), 'lon': (140, 156)},
        'FJI': {'lat': (-21, -12), 'lon': (177, 180)},
        'NCL': {'lat': (-23, -19), 'lon': (163, 168)},
        'MDG': {'lat': (-26, -11), 'lon': (43, 51)},
        'MWI': {'lat': (-17, -9), 'lon': (32, 36)},
        'ZMB': {'lat': (-18, -8), 'lon': (21, 34)},
        'ZWE': {'lat': (-23, -15), 'lon': (25, 33)},
        'BWA': {'lat': (-27, -17), 'lon': (20, 29)},
        'NAM': {'lat': (-29, -16), 'lon': (11, 25)},
        'AGO': {'lat': (-18, -4), 'lon': (11, 24)},
        'MOZ': {'lat': (-27, -10), 'lon': (30, 41)},
        'TZA': {'lat': (-12, -1), 'lon': (29, 41)},
        'UGA': {'lat': (-2, 4), 'lon': (29, 35)},
        'RWA': {'lat': (-3, -1), 'lon': (28, 31)},
        'BDI': {'lat': (-5, -2), 'lon': (28, 31)},
        'COD': {'lat': (-14, 6), 'lon': (12, 32)},
        'CAF': {'lat': (2, 11), 'lon': (14, 28)},
        'TCD': {'lat': (7, 23), 'lon': (13, 24)},
        'SDN': {'lat': (8, 22), 'lon': (21, 39)},
        'SSD': {'lat': (3, 13), 'lon': (24, 36)},
        'ERI': {'lat': (12, 18), 'lon': (36, 44)},
        'DJI': {'lat': (10, 13), 'lon': (41, 44)},
        'SOM': {'lat': (-2, 12), 'lon': (41, 52)},
        'GHA': {'lat': (4, 12), 'lon': (-4, 2)},
        'CIV': {'lat': (4, 11), 'lon': (-9, -2)},
        'BFA': {'lat': (9, 15), 'lon': (-6, 3)},
        'MLI': {'lat': (10, 25), 'lon': (-13, 5)},
        'NER': {'lat': (11, 24), 'lon': (-1, 16)},
        'TUN': {'lat': (30, 38), 'lon': (7, 12)},
        'LBN': {'lat': (33, 35), 'lon': (35, 37)},
        'SYR': {'lat': (32, 38), 'lon': (35, 43)},
        'JOR': {'lat': (29, 34), 'lon': (34, 40)},
        'ISR': {'lat': (29, 34), 'lon': (34, 36)},
        'PSE': {'lat': (31, 33), 'lon': (34, 36)},
        'IRQ': {'lat': (29, 38), 'lon': (38, 49)},
        'KWT': {'lat': (28, 31), 'lon': (46, 49)},
        'QAT': {'lat': (24, 27), 'lon': (50, 52)},
        'BHR': {'lat': (25, 27), 'lon': (50, 51)},
        'ARE': {'lat': (22, 27), 'lon': (51, 57)},
        'OMN': {'lat': (16, 27), 'lon': (51, 60)},
        'YEM': {'lat': (12, 19), 'lon': (42, 54)},
        'GEO': {'lat': (41, 44), 'lon': (39, 47)},
        'ARM': {'lat': (38, 42), 'lon': (43, 47)},
        'AZE': {'lat': (38, 42), 'lon': (44, 51)},
        'UZB': {'lat': (37, 46), 'lon': (55, 74)},
        'TKM': {'lat': (35, 43), 'lon': (52, 67)},
        'TJK': {'lat': (36, 41), 'lon': (67, 75)},
        'KGZ': {'lat': (39, 44), 'lon': (69, 81)},
        'NPL': {'lat': (26, 31), 'lon': (80, 89)},
        'BTN': {'lat': (26, 29), 'lon': (88, 93)},
        'LKA': {'lat': (5, 10), 'lon': (79, 82)},
        'MDV': {'lat': (-1, 8), 'lon': (72, 74)},
        # Additional European countries
        'GBR': {'lat': (50, 61), 'lon': (-8, 2)},
        'NLD': {'lat': (50, 54), 'lon': (3, 8)},
        'BEL': {'lat': (49, 52), 'lon': (2, 7)},
        'AUT': {'lat': (46, 49), 'lon': (9, 17)},
        'CHE': {'lat': (45, 48), 'lon': (5, 11)},
        'CZE': {'lat': (48, 51), 'lon': (12, 19)},
        'SVK': {'lat': (47, 50), 'lon': (16, 23)},
        'HUN': {'lat': (45, 49), 'lon': (16, 23)},
        'ROU': {'lat': (43, 49), 'lon': (20, 30)},
        'BGR': {'lat': (41, 44), 'lon': (22, 29)},
        'GRC': {'lat': (34, 42), 'lon': (19, 30)},
        'PRT': {'lat': (36, 43), 'lon': (-10, -6)},
        'IRL': {'lat': (51, 56), 'lon': (-11, -5)},
        'DNK': {'lat': (54, 58), 'lon': (8, 15)},
        'LTU': {'lat': (53, 57), 'lon': (20, 27)},
        'LVA': {'lat': (55, 58), 'lon': (20, 28)},
        'EST': {'lat': (57, 60), 'lon': (21, 29)},
        'SVN': {'lat': (45, 47), 'lon': (13, 17)},
        'HRV': {'lat': (42, 47), 'lon': (13, 20)},
        'BIH': {'lat': (42, 46), 'lon': (15, 20)},
        'SRB': {'lat': (42, 47), 'lon': (18, 23)},
        'MNE': {'lat': (41, 44), 'lon': (18, 21)},
        'MKD': {'lat': (40, 43), 'lon': (20, 23)},
        'ALB': {'lat': (39, 43), 'lon': (19, 22)},
        'LUX': {'lat': (49, 51), 'lon': (5, 7)},
        'MLT': {'lat': (35, 36), 'lon': (14, 15)},
        # Additional South American countries
        'ARG': {'lat': (-55, -21), 'lon': (-74, -53)},
        'PER': {'lat': (-18, 0), 'lon': (-82, -68)},
        'CHL': {'lat': (-56, -17), 'lon': (-76, -66)},
        'ECU': {'lat': (-5, 2), 'lon': (-81, -75)},
        'BOL': {'lat': (-23, -9), 'lon': (-70, -57)},
        'URY': {'lat': (-35, -30), 'lon': (-58, -53)},
        'GUY': {'lat': (1, 9), 'lon': (-61, -56)},
        'SUR': {'lat': (1, 6), 'lon': (-58, -53)},
        'GUF': {'lat': (2, 6), 'lon': (-55, -51)},  # French Guiana
        # Southeast Asian countries
        'KHM': {'lat': (10, 15), 'lon': (102, 108)},  # Cambodia
        'LAO': {'lat': (13, 23), 'lon': (100, 108)},  # Laos
        'BRN': {'lat': (4, 5), 'lon': (114, 115)},   # Brunei
    }
    
    # Check every grid point for each country (more thorough but slower)
    for country_code, bounds in country_boundaries.items():
        country_values = []
        
        for i, lat in enumerate(lat_coords):
            # Quick latitude filter
            if not (bounds['lat'][0] <= lat <= bounds['lat'][1]):
                continue
                
            for j, lon in enumerate(lon_coords):
                # Convert longitude from 0-360 to -180-180 system
                lon_converted = lon if lon <= 180 else lon - 360
                
                # Check if within country bounds
                if bounds['lon'][0] <= lon_converted <= bounds['lon'][1]:
                    value = data_array.isel(latitude=i, longitude=j).values
                    if not np.isnan(value):
                        country_values.append(value)
        
        if country_values:
            country_data[country_code] = country_values
    
    # Calculate country averages
    country_averages = {}
    for country, values in country_data.items():
        if values:  # Only if we have data
            country_averages[country] = {
                'mean': np.mean(values),
                'min': np.min(values),
                'max': np.max(values),
                'std': np.std(values),
                'count': len(values)
            }
    
    print(f"✅ Aggregated data for {len(country_averages)} countries")
    return country_averages

# --- Compare 2000 vs 2025 Heat Index Data ---

print("🔄 Creating comparison analysis between 2000 and 2025 heat index data...")

# Check if individual year files exist
files_2000 = ['heat_index_2000_avg.nc', 'heat_index_2000_full.nc']
files_2025 = ['heat_index_2025_avg.nc', 'heat_index_2025_full.nc']

missing_files = []
for f in files_2000 + files_2025:
    if not os.path.exists(f):
        missing_files.append(f)

if missing_files:
    print("❌ Missing required files:")
    for f in missing_files:
        print(f"  - {f}")
    print("\n💡 Please run process_2000_data.py and process_2025_data.py first")
    exit(1)

# Load the averaged data
print("Loading 2000 and 2025 averaged data...")
hi_2000_avg = xr.open_dataarray('heat_index_2000_avg.nc')
hi_2025_avg = xr.open_dataarray('heat_index_2025_avg.nc')

print("✅ Data loaded successfully")

# Calculate comparison metrics
print("\n📊 Calculating comparison statistics...")

# Calculate difference (2025 - 2000)
hi_difference = hi_2025_avg - hi_2000_avg
hi_difference.attrs = {
    'units': 'degrees_F', 
    'long_name': 'Heat Index Change (2025 - 2000)',
    'description': 'Positive values indicate warming, negative values indicate cooling'
}

# Calculate percentage change
hi_percent_change = ((hi_2025_avg - hi_2000_avg) / hi_2000_avg) * 100
hi_percent_change.attrs = {
    'units': 'percent', 
    'long_name': 'Heat Index Percent Change (2025 vs 2000)',
    'description': 'Percentage change in heat index from 2000 to 2025'
}

# Print statistics
print(f"\n📈 Global Comparison Statistics:")
print(f"2000 global average heat index: {hi_2000_avg.mean().values:.1f}°F")
print(f"2025 global average heat index: {hi_2025_avg.mean().values:.1f}°F")
print(f"Average change: {hi_difference.mean().values:.2f}°F")
print(f"Average percent change: {hi_percent_change.mean().values:.2f}%")

print(f"\n🌡️ Temperature Change Extremes:")
print(f"Maximum warming: {hi_difference.max().values:.1f}°F")
print(f"Maximum cooling: {hi_difference.min().values:.1f}°F")
print(f"Standard deviation: {hi_difference.std().values:.2f}°F")

# Create country mapping and aggregate data by country
print("\n🌍 Creating country-level analysis...")
country_map = create_country_mapping(hi_2000_avg.latitude.values, hi_2000_avg.longitude.values)

# Aggregate data by country
countries_2000 = aggregate_by_country(hi_2000_avg, country_map)
countries_2025 = aggregate_by_country(hi_2025_avg, country_map)
countries_diff = aggregate_by_country(hi_difference, country_map)

# Create country comparison dataset
country_comparison = {}
for country in countries_2000.keys():
    if country in countries_2025 and country in countries_diff:
        try:
            # Get country name
            country_obj = pycountry.countries.get(alpha_3=country)
            country_name = country_obj.name if country_obj else country
        except:
            country_name = country
        
        country_comparison[country] = {
            'country_code': country,
            'country_name': country_name,
            'heat_index_2000': countries_2000[country]['mean'],
            'heat_index_2025': countries_2025[country]['mean'],
            'difference': countries_2025[country]['mean'] - countries_2000[country]['mean'],  # Calculate directly
            'percent_change': ((countries_2025[country]['mean'] - countries_2000[country]['mean']) / countries_2000[country]['mean']) * 100,
            'data_points': countries_2000[country]['count']
        }

# Convert to DataFrame for easier analysis
country_df = pd.DataFrame.from_dict(country_comparison, orient='index')
country_df = country_df.sort_values('difference', ascending=False)

print(f"\n🏆 Top 10 Countries with Highest Warming:")
for i, (_, row) in enumerate(country_df.head(10).iterrows()):
    print(f"{i+1:2d}. {row['country_name']:<20} {row['difference']:+.1f}°F ({row['percent_change']:+.1f}%)")

print(f"\n❄️ Top 10 Countries with Highest Cooling:")
for i, (_, row) in enumerate(country_df.tail(10).iterrows()):
    print(f"{i+1:2d}. {row['country_name']:<20} {row['difference']:+.1f}°F ({row['percent_change']:+.1f}%)")

# Save country data
country_df.to_csv('heat_index_by_country.csv', index=False)
country_dict = country_df.to_dict('records')
with open('heat_index_by_country.json', 'w') as f:
    json.dump(country_dict, f, indent=2)

# Find regions with significant changes
warming_threshold = 2.0  # °F
cooling_threshold = -2.0  # °F

significant_warming = (hi_difference > warming_threshold).sum().values
significant_cooling = (hi_difference < cooling_threshold).sum().values
total_points = hi_difference.size

print(f"\n🗺️ Regional Analysis:")
print(f"Grid points with >2°F warming: {significant_warming:,} ({significant_warming/total_points*100:.1f}%)")
print(f"Grid points with >2°F cooling: {significant_cooling:,} ({significant_cooling/total_points*100:.1f}%)")
print(f"Total grid points analyzed: {total_points:,}")

# Create comparison dataset with all metrics
comparison_ds = xr.Dataset({
    'heat_index_2000': hi_2000_avg,
    'heat_index_2025': hi_2025_avg,
    'difference_2025_minus_2000': hi_difference,
    'percent_change': hi_percent_change
})

comparison_ds.attrs = {
    'title': 'Heat Index Comparison: 2000 vs 2025',
    'description': 'Comparison of heat index values between 2000 and 2025',
    'created_date': str(np.datetime64('now')),
    'warming_threshold_degF': warming_threshold,
    'cooling_threshold_degF': cooling_threshold
}

# Save comparison results
print("\n💾 Saving comparison datasets...")

# Individual files for specific visualizations
hi_difference.to_netcdf('heat_index_difference_2025_2000.nc')
hi_percent_change.to_netcdf('heat_index_percent_change_2025_2000.nc')

# Combined dataset for comprehensive analysis
comparison_ds.to_netcdf('heat_index_comparison_complete.nc')

print("✅ Difference data saved to 'heat_index_difference_2025_2000.nc'")
print("✅ Percent change data saved to 'heat_index_percent_change_2025_2000.nc'")
print("✅ Complete comparison saved to 'heat_index_comparison_complete.nc'")
print("✅ Country data saved to 'heat_index_by_country.csv'")
print("✅ Country data saved to 'heat_index_by_country.json'")

print("\n🎯 Files ready for visualization:")
print("  📊 For mapping temperature differences: heat_index_difference_2025_2000.nc")
print("  📈 For percentage change maps: heat_index_percent_change_2025_2000.nc")
print("  📋 For complete analysis: heat_index_comparison_complete.nc")
print("  🌍 For country-level analysis: heat_index_by_country.csv")
print("  🗂️ For web applications: heat_index_by_country.json")

print("\n✅ Comparison analysis complete!")
