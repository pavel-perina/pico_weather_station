#!/usr/bin/julia

# Solar position calculator
# Coordinates: Brno, Czech Republic (49.20°N, 16.60°E)

using Printf

# ============================================================================
# Basic date functions
# ============================================================================

function is_leap_year(year)
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
end

function day_of_year(year, month, day)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(year)
        days_in_month[2] = 29
    end
    return sum(days_in_month[1:month-1]) + day
end

# ============================================================================
# Solar calculations
# ============================================================================

"""
Calculate solar declination (degrees)
Declination is the angle between sun and equatorial plane
Varies from +23.44° (summer solstice) to -23.44° (winter solstice)
"""
#function solar_declination(doy)
#    # Cooper's equation - simplified approximation
#    return 23.44 * sind(360/365 * (doy - 81))
#end

"""
Calculate solar declination (degrees) - more accurate formula
"""
function solar_declination(doy)
    # More accurate formula using multiple harmonics
    n = doy - 1  # Days since Jan 1
    L = 280.460 + 0.9856474 * n  # Mean longitude
    g = 357.528 + 0.9856003 * n  # Mean anomaly

    lambda = L + 1.915 * sind(g) + 0.020 * sind(2*g)  # Ecliptic longitude
    epsilon = 23.439 - 0.0000004 * n  # Obliquity of ecliptic

    return asind(sind(epsilon) * sind(lambda))
end

"""
Calculate equation of time (minutes)
Corrects for Earth's elliptical orbit and axial tilt
Varies from -16 to +16 minutes throughout the year
"""
#function equation_of_time(doy)
#    b = 360/365 * (doy - 81)
#    # Spencer's formula - empirical approximation
#    return 9.87 * sind(2*b) - 7.53 * cosd(b) - 1.5 * sind(b)
#end
function equation_of_time(doy)
    #Calculate equation of time (minutes) - NOAA formula
    # Fractional year in radians
    gamma = 2 * pi / 365 * (doy - 1 + (12 - 12) / 24)
    
    # Equation of time in minutes
    eot = (229.18 * (0.000075 + 
                     0.001868 * cos(gamma) - 
                     0.032077 * sin(gamma) -
                     0.014615 * cos(2 * gamma) - 
                     0.040849 * sin(2 * gamma)))
    
    return eot
end

"""
Calculate hour angle for given solar elevation
Returns hour angle in degrees, or nothing if sun never reaches that elevation

Parameters:
- latitude: observer latitude (degrees, positive North)
- declination: solar declination (degrees)
- elevation: solar elevation angle (degrees above horizon)

Common elevations:
- -0.833°: Sunrise/sunset (accounts for refraction + solar radius)
- -6°: Civil twilight
- -12°: Nautical twilight
- -18°: Astronomical twilight
- 6°: Golden hour
"""
function hour_angle_for_elevation(latitude, declination, elevation)
    lat_rad = deg2rad(latitude)
    dec_rad = deg2rad(declination)
    elev_rad = deg2rad(elevation)
    
    # Spherical astronomy formula
    cos_h = (sin(elev_rad) - sin(lat_rad) * sin(dec_rad)) / 
            (cos(lat_rad) * cos(dec_rad))
    
    # Check if sun reaches this elevation today
    if cos_h < -1.0
        return nothing  # Sun always above this elevation (polar summer)
    elseif cos_h > 1.0
        return nothing  # Sun never reaches this elevation (polar winter)
    end
    
    return rad2deg(acos(cos_h))
end

"""
Calculate sunrise and sunset times in solar time

Parameters:
- latitude: observer latitude (degrees)
- doy: day of year (1-365/366)
- elevation: solar elevation angle (degrees, default -0.833° for sunrise/sunset)

Returns:
- (sunrise_hour, sunset_hour) in decimal hours of solar time
- (nothing, nothing) if sun doesn't rise/set (polar day/night)
"""
function sun_times_solar(latitude, doy; elevation=-0.833)
    decl = solar_declination(doy)
    eot = equation_of_time(doy)
    
    h_angle = hour_angle_for_elevation(latitude, decl, elevation)
    
    if h_angle === nothing
        return (nothing, nothing)
    end
    
    # Convert hour angle to time
    # Hour angle is in degrees: 15° = 1 hour
    # Sunrise is before solar noon (12:00), sunset after
    sunrise = 12.0 - h_angle/15.0 - eot/60.0
    sunset = 12.0 + h_angle/15.0 - eot/60.0
    
    return (sunrise, sunset)
end

"""
Convert solar time to local clock time

Parameters:
- solar_hour: time in solar hours (0-24)
- longitude: observer longitude (degrees, positive East, negative West)
- timezone_offset: hours from UTC (e.g., +1 for CET, +2 for CEST)

Returns:
- local clock time in decimal hours (0-24)
"""
function solar_to_local_time(solar_hour, longitude, timezone_offset)
    # Longitude correction: 15° = 1 hour
    # Eastern longitudes see sun earlier
    local_hour = solar_hour - longitude/15.0 + timezone_offset
    
    # Wrap to 0-24 range
    while local_hour < 0.0
        local_hour += 24.0
    end
    while local_hour >= 24.0
        local_hour -= 24.0
    end
    
    return local_hour
end

"""
Calculate sunrise and sunset times in local clock time

Parameters:
- latitude: observer latitude (degrees)
- longitude: observer longitude (degrees)
- doy: day of year
- timezone_offset: hours from UTC
- elevation: solar elevation angle (degrees)

Returns:
- (sunrise, sunset) in decimal hours of local time
"""
function sun_times(latitude, longitude, doy, timezone_offset; elevation=-0.833)
    sunrise_solar, sunset_solar = sun_times_solar(latitude, doy; elevation=elevation)
    
    if sunrise_solar === nothing
        return (nothing, nothing)
    end
    
    sunrise = solar_to_local_time(sunrise_solar, longitude, timezone_offset)
    sunset = solar_to_local_time(sunset_solar, longitude, timezone_offset)
    
    return (sunrise, sunset)
end

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
function solar_position(latitude, doy, solar_hour)
    decl = solar_declination(doy)
    eot = equation_of_time(doy)
    
    # Hour angle from solar noon (15° per hour)
    hour_angle = 15.0 * (solar_hour - 12.0 + eot/60.0)
    
    lat_rad = deg2rad(latitude)
    dec_rad = deg2rad(decl)
    h_rad = deg2rad(hour_angle)
    
    # Solar elevation (altitude)
    sin_elev = sin(lat_rad) * sin(dec_rad) + 
               cos(lat_rad) * cos(dec_rad) * cos(h_rad)
    elevation = rad2deg(asin(sin_elev))
    
    # Solar azimuth
    cos_azim = (sin(dec_rad) - sin(lat_rad) * sin_elev) / 
               (cos(lat_rad) * cos(asin(sin_elev)))
    # Clamp to prevent numerical errors
    cos_azim = clamp(cos_azim, -1.0, 1.0)
    azimuth = rad2deg(acos(cos_azim))
    
    # Adjust azimuth for afternoon (hour angle > 0)
    if hour_angle > 0
        azimuth = 360.0 - azimuth
    end
    
    return (azimuth, elevation)
end

# ============================================================================
# Utility functions
# ============================================================================

"""Format decimal hours as HH:MM"""
function format_time(hour)
    if hour === nothing
        return "N/A"
    end
    h = floor(Int, hour)
    m = round(Int, (hour - h) * 60)
    if m == 60
        h += 1
        m = 0
    end
    return @sprintf("%02d:%02d", h % 24, m)
end

"""Format decimal hours as HH:MM:SS"""
function format_time_precise(hour)
    if hour === nothing
        return "N/A"
    end
    h = floor(Int, hour)
    m = floor(Int, (hour - h) * 60)
    s = round(Int, ((hour - h) * 60 - m) * 60)
    if s == 60
        m += 1
        s = 0
    end
    if m == 60
        h += 1
        m = 0
    end
    return @sprintf("%02d:%02d:%02d", h % 24, m, s)
end

# ============================================================================
# Main demonstration
# ============================================================================

function demo()
    # Brno, Czech Republic (49 12 / 16 36)
    latitude = 49.20
    longitude = 16.60
    
    # Get current date or use example
    year = 2025
    month = 12
    day = 12
    
    doy = day_of_year(year, month, day)
    
    # Timezone: CET (UTC+1) in winter, CEST (UTC+2) in summer
    # Simplified: CET for Nov-Mar, CEST for Apr-Oct
    timezone_offset = (month >= 4 && month <= 10) ? 2 : 1
    tz_name = (timezone_offset == 2) ? "CEST" : "CET"
    
    println("=" ^ 70)
    println("Solar Calculator for Brno, Czech Republic")
    println("=" ^ 70)
    println("Location: $(latitude)°N, $(longitude)°E")
    println("Date: $year-$(lpad(month, 2, '0'))-$(lpad(day, 2, '0')) (day $doy of year)")
    println("Timezone: $tz_name (UTC+$timezone_offset)")
    println()
    
    # ========================================================================
    # Sunrise and sunset
    # ========================================================================
    
    sunrise, sunset = sun_times(latitude, longitude, doy, timezone_offset)
    
    if sunrise === nothing
        println("⚠ Polar day/night - sun does not rise/set today")
        return
    end
    
    println("─" ^ 70)
    println("SUNRISE & SUNSET")
    println("─" ^ 70)
    println("Sunrise: $(format_time(sunrise)) $tz_name")
    println("Sunset:  $(format_time(sunset)) $tz_name")
    
    daylight_hours = sunset - sunrise
    if daylight_hours < 0
        daylight_hours += 24
    end
    daylight_h = floor(Int, daylight_hours)
    daylight_m = round(Int, (daylight_hours - daylight_h) * 60)
    println("Daylight: $(daylight_h)h $(daylight_m)m")
    println()
    
    # ========================================================================
    # Twilight times
    # ========================================================================
    
    println("─" ^ 70)
    println("TWILIGHT TIMES")
    println("─" ^ 70)
    
    twilight_events = [
        ("Astronomical twilight begins", -18, "morning"),
        ("Nautical twilight begins", -12, "morning"),
        ("Civil twilight begins", -6, "morning"),
        ("Civil twilight ends", -6, "evening"),
        ("Nautical twilight ends", -12, "evening"),
        ("Astronomical twilight ends", -18, "evening"),
    ]
    
    for (name, elev, time_of_day) in twilight_events
        morning, evening = sun_times(latitude, longitude, doy, timezone_offset; elevation=elev)
        
        if morning === nothing
            println("$name: N/A (sun doesn't reach $(elev)°)")
        else
            if time_of_day == "morning"
                println("$name: $(format_time(morning)) $tz_name")
            else
                println("$name: $(format_time(evening)) $tz_name")
            end
        end
    end
    println()
    
    # ========================================================================
    # Golden hour
    # ========================================================================
    
    println("─" ^ 70)
    println("GOLDEN HOUR (sun between 0° and 6° elevation)")
    println("─" ^ 70)
    
    golden_morning, golden_evening = sun_times(latitude, longitude, doy, timezone_offset; elevation=6)
    
    if golden_morning !== nothing
        println("Morning golden hour: $(format_time(sunrise)) - $(format_time(golden_morning)) $tz_name")
        println("Evening golden hour: $(format_time(golden_evening)) - $(format_time(sunset)) $tz_name")
    end
    println()
    
    # ========================================================================
    # Solar noon
    # ========================================================================
    
    println("─" ^ 70)
    println("SOLAR NOON")
    println("─" ^ 70)

    eot = equation_of_time(doy)
    println("EOT=$eot")
    solar_noon_solar = 12.0 - eot/60.0  # Apply equation of time
    solar_noon_local = solar_to_local_time(solar_noon_solar, longitude, timezone_offset)

    # Solar noon is at 12:00 solar time
    #solar_noon_local = solar_to_local_time(12.0, longitude, timezone_offset)
    
    # Calculate solar position at noon
    azim_noon, elev_noon = solar_position(latitude, doy, solar_noon_solar)
    
    println("Solar noon: $(format_time_precise(solar_noon_local)) $tz_name")
    println("Sun azimuth: $(round(azim_noon, digits=1))° (180° = due South)")
    println("Sun elevation: $(round(elev_noon, digits=1))° above horizon")
    println()
    
    # ========================================================================
    # Solar position at key times
    # ========================================================================
    
    println("─" ^ 70)
    println("SOLAR POSITION THROUGHOUT DAY")
    println("─" ^ 70)
    println(@sprintf("%-15s %-10s %-12s %-12s", "Local Time", "Solar Time", "Azimuth", "Elevation"))
    println("─" ^ 70)
    
    for local_hour in 6:1:18
        # Convert local time to solar time
        solar_hour = local_hour + longitude/15.0 - timezone_offset
        
        azim, elev = solar_position(latitude, doy, solar_hour)
        
        println(@sprintf("%-15s %-10s %8.1f° %11.1f°", 
                format_time(float(local_hour)),
                format_time(solar_hour),
                azim,
                elev))
    end
    
    println()
    println("=" ^ 70)
end

# Run the demo
demo()
