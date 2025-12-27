#!/usr/bin/micropython

import struct, math, time

declination = []
equation_of_time = []

# Time conversions and formatting

def date_to_index(year, month, day, ref_year=2025, ref_month=12, ref_day=1):
    """Convert a date to table index (days since reference date)"""
    date_ts = time.mktime((year, month, day, 0, 0, 0, 0, 0))
    ref_ts = time.mktime((ref_year, ref_month, ref_day, 0, 0, 0, 0, 0))
    return (date_ts - ref_ts) // 86400

def index_to_date(index, ref_year=2025, ref_month=12, ref_day=1):
    """Convert table index to (year, month, day) tuple"""
    ref_ts = time.mktime((ref_year, ref_month, ref_day, 0, 0, 0, 0, 0, 0))
    target_ts = ref_ts + (index * 86400)
    date_tuple = time.localtime(target_ts)
    return (date_tuple[0], date_tuple[1], date_tuple[2])

def index_to_date_str(index, ref_year=2025, ref_month=12, ref_day=1):
    """Convert table index to date string YYYY-MM-DD"""
    year, month, day = index_to_date(index, ref_year, ref_month, ref_day)
    return f"{year}-{month:02d}-{day:02d}"

def fraction_to_time(fraction):
    hours   = int(fraction * 24)
    minutes = int((fraction * 24 - hours) * 60)
    seconds = int((fraction * 86400) % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# For sunrise, twilight, ...

def hour_angle_for_elevation(latitude, declination, elevation):
    lat_rad  = math.radians(latitude)
    dec_rad  = math.radians(declination)
    elev_rad = math.radians(elevation)
    
    # Spherical astronomy formula
    cos_h = (math.sin(elev_rad) - math.sin(lat_rad) * math.sin(dec_rad)) / (math.cos(lat_rad) * math.cos(dec_rad))
    
    # Check if sun reaches this elevation today
    if cos_h < -1.0:
        return None  # Sun always above this elevation (polar summer)
    elif cos_h > 1.0:
        return None  # Sun never reaches this elevation (polar winter)

    return math.degrees(math.acos(cos_h))

## Main program #############################################3

# Read precomputed data
with open('sun_data.bin', 'rb') as f:
    count = struct.unpack('H', f.read(2))[0]
    for _ in range(count):
        decl, eot = struct.unpack('ff', f.read(8))
        declination.append(decl)
        equation_of_time.append(eot)

# Settings for Brno, Czechia
latitude  = 49.19528 
longitude = 16.60778
timezone_offset = 1   # UTC+1, CET

# Print table around winter solstice
for i in range(0, 40):
    sun_declin = declination[i]
    eq_of_time = equation_of_time[i]
    ha_sunrise = hour_angle_for_elevation(latitude, sun_declin, -0.8333)
    solar_noon = (720 - 4 * longitude - eq_of_time + timezone_offset * 60) / 1440
    sunrise_time = solar_noon - ha_sunrise * 4 / 1440
    sunset_time = solar_noon + ha_sunrise * 4 / 1440
    daylight = ha_sunrise * 4 * 2 / 1440
    print(f"| {index_to_date_str(i)} | {fraction_to_time(sunrise_time)} | {fraction_to_time(solar_noon)} | {fraction_to_time(sunset_time)} | {fraction_to_time(daylight)}")
