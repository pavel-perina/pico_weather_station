from datetime import datetime, timedelta
import math
import struct

EXCEL_EPOCH = datetime(1899, 12, 30)     # Excel epoch (1900-01-01) with the 1900 leap year bug correction
J2000_EPOCH = 2451545.0                  # Noon 2000-01-01T12:00Z
DAYS_PER_CENTURY = 36525.0

def excel_date_to_julian_day(excel_date:float, timezone_offset:float) -> float:
    # Excel's date system starts at 1900-01-01 (Excel day 1)
    # But Excel incorrectly assumes 1900 is a leap year, so day 60 is 1900-02-29 (which doesn't exist)
    # So we adjust for this bug (comes from Lotus-1-2-3)
    delta = timedelta(days=excel_date)  # Subtract 2 to correct for Excel's 1900 leap year bug
    date = EXCEL_EPOCH + delta

    # Calculate Julian Day
    # Excel formula: JD = EXCEL_DATE + 2415018.5 + DAY_FRACTION - TIMEZONE/24
    # Here, DAY_FRACTION is 0.5 for noon, but you can adjust as needed
    # Magic constant is Julian date of 1899-12-30T00:00Z
    jd = excel_date + 2415018.5 - timezone_offset / 24
    return jd

def date_to_excel_serial_date(date: datetime) -> float:
    delta = date - EXCEL_EPOCH
    return delta.days

def date_to_julian_day(date, timezone_offset):
    # https://en.wikipedia.org/wiki/Julian_day#History yes, we have year 6738 in 2025
    excel_date = date_to_excel_serial_date(date)
    jd = excel_date_to_julian_day(excel_date, timezone_offset)    
    return jd

def date_to_julian_century(date: datetime,
                           timezone_offset: float, 
                           time_fraction: float = 0.5) -> float:
    """
    Convert date to Julian centuries since J2000.0 epoch
    
    Args:
        date: Date to convert
        timezone_offset: UTC offset in hours
        time_fraction: Time of day as fraction (0.5 = noon)
    """
    jd = date_to_julian_day(date, timezone_offset)
    return (jd + time_fraction - J2000_EPOCH) / DAYS_PER_CENTURY

def fraction_to_time(fraction):
    hours   = int(fraction * 24)
    minutes = int((fraction * 24 - hours) * 60)
    seconds = int((fraction * 86400) % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def precalc(julian_century):
    # Geometrická střední délka slunce (I)
    geom_mean_long_sun = (280.46646 + julian_century * (36000.76983 + julian_century * 0.0003032)) % 360

    # Geometrická střední anomálie slunce (J)
    geom_mean_anom_sun = 357.52911 + julian_century * (35999.05029 - 0.0001537 * julian_century)

    # Excentricita zemské dráhy (K)
    eccent_earth_orbit = 0.016708634 - julian_century * (0.000042037 + 0.0000001267 * julian_century)

    # Rovnice středu (L)
    sun_eq_of_ctr = (
        math.sin(math.radians(geom_mean_anom_sun)) * (1.914602 - julian_century * (0.004817 + 0.000014 * julian_century))
        + math.sin(math.radians(2 * geom_mean_anom_sun)) * (0.019993 - 0.000101 * julian_century)
        + math.sin(math.radians(3 * geom_mean_anom_sun)) * 0.000289
    )

    # Pravá délka slunce (M)
    sun_true_long = geom_mean_long_sun + sun_eq_of_ctr

    # Pravá anomálie slunce (N)
    sun_true_anom = geom_mean_anom_sun + sun_eq_of_ctr

    # Vzdálenost slunce od Země (O)
    # sun_rad_vector = (1.000001018 * (1 - eccent_earth_orbit**2)) / (1 + eccent_earth_orbit * math.cos(math.radians(sun_true_anom)))

    # Zdánlivá délka slunce (P)
    sun_app_long = sun_true_long - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * julian_century))

    # Střední sklon ekliptiky (Q)
    mean_obliq_ecliptic = 23 + (26 + ((21.448 - julian_century * (46.815 + julian_century * (0.00059 - julian_century * 0.001813)))) / 60) / 60

    # Korekce sklonu ekliptiky (R)
    obliq_corr = mean_obliq_ecliptic + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * julian_century))

    # Rektascenze slunce (S)
    sun_rt_ascen = math.degrees(
        math.atan2(
            math.cos(math.radians(sun_app_long)),
            math.cos(math.radians(obliq_corr)) * math.sin(math.radians(sun_app_long)),
        )
    )

    # Deklinace slunce (T)
    sun_declin = math.degrees(math.asin(math.sin(math.radians(obliq_corr)) * math.sin(math.radians(sun_app_long))))

    # Pomocná proměnná (U)
    var_y = math.tan(math.radians(obliq_corr / 2)) ** 2

    # Rovnice času (V)
    eq_of_time = 4 * math.degrees(
        var_y * math.sin(2 * math.radians(geom_mean_long_sun))
        - 2 * eccent_earth_orbit * math.sin(math.radians(geom_mean_anom_sun))
        + 4 * eccent_earth_orbit * var_y * math.sin(math.radians(geom_mean_anom_sun)) * math.cos(2 * math.radians(geom_mean_long_sun))
        - 0.5 * var_y**2 * math.sin(4 * math.radians(geom_mean_long_sun))
        - 1.25 * eccent_earth_orbit**2 * math.sin(2 * math.radians(geom_mean_anom_sun))
    )

    return (sun_declin, eq_of_time)

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

# Hodinový úhel východu/západu slunce (ha_sunrise)
# 90.833 je úhel slunce pod zenitem (počítá s refrakcí a poloměrem slunce)
# Hodinový úhel 90 koresponduje s šestou hodinou ráno, 15 stupňů na hodinu, stupeň na 4 minuty
#ha_sunrise = math.degrees(
#    math.acos(
#        math.cos(math.radians(90.833))
#        / (math.cos(math.radians(latitude)) * math.cos(math.radians(sun_declin)))
#        - math.tan(math.radians(latitude)) * math.tan(math.radians(sun_declin))
#    )
#)


# Brno, CZ, Náměstí svobody
latitude  = 49.19528 
longitude = 16.60778

timezone_offset = 1   # UTC+1, CET

time_past_midnight = 0.5

# Precompute array of sun_declin, eq_of_time
start_date = datetime(2025, 12, 1)
end_date   = datetime(2025, 12, 31)

current_date = start_date
#julian_century      = (julian_day(start_date, timezone_offset) + time_past_midnight - 2451545)/36525
julian_century = date_to_julian_century(start_date, timezone_offset, time_past_midnight)
array = []
while current_date <= end_date:
    sun_declin, eq_of_time = precalc(julian_century)
    array.append((sun_declin, eq_of_time))
    current_date   += timedelta(days=1)
    julian_century += 1/DAYS_PER_CENTURY

print("| Date | Sunrise | Noon | Sunset |")
print("|------|---------|------|--------|")

for index, (sun_declin, eq_of_time) in enumerate(array):
    sun_declin, eq_of_time = array[index]
    current_date = start_date + timedelta(days=index)
    ha_sunrise = hour_angle_for_elevation(latitude, sun_declin, -0.8333)

    # Sluneční poledne (X)
    solar_noon = (720 - 4 * longitude - eq_of_time + timezone_offset * 60) / 1440

    # Čas východu slunce (Y)
    sunrise_time = solar_noon - ha_sunrise * 4 / 1440

    # Čas západu slunce (Z)
    sunset_time = solar_noon + ha_sunrise * 4 / 1440
    print(f"| {current_date:%Y-%m-%d} | {fraction_to_time(sunrise_time)} | {fraction_to_time(solar_noon)} | {fraction_to_time(sunset_time)} |")



def solar_position(latitude, sun_declin, eq_of_time, local_hour):
    """
    Calculate solar azimuth and elevation at given time

    Parameters:
    - latitude: observer latitude (degrees)
    - doy: day of year
    - solar_hour: time in solar hours (0-24)

    Returns:
    - (azimuth, elevation) in degrees
    - azimuth: 0° = North, 90° = East, 180° = South, 270° = West
    - elevation: angle above horizon (negative = below horizon)
    """

    # Hour angle from solar noon (15° per hour)
    solar_hour = local_hour + longitude/15.0 - timezone_offset
    hour_angle = 15.0 * (solar_hour - 12.0 + eq_of_time/60.0)
    
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(sun_declin)
    h_rad   = math.radians(hour_angle)
    
    # Solar elevation (altitude)
    sin_elev = math.sin(lat_rad) * math.sin(dec_rad) + \
               math.cos(lat_rad) * math.cos(dec_rad) * math.cos(h_rad)
    elevation = math.degrees(math.asin(sin_elev))
    
    # Solar azimuth
    cos_azim = (math.sin(dec_rad) - math.sin(lat_rad) * sin_elev) / \
               (math.cos(lat_rad) * math.cos(math.asin(sin_elev)))
    # Clamp to prevent numerical errors
    #cos_azim = math.clamp(cos_azim, -1.0, 1.0)
    if cos_azim > 1:
        cos_azim = 1
    if cos_azim < -1:
        cos_azim = -1
    azimuth = math.degrees(math.acos(cos_azim))
    
    # Adjust azimuth for afternoon (hour angle > 0)
    if hour_angle > 0:
        azimuth = 360.0 - azimuth

    return (azimuth, elevation)


date_to_julian_century(datetime(2025, 12, 24), timezone_offset, time_past_midnight)
print("| Hour | Azimuth | Elevation |")
print("|-----:|--------:|----------:|")
for hour in range (0, 23):
    sun_declin, eq_of_time = precalc(julian_century)
    azimuth, elevation = solar_position(latitude, sun_declin, eq_of_time, hour)
    print(f"| {hour:d} | {azimuth:6.2f} | {elevation:6.2f} |")

start_date = datetime(2025, 12, 1)
end_date   = datetime(2027, 12, 31)
current_date = start_date
#julian_century      = (julian_day(start_date, timezone_offset) + time_past_midnight - 2451545)/36525
julian_century = date_to_julian_century(start_date, timezone_offset, time_past_midnight)
array = []
while current_date <= end_date:
    sun_declin, eq_of_time = precalc(julian_century)
    array.append((sun_declin, eq_of_time))
    current_date   += timedelta(days=1)
    julian_century += 1/DAYS_PER_CENTURY

# Write binary
with open('sun_data.bin', 'wb') as f:
    f.write(struct.pack('H', len(array)))  # number of entries
    for decl, eot in array:
        f.write(struct.pack('ff', decl, eot))  # two floats
