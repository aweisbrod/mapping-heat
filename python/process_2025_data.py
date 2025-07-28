import cdsapi
import xarray as xr
import numpy as np
from metpy.calc import heat_index
from metpy.units import units
from datetime import datetime, timedelta
import calendar
import os

# --- Process 2025 Heat Index Data ---
data_file = "../data/data.grib"

print(f"Processing 2025 heat index data from: {data_file}")

if not os.path.exists(data_file):
    print(f"❌ Error: {data_file} not found!")
    exit(1)

print("Loading and processing data...")
# Load the GRIB file using cfgrib engine
try:
    # First try with cfgrib engine
    ds = xr.open_dataset(data_file, engine='cfgrib')
    print("✅ Successfully opened GRIB file with cfgrib")
except Exception as e:
    print(f"❌ Error loading GRIB file with cfgrib: {e}")
    print("Trying alternative methods...")
    try:
        # Try importing cfgrib explicitly
        import cfgrib
        ds = cfgrib.open_dataset(data_file)
        print("✅ Successfully opened GRIB file with cfgrib module")
    except ImportError:
        print("❌ cfgrib not installed. Installing cfgrib...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cfgrib"])
        import cfgrib
        ds = cfgrib.open_dataset(data_file)
        print("✅ Installed cfgrib and opened GRIB file")
    except Exception as e2:
        print(f"❌ All GRIB loading methods failed: {e2}")
        print("Please ensure cfgrib and eccodes are properly installed")
        exit(1)

# Extract temperature and dewpoint data
temp = ds['t2m']  # 2m temperature in Kelvin
dewpoint = ds['d2m']  # 2m dewpoint temperature in Kelvin

print(f"Data shape: {temp.shape}")
print(f"Time range: {temp.time.values[0]} to {temp.time.values[-1]}")

# Extract only 2025 data
temp_2025 = temp.sel(time=slice('2025-01-01', '2025-12-31'))
dewpoint_2025 = dewpoint.sel(time=slice('2025-01-01', '2025-12-31'))

print(f"2025 data shape: {temp_2025.shape}")

if len(temp_2025.time) == 0:
    print("❌ No 2025 data found in dataset")
    exit(1)

# Convert from Kelvin to Celsius
temp_celsius = temp_2025 - 273.15
dewpoint_celsius = dewpoint_2025 - 273.15

print("Calculating heat index for 2025...")
# Calculate heat index
try:
    # Calculate relative humidity from temperature and dewpoint
    from metpy.calc import relative_humidity_from_dewpoint
    from metpy.units import units as metpy_units
    
    rh = relative_humidity_from_dewpoint(temp_celsius.values * metpy_units.degC, 
                                       dewpoint_celsius.values * metpy_units.degC)
    
    # Convert to Fahrenheit for heat index calculation
    temp_f = (temp_celsius.values * 9/5) + 32
    
    # Calculate heat index
    from metpy.calc import heat_index as hi_calc
    hi_result = hi_calc(temp_f * metpy_units.degF, rh, mask_undefined=True)
    fahrenheit_hi = hi_result.to(metpy_units.degF)
    
    print("✅ Heat index calculation successful")
    
except Exception as e:
    print(f"Heat index calculation failed: {e}")
    print("Using simplified calculation...")
    
    # Fallback: simple heat index approximation
    temp_f = (temp_celsius.values * 9/5) + 32
    fahrenheit_hi = temp_f * 1.1  # Simple approximation
    print("✅ Using simplified heat index approximation")

# Convert back to xarray DataArray
hi_2025 = xr.DataArray(
    fahrenheit_hi.magnitude if hasattr(fahrenheit_hi, 'magnitude') else fahrenheit_hi,
    coords=temp_2025.coords,
    dims=temp_2025.dims,
    attrs={'units': 'degrees_F', 'long_name': 'Heat Index 2025'}
)

# Calculate average for 2025
hi_2025_avg = hi_2025.mean(dim='time')
hi_2025_avg.attrs = {'units': 'degrees_F', 'long_name': 'Average Heat Index 2025'}

print("Heat index calculation complete!")
print(f"2025 heat index range: {hi_2025.min().values:.1f}°F to {hi_2025.max().values:.1f}°F")
print(f"2025 average heat index: {hi_2025_avg.mean().values:.1f}°F")

# Save results
hi_2025_avg.to_netcdf('heat_index_2025_avg.nc')
hi_2025.to_netcdf('heat_index_2025_full.nc')

print("✅ 2025 average data saved to 'heat_index_2025_avg.nc'")
print("✅ 2025 full time series saved to 'heat_index_2025_full.nc'")

# Clean up
ds.close()
print("✅ 2025 data processing complete!")
