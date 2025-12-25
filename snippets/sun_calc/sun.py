# NOTE: this code was written against excel/openoffice write table from NOAA
# Used as a reference - time is 6 minutes after midnight (first row)
from datetime import datetime, timedelta
import math

def excel_date_to_julian_day(excel_date, timezone_offset):
    # Excel's date system starts at 1900-01-01 (Excel day 1)
    # But Excel incorrectly assumes 1900 is a leap year, so day 60 is 1900-02-29 (which doesn't exist)
    # So we adjust for this bug (comes from Lotus-1-2-3)
    excel_epoch = datetime(1899, 12, 30)
    delta = timedelta(days=excel_date)  # Subtract 2 to correct for Excel's 1900 leap year bug
    date = excel_epoch + delta

    # Calculate Julian Day
    # Excel formula: JD = DATE + 2415018.5 + DAY_FRACTION - TIMEZONE/24
    # Here, DAY_FRACTION is 0.5 for noon, but you can adjust as needed
    jd = excel_date + 2415018.5 - timezone_offset / 24
    return jd

def date_to_excel_serial_date(date):
    # Excel epoch (1900-01-01) with the 1900 leap year bug correction
    excel_epoch = datetime(1899, 12, 30)
    delta = date - excel_epoch
    return delta.days

def julian_day(date, timezone_offset):
    excel_date = date_to_excel_serial_date(date)
    jd = excel_date_to_julian_day(excel_date, timezone_offset)    
    return jd

def fraction_to_time(fraction):
    hours   = int(fraction * 24)
    minutes = int((fraction * 24 - hours) * 60)
    seconds = int((fraction * 86400) % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Morovy sloup
latitude  = 49.19528 
longitude = 16.60778

date_year  = 2025
date_month = 12
date_day   = 24

timezone_offset = 1

time_past_midnight = 6 / 1440

julian_century      = (julian_day(datetime(2025, 12, 24), timezone_offset) + time_past_midnight-2451545)/36525             # G

# NOTE: this code does not depend on location (except of timezone via julian century)
geom_mean_long_sun  = (280.46646   + julian_century * (36000.76983 + julian_century * 0.0003032)) % 360 # I
geom_mean_anom_sun  = 357.52911   + julian_century * (35999.05029 - 0.0001537 * julian_century)       # J
eccent_earth_orbit  = 0.016708634 - julian_century * (0.000042037 + 0.0000001267 * julian_century)    # K
sun_eq_of_ctr       = math.sin(math.radians(  geom_mean_anom_sun))*(1.914602-julian_century*(0.004817+0.000014*julian_century)) \
                    + math.sin(math.radians(2*geom_mean_anom_sun))*(0.019993-0.000101*julian_century) \
                    + math.sin(math.radians(3*geom_mean_anom_sun))*0.000289                           # L
sun_true_long       = geom_mean_long_sun + sun_eq_of_ctr    # M
sun_true_anom       = geom_mean_anom_sun + sun_eq_of_ctr    # N
sun_rad_vector      = (1.000001018*(1-eccent_earth_orbit*eccent_earth_orbit)) \
                    / (1+eccent_earth_orbit*math.cos(math.radians(sun_true_anom)))                    # O
sun_app_long        = sun_true_long - 0.00569 - 0.00478 \
                    * math.sin(math.radians(125.04-1934.136*julian_century))                          # P
mean_obliq_ecliptic = 23+(26+((21.448-julian_century*(46.815+julian_century*(0.00059-julian_century*0.001813))))/60)/60 # Q
obliq_corr          = mean_obliq_ecliptic+0.00256*math.cos(math.radians(125.04-1934.136*julian_century))                # R
sun_rt_ascen        = math.degrees(math.atan2(math.cos(math.radians(sun_app_long)), \
                                              math.cos(math.radians(obliq_corr))*math.sin(math.radians(sun_app_long)))) # S
sun_declin          = math.degrees(math.asin(math.sin(math.radians(obliq_corr )) \
                                           * math.sin(math.radians(sun_app_long)))) # T
var_y               = math.tan(math.radians(obliq_corr/2)) \
                    * math.tan(math.radians(obliq_corr/2))  # U
eq_of_time          = 4 * math.degrees( \
                       var_y*math.sin(2*math.radians(geom_mean_long_sun)) \
                       -2*eccent_earth_orbit*math.sin(math.radians(geom_mean_anom_sun)) \
                       +4*eccent_earth_orbit*var_y*math.sin(math.radians(geom_mean_anom_sun))*math.cos(2*math.radians(geom_mean_long_sun)) \
                       -0.5*var_y*var_y*math.sin(4*math.radians(geom_mean_long_sun)) \
                       -1.25*eccent_earth_orbit*eccent_earth_orbit*math.sin(2*math.radians(geom_mean_anom_sun)) \
                      )                                     # V

ha_sunrise          = math.degrees(math.acos( \
                        math.cos(math.radians(90.833)) / \
                        (math.cos(math.radians(latitude))*math.cos(math.radians(sun_declin)))
                        -math.tan(math.radians(latitude))*math.tan(math.radians(sun_declin)) \
                      ))
solar_noon          = (720-4*longitude-eq_of_time+timezone_offset*60)/1440   # X
sunrise_time        = solar_noon-ha_sunrise*4/1440 # Y
sunset_time         = solar_noon+ha_sunrise*4/1440 # Z

# Výsledky
print(f"Julian Day: {julian_day(datetime(2025, 12, 24), timezone_offset)}")
print(f"Čas východu slunce: {fraction_to_time(sunrise_time)}")
print(f"Čas poledne: {fraction_to_time(solar_noon)}")
print(f"Čas západu slunce:  {fraction_to_time(sunset_time)}")
